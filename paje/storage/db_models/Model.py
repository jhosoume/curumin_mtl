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
    def _get_id_saved(cls):
        return cls.db._cursor.lastrowid

    @classmethod
    def _fetchone(cls, sql_select, args = None):
        cls.db.query(sql_select, args)
        instance = cls.db._cursor.fetchone()
        return cls._from_query(instance)

    @classmethod
    def _fetchall(cls, sql_select, args = None):
        cls.db.query(sql_select, args)
        instances = cls.db._cursor.fetchall()
        return [cls._from_query(inst) for inst in instances]

    @classmethod
    @abstractmethod
    def _from_query(cls, inst):
        pass

    @classmethod
    def get_all(cls):
        sql_all = "SELECT * FROM {};".format(cls.table_name)
        return cls._fetchall(sql_all)
