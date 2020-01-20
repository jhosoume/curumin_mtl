from paje.storage.db_models.Model import Model

class Feature(Model):
    table_name = "features"

    def __init__(self, name = "", id = None):
        self.id = id
        self.name = name

    def __repr__(self):
        return "Feature(id = {}, name = {})".format(self.id, self.name)

    @classmethod
    def create_table(cls):
        sql_create = """
            CREATE TABLE IF NOT EXISTS {} (
                id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(255) NOT NULL UNIQUE,
                INDEX (name)
            );
        """.format(cls.table_name)
        Feature._create_table(sql_create)

    def save(self):
        sql_insert = """
            INSERT INTO datasets (name)
                VALUES (%s);
        """
        attrs = [self.name, self.preprocessed, self.preprocess]
        Feature._query(sql_insert, attrs)
        Feature._commit()
        self.id = Feature._get_id_saved()
        print("Feature record inserted.")

    @classmethod
    def _from_query(cls, inst):
        return Feature(
            id = inst[0],
            name = inst[1],
            preprocess = inst[3]
        )

    @classmethod
    def get(cls, feature):
        sql_select = """
            SELECT * FROM features
            WHERE id = %s;
        """
        return cls._fetchone(sql_select, [dataset.id])

    @classmethod
    def get_one(cls, name, preprocess):
        sql_select = """
            SELECT * FROM features
            WHERE name = %s AND
                  preprocess = %s;
        """
        attrs = [name, preprocess]
        return cls._fetchone(sql_select, attrs)

    @classmethod
    def get_by_name(cls, name):
        sql_select = """
            SELECT * FROM features
            WHERE name = %s;
        """
        return cls._fetchall(sql_select, [name])

    @classmethod
    def get_preprocessed_by(cls, preprocess):
        sql_select = """
            SELECT * FROM features
            WHERE preprocess = %s;
        """
        return cls._fetchall(sql_select, [preprocess])
