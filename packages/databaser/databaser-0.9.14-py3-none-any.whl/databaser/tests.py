# from engine.engine import DatabaseEngine
from databaser.engine.engine import DatabaseEngine

from databaser.db_parser.database.create_database import CreateDatabase
from databaser.db_parser.database.drop_database import DropDatabase
from databaser.pgsql import Query, TableStructure
from databaser.db_parser.table_data.insert_from_select import InsertFromSelect
from databaser.db_parser.table_data.update import Update
from databaser.db_parser.table_structure.add_column import AddColumn
from databaser.db_parser.table_structure.create_table import CreateTable, TableField


def test_queries():
    print("*"*15, "Testing queries", "*"*15)
    # SELECT * FROM tablename
    sql = Query("pgsql").find("table_name").get_sql()
    print(sql)
    assert sql == 'SELECT * FROM "public"."table_name";'

    # SELECT a, b, c FROM table_name
    sql = Query("pgsql").find("table_name", ["a", "b", "c"]).get_sql()
    print(sql)
    assert sql == 'SELECT "a","b","c" FROM "public"."table_name";'

    # SELECT a, b, c FROM table_name LIMIT 10
    sql = Query("pgsql").find("table_name", ["a", "b", "c"], limit=10).get_sql()
    print(sql)
    assert sql == 'SELECT "a","b","c" FROM "public"."table_name" LIMIT 10;'

    # SELECT * FROM table_name WHERE name = 'abc'
    condition = {
        "name": {
            "$value": "abc"
        },
    }
    sql = Query("pgsql").find("table_name", ["a", "b", "c"], condition=condition, limit=10).get_sql()
    print(sql)
    assert sql == """SELECT "a","b","c" FROM "public"."table_name" WHERE "name" = 'abc' LIMIT 10;"""

    # SELECT * FROM table_name WHERE name = 'abc' AND names = 'abc'
    condition = {
        "name": {
            "$value": "abc"
        },
        "names": {
            "$value": "abc"
        },
    }
    sql = Query("pgsql").find("table_name", ["a", "b", "c"], condition=condition, limit=10).get_sql()
    print(sql)
    assert sql == """SELECT "a","b","c" FROM "public"."table_name" WHERE "name" = 'abc' AND "names" = 'abc' LIMIT 10;"""

    # SELECT * FROM table_name WHERE name = 'abc'
    condition = {
        "name": {
            "$value": "abc"
        },
        "$group": {
            "$type": "OR",
            "name": {
                "$value": "abc",
            },
            "names": {
                "$like": "%abc%"
            },
            "named": {
                "$in": "a,b,c"
            },
        }
    }
    sql = Query("pgsql").find("table_name", ["a", "b", "c"], condition=condition, limit=10).get_sql()
    print(sql)
    assert sql == """SELECT "a","b","c" FROM "public"."table_name" WHERE "name" = 'abc' AND ("name" = 'abc' OR "names" LIKE '%abc%' OR "named" IN ('a','b','c')) LIMIT 10;"""

    # SELECT * FROM table_name GROUP BY name, lol
    sql = Query("pgsql").find("table_name", group_by=["name", "lol"]).get_sql()
    print(sql)
    assert sql == """SELECT * FROM "public"."table_name" GROUP BY "name", "lol";"""

    # SELECT * FROM table_name ORDER BY name ASC
    sql = Query("pgsql").find("table_name", order_by={"name": True}).get_sql()
    print(sql)
    assert sql == """SELECT * FROM "public"."table_name" ORDER BY "name" ASC;"""

    # SELECT * FROM tableA INNER JOIN tableB ON tableA.columnX = tableB.columnY
    joins = {
        "tableB": {
            "$table": "$this",
            "$type": "innerJoin",  # innerJoin, leftJoin, rightJoin
            "$on": {
                "$type": "$eq",
                "$tableA": "columnX",
                "$tableB": "columnY",
                "$and": {
                    "$table": "$this",
                    "$on": {
                        "$type": "$eq",
                        "$tableA": "columnX",
                        "$tableB": "columnY",
                        "$or": {
                            "$table": "$this",
                            "$on": {
                                "$type": "$eq",
                                "$tableA": "columnX",
                                "$tableB": "columnY",
                            }
                        }
                    }
                }
            }
        },
    }
    sql = Query("pgsql").find("tableA", joins=joins).get_sql()
    print(sql)
    assert sql == """SELECT * FROM "public"."tableA" INNER JOIN "tableB" ON "tableA"."columnX" = "tableB"."columnY" AND "tableA"."columnX" = "tableB"."columnY" OR "tableA"."columnX" = "tableB"."columnY";"""


