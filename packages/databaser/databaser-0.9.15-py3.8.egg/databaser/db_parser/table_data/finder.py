from typing import List

from databaser.db_parser.table_data.field_parser import FieldParser
from databaser.engine.engine import DatabaseEngine
from databaser.engine.result import ExecutionResult
from databaser.db_parser.table_data.condition_parser import ConditionParser
from databaser.db_parser.table_data.join_parser import JoinParser


class Finder:

    def __init__(self, table_name: str, fields: List[str] = None, condition: dict = {}, joins: dict = {},
                 group_by: list = [], order_by: dict = {}, limit: int = 0, skip: int = 0, table_quote="",
                 field_quote="", schema_name: str = "public"):
        self.table_name = table_name
        self.schema_name = schema_name
        self.limit = limit
        self.offset = skip
        self.conditions = condition
        self.joins = joins

        self.table_quote = table_quote
        self.field_quote = field_quote

        self.group_by = group_by
        if group_by is None or len(group_by) == 0:
            self.group_by = []

        self.order_by = order_by
        if order_by is None or len(order_by.keys()) == 0:
            self.order_by = {}

        self.fields = fields

    def order_by_parser(self, order_by: dict):
        orders = []
        for field in order_by.keys():
            order_type = order_by[field]
            if type(order_type) is not str:
                if type(order_type) is int:
                    order_type = "ASC" if order_type > 0 else "DESC"
                elif type(order_type) is bool:
                    order_type = "ASC" if order_type else "DESC"
                else:
                    order_type = "ASC"
            else:
                order_type = order_type.upper()

            orders.append(f'{self.field_quote}{field}{self.field_quote} {order_type}')

        return f"ORDER BY {','.join(orders)}"

    def get_sql(self) -> str:
        clauses = []

        if len(self.joins.keys()) > 0:
            joins = JoinParser(
                self.table_name,
                self.joins,
                self.table_quote,
                self.field_quote
            ).get_parsed()

            clauses.append(joins)

        # Set fields shape
        self.fields = FieldParser(self.fields, self.table_name, self.schema_name).parse()

        where = "" if len(self.conditions.keys()) == 0 else "WHERE " + ConditionParser(self.conditions,
                                                                                       self.field_quote).get_parsed()
        if where != "":
            clauses.append(where)

        # group_by = "" if len(
        #     self.group_by) == 0 else f"GROUP BY {self.field_quote}{f'{self.field_quote}, {self.field_quote}'.join(self.group_by)}{self.field_quote}"
        # if group_by != "":
        #     clauses.append(group_by)

        if self.group_by.__len__() != 0:
            group_by = "GROUP BY "
            count = self.group_by.__len__()
            for idx, group in enumerate(self.group_by):
                table_name = self.table_name
                field = group.split(".")
                if len(field) > 1:
                    table_name = field[0]
                field = field[-1]

                group_by += f"{self.table_quote}{self.schema_name}{self.table_quote}.{self.table_quote}{table_name}{self.table_quote}.{self.field_quote}{field}{self.field_quote}"
                group_by += ", " if count > 1 and idx < (count-1) else ""
            # group_by = f"GROUP BY {self.field_quote}{self.schema_name}{self.field_quote}.{self.field_quote}{self.table_name}{self.field_quote}.{self.field_quote}{f'{self.field_quote}, {self.field_quote}{self.schema_name}{self.field_quote}.{self.table_quote}{self.table_name}{self.table_quote}.{self.field_quote}'.join(self.group_by)}{self.field_quote}"
            clauses.append(group_by)

        order_by = "" if len(self.order_by.keys()) == 0 else self.order_by_parser(self.order_by)
        if order_by != "":
            clauses.append(order_by)

        limit = f"LIMIT {self.limit}" if self.limit is not None and self.limit > 0 else ""
        if limit != "":
            clauses.append(limit)

        offset = f"OFFSET {self.offset}" if self.offset is not None and self.offset > 0 else ""
        if offset != "":
            clauses.append(offset)

        if len(clauses) > 0:
            clauses.insert(0, "")

        return f"""SELECT {self.fields} FROM {self.table_quote}{self.schema_name}{self.table_quote}.{self.table_quote}{self.table_name}{self.table_quote}{' '.join(clauses)};"""

    def run(self, **connection_params) -> ExecutionResult:
        sql = self.get_sql()
        result = DatabaseEngine(**connection_params).execute(sql=sql, transaction=False,
                                                     has_return=False, return_many=False)

        return result
