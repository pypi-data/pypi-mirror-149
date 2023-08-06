from databaser.db_parser.table_data.condition_parser import ConditionParser


class Delete:
    def __init__(self, table_name: str, conditions, table_quote: str = "", field_quote: str = "", value_quote: bool = False, schema_name: str = "public"):
        self.table_name = table_name
        self.schema_name = schema_name
        self.conditions = conditions

        self.table_quote = table_quote
        self.field_quote = field_quote
        self.value_quote = "'" if value_quote else ""

    def get_sql(self):
        where = "" if len(self.conditions.keys()) == 0 else ConditionParser(self.conditions, self.table_quote).get_parsed()

        if where != "":
            where = "WHERE " + where

        return f"DELETE FROM {self.table_quote}{self.schema_name}{self.table_quote}.{self.table_quote}{self.table_name}{self.table_quote} {where}"
