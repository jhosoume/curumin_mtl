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
        Metadata.get_matrix()

    # Calculates a metric for each dataset
    def calculate(self, dataset_filename):
        # Reading dataset
        data = Data.read_arff(self.datasets_dir + dataset_filename, "class")
        # The pipeline is created (creates all the possible combinations of
        # preprocessors and modellers indicated)
        preprocesses = [None] + self.preprocessors
        for preproc in preprocesses:
            for classifier in self.classifiers:
                pipeline = [preproc, classifier] if preproc else [classifier]
                pipe = self.pipeline_evaluator(
                    Seq.cfg(
                            configs = pipeline,
                            random_state = self.random_state
                    )
                )
                # Apply and use the defined pipeline on the data
                datapp = pipe.apply(data)
                datause = pipe.use(data)
                # The value is stored into data as assigned in the field parameter inside
                # the configuration of the reducer (Summ = np.mean)
                preproc_name = preproc['class'] if preproc else 'None'
                eval = ClfEval(
                    classifier = classifier['class'],
                    dataset = dataset_filename,
                    score = self.metric['function'],
                    preprocess = preproc_name,
                    value = datause.s
                ).save()
                print(pipe, datapp.s, datause.s)

    # Define basis pipeline -> execute CV, the
    def pipeline_evaluator(self, pipeline):
        # Pipeline should be a configuration of preprocessors + modellers
        # For each CV slice executes the pipeline (preprocess + modeller) then
        # calculates a Metric
        internal_pipe = Seq.cfg(
            configs=[
                pipeline,
                self.metric  # from Y to r
            ],
            random_state = self.random_state
        )

        # Defines the CV to be applied in the dataset and the function to reduce
        # the metric calc
        iterator_pipe = Seq.cfg(
            configs=[
                Iterator.cfg(
                    iterable=CV.cfg(split='cv', steps=10, fields=['X', 'Y']),
                    configs=[internal_pipe],
                    field='r'
                ),
                Summ.cfg(field='s', function='mean')
            ]
        )
        # Wrapper? Note that it does not call the cfg, but is an instance of the class
        pipe = Seq(
            config={
                'configs': [iterator_pipe],
                'random_state': self.random_state
            }
        )
        return pipe

    def apply(self, datasets_fd = "mock_datasets/"):
        # Calculates metafeatures for every datasets in the datasets directory
        self.datasets_dir = datasets_fd
        # Getting list of datasets inside directory
        self.datasets = [f for f in listdir(self.datasets_dir)
            if ( isfile(join(self.datasets_dir, f)) and
               ( f.endswith("json") or f.endswith("arff") ) )]
        for dataset in self.datasets:
            self.calculate(dataset)
