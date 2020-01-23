from os import listdir
from os.path import isfile, join
import pandas as pd
import pickle
from sklearn import preprocessing
from paje.storage.db_models.Metadata import Metadata
from paje.storage.db_models.ClfEval import ClfEval
from paje.base.data import Data
from paje.ml.element.modelling.supervised.classifier.dt import DT
from paje.ml.element.modelling.supervised.classifier.nb import NB
from paje.ml.element.preprocessing.supervised.instance.imbalance.smote import Smote
from paje.automl.composer.iterator import Iterator
from paje.automl.composer.seq import Seq
from paje.base.cache import Cache
from paje.ml.element.posprocessing.metric import Metric
from paje.ml.element.posprocessing.summ import Summ
from paje.ml.element.preprocessing.supervised.instance.sampler.cv import CV
from sklearn import tree, ensemble

class RegressorsEval:
    def __init__(self, regressors,
                       preprocessors = [Smote.default()],
                       classifiers = [DT.default()],
                       metric = Metric.cfg(function='accuracy')):
        self.reg_models = regressors
        self.le = preprocessing.LabelEncoder()
        self.random_state = 123
        self.preprocessors = preprocessors
        self.classifiers = classifiers
        self.metric = metric

    # Calculates a metric for each dataset
    def calculate(self, classifier_name, preprocess_name, score = "accuracy"):
        metadata = Metadata.get_matrix()
        clf_evals = ClfEval.get_matrix(classifier_name, preprocess_name)
        data = pd.merge(metadata, clf_evals, on = "dataset_id")
        values = data.drop(["dataset_id", "eval"], axis = 1).values
        target = data["eval"].values
        for regressor in self.reg_models:
            model = self.reg_models[regressor].fit(values, target)
            with open("regressors/{}_{}_{}_{}.pickle".format(
                        regressor, classifier_name, score, preprocess_name), "wb") as fd:
                pickle.dump(model, fd)

    def apply(self):
        for classifier in self.classifiers:
            for preproc in [None] + self.preprocessors:
                preproc_name = preproc['class'] if preproc else 'None'
                self.calculate(classifier["class"], preproc_name)
