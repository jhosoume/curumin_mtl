from paje.storage.db_models.Model import Model

class Classifier(Model):
    table_name = "classifiers"

    def __init__(self, name = "", type = "", id = None):
        self.id = id
        self.name = name
        self.type = type

    def __repr__(self):
        return "Classifier(id = {}, name = {}, type = {})".format(
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
        Classifier._create_table(sql_create)

    def save(self):
        sql_insert = """
            INSERT INTO classifiers (name, type)
                VALUES (%s, %s);
        """
        Classifier._query(sql_insert, [self.name, self.type])
        Classifier._commit()
        self.id = Classifier._get_id_saved()
        print("Classifier record inserted.")

    @classmethod
    def _from_query(cls, inst):
        return Classifier(
            id = inst[0],
            name = inst[1],
            type = inst[2]
        )

    @classmethod
    def get(cls, classifier):
        sql_select = """
            SELECT * FROM classifiers
            WHERE id = %s;
        """
        return cls._fetchone(sql_select, [classifier])

    @classmethod
    def get_one(cls, name):
        sql_select = """
            SELECT * FROM classifiers
            WHERE name = %s;
        """
        return cls._fetchone(sql_select, [name])

    @classmethod
    def get_or_insert(cls, name):
        sql_select = """
            SELECT * FROM classifiers
            WHERE name = %s
            LIMIT 1;
        """
        result = cls._fetchone(sql_select, [name])
        if result:
            return result
        else:
            sql_insert = """
                INSERT INTO classifiers (name)
                    VALUES (%s);
            """
            cls._query(sql_insert, [name])
            cls._commit()
            return cls.get_one(name)

    @classmethod
    def get_by_type(cls, type):
        sql_select = """
            SELECT * FROM classifiers
            WHERE type = %s;
        """
        return cls._fetchall(sql_select, [type])
