from typing import Union


class JoinParser:
    def __init__(self, table_name: str, joins: dict, table_quote: str = "", field_quote: str = ""):
        self.joins = joins
        self.table_name = table_name
        self.table_quote = table_quote
        self.field_quote = field_quote

    def get_parsed(self) -> str:
        joins = []
        for join_table in self.joins.keys():  # Get all joining tables
            if join_table == "$schema_name":
                continue
            joins.append(self.parse(join_table, self.joins[join_table]))

        return ' '.join(joins)

    def parse(self, joining_table: str, table: dict, recursive: bool = False):

        conditions = self.parse_join_condition(joining_table=joining_table, table=table, schema_name=self.joins['$schema_name'])

        print("conditions", "$and" in table['$on'])
        if "$and" in table['$on']:
            conditions += " AND " + self.parse(joining_table, table['$on']['$and'], True)

        if "$or" in table['$on']:
            conditions += " OR " + self.parse(joining_table, table['$on']['$or'], True)

        if recursive:
            return conditions

        joined_type = table['$type']  # innerJoin, leftJoin, rightJoin
        joined_type = self.parse_join_type(joined_type)

        if joined_type is None:
            raise Exception("Undefined Join Type")

        return f"{joined_type} {self.table_quote}{self.joins['$schema_name']}{self.table_quote}.{self.table_quote}{joining_table}{self.table_quote} ON {conditions}"

    def parse_join_type(self, joined_type) -> Union[str, None]:
        if joined_type == "innerJoin":
            return "INNER JOIN"

        if joined_type == "leftJoin":
            return "LEFT JOIN"

        if joined_type == "rightJoin":
            return "RIGHT JOIN"

        return None

    def parse_join_condition(self, joining_table: str, table: dict, schema_name: str = "public"):
        operator = ""
        if "$type" in table['$on']:
            if table['$on']['$type'] == "$eq":
                operator = "="
            elif table['$on']['$type'] == "$gt":
                operator = ">"
            elif table['$on']['$type'] == "$gte":
                operator = ">="
            elif table['$on']['$type'] == "$lt":
                operator = "<"
            elif table['$on']['$type'] == "$lte":
                operator = "<="
            elif table['$on']['$type'] == "$ne":
                operator = "<>"

        columnX = table['$on']['$tableA']
        columnY = table['$on']['$tableB']

        if "$table" not in table:
            raise Exception("Joined Table not specified")

        table_name = table['$table'] if table['$table'] != "$this" else self.table_name
        table_name = f"{self.table_quote}{schema_name}{self.table_quote}.{self.table_quote}{table_name}{self.table_quote}"

        conditions = f"{table_name}." \
                     f"{self.field_quote}{columnX}{self.field_quote} "\
                     f"{operator} " \
                     f"{self.table_quote}{joining_table}{self.table_quote}." \
                     f"{self.field_quote}{columnY}{self.field_quote}"

        return conditions