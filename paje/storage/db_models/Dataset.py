from paje.storage.db_models.Model import Model

class Dataset(Model):
    table_name = "datasets"

    def __init__(self, name = "", id = None):
        self.id = id
        self.name = name

    def __repr__(self):
        return "Dataset(id = {}, name = {})".format(self.id, self.name)

    @classmethod
    def create_table(cls):
        sql_create = """
            CREATE TABLE IF NOT EXISTS {} (
                id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(255) NOT NULL,
                INDEX (name)
            );
        """.format(cls.table_name)
        Dataset._create_table(sql_create)

    def save(self):
        sql_insert = """
            INSERT INTO datasets (name)
                VALUES (%s);
        """
        Dataset._query(sql_insert, [self.name])
        Dataset._commit()
        self.id = Dataset._get_id_saved()

    @classmethod
    def _from_query(cls, inst):
        return Dataset(
            id = inst[0],
            name = inst[1]
        )

    @classmethod
    def get(cls, dataset):
        sql_select = """
            SELECT * FROM datasets
            WHERE id = %s;
        """
        return cls._fetchone(sql_select, [dataset])

    @classmethod
    def get_one(cls, name):
        sql_select = """
            SELECT * FROM datasets
            WHERE name = %s;
        """
        return cls._fetchone(sql_select, [name])

    @classmethod
    def get_or_insert(cls, name):
        sql_select = """
            SELECT * FROM datasets
            WHERE name = %s
            LIMIT 1;
        """
        attrs = [name]
        result = cls._fetchone(sql_select, attrs)
        if result:
            return result
        else:
            sql_insert = """
                INSERT INTO datasets (name)
                    VALUES (%s);
            """
            cls._query(sql_insert, [name])
            cls._commit()
            return cls.get_one(name)
