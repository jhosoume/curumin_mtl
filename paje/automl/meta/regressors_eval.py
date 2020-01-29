from os import listdir
from os.path import isfile, join
import pandas as pd
import pickle
from sklearn import tree, ensemble
from sklearn import preprocessing, base
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

class RegressorsEval:
    def __init__(self, preprocessors = [Smote.default()],
                       classifiers = [DT.default()],
                       metric = Metric.cfg(function='accuracy')):
        self.le = preprocessing.LabelEncoder()
        self.random_state = 123
        self.preprocessors = preprocessors
        self.classifiers = classifiers
        self.metric = metric
        # Using lambda to create new instances of estimators! If the same estimator is refited
        # the previous model is lost.
        self.reg_models = {}
        self.reg_models["decision_tree"] = lambda: tree.DecisionTreeRegressor()
        self.reg_models["random_forest"] = lambda: ensemble.RandomForestRegressor()

    # Calculates a metric for each dataset
    def calculate(self, classifier_name, preprocess_name, score = "accuracy"):
        # Initialize array to store results
        regressor_data = []
        # Get mfe and classifiers scores to train regressors
        metadata = Metadata.get_matrix()
        clf_evals = ClfEval.get_matrix(classifier_name, preprocess_name)
        # Merge both matrix to ensure that results are associeted
        # (mfe and score for the same dataset)
        data = pd.merge(metadata, clf_evals, on = "dataset_id")
        values = data.drop(["dataset_id", "eval"], axis = 1).values
        target = data["eval"].values
        for regressor in self.reg_models:
            # Initialize new estimator
            model = self.reg_models[regressor]()
            # Fit and save the regressor
            model = model.fit(values, target)
            with open("regressors/{}_{}_{}_{}.pickle".format(
                        regressor, classifier_name, score, preprocess_name), "wb") as fd:
                pickle.dump(model, fd)
            # Informatio of regresssor is storeed as a dict,
            # must be subtituted for a regeval instance
            regressor_info = {
                'reg': regressor,
                'clf': classifier_name,
                'score': score,
                'preprocess': preprocess_name,
                'model': model
            }
            regressor_data.append(regressor_info)
        return regressor_data

    def apply(self):
        # Applyies the regressor training (calculate) for all regressors,
        # classifiers and preprocessors
        all_regressors = []
        for classifier in self.classifiers:
            for preproc in [None] + self.preprocessors:
                preproc_name = preproc['class'] if preproc else 'None'
                all_regressors += self.calculate(classifier["class"], preproc_name)
        return all_regressors
