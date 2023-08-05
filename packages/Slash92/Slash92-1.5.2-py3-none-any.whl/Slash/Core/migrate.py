from multiprocessing import Queue
from typing import Any
import hashlib
import rich
import json
import copy
import os

from migration_templates import (
    STANDART_JSON_CONFIG,
    MIGRATION_BLOCK
)
from ..types_ import (
    Column,
    BasicTypes,
    Table, TablesManager, TableMeta,
)


class MigrationTableBlock:
    def __init__(self, name, columns, path):
        self.__name = name
        self.__columns = columns

    def get_table_block(self):
        return [
            {
                self.__name: list(
                    zip(
                        [c.name for c in self.__columns],
                        [BasicTypes.DB_TYPES_LIST[c.type] for c in self.__columns]
                    )
                )
            },
            "".join([c.name for c in self.__columns])
        ]

        return (self.__name, [c.name for c in self.__columns])


class VersionManager:
    QUEUE: Queue = Queue()

    MAX_MAIN_VERSION = 25
    MAX_MIDDLE_VERSION = 25
    MAX_MINI_VERSION = 25
    FORMAT = "{}.{}.{}" # min: 0.0.1 > max: 25.25.25
    VERSION_RULES: dict = {
        "main": ("tables", "columns"),
        "middle": ("tables"),
        "mini": ("columns")
    }

    def __init__(self, debug_messages: bool):
        rich.print(f"\n\t[green][Info] -> [cyan]Call VersionManager\n\t{'-'*30}\n") if debug_messages else ""
        self.debug_messages = debug_messages

    def get_current_version(self):
        with open(str(os.environ.get("MIGRATION_FILE")), "r") as file_:
            while True:
                data = file_.readline()
                if data == "" or "version" in data:
                    return json.loads("{" + data.strip().replace(",", "") + "}")["version"]

    def push(self, event: str, data):
        if event == "tables":
            if self.debug_messages:
                rich.print("\t[green][Info] -> [blue]Detected table difference")
                rich.print(f"\n: Current tables: {data[0]}")
                rich.print(f": Last tables: {data[1]}")
                rich.print(f": Difference: {data[0].symmetric_difference(data[1])}\n")
        elif event == "columns":
            if self.debug_messages:
                rich.print("\n\t[green][Info] -> [blue]Detected columns difference")
                rich.print(f": Table: {data[0]}")
                rich.print(f": Columns: {data[1]}")

        VersionManager.QUEUE.put(event)

    def pop(self):
        return VersionManager.QUEUE.get()

    def generate_version(self):
        current_version = self.get_current_version()
        rich.print(f"\n\n\tCurrent version: [yellow]{current_version}") if self.debug_messages else ""

        main, middle, mini = map(int, current_version.split("."))

        while not self.QUEUE.empty():
            data = self.pop()
            if data == "tables":
                middle += 1
            elif data == "columns":
                mini += 1

        new_version = VersionManager.FORMAT.format(main, middle, mini)
        rich.print(f"\tNew version: [yellow]{new_version}") if self.debug_messages else ""
        return new_version


