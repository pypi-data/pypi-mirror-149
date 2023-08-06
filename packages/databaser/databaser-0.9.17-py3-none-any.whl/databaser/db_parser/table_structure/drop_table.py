class DropTable:
    def __init__(self, table_name: str, table_quote: str = "", if_exists: bool = False):
        self.table_name = table_name
        self.table_quote = table_quote
        self.if_exists = if_exists

    def get_sql(self):
        if_exists = "IF EXISTS" if self.if_exists else ""
        return f"DROP TABLE {if_exists} {self.table_quote}{self.table_name}{self.table_quote};"
