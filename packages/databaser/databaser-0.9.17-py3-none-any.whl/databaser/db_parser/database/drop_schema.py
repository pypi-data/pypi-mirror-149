class DropSchema:
    def __init__(self, schema_name: str, table_quote: str = '"', cascade: bool = False):
        self.schema_name = schema_name
        self.table_quote = table_quote
        self.cascade = cascade

    def get_sql(self):
        return f"DROP SCHEMA IF EXISTS {self.table_quote}{self.schema_name}{self.table_quote} {'CASCADE' if self.cascade else ''};"
