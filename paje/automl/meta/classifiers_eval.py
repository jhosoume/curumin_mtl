import pandas as pd
import numpy as np
from scipy.io import arff as arff_io
from sklearn import preprocessing
from paje.storage.db_models.Dataset import Dataset
from paje.storage.db_models.ClfEval import ClfEval
from paje.base.data import Data
from paje.ml.element.modelling.supervised.classifier.dt import DT
from paje.ml.element.modelling.supervised.classifier.nb import NB
from paje.ml.element.preprocessing.supervised.instance.imbalance.smote import SMOTE
from paje.automl.composer.iterator import Iterator
from paje.automl.composer.seq import Seq
from paje.base.cache import Cache
from paje.ml.element.posprocessing.metric import Metric
from paje.ml.element.posprocessing.summ import Summ
from paje.ml.element.preprocessing.supervised.instance.sampler.cv import CV

class ClassifiersEval:
    def __init__(self):
        self.le = preprocessing.LabelEncoder()
        self.random_state = 123

    # Calculates a metric for each dataset
    def calculate(self, dataset_filename):
        # Reading dataset
        data = Data.read_arff(dataset_filename, "class")
        # The pipeline is created (creates all the possible combinations of
        # preprocessors and modellers indicated)
        pipe = self.pipeline_evaluator(
            Seq.cfg(
                    configs = [DT.default()],
                    random_state = self.random_state
            )
        )

        # Apply and use the defined pipeline on the data
        datapp = pipe.apply(data)
        datause = pipe.use(data)
        # The value is stored into data as assigned in the field parameter inside
        # the configuration of the reducer (Summ = np.mean)
        print(pipe, datapp.s, datause.s)
        return datause.s

    # Define basis pipeline -> execute CV, the
    def pipeline_evaluator(self, pipeline):
        # Pipeline should be a configuration of preprocessors + modellers
        # For each CV slice executes the pipeline (preprocess + modeller) then
        # calculates a Metric
        internal_pipe = Seq.cfg(
            configs=[
                pipeline,
                Metric.cfg(function='accuracy')  # from Y to r
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
