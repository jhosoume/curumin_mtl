import pandas as pd
import numpy as np
from paje.storage.db_models.Model import Model
from paje.storage.db_models.Dataset import Dataset
from paje.storage.db_models.Feature import Feature

class Metadata(Model):
    table_name = "metadata"

    def __init__(self, dataset = None, features = None, values = None, id = None, dataset_id = None):
        self.id = id
        self.dataset = dataset
        self.dataset_id =   dataset_id
        self.features = features
        self.values = values

    def __repr__(self):
        return "Metadata(id = {}, dataset = {})".format(
            self.id, self.dataset)

    @classmethod
    def create_table(cls):
        sql_create = """
            CREATE TABLE IF NOT EXISTS metadata (
                id INT PRIMARY KEY AUTO_INCREMENT,
                dataset_id INT NOT NULL{}
                UNIQUE INDEX (dataset_id),
                FOREIGN KEY (dataset_id)
                    REFERENCES datasets(id)
                    ON DELETE CASCADE
            );
        """
        for feature in cls._get_feats():
            if feature == "int":
                feature = "intt"
            sql_create = sql_create.format(""", {} DOUBLE{}""").format(feature, {})
        sql_create = sql_create.format(",\n")
        cls._create_table(sql_create)

    def save(self):
        dt = Dataset.get_or_insert(self.dataset)
        sql_insert = """
            INSERT INTO metadata ({})
                VALUES (
                    {}
                )
        """
        # Getting types in the format suitable for inclusion
        valid_types = ""
        for type in ["dataset_id"] + self.features:
            if type == "int":
                type = "intt"
            valid_types += type.replace(".", "_") + ", "
        valid_types = valid_types[:-2]
        # Including fields to be substituted by the values
        to_subst = ""
        for indx in range(len(self.values) + 1):
            to_subst += "%s, "
        to_subst = to_subst[:-2] # Elimineting comma and empty space
        # print(sql_insert.format(valid_types, to_subst))

        Metadata._query(sql_insert.format(valid_types, to_subst), [dt.id] + self.values)
        Metadata._commit()
        self.id = Metadata._get_id_saved()

    @classmethod
    def _from_query(cls, inst):
        return Metadata(
            id = inst[0],
            dataset_id = inst[1],
            dataset = Dataset.get(inst[1]).name,
            values = inst[2:]
        )

    @classmethod
    def get(cls, metadata):
        sql_select = """
            SELECT * FROM metadata
            WHERE id = %s;
        """
        return cls._fetchone(sql_select, [metadata])


    @classmethod
    def get_by_dataset(cls, dataset_name):
        sql_select = """
            SELECT * FROM metadata
            WHERE dataset_id = (SELECT id FROM datasets WHERE name = %s);
        """
        return cls._fetchall(sql_select, [dataset_name])

    @classmethod
    def _get_feats(cls):
        from sklearn.datasets import load_iris
        from pymfe.mfe import MFE
        data = load_iris()
        mfe = MFE()
        mfe.fit(data.data, data.target)
        ft = mfe.extract()
        _feats = [feature.replace(".", "_") for feature in ft[0]]
        return _feats

    @classmethod
    def get_matrix(cls):
        metadata = pd.DataFrame([[meta.id, meta.dataset_id, *meta.values] for meta in cls.get_all()], columns = cls._columns()).drop("id", axis = 1)
        metadata_means = {feature: np.mean(metadata[feature]) for feature in metadata.columns if feature != "name"}
        metadata.fillna(value = metadata_means, inplace = True)
        return metadata
