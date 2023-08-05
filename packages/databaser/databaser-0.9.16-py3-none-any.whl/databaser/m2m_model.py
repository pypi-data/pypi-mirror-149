from typing import List

from .data_model import DataModel
from .pgsql import Query


class Many2ManyModel(DataModel):

    table_b = None
    join_field = None

    def get(self, fields: List = None, condition: dict = {}, joins: dict = None,
                 group_by: list = [], order_by: dict = {}, limit: int = 0, skip: int = 0):

        # TODO: Add filter param w/ default

        if self.table_b is not None:
            raise Exception("Joining Table Missing")

        if fields is None:
            fields = self.__get_fields()

        if joins is None:
            joins = {
                self.table_b: {
                    "$table": "$this",
                    "$type": "innerJoin",  # innerJoin, leftJoin, rightJoin
                    "$on": {
                        "$type": "$eq",
                        self.table_name: str(self.join_field),
                        self.table_b: str("id"),
                    }
                },
            }

        sql = Query(
            'pgsql'
        ).find(self.table_name, fields, condition, joins, group_by, order_by, limit, skip,
               schema_name=self.schema_name).get_sql()

        self.__sql.append(sql)
        return self
