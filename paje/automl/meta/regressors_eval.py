from os import listdir
from os.path import isfile, join
from scipy.io import arff as arff_io
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
    def __init__(self, preprocessors = [Smote.default()],
                       classifiers = [DT.default()],
                       metric = Metric.cfg(function='accuracy')):
        self.reg_models = {}
        self.reg_models["decision_tree"] = tree.DecisionTreeRegressor()
        self.reg_models["random_forest"] = ensemble.RandomForestRegressor()
        self.le = preprocessing.LabelEncoder()
        self.random_state = 123
        self.preprocessors = preprocessors
        self.classifiers = classifiers
        self.metric = metric

    # Calculates a metric for each dataset
    def calculate(self, classifier_name, preprocess_name, score = "accuracy"):
        metadata = Metadata.get_matrix()
        clf_evals = ClfEval.get_matrix(classifier_name, preprocess_name)
        data = pd.merge(metadata, clf_evals, on = "name")
        values = data.drop(["dataset_id", "eval"], axis = 1).values
        target = data["eval"].values
        import pdb; pdb.set_trace()

    def apply(self, datasets_fd = "mock_datasets/"):
        # Calculates metafeatures for every datasets in the datasets directory
        self.datasets_dir = datasets_fd
        # Getting list of datasets inside directory
        self.datasets = [f for f in listdir(self.datasets_dir)
            if ( isfile(join(self.datasets_dir, f)) and
               ( f.endswith("json") or f.endswith("arff") ) )]
        for dataset in self.datasets:
            self.calculate(dataset)
