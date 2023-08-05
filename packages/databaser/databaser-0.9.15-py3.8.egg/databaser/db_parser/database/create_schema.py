class CreateSchema:
    def __init__(self, schema_name: str, table_quote: str = '"'):
        self.schema_name = schema_name
        self.table_quote = table_quote

    def get_sql(self):
        sql = f"CREATE SCHEMA {self.table_quote}{self.schema_name}{self.table_quote};"
        return sql
