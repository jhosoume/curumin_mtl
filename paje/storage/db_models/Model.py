from abc import abstractmethod, ABC

from paje.storage.db_models.mtldbbase import MtLDBBase

class Model(ABC):
    db = MtLDBBase()

    @property
    @abstractmethod
    def table_name(self):
        pass

    @classmethod
    def _create_table(cls, sql_string):
        cls.db.query(sql_string)
        cls._commit()

    @classmethod
    def _query(cls, sql_string, attrs = None):
        cls.db.query(sql_string, attrs)

    @classmethod
    def _commit(cls):
        cls.db._con.commit()

    @classmethod
    @abstractmethod
    def create_table(cls):
        pass

    @classmethod
    def delete_table(cls):
        sql_delete = """
            DROP TABLE {};
        """.format(cls.table_name)
        cls.db.query(sql_delete)
        cls._commit()

    @abstractmethod
    def save(self):
        pass

    @classmethod
    @abstractmethod
    def _from_query(cls, inst):
        pass

    @classmethod
    def get_all(cls):
        sql_all = "SELECT * FROM {};".format(cls.table_name)
        cls.db.query(sql_all)
        instances = cls.db._cursor.fetchall()
        return [cls._from_query(inst) for inst in instances]
