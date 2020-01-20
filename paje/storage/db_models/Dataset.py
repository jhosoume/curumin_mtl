from paje.storage.db_models.Model import Model

class Dataset(Model):
    table_name = "datasets"

    def __init__(self, name = "", preprocess = None, id = None):
        self.id = id
        self.name = name
        if preprocess:
            self.preprocessed = True
            self.preprocess = preprocess
        else:
            self.preprocessed = False
            self.preprocess = None

    def __repr__(self):
        return "Dataset(id = {}, name = {}, preprocess = {})".format(
                    self.id, self.name, self.preprocess)

    @classmethod
    def create_table(cls):
        sql_create = """
            CREATE TABLE IF NOT EXISTS {} (
                id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(255) NOT NULL,
                preprocessed BOOLEAN NOT NULL DEFAULT 0,
                preprocess VARCHAR(255) DEFAULT NULL,
                INDEX (name)
            );
        """.format(cls.table_name)
        Dataset._create_table(sql_create)
        sql_unique = """
            ALTER TABLE datasets
                ADD UNIQUE INDEX (name, preprocess);
        """
        Dataset._query(sql_unique)

    def save(self):
        sql_insert = """
            INSERT INTO datasets (name, preprocessed, preprocess)
                VALUES (%s, %s, %s);
        """
        attrs = [self.name, self.preprocessed, self.preprocess]
        Dataset._query(sql_insert, attrs)
        Dataset._commit()
        self.id = Dataset._get_id_saved()
        print("Dataset record inserted.")

    @classmethod
    def _from_query(cls, inst):
        return Dataset(
            id = inst[0],
            name = inst[1],
            preprocess = inst[3]
        )

    @classmethod
    def get(cls, dataset):
        sql_select = """
            SELECT * FROM datasets
            WHERE id = %s;
        """
        return cls._fetchone(sql_select, [dataset.id])

    @classmethod
    def get_one(cls, name, preprocess):
        sql_select = """
            SELECT * FROM datasets
            WHERE name = %s AND
                  preprocess = %s;
        """
        attrs = [name, preprocess]
        return cls._fetchone(sql_select, attrs)

    @classmethod
    def get_or_insert(cls, name, preprocess):
        preprocessed = True if preprocess else False
        sql_select = """
            SELECT * FROM datasets
            WHERE name = %s AND
                  preprocess = %s
            LIMIT 1;
        """
        attrs = [name, preprocess]
        result = cls._fetchone(sql_select, attrs)
        if result:
            return result
        else:
            sql_insert = """
                INSERT INTO datasets (name, preprocessed, preprocess)
                    VALUES (%s, %s, %s);
            """
            attrs = [name, preprocessed, preprocess]
            Dataset._query(sql_insert, attrs)
            Dataset._commit()
            return cls.get_one(name, preprocess)

    @classmethod
    def get_by_name(cls, name):
        sql_select = """
            SELECT * FROM datasets
            WHERE name = %s;
        """
        return cls._fetchall(sql_select, [name])

    @classmethod
    def get_preprocessed_by(cls, preprocess):
        sql_select = """
            SELECT * FROM datasets
            WHERE preprocess = %s;
        """
        return cls._fetchall(sql_select, [preprocess])
