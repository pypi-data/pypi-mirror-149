import re
from typing import List


class FieldParser:
    def __init__(self, fields: List[str], table_name: str, schema_name: str = "public", table_quote: str = '"',
                 field_quote: str = '"'):
        self.fields = fields
        self.table_name = table_name
        self.schema_name = schema_name
        self.table_quote = table_quote
        self.field_quote = field_quote

    def parse(self):
        if self.fields is None or len(self.fields) == 0:
            return "*"

        fields = []
        for field in self.fields:
            alias = field.split(" as ")
            if alias.__len__() > 1:
                field = alias[0]
                alias = alias[-1]
            else:
                alias = ""

            f = ""
            if re.search("[a-zA-Z]+\([^\)]*\)(\.[^\)]*\))?", field):
                split = field.split("(")
                f = split[0]
                field = split[-1][:-1]

            field_split = field.split(".")
            field = field_split[-1] if field_split.__len__() in [1, 2, 3] else field
            table_name = field_split[-2] if field_split.__len__() in [2, 3] else self.table_name
            schema_name = field_split[-3] if field_split.__len__() == 3 else self.schema_name

            schema_name = f"{self.table_quote}{schema_name}{self.table_quote}."
            table_name = f"{self.table_quote}{table_name}{self.table_quote}."
            field = schema_name + table_name + f"{self.field_quote}{field}{self.field_quote}"
            field = f"{f}({field})" if f != "" else field
            field = f"{field} as {alias}" if alias != "" else field
            fields.append(field)
        # fields = [f"{self.table_quote}{self.schema_name}{self.table_quote}.{self.table_quote}{self.table_name}{self.table_quote}.{self.field_quote}{field}{self.field_quote}"
        #                for field in self.fields]

        fields = f','.join(fields)

        return fields
