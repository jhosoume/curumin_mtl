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

    def calculate(self, dataset_filename):
        # Reading dataset
        data = Data.read_arff(dataset_filename, "class")
        internal = Seq.cfg(
            configs=[
                Cache.cfg(
                    configs=[Seq.cs(config_spaces = [DT.cs()])],
                ),
                Metric.cfg(function='accuracy')  # from Y to r
            ],
            random_state=self.random_state
        )

        iterat = Seq.cfg(
            configs=[
                Iterator.cfg(
                    iterable=CV.cfg(split='cv', steps=10, fields=['X', 'Y']),
                    configs=[internal],
                    field='r'
                ),
                Summ.cfg(field='s', function='mean')
            ]
        )
        pip = Seq(
            config={
                'configs': [iterat],
                'random_state': self.random_state
            }
        )
        datapp = pip.apply(data)
        datause = pip.use(data)
        print(pip, datapp.s, datause.s)
