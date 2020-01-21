from paje.storage.db_models.Model import Model
from paje.storage.db_models.Dataset import Dataset
from paje.storage.db_models.Feature import Feature

class Metadata(Model):
    table_name = "metadata"

    def __init__(self, dataset = None, feature = None, value = 0.0, id = None):
        self.id = id
        self.dataset = dataset
        self.feature = feature
        self.value = value

    def __repr__(self):
        return "Metadata(id = {}, dataset = {}, feature = {}, value = {})".format(
            self.id, self.dataset, self.feature, self.value)

    @classmethod
    def create_table(cls):
        sql_create = """
            CREATE TABLE IF NOT EXISTS {} (
                id INT PRIMARY KEY AUTO_INCREMENT,
                dataset_id INT NOT NULL,
                feature_id INT NOT NULL,
                value DOUBLE NOT NULL,
                UNIQUE INDEX (dataset_id, feature_id),
                FOREIGN KEY (dataset_id)
                    REFERENCES datasets(id)
                    ON DELETE CASCADE,
                FOREIGN KEY (feature_id)
                    REFERENCES features(id)
                    ON DELETE CASCADE
            );
        """.format(cls.table_name)
        Metadata._create_table(sql_create)

    def save(self):
        dt = Dataset.get_or_insert(self.dataset)
        ft = Feature.get_or_insert(self.feature)
        sql_insert = """
            INSERT INTO metadata (dataset_id, feature_id, value)
                VALUES (
                    %s, %s, %s
                );
        """
        attrs = [dt.id, ft.id, self.value]
        Metadata._query(sql_insert, attrs)
        Metadata._commit()
        self.id = Metadata._get_id_saved()
        print("Metadata record inserted.")

    @classmethod
    def _from_query(cls, inst):
        return Metadata(
            id = inst[0],
            dataset = Dataset.get(inst[1]).name,
            feature = Feature.get(inst[2]).name,
            value = inst[3]
        )

    @classmethod
    def get(cls, metadata):
        sql_select = """
            SELECT * FROM metadata
            WHERE id = %s;
        """
        return cls._fetchone(sql_select, [metadata])

    @classmethod
    def get_one(cls, dataset_name, feature_name):
        dt = Dataset.get_or_insert(dataset_name)
        ft = Feature.get_or_insert(feature_name)
        sql_select = """
            SELECT * FROM metadata
            WHERE dataset_id = %s AND
                  feature_id = %s
            LIMIT 1;
        """
        attrs = [dt.id, ft.id]
        return cls._fetchone(sql_select, attrs)

    @classmethod
    def get_by_dataset(cls, dataset_name):
        sql_select = """
            SELECT * FROM metadata
            WHERE dataset_id = (SELECT id FROM datasets WHERE name = %s);
        """
        return cls._fetchall(sql_select, [dataset_name])

    @classmethod
    def get_by_feature(cls, feature_name):
        sql_select = """
            SELECT * FROM metadata
            WHERE feature_id = (SELECT id FROM features WHERE name = %s);
        """
        return cls._fetchall(sql_select, [feature_name])
