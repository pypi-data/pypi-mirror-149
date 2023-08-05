from typing import Any, Dict
from .core import CheckDatas, Connection, SQLCnd, CheckColumns, OperationsConveyor
from ..types_ import Column, DataSet, Table, BasicTypes

from .exceptions_ import SlashRulesError, SlashLenMismatch, SlashTypeError


class Insert():
    def __init__(self, conn: Connection, table: Table, names: Any, values: Any, rules="*"):
        names = [names] if (type(names) != list) and (type(names) != tuple) else names
        values = [values] if (type(values) != list) and (type(values) != tuple) else values

        if len(names) != len(values):
            raise SlashLenMismatch(
                """The length of the data and the length of the columns do not match.
                    Column length: {}
                    Values length: {}
                """.format(
                    len(names),
                    len(values)
                )
            )

        self.__names = names
        self.__values = values
        self.__rules = rules
        self.__table = table
        self.__responce = self.__validate()
        conn.execute(
            CheckDatas.check_sql(self.__responce[0], "insert"),
           "insert operation",
            self.__responce[1]
        )

    def __validate(self):
        CheckDatas.check_str(self.__table.name)
        CheckDatas.check_column_names(self.__names, "INSERT")
        CheckDatas.check_rules(self.__values, self.__rules)

        return OperationsConveyor.make_queryset(
            table=self.__table,
            names=self.__names,
            values=self.__values,
            operation_title="INSERT"
        )

    @property
    def responce(self):
        return self.__responce

    @property
    def table(self):
        return self.__table


class Delete():
    def __init__(self, conn: Connection, table: Table, condition: SQLCnd):
        self.__responce = self.__validate(table, condition)
        conn.execute(
            CheckDatas.check_sql(self.__responce, "delete"),
            "delete operation"
        )

    def __validate(self, table, condition):
        CheckDatas.check_str(table.name)

        return OperationsConveyor.make_queryset(
            table=table,
            condition=condition,
            operation_title="DELETE"
        )

    @property
    def responce(self):
        return self.__responce


class Select():
    def __init__(self, conn: Connection, table: Table, names: tuple, condition: SQLCnd):
        names = [names] if (type(names) != list) and (type(names) != tuple) else names

        self.__conn = conn
        self.__table = table
        self.__names = names
        self.__responce = self.__validate(condition)

    def __validate(self, condition):
        CheckDatas.check_str(self.__table.name)
        CheckDatas.check_column_names(self.__names, "SELECT")

        return OperationsConveyor.make_queryset(
            table=self.__table,
            names=self.__names,
            condition=condition,
            operation_title="SELECT"
        )

    def get(self):
        self.__conn.execute(
            CheckDatas.check_sql(self.__responce, "select"),
            "select operation"
        )

        return DataSet(
            self.__table.name, self.__names, self.__conn.fetchall()
        )

    @property
    def responce(self):
        return self.__responce


class Update():
    def __init__(
        self,
        conn: Connection,
        table: Table,
        names: tuple,
        values: tuple,
        condition,
        rules="*"
    ):
        self.__responce = self.__validate(
            table, names, values, condition, rules
        )
        conn.execute(
            CheckDatas.check_sql(self.__responce, "update"),
            "update operation"
        )

    def __validate(self, table, names, values, condition, rules):
        names = [names] if (type(names) != list) and (type(names) != tuple) else names
        values = [values] if (type(values) != list) and (type(values) != tuple) else values

        CheckDatas.check_str(table.name)

        CheckDatas.check_column_names(names, "UPDATE")
        names = [i.name for i in names]

        return OperationsConveyor.make_queryset(
            table=table,
            names=names,
            values=values,
            condition=condition,
            rules=rules,
            operation_title="UPDATE"
        )

    @property
    def responce(self):
        return self.__responce


