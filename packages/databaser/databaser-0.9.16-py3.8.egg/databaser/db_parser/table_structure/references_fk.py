from pydantic import BaseModel


class ReferencesFK:  # TODO: Better scenario needed
    def __init__(self, table_name: str, field_name: str, schema_name: str = "public", table_quote: str = "", field_quote: str = ""):
        self.schema_name = schema_name
        self.table_name = table_name
        self.field_name = field_name

        self.table_quote = table_quote
        self.field_quote = field_quote

    def get_sql(self):
        return f"""REFERENCES {self.table_quote}{self.schema_name}{self.table_quote}.{self.table_quote}{self.table_name}{self.table_quote} ({self.field_quote}{self.field_name}{self.field_quote})"""