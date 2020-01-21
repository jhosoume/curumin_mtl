from paje.storage.db_models.Model import Model
from paje.storage.db_models.Classifier import Classifier
from paje.storage.db_models.Dataset import Dataset
from paje.storage.db_models.Score import Score
from paje.storage.db_models.Preprocess import Preprocess

class ClfEval(Model):
    table_name = "clfevals"

    def __init__(self, classifier = None, dataset = None, score = None, preprocess = None, value = 0.0, id = None):
        self.id = id
        self.classifier = classifier
        self.dataset = dataset
        self.score = score
        self.preprocess = preprocess
        self.value = value

    def __repr__(self):
        return "ClfEval(id = {}, classifier = {}, dataset = {}, score = {}, preprocess = {}, value = {})".format(
            self.id, self.classifier, self.dataset, self.score, self.preprocess, self.value)

    @classmethod
    def create_table(cls):
        sql_create = """
            CREATE TABLE IF NOT EXISTS {} (
                id INT PRIMARY KEY AUTO_INCREMENT,
                classifier_id INT NOT NULL,
                dataset_id INT NOT NULL,
                score_id INT NOT NULL,
                preprocess_id INT NOT NULL,
                value DOUBLE NOT NULL,
                UNIQUE INDEX (classifier_id, dataset_id, score_id, preprocess_id),
                FOREIGN KEY (classifier_id)
                    REFERENCES classifiers(id)
                    ON DELETE CASCADE
                FOREIGN KEY (dataset_id)
                    REFERENCES datasets(id)
                    ON DELETE CASCADE,
                FOREIGN KEY (score_id)
                    REFERENCES scores(id)
                    ON DELETE CASCADE,
                FOREIGN KEY (preprocess_id)
                    REFERENCES preprocesses(id)
                    ON DELETE CASCADE,
            );
        """.format(cls.table_name)
        ClfEval._create_table(sql_create)

    def save(self):
        cls = Classifier.get_or_insert(self.classifier)
        dt = Dataset.get_or_insert(self.dataset)
        score = Score.get_or_insert(self.score)
        preprocess = Preprocess.get_or_insert(self.preprocess)
        sql_insert = """
            INSERT INTO clfevals (classifier_id, dataset_id, score_id, preprocess_id, value)
                VALUES (
                    %s, %s, %s, %s, %s
                );
        """
        attrs = [cls.id, dt.id, score.id, preprocess.id, self.value]
        ClfEval._query(sql_insert, attrs)
        ClfEval._commit()
        self.id = ClfEval._get_id_saved()
        print("ClfEval record inserted.")

    @classmethod
    def _from_query(cls, inst):
        return ClfEval(
            id = inst[0],
            classifier = Classifier.get(inst[1]).name,
            dataset = Dataset.get(inst[2]).name,
            score = Score.get(inst[3]).name,
            preprocess = Preprocess.get(inst[4]).name,
            value = inst[5]
        )

    @classmethod
    def get(cls, clfeval):
        sql_select = """
            SELECT * FROM clfevals
            WHERE id = %s;
        """
        return cls._fetchone(sql_select, [clfeval])

    @classmethod
    def get_one(cls, classifier, dataset, score, preprocess):
        cls = Classifier.get_or_insert(classifier)
        dt = Dataset.get_or_insert(dataset)
        score = Score.get_or_insert(score)
        preprocess = Preprocess.get_or_insert(preprocess)
        sql_select = """
            SELECT * FROM clfevals
            WHERE classifier_id = %s AND
                  dataset_id = %s AND
                  score_id = %s AND
                  preprocess_id = %s
            LIMIT 1;
        """
        attrs = [cls.id, dt.id, score.id, preprocess.id]
        return cls._fetchone(sql_select, attrs)

    @classmethod
    def get_by_dataset(cls, dataset_name):
        sql_select = """
            SELECT * FROM clfevals
            WHERE dataset_id = (SELECT id FROM datasets WHERE name = %s);
        """
        return cls._fetchall(sql_select, [dataset_name])

    @classmethod
    def get_by_classifier(cls, classifier_name):
        sql_select = """
            SELECT * FROM clfevals
            WHERE classifier_id = (SELECT id FROM classifiers WHERE name = %s);
        """
        return cls._fetchall(sql_select, [classifier_name])
