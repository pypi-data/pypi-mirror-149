import pyodbc, pandas
import urllib
from sqlalchemy import create_engine
from Richdata.abcdatabase import AbcDatabase


class SQLServer(AbcDatabase):
    conn_string = None
    port = None # don't use
    sslmode = None # don't use
    driver = 'FreeTDS'
    conn = None


    def __init__(self):
        try:
            self.conn_string = f"DRIVER={{{self.driver}}};SERVER={self.host};DATABASE={self.dbname};UID={self.user};PWD={self.password}"
            self.conn = pyodbc.connect(self.conn_string)
        except Exception as e:
            raise Exception(e)

    def _conn(self):
        self.conn = pyodbc.connect(self.conn_string)
        return self.conn

    def get_cursor(self):
        """Don't use"""
        # TODO get_cursor()
        pass

    def fetchAll(self, query):
        try:
            self._conn()
            df = pandas.read_sql(query, con=self.conn)
        except Exception as e:
            raise Exception(e)
        finally:
            self.conn.close()
        return df

    def fetchOne(self, query):
        try:
            self._conn()
            db = self.conn.cursor()
            db.execute(query)
            rows = db.fetchone()
            if rows is None:
                return None
            if len(rows) > 0:
                return rows[0]
            else:
                return None
        except Exception as e:
            raise Exception(e)

    def fetchRow(self, query):
        try:
            self._conn()
            db = self.conn.cursor()
            db.execute(query)
            rows = db.fetchone()
            if len(rows) > 0:
                return list(rows)
            else:
                return list()
        except Exception as e:
            raise Exception(e)

    def fetchCol(self, query):
        df = self.fetchAll(query)
        return df.iloc[:, 0].tolist()

    def fetchNative(self, query):
        try:
            self._conn()
            db = self.conn.cursor()
            db.execute(query)
            return db.fetchone()
        except Exception as e:
            raise Exception(e)

    def execute(self, script):
        """Don't use"""
        # TODO: execute()
        pass

    def table_exists(self, table_name, schema=None):
        if schema is None:
            cant = self.fetchOne(f"SELECT COUNT(*) FROM information_schema.tables WHERE table_name = '{table_name}' ")
        else:
            cant = self.fetchOne(
                f"SELECT COUNT(*) FROM information_schema.tables WHERE table_name = '{table_name}' AND table_schema='{schema}'")
        return cant > 0

    def close(self):
        """Don't use"""
        # TODO: close()
        # self.conn.close()
        pass

    def create_engine(self):
        params = urllib.parse.quote_plus(self.conn_string)
        create_engine_string = "mssql+pyodbc:///?odbc_connect=%s" % params
        return create_engine(create_engine_string)