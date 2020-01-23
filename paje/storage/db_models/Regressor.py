from paje.storage.db_models.Model import Model

class Regressor(Model):
    table_name = "regressors"

    def __init__(self, name = "", type = "", id = None):
        self.id = id
        self.name = name
        self.type = type

    def __repr__(self):
        return "Regressor(id = {}, name = {}, type = {})".format(
            self.id, self.name, self.type)

    @classmethod
    def create_table(cls):
        sql_create = """
            CREATE TABLE IF NOT EXISTS {} (
                id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(255) NOT NULL UNIQUE,
                type VARCHAR(255),
                INDEX (name)
            );
        """.format(cls.table_name)
        Regressor._create_table(sql_create)

    def save(self):
        sql_insert = """
            INSERT INTO regressors (name, type)
                VALUES (%s, %s);
        """
        Regressor._query(sql_insert, [self.name, self.type])
        Regressor._commit()
        self.id = Regressor._get_id_saved()

    @classmethod
    def _from_query(cls, inst):
        return Regressor(
            id = inst[0],
            name = inst[1],
            type = inst[2]
        )

    @classmethod
    def get(cls, regressor):
        sql_select = """
            SELECT * FROM regressors
            WHERE id = %s;
        """
        return cls._fetchone(sql_select, [regressor])

    @classmethod
    def get_one(cls, name):
        sql_select = """
            SELECT * FROM regressors
            WHERE name = %s;
        """
        return cls._fetchone(sql_select, [name])

    @classmethod
    def get_or_insert(cls, name):
        sql_select = """
            SELECT * FROM regressors
            WHERE name = %s
            LIMIT 1;
        """
        result = cls._fetchone(sql_select, [name])
        if result:
            return result
        else:
            sql_insert = """
                INSERT INTO regressors (name)
                    VALUES (%s);
            """
            cls._query(sql_insert, [name])
            cls._commit()
            return cls.get_one(name)

    @classmethod
    def get_by_type(cls, type):
        sql_select = """
            SELECT * FROM regressors
            WHERE type = %s;
        """
        return cls._fetchall(sql_select, [type])
