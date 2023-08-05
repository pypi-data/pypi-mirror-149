import sys
BASE_DIR = "\\".join(__file__.split("\\")[0:-1])
sys.path.append(BASE_DIR + "\\utilities")
sys.path.append(BASE_DIR)

from typing import Any, final, Dict, List
import datetime
import hashlib
import json
import re
import os

# from utils_for_rules import WinJsonConverter
# from kolatz_utils.slash3_core import *
from Core.exceptions_ import SlashAttributeError


class Rules:
    """BAse rules for data"""
    def __init__(self):
        self.__rules = {
            "type_int": {
                "min": 0,
                "max": 255,
                "type": int,
                "valide_foo": self.valid_int
            },
            "type_text": {
                "length": 100,
                "valide_foo": self.valid_text
            },
            "type_bool": {
                "valide_foo": self.valid_bool
            },
            "type_date": {
                "template": "\\d{4}-\\d{2}-\\d{2}",
                "valide_foo": self.valid_date
            },
            "type_hidden": {
                "valide_foo": self.valid_hidden
            },
            "type_email": {
                "template": "^[a-zA-Z0-9\\-_\\.]*@[a-z\\.]*$",
                "valide_foo": self.valid_email
            },
            "type_phone": {
                "template": "\\+[0-9]*",
                "valide_foo": self.valid_phone
            },
            "type_ipv4": {
                "template": "[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}.[0-9]{1,3}",
                "valide_foo": self.valid_ipv4
            },
            "type_ipv6": {
                "template": "^(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))$",
                "valide_foo": self.valid_ipv6
            },
            "type_url": {
                "template": "^https://[0-9a-zA-Z\\./\\-_&=]*$",
                "valide_foo": self.valid_url
            }
        }

        self._user_rules = {}

    def get_rules(self):
        """Return current rules"""
        return self.__rules

    def get_user_rules(self):
        """Return user rules"""
        return self._user_rules

    def new_rules(self, rules: dict):
        """Create new rules(user rules)"""
        self._user_rules = rules
        return self._user_rules

    def valid_int(self, int_val, rule):
        """Validate int"""
        if type(int_val) != rule["type"]:
            return False 
        return rule["min"] <= int_val <= rule["max"]

    def valid_text(self, text_val, rule):
        """Validate text"""
        return len(text_val) <= rule["length"]

    def valid_bool(self, bool_val, rule):
        """Validate bool"""
        return bool_val

    def valid_date(self, date_val, rule):
        """Validate data"""
        return re.findall(rule["template"], str(date_val))

    def valid_hidden(self, hidden_val, rule):
        return type(hidden_val) is str

    def valid_email(self, email_val, rule):
        res = re.findall(rule["template"], email_val)
        return res

    def valid_phone(self, phone_val, rule):
        return len(re.findall(rule["template"], phone_val)) == 1

    def valid_ipv4(self, ipv4_val, rule):
        res = re.findall(rule["template"], ipv4_val)
        return (res and len(res) == 1)

    def valid_ipv6(self, ipv6_val, rule):
        res = re.findall(rule["template"], ipv6_val)
        return (res and len(res) == 1)

    def valid_url(self, url_val, rule):
        res = re.findall(rule["template"], url_val)
        return (len(res) == 1)

    def __check_path(self, path):
        return os.path.exists(path)


class JsonConverter:
    def __init__(self, rules={}):
        self.__rules: dict = rules.copy()

    def __validate_json(self):
        for key in self.__rules.keys():
            type_rules: dict = self.__rules[key].copy()

            for rule_item in type_rules.keys():
                match rule_item:
                    case "valide_foo":
                        template = re.findall("valid_[a-zA-Z]*", str(type_rules[rule_item]))
                        type_rules.update({"valide_foo": template[0]})
                        self.__rules.update({key: type_rules})
                    case "do":
                        type_rules.update({"do": "do"})
                        self.__rules.update({key: type_rules})

                    case "type":
                        type_rules.update({"type": "int"})
                        self.__rules.update({key: type_rules})

                    case "available":
                        type_rules.update({"available": ["str"]})
                        self.__rules.update({key: type_rules})

        return self.__rules

    def write(self):
        with open("rules.json", "w") as file_:
            json.dump(self.__validate_json(), file_, indent=4)

    def read(self, rules_class):
        class_dict = rules_class.__dict__["_Rules__rules"]

        with open("rules.json", "r") as file_:
            data_: dict = json.load(file_)

            for key in class_dict.keys():
                data_[key]["valide_foo"] = class_dict[key]["valide_foo"]
                if key == "type_date":
                    data_[key]["do"] = class_dict[key]["do"]
                elif key == "type_int":
                    data_[key]["type"] = int
                elif key == "type_hidden":
                    data_[key]["available"] = [str]

            rules_class._Rules__rules = data_

            return data_


class ORMType:
    """Base type class"""
    def __init__(self, type_name, value):
        self.type_name: str = type_name
        self.value: Any = value

    def _is_valid_datas(self, user_rules: str | Rules="*"):
        if user_rules == "*":
            rules = Rules()
            rule = rules.get_rules()[self.type_name]

            return (rule["valide_foo"](self.value, rule), rule)

        rule = user_rules.get_user_rules()[self.type_name]

        return (rule["valide_foo"](self.value, rule), rule)


