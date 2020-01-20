from paje.storage.db_models.Model import Model

class Preprocess(Model):
    table_name = "preprocesses"

    def __init__(self, name = "", type = "", id = None):
        self.id = id
        self.name = name
        self.type = type

    def __repr__(self):
        return "Preprocess(id = {}, name = {}, type = {})".format(
            self.id, self.name, self.type)

    @classmethod
    def create_table(cls):
        sql_create = """
            CREATE TABLE IF NOT EXISTS {} (
                id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(255) NOT NULL UNIQUE,
                type VARCHAR(255) NOT NULL,
                INDEX (name)
            );
        """.format(cls.table_name)
        Preprocess._create_table(sql_create)

    def save(self):
        sql_insert = """
            INSERT INTO preprocesses (name, type)
                VALUES (%s, %s);
        """
        Preprocess._query(sql_insert, [self.name, self.type])
        Preprocess._commit()
        self.id = Preprocess._get_id_saved()
        print("Preprocess record inserted.")

    @classmethod
    def _from_query(cls, inst):
        return Preprocess(
            id = inst[0],
            name = inst[1],
            type = inst[2]
        )

    @classmethod
    def get(cls, feature):
        sql_select = """
            SELECT * FROM preprocesses
            WHERE id = %s;
        """
        return cls._fetchone(sql_select, [feature.id])

    @classmethod
    def get_one(cls, name):
        sql_select = """
            SELECT * FROM preprocesses
            WHERE name = %s;
        """
        return cls._fetchone(sql_select, [name])

    @classmethod
    def get_by_type(cls, type):
        sql_select = """
            SELECT * FROM preprocesses
            WHERE type = %s;
        """
        return cls._fetchall(sql_select, [type])
