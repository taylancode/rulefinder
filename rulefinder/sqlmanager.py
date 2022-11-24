'''
PostgresSQL Manager
SQL wrapper to execute queries
'''

import psycopg2
from rulefinder.config import config

class SQL:

    '''
    Main wrapper class
    '''

    def __init__(self) -> None:
        '''
        Initiates the DB connection and creates a cursor
        '''
        self.db_con = None

        try:
            
            if not self.db_con:
                params = config()
                self.db_con = psycopg2.connect(**params)
                self.cur = self.db_con.cursor()

        except (Exception, psycopg2.DatabaseError) as err:
            raise Exception(f"Failure to initiate Database cursor {err}")


    def excecute_sql(self, sql: str, *args: str) -> str:

        '''
        Executes SQL query and returns data if it's a SELECT query

        :param sql: SQL Query string
        :return: Data string if SELECT query
        '''
        
        self.cur.execute(sql, *args)
        try:
            result = self.cur.fetchall()
            return result

        #We ignore this error since it occurs if trying to return data from non SELECT query
        except psycopg2.ProgrammingError:
            pass
        

    def close_connect(self, close_cur: bool, close_DB: bool, commit: bool) -> None:
        '''
        Handle closing the DB connections

        :param close_cur: Boolean to close cursor
        :param close_DB: Boolean to close Database connection
        :param commit: Boolean to commit changes to Database
        '''
        
        if commit is True:
            self.db_con.commit()
        
        if close_cur is True:
            self.cur.close()

        if close_DB is True:
            self.db_con.close()