class Hidden(ORMType):
    def __init__(self, value: Any):
        super().__init__(
            "type_hidden",
            hashlib.sha512(str(value).encode("utf-8")).hexdigest()
        )


class Int(ORMType):
    """
        SQL    - INT
        Python - int
    """
    def __init__(self, value):
        super().__init__("type_int", value)


class Text(ORMType):
    """
        SQL    - TEXT
        Python - str
    """
    def __init__(self, value):
        super().__init__("type_text", value)


class Bool(ORMType):
    """
        SQL    - BOOL
        Python - bool
    """
    def __init__(self, value):
        super().__init__("type_bool", value)


class Date(ORMType):
    """
        SQL    - DATE
        Python - datetime.today()
    """
    def __init__(self, value):
        super().__init__("type_date", value)
    
    @staticmethod
    def now():
        return datetime.datetime.now()


class Email(ORMType):
    def __init__(self, value):
        super().__init__("type_email", value)


class Phone(ORMType):
    def __init__(self, value):
        super().__init__("type_phone", value)


class IPv4(ORMType):
    def __init__(self, value):
        super().__init__("type_ipv4", value)


class IPv6(ORMType):
    def __init__(self, value):
        super().__init__("type_ipv6", value)


class Url(ORMType):
    def __init__(self, value):
        super().__init__("type_url", value)


class BasicTypes:
    """Contains all available types"""
    TYPES_LIST = (Int, Text, Bool, Date, Hidden, Email, Phone, IPv4, IPv6, Url)
    NEED_FORMAT = (
        "type_text", "type_date", "type_hidden",
        "type_email", "type_phone", "type_ipv4",
        "type_ipv6", "type_url"
    )
    DB_TYPES_LIST = {
        Int: "INT", Text: "TEXT",
        Bool: "BOOL", Date: "DATE",
        Hidden: "TEXT", Email: "TEXT",
        Phone: "TEXT", IPv4: "TEXT",
        IPv6: "TEXT", Url: "TEXT"
    }
    ORM_TYPES_LIST = {
        "INT": Int, "TEXT": Text,
        "BOOL": Bool, "DATE": Date,
        "HIDDEN": Hidden, "EMAIL": Email,
        "PHONE": Phone, "IPV4": IPv4,
        "IPV6": IPv6, "URL": Url
    }


class Column:
    """Field of table"""
    def __init__(self, column_type, column_name):
        self.__column_type = column_type
        self.__column_name = column_name
        self.__column_sql_type = BasicTypes.DB_TYPES_LIST.get(
            self.__column_type
        )

    def set_sql_type(self, column):
        self.__column_sql_type = BasicTypes.DB_TYPES_LIST.get(column)

    @property
    def type(self):
        """Return orm-type of the column"""
        return self.__column_type

    @property
    def name(self):
        """Return name of the column"""
        return self.__column_name

    def set_name(self, name):
        self.__column_name = name
        return self.__column_name

    @property
    def sql_type(self):
        """Return sql-type of the column"""
        return self.__column_sql_type


@final
class TablesManager:
    """
        Give access to tables and accept to manipulate them
    """
    tables: Dict = {}
    Utables: Dict = {}

    @staticmethod
    def find_by_name(name):
        """Return one tables by name of table"""
        return TablesManager.tables.get(hashlib.sha512(name.encode("utf-8")).hexdigest())

    @staticmethod
    def find_one_by_column(*column_names):
        """Select one table by name of column"""
        count = len(column_names)

        for table in TablesManager.tables.values():
            for column in table.columns:
                if column.name in column_names:
                    count -= 1

                if count == 0:
                    return table

            count = len(column_names)
        return False

    @staticmethod
    def find_many_by_column(*column_names):
        """Select all tables by name of column"""
        tables = []
        count = len(column_names)

        for table in TablesManager.tables.values():
            for column in table.columns:
                if column.name in column_names:
                    count -= 1

                if count == 0:
                    tables.append(table)
                    break

            count = len(column_names)

        return tables

    @staticmethod
    def unite(*tables):
        """A function that returns multiple wrapped tables"""
        columns_u = []
        name_ = []
        for table in tables:
            for column in table.columns:
                if column.name not in columns_u:
                    columns_u.append(column)
            name_.append(table.name.lower())
        name_ = "U".join(name_)

        class UnitedTable(
            Table, metaclass=UnitedTableMeta, parent=Table,
            U_table_name=name_, U_table_columns=columns_u,
            U_tables=tables
        ):
            """Table which are few tables"""
            def __init__(self, name: str):
                self._is_unated = True
                self._parent_tables = tables

                TablesManager.Utables.update(
                    {
                        hashlib.sha512(self.name.encode("utf-8")).hexdigest(): self
                    }
                )
        s_len = len(columns_u)
        for i in range(s_len):
            if s_len > len(columns_u):
                break

            for n in range(len(columns_u)):
                if columns_u[i] == columns_u[n]:
                    del columns_u[n]
                    break

        u_table = UnitedTable(name_)
        u_table.set_columns(*columns_u)

        u_table.set_columns = lambda x=None: print("Not allowed for united tables")

        return u_table


