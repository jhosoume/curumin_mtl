from paje.storage.db_models.Model import Model

class Score(Model):
    table_name = "scores"

    def __init__(self, name = "", id = None):
        self.id = id
        self.name = name

    def __repr__(self):
        return "Score(id = {}, name = {})".format(self.id, self.name)

    @classmethod
    def create_table(cls):
        sql_create = """
            CREATE TABLE IF NOT EXISTS {} (
                id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(255) NOT NULL UNIQUE,
                INDEX (name)
            );
        """.format(cls.table_name)
        Score._create_table(sql_create)

    def save(self):
        sql_insert = """
            INSERT INTO scores (name)
                VALUES (%s);
        """
        Score._query(sql_insert, [self.name])
        Score._commit()
        self.id = Score._get_id_saved()

    @classmethod
    def _from_query(cls, inst):
        return Score(
            id = inst[0],
            name = inst[1]
        )

    @classmethod
    def get(cls, score):
        sql_select = """
            SELECT * FROM scores
            WHERE id = %s;
        """
        return cls._fetchone(sql_select, [score])

    @classmethod
    def get_one(cls, name):
        sql_select = """
            SELECT * FROM scores
            WHERE name = %s;
        """
        return cls._fetchone(sql_select, [name])

    @classmethod
    def get_or_insert(cls, name):
        sql_select = """
            SELECT * FROM scores
            WHERE name = %s
            LIMIT 1;
        """
        result = cls._fetchone(sql_select, [name])
        if result:
            return result
        else:
            sql_insert = """
                INSERT INTO scores (name)
                    VALUES (%s);
            """
            cls._query(sql_insert, [name])
            cls._commit()
            return cls.get_one(name)
