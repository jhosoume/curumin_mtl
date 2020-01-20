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
            INSERT INTO features (name)
                VALUES (%s);
        """
        Feature._query(sql_insert, [self.name])
        Feature._commit()
        self.id = Feature._get_id_saved()
        print("Feature record inserted.")

    @classmethod
    def _from_query(cls, inst):
        return Feature(
            id = inst[0],
            name = inst[1]
        )

    @classmethod
    def get(cls, feature):
        sql_select = """
            SELECT * FROM features
            WHERE id = %s;
        """
        return cls._fetchone(sql_select, [feature.id])

    @classmethod
    def get_one(cls, name):
        sql_select = """
            SELECT * FROM features
            WHERE name = %s;
        """
        return cls._fetchone(sql_select, [name])
