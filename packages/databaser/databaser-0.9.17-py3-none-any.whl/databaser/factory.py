
# TODO: Init DB and tables automatically
# Not Advised to use in production

class Factory:
    def __init__(self, tables, **kwargs):
        self.kwargs = kwargs
        self.drop_tables: int = int(kwargs['drop_tables'])

        self.tables: list = tables

    def create_table(self):
        pass

    def create_database(self):
        pass

    def drop_table(self, table):
        pass

    def run(self):
        if self.drop_tables > 0:
            print(("-" * 10), "DROP TABLES", ("-" * 10))
            for table in reversed(self.tables):
                self.drop_table(table)

        for table in tables:
            create_table(table)
