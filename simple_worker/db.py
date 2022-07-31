import pymysql
from queries import *
from pymysql.cursors import DictCursor

class Database:

    def __init__(self, host, username, password, databasename):
        self.host = host
        self.username = username
        self.password = password
        self.databasename = databasename
        self.conn = self.connect()

    def connect(self):
        return pymysql.connect( host=self.host, user=self.username, password=self.password, db=self.databasename,)

    def execute_query(self,query):
        cur = self.conn.cursor(DictCursor)
        cur.execute(query)
        return cur.fetchall()

    def fetch_sp_list_for_db(self):
        return self.execute_query(get_sp_list_for_db(self.databasename))

    def fetch_table_list_for_db(self):
        return self.execute_query(get_table_list_for_db(self.databasename))

    def fetch_table_definition(self, tablename):
        try:
            return self.execute_query(get_table_definition(tablename))
        except Exception as e:
            return False

    def fetch_sp_def_for_db_spname(self, spname):
        return self.execute_query(get_sp_def_for_db_spname(self.databasename, spname))

    def fetch_sp_def_for_db(self):
        return self.execute_query(get_sp_def_for_db(self.databasename))

    def fetch_sp_param_for_db_spname(self, spname):
        return self.execute_query(get_sp_param_for_db_spname(self.databasename, spname))

    def fetch_sp_param_for_db(self):
        return self.execute_query(get_sp_param_for_db(self.databasename))

    def fetch_index_list_for_db(self):
        return self.execute_query(get_index_list_for_db(self.databasename))

    def fetch_fk_list_for_db(self):
        return self.execute_query(get_fk_list_for_db(self.databasename))