class TableMeta(type):
    def __new__(cls, name, parrent, args: dict):
        columns: list = []
        dot_col: dict = {}
        for k in args:
            if type(args[k]) is Column:
                args[k].set_name(k)
                columns.append(args[k])
                dot_col.update({k: args[k]})

        for column in columns:
            args.pop(column.name)

        if args.get("__table__name__"):
            args.update({"_Table__name": args.get("__table__name__")})

        args.update({"columns": columns})
        args.update(dot_col)
        args.update({"rowid": Column(Int, "rowid")})
        return type(name, parrent, args)


class Table:
    """Table of database"""
    def __init__(self, name: str=None):
        self.op = None
        self.__name = name if name else self.name
        self.__columns: List[Column] = []
        self.__connection = None

        if type(self.__name) is Column:
            raise SlashAttributeError(
                    f"""
                        >> A column with this name already exists.
                        Column name: '{self.__name.name}'

                    """
                )
        TablesManager.tables.update(
            {
                hashlib.sha512(self.__name.encode("utf-8")).hexdigest(): self
            }
        )

    @property
    def name(self):
        """Get name of the table"""
        return self.__name

    @property
    def columns(self):
        """Get columns of the table"""
        return self.__columns

    def set_columns(self, *columns):
        """Set columns for table:
            .set_columns(Column(type of datas, name of column))
        """
        rowid_column = Column(Int, "rowid")
        rowid_column.__setattr__("_p", self.name)
        self.__setattr__("rowid", rowid_column)
        for column in columns:
            column.__setattr__("_p", self.name)
            try:
                self.__setattr__(column.name, column)
            except AttributeError as e:
                raise SlashAttributeError(
                    f"""
                        >> An attribute with this name already exists.
                        Attribute name: '{column.name}'

                    """
                )

        self.__columns = list(columns)

    def __or__(self, table):
        if isinstance(table, Table):
            return TablesManager.unite(self, table)

    def __lshift__(self, component):
        if "Slash.Core.operations_.Operations" in str(component.__class__):
            self.__setattr__("op", component)
            self.__connection = component.connection

    def __add__(self, column: Column):
        if isinstance(column, Column):
            self.__setattr__(column.name, column)
            self.columns.append(column)
            self.__connection.add_column(self, column)

    def __sub__(self, column: Column):
#        raise NotImplementedError("\n\tDon't touch this protocol")
        if isinstance(column, Column):
            self.columns = [item for item in self.__columns if item != column]
            self.__connection.delete_column(self, column.name)


class UnitedTableMeta(type):
    """Metaclass for Table, will create UnatedTable"""
    def __new__(cls, name, parents, namespace, **kwargs):
        parent_name: Table = kwargs["parent"](kwargs["U_table_name"])

        namespace.update(
            {
                "name": parent_name.name,
                "columns": kwargs["U_table_columns"],
                "set_columns": parent_name.set_columns,
                "tables": kwargs["U_tables"]
            }
        )
        return type(name, (), namespace)


class DataSet(object):
    """Will return data from database"""
    def __init__(self, table_name, columns, data):
        self.__table_name = table_name
        self.__columns = columns
        self.__data = data

    def get_column_names(self):
        """Return column names of table"""
        return self.__columns

    def get_data(self):
        """Return tuple of data"""
        return tuple(self.__data)

    def get_table_name(self):
        """Return table name"""
        return self.__table_name


@final
class Role:
    def __init__(self, name: str, password: str, marker: str) -> None:
        self.__name = name
        self.__password = password
        self.__marker = marker

    @property
    def name(self) -> str:
        return self.__name

    @property
    def password(self) -> str:
        return self.__password
    
    @property
    def marker(self) -> str:
        return self.__marker

    def set_marker(self, new_marker: str) -> None:
        self.__marker = new_marker


class RoleRights:
    SUPERUSER = 50
    CREATEROLE = 30
    CREATEDATABASE = 10


class RolesManager:
    OBJECT = None

    def __new__(cls, *args):
        if not RolesManager.OBJECT:
            RolesManager.OBJECT = super().__new__(cls)
            return RolesManager.OBJECT
        else:
            return RolesManager.OBJECT

    def __init__(self, connection) -> None:
        self.__roles_center: dict = {}
        self.__connection = connection

    def create_role(self, role: Role):
        self.__roles_center.update({role.name : role})
        self.__connection.execute(
            "CREATE ROLE {} WITH LOGIN PASSWORD '{}' {};".format(
                role.name,
                role.password,
                role.marker
            )
        )

    def delete_role(self, name: str):
        self.__roles_center.pop(name)

    def change_rights(self, name: str, marker: str):
        user: Role | None = self.__roles_center.get(name)
        if user:
            user.set_marker(marker)
            return True
        return False

    def get_roles(self):
        return self.__roles_center
