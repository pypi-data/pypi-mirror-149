from abc import ABC, abstractmethod
class AbcDatabase(ABC):
    conn_string = None
    port = ''


    @property
    @abstractmethod
    def host(self):
        pass

    @property
    @abstractmethod
    def user(self):
        pass

    @property
    @abstractmethod
    def password(self):
        pass

    @property
    @abstractmethod
    def dbname(self):
        pass

    @abstractmethod
    def _conn(self):
        pass

    @abstractmethod
    def fetchAll(self, query):
        pass

    @abstractmethod
    def fetchOne(self, sql):
        pass

    @abstractmethod
    def fetchRow(self, sql):
        pass

    @abstractmethod
    def fetchCol(self, sql):
        pass

    @abstractmethod
    def execute(self, script):
        pass