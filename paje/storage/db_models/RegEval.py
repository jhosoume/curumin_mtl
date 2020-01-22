from paje.storage.db_models.Model import Model
from paje.storage.db_models.Regressor import Regressor
from paje.storage.db_models.Classifier import Classifier
from paje.storage.db_models.Score import Score
from paje.storage.db_models.Preprocess import Preprocess

class RegEval(Model):
    table_name = "regevals"

    def __init__(self, regressor = None, classifier = None, score = None, preprocess = None, value = 0.0, id = None):
        self.id = id
        self.regressor = regressor
        self.classifier = classifier
        self.score = score
        self.preprocess = preprocess
        self.value = value

    def __repr__(self):
        return "RegEval(id = {}, regressor = {}, classifier = {}, score = {}, preprocess = {}, value = {})".format(
            self.id, self.regressor, self.classifier, self.score, self.preprocess, self.value)

    @classmethod
    def create_table(cls):
        sql_create = """
            CREATE TABLE IF NOT EXISTS {} (
                id INT PRIMARY KEY AUTO_INCREMENT,
                regressor_id INT NOT NULL,
                classifier_id INT NOT NULL,
                score_id INT NOT NULL,
                preprocess_id INT NOT NULL,
                value DOUBLE NOT NULL,
                UNIQUE INDEX (regressor_id, classifier_id, score_id, preprocess_id),
                FOREIGN KEY (regressor_id)
                    REFERENCES regressors(id)
                    ON DELETE CASCADE,
                FOREIGN KEY (classifier_id)
                    REFERENCES classifiers(id)
                    ON DELETE CASCADE,
                FOREIGN KEY (score_id)
                    REFERENCES scores(id)
                    ON DELETE CASCADE,
                FOREIGN KEY (preprocess_id)
                    REFERENCES preprocesses(id)
                    ON DELETE CASCADE
            );
        """.format(cls.table_name)
        RegEval._create_table(sql_create)

    def save(self):
        reg = Regressor.get_or_insert(self.regressor)
        cls = Classifier.get_or_insert(self.classifier)
        score = Score.get_or_insert(self.score)
        preprocess = Preprocess.get_or_insert(self.preprocess)
        sql_insert = """
            INSERT INTO regevals (regressor_id, classifier_id, score_id, preprocess_id, value)
                VALUES (
                    %s, %s, %s, %s, %s
                );
        """
        attrs = [reg.id, cls.id, score.id, preprocess.id, self.value]
        RegEval._query(sql_insert, attrs)
        RegEval._commit()
        self.id = RegEval._get_id_saved()

    @classmethod
    def _from_query(cls, inst):
        return RegEval(
            id = inst[0],
            regressor = Regressor.get(inst[1]).name,
            classifier = Classifier.get(inst[2]).name,
            score = Score.get(inst[3]).name,
            preprocess = Preprocess.get(inst[4]).name,
            value = inst[5]
        )

    @classmethod
    def get(cls, regeval):
        sql_select = """
            SELECT * FROM regevals
            WHERE id = %s;
        """
        return cls._fetchone(sql_select, [regeval])

    @classmethod
    def get_one(cls, regressor, classifier, score, preprocess):
        reg = Regressor.get_or_insert(regressor)
        cls = Classifier.get_or_insert(classifier)
        score = Score.get_or_insert(score)
        preprocess = Preprocess.get_or_insert(preprocess)
        sql_select = """
            SELECT * FROM regevals
            WHERE regressor_id = %s AND
                  classifier_id = %s AND
                  score_id = %s AND
                  preprocess_id = %s
            LIMIT 1;
        """
        attrs = [reg.id, cls.id, score.id, preprocess.id]
        return cls._fetchone(sql_select, attrs)

    @classmethod
    def get_by_dataset(cls, dataset_name):
        sql_select = """
            SELECT * FROM regevals
            WHERE dataset_id = (SELECT id FROM datasets WHERE name = %s);
        """
        return cls._fetchall(sql_select, [dataset_name])

    @classmethod
    def get_by_classifier(cls, classifier_name):
        sql_select = """
            SELECT * FROM regevals
            WHERE classifier_id = (SELECT id FROM classifiers WHERE name = %s);
        """
        return cls._fetchall(sql_select, [classifier_name])