class _Joins:
    PARTS: Dict = {
        "ij": ("INNER JOIN",),
        "foj": ("FULL OUTER JOIN",),
        "foj_": ("FULL OUTER JOIN", "WHERE {} IS NULL OR {} IS NULL"),
        "lj": ("LEFT JOIN",),
        "lj_": ("LEFT JOIN", "WHERE {} IS NULL"),
        "rj": ("RIGHT JOIN",),
        "rj_": ("RIGHT JOIN", "WHERE {} IS NULL"),
    }
    def __init__(
        self,
        conn: Connection,
        tables,
        names: Any,
        condition: str,
        t_: str
    ):
        self._conn = conn
        self._tables = tables
        self.names = names
        self.t_ = t_
        self.join_type = _Joins.PARTS.get(t_)

        self._responce = self.__validate(condition)

    def __validate(self, condition):
        SQL_RESPONCE = "SELECT {} FROM {} {} {} ON {} {}"
        for name in self.names:
            if type(name) is not Column:
                raise SlashTypeError(
                    f"""
                    Type of this object should be Column, not {type(name)}
                    Operation: INNER JOIN
                    Object value: --{name}--
                    """
                )
            CheckDatas.check_str(name.name)

        for table in self._tables:
            if type(table) is not Table:
                raise SlashTypeError(
                    f"""
                    Type of this object should be Table, not {type(name)}
                    Operation: INNER JOIN
                    Object value: --{name}--
                    """
                )
            CheckDatas.check_str(table.name)
        
        temp = None
        if self.t_ == "foj_":
            temp = condition.split(" ")
        elif self.t_ == "lj_":
            temp = condition.split(" ")[-1]
        elif self.t_ == "rj_":
            temp = condition.split(" ")[0]

        return SQL_RESPONCE.format(
            ", ".join([".".join((item._p, item.name)) for item in self.names]),
            self._tables[0].name,
            self.join_type[0],
            self._tables[1].name,
            condition,
            "" if len(self.join_type) == 1 else self.join_type[1].format(
                *[temp[0], temp[-1]] if self.t_ == "foj_" else temp.split()
            )
        )

    def get(self):
        self._conn.execute(
            CheckDatas.check_sql(self._responce, "select"),
            "select operation"
        )
        return DataSet(
            self._tables, self.names, self._conn.fetchall()
        )


class Operations:
    def __init__(self, connection, table_link=None):
        self.__connection = connection
        self.__table = table_link

    @property
    def connection(self):
        return self.__connection

    def insert(self, table, names, values, *, rules="*"):
        if self.__table:
            table = self.__table

        if table.__dict__.get("_is_unated") is not None:
            table._is_unated

            data: dict = dict(zip(names, values))

            for one_table in table.tables:
                columns_list = []
                for column in one_table.columns:
                    columns_list.append(column.name)

                Insert(
                    self.__connection,
                    one_table,
                    columns_list,
                    [data[i] for i in columns_list],
                    rules
                )
        else:
            if rules == "*":
                Insert(self.__connection, table, names, values)
            else:
                Insert(
                    self.__connection, table, names, values, rules
                )

    def select(self, table, names, condition=" "):
        if self.__table:
            table = self.__table

        if table.__dict__.get("_is_unated") is not None:
            table._is_unated

            data_matrix = []
            output = []
            result = []

            for one_table in table.tables:
                columns_list = []
                for column in one_table.columns:
                    columns_list.append(column.name)

                select_query = Select(self.__connection, one_table, columns_list, condition).get()
                temp = []
                for data in select_query.get_data():
                    temp.append(data)
                data_matrix.append(temp)

            for t in range(len(data_matrix)):
                temp_data = []
                for i, item in enumerate(data_matrix):
                    for n, _ in enumerate(item):
                        temp_data.append(data_matrix[n][t])
                    break
                output.append(temp_data)

            for i, output_item in enumerate(output):
                temp_user_data = []
                for item_frame in output_item:
                    for item in item_frame:
                        temp_user_data.append(item)
                len_ = len(temp_user_data)

                for n in range(len_-1):
                    if temp_user_data.count(temp_user_data[n]) > 1:
                        del temp_user_data[n]
                result.append(tuple(temp_user_data))

            return DataSet(table.name, table.columns, result)
        else:
            return Select(self.__connection, table, names, condition).get()

    def delete(self, table, condition=" "):
        if self.__table:
            table = self.__table

        if table.__dict__.get("_is_unated") is not None:
            table._is_unated

            CheckColumns.check(condition, table.tables)
            for table_item in table.tables:
                Delete(self.__connection, table_item, condition)
        else:
            return Delete(self.__connection, table, condition)

    def update(self, table, column_names, values, condition=" "):
        if self.__table:
            table = self.__table

        if table.__dict__.get("_is_unated") is not None:
            table._is_unated

            data: dict = dict(zip(column_names, values))

            for one_table in table.tables:
                columns_list = []
                for column in one_table.columns:
                    columns_list.append(column.name)

                Update(
                    self.__connection,
                    one_table,
                    columns_list,
                    [data[i] for i in columns_list],
                    condition
                )
        else:
            Update(self.__connection, table, column_names, values, condition)

    def inner_join(self, tables, names, condition):
        return _Joins(self.__connection, tables, names, condition, "ij").get()

    def full_join(self, tables, names, condition):
        return _Joins(self.__connection, tables, names, condition, "foj").get()
    
    def full_not_same_join(self, tables, names, condition):
        return _Joins(self.__connection, tables, names, condition, "foj_").get()

    def left_join(self, tables, names, condition):
        return _Joins(self.__connection, tables, names, condition, "lj").get()

    def left_not_r_join(self, tables, names, condition):
        return _Joins(self.__connection, tables, names, condition, "lj_").get()

    def right_join(self, tables, names, condition):
        return _Joins(self.__connection, tables, names, condition, "rj").get()

    def right_not_l_join(self, tables, names, condition):
        return _Joins(self.__connection, tables, names, condition, "rj_").get()

    def __enter__(self):
        return self
    
    def __exit__(self, *args): ...