def test_insertions():
    print("*"*15, "Testing Insertions", "*"*15)
    # SELECT * FROM tablename
    data = {
        "a": 1,
        "b": 2,
        "c": 3,
    }
    sql = Query("pgsql").insert("table_name", data=data, value_quote=True).get_sql()
    print(sql)
    assert sql == """INSERT INTO "public"."table_name" ("a", "b", "c") VALUES ('1', '2', '3');"""

    # TODO: Assign
    # select = Query("pgsql").find("tableB", group_by=["name", "lol"])
    # sql = Query("pgsql").insert_select("table_name", select=select,).get_sql()
    # print(sql)
    # assert sql == """INSERT INTO "public"."table_name" (a,b,c) SELECT * FROM "public"."tableB" GROUP BY "name", "lol";"""


def test_update():
    print("*"*15, "Testing update", "*"*15)
    # UPDATE table_name SET name = 'lol' WHERE name = 'mido'
    conditions = {
        "name": {
            "$value": "mido"
        }
    }
    data = {
        "name": "lol"
    }
    sql = Query("pgsql").update("table_name", data=data, conditions=conditions).get_sql()
    print(sql)
    assert sql == """UPDATE "public"."table_name" SET "name" = 'lol' WHERE "name" = 'mido';"""

    # UPDATE table_name SET name = 'lol' WHERE name = 'mido'
    conditions = {
        "name": {
            "$value": "mido"
        }
    }
    data = {
        "name": "lol",
        "date": "lol",
    }
    sql = Query("pgsql").update("table_name", data=data, conditions=conditions).get_sql()
    print(sql)
    assert sql == """UPDATE "public"."table_name" SET "name" = 'lol', "date" = 'lol' WHERE "name" = 'mido';"""


def test_delete():
    print("*"*15, "Testing Delete", "*"*15)
    # UPDATE table_name SET name = 'lol' WHERE name = 'mido'
    conditions = {
        "name": {
            "$value": "mido"
        }
    }
    sql = Query("pgsql").delete("table_name", conditions=conditions).get_sql()
    print(sql)
    assert sql == """DELETE FROM "public"."table_name" WHERE "name" = 'mido'"""


def table_structure():
    print("*"*15, "Testing Table Structure", "*"*15)
    fields = [
        TableField(**{
            "name": "field_one",
            "data_type": "character varying",
            "not_null": False,
            "primary_key": True,
            "constraint": "UNIQUE",
        }),
        TableField(**{
            "name": "field_one",
            "data_type": "character varying",
            "not_null": False,
            "primary_key": False,
            "constraint": "UNIQUE",
        }),
    ]
    sql = TableStructure("pgsql").create_table("table_name", fields).get_sql()
    print("SQL:", sql)

    sql = TableStructure("pgsql").add_column("tablename", "column_name", "string", True).get_sql()
    print("SQL:", sql)
    # assert sql == "ALTER TABLE tablename ADD COLUMN column_name string NOT NULL"


def test_DB():
    print("*"*15, "Testing test_create_DB", "*"*15)
    # CREATE DATABASE database_name
    sql = CreateDatabase("database_name").get_sql()
    print(sql)
    assert sql == """CREATE DATABASE "database_name";"""

    # CREATE DATABASE database_name
    sql = DropDatabase("database_name").get_sql()
    print(sql)
    assert sql == """DROP DATABASE "database_name";"""

    sql = Query("pgsql").find("table_name").get_sql()
    print(sql)


def test_engine():
    x = {}
    DatabaseEngine(**x).execute("SELECT * FROM X")
