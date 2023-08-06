class AddColumn:
    def __init__(self, table_name: str, column_name: str, data_type: str, not_null: bool, table_quote: str = "",
                 field_quote: str = ""):
        self.table_name = table_name
        self.column_name = column_name
        self.data_type = data_type
        self.not_null = not_null
        self.table_quote = table_quote
        self.field_quote = field_quote

    def get_sql(self):
        nullable = 'NOT NUll' if self.not_null else 'NULL'
        return f"ALTER TABLE {self.table_quote}{self.table_name}{self.table_quote} ADD COLUMN {self.field_quote}{self.column_name}{self.field_quote} {self.data_type} {nullable};"
