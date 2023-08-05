class DropDatabase:
    def __init__(self, database_name: str, table_quote: str = '"'):
        self.database_name = database_name
        self.table_quote = table_quote

    def get_sql(self):
        return f"DROP DATABASE {self.table_quote}{self.database_name}{self.table_quote};"
