import psycopg2,pandas
from sqlalchemy import create_engine
from Richdata.abcdatabase import AbcDatabase


class PostgreSQL(AbcDatabase):
    conn_string = None
    port = '5432'
    sslmode = 'allow'  # { required, disable, allow }
    driver = None # don't use
    conn = None

    def __init__(self):
        self._conn()


    def _conn(self):
        self.conn_string = 'host={} user={} dbname={} password={} port={} sslmode={}'.format(
            self.host, self.user, self.dbname, self.password, str(self.port), self.sslmode
        )
        try:
            self.conn = psycopg2.connect(self.conn_string)
        except psycopg2.OperationalError as e:
            raise Exception("OperationalError, verifique la VPN o su red")
        except Exception as e:
            raise Exception(e)

        return self.conn

    def get_cursor(self):
        conn = self._conn()
        return conn.cursor()


    def fetchAll(self, query):
        self._conn()
        df = pandas.read_sql(query, con=self.conn)
        self.conn.close()
        self.conn.close()
        return df



    def fetchOne(self, query):
        self._conn()
        db = self.conn.cursor()
        db.execute(query)
        rows = db.fetchone()
        if len(rows) > 0:
            return rows[0]
        else:
            return None


    def fetchRow(self, query):
        self._conn()
        db = self.conn.cursor()
        db.execute(query)
        rows = db.fetchone()
        if len(rows) > 0:
            return list(rows)
        else:
            return list()


    def fetchCol(self, query):
        df = self.fetchAll(query)
        return df.iloc[:, 0].tolist()

    def fetchNative(self, query):
        """Don't use"""
        # TODO fetchNative()
        pass

    def execute(self, script):
        affected_rows = -1
        self._conn()
        cursor = self.conn.cursor()
        cursor.execute(script)

        self.conn.commit()
        affected_rows = cursor.rowcount
        self.conn.close()
        return affected_rows


    def table_exists(self, table_name,schema=None):
        if schema is None:
            cant = self.fetchOne(f"SELECT COUNT(*) FROM information_schema.tables WHERE table_name = '{table_name}' ")
        else:
            cant = self.fetchOne(f"SELECT COUNT(*) FROM information_schema.tables WHERE table_name = '{table_name}' AND table_schema='{schema}'")
        return cant > 0

    def close(self):
        self.conn.close()

    def create_engine(self):
        # TODO deactivate logging 'sqlalchemy.engine'
        #import logging as log
        #log.getLogger('sqlalchemy.engine').setLevel(log.ERROR)
        return create_engine(f'postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}?sslmode={self.sslmode}')