class MigrationCore:
    def __init__(self, path_, show_messages: bool = True) -> None:
        self._connection: Any = None
        if not os.path.exists(path_):
            os.mkdir(path_)
            with open(path_+"/config.json", "w") as file_:
                json.dump(STANDART_JSON_CONFIG, file_, indent=4)
        self.__migrations_folder = path_
        os.environ.setdefault("MIGRATION_FILE", self.__migrations_folder+"/config.json")
        self.show_messages = show_messages

    @property
    def path(self):
        return self.__migrations_folder

    def make_migrations(self, data_type, *templates):
        config: dict = self._read_config_file()
        merged_table_blocks: dict = {}
        column_names: str = ""

        first: bool = True

        version_manager: VersionManager = VersionManager(self.show_messages)

        last_block: dict = {}        # останній блок міграції
        last_tables: set             # останні таблиці
        current_tables: set          # теперішні таблиці
        delta_tables: set            # таблиці якими відрізняються попередні набори таблиць


        if config["count_of_blocks"] == 0:
            for template_item in templates:
                table_block = MigrationTableBlock(
                    template_item.name, template_item.columns, self.path
                ).get_table_block()
                merged_table_blocks.update(table_block[0])

            self._make_migration_block(config, merged_table_blocks, column_names)
            config["count_of_blocks"] += 1
            config["blocks"]["migration_0"]["version"] = "0.1.0"
        else:
            current_tables = set([item.name for item in templates])

            last_block = config["blocks"][f"migration_{config['count_of_blocks']-1}"]

            last_tables = set(last_block["tables"].keys())

            delta_tables = current_tables.symmetric_difference(last_tables)

            if delta_tables:
                version_manager.push("tables", (current_tables, last_tables))

            first = False

        if not first:
            for template_item in templates:
                table_block = MigrationTableBlock(
                    template_item.name, template_item.columns, self.path
                ).get_table_block()

                merged_table_blocks.update(table_block[0])
                column_names += table_block[1]

                current_ = merged_table_blocks.get(template_item.name)
                last_ = last_block["tables"].get(template_item.name)

                current_ = set([tuple(i) for i in current_]) if current_ is not None else set()
                last_ = set([tuple(i) for i in last_]) if last_ is not None else set()

                status: int = 0 if len(current_) == len(last_) else (
                    1 if len(current_) > len(last_) else -1
                )
                columns_difference: set = current_.symmetric_difference(last_)

                if columns_difference:
                    table_from_manager: Table = TablesManager.tables.get(
                        hashlib.sha512(
                            template_item.name.encode("utf-8")
                        ).hexdigest()
                    )
                    if status == 1:
                        new_column_object: Column
                        for column_item in columns_difference:
                            new_column_object = Column(
                                BasicTypes.ORM_TYPES_LIST.get(column_item[1]),
                                column_item[0]
                            )
                            self._connection.add_column(
                                table_from_manager,
                                new_column_object,
                                False
                            )
                    elif status == -1:
                        for column_item in columns_difference:
                            self._connection.delete_column(
                                table_from_manager,
                                column_item[0],
                                False
                            )

                    version_manager.push("columns", (template_item, columns_difference))

        # generate a new version of db of stay old
        n_version: str = version_manager.generate_version()
        if (n_version != version_manager.get_current_version()):
            rich.print("\n\nCreating new migration block...") if self.show_messages else ""

            self._make_migration_block(
                config,               # global configs (migration file)
                merged_table_blocks,  # tables
                column_names,         # columns
                n_version,            # new version
                last_block["hash"]    # hash of the last migration block
            )
            config["version"] = n_version
            config["count_of_blocks"] += 1

            rich.print("Migration block was created...") if self.show_messages else ""
        else:
            rich.print("Versions the same...") if self.show_messages else ""

        self._write_config_file(config)

    def _make_migration_block(
        self,
        global_config: dict,
        table_blocks: dict,
        columns_names: str,
        n_version: str="",
        last_hash: str=""
    ):
        new_migration: dict = copy.deepcopy(MIGRATION_BLOCK)
        new_migration["is_first"] = True if not last_hash else False
        new_migration["table_count"] = len(table_blocks)
        new_migration["tables"].update(table_blocks)
        new_migration["version"] = n_version

        new_migration["hash"] = hashlib.sha512(
            (
                last_hash + "".join([k for k in table_blocks.keys()]) + columns_names
            ).encode("utf-8")
        ).hexdigest()

        global_config["blocks"].update(
            {
               "migration_"+str(global_config["count_of_blocks"]): new_migration
           }
        )
        global_config["last_hash"] = new_migration["hash"]

    def _read_config_file(self):
        if os.path.exists(self.__migrations_folder + "\\config.json"):
            with open(self.__migrations_folder + "\\config.json") as json_configs:
                return json.load(json_configs)
        else:
            raise FileExistsError(f"\n\tConfig file is not found...\n\t\t{self.__migrations_folder}\config.json")

    def _write_config_file(self, data):
        with open(self.__migrations_folder + "\\config.json", "w") as json_configs:
            json.dump(data, json_configs, indent=4)
