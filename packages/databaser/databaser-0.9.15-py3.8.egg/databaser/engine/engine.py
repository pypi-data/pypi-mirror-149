from typing import List, Dict, Union

import psycopg2
import psycopg2.extras

from .result import ExecutionResult


class DatabaseEngine:
    transaction = 'BEGIN;'

    def __init__(self, **params):
        # print("params", params)
        if params is None:
            raise Exception("Missing Database Connection string")
        self.params = params

    # TODO: Add SubClasses to handle multiple databases like, MySQL
    def execute(self, sql: Union[str, List] = 'SELECT version()', transaction=False,
                has_return=False, return_many=False) -> ExecutionResult:

        conn = None
        result: List[Dict] = []
        failure = None

        if isinstance(sql, list):
            sql = ''.join(sql)
            # print("SQL:", sql)

        try:
            # read connection parameters
            # connect to the PostgreSQL server
            print('Connecting to the database...')
            conn = psycopg2.connect(**self.params)

            # create a cursor
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            conn.autocommit = False
            try:
                # execute a statement
                # print('PostgreSQL database version:')
                if transaction:
                    sql = self.transaction + sql

                # print('Executing SQL:', sql)
                cur.execute(str(sql))

                # display the PostgreSQL database server version
                if has_return:
                    if return_many:
                        res = cur.fetchall()
                        if res is not None:
                            result.extend(res)

                    else:
                        res = cur.fetchone()
                        if res is not None:
                            result: Dict = dict(res)

                    # print("Result:", dict(result[0]))

                if len(result):
                    has_return = True
                else:
                    has_return = False

                print("COMMITTING")
                conn.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                print("ROLLBACK")
                # print(error)
                conn.rollback()
                raise error

            # close the communication with the PostgreSQL
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            failure = error
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')

        # print("Resulting SQL:", str(sql), type(str(sql)))
        if failure is not None:
            print("failure:", failure)
            raise Exception(failure)

        return ExecutionResult(**{
            "has_values": has_return,
            "sql": str(sql),
            "result": result,
        })
