from databaser.db_parser.table_data.condition_parser import ConditionParser


class Update:
    def __init__(self, table_name: str, data: dict, conditions: dict, table_quote: str = "", field_quote: str = "", value_quote: bool = False, schema_name: str = "public"):
        self.table_name = table_name
        self.schema_name = schema_name
        self.conditions = conditions
        self.data = data

        self.table_quote = table_quote
        self.field_quote = field_quote
        self.value_quote = "'" if value_quote else ""

    def get_sql(self):
        data = []
        where = "" if len(self.conditions.keys()) == 0 else ConditionParser(self.conditions, self.field_quote).get_parsed()

        for field in self.data.keys():
            value = f"{self.field_quote}{field}{self.field_quote} = '{self.data[field]}'"
            data.append(value)

        if len(data) == 0:
            return ""

        if where != "":
            where = "WHERE " + where

        return f"UPDATE {self.table_quote}{self.schema_name}{self.table_quote}.{self.table_quote}{self.table_name}{self.table_quote} SET {f', '.join(data)} {where};"
