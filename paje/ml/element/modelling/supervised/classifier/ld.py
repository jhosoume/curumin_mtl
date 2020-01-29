from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

from paje.searchspace.hp import CatHP, IntHP, RealHP
from paje.searchspace.configspace import ConfigSpace
from numpy.random import choice, uniform
from paje.ml.element.modelling.supervised.classifier.classifier import Classifier


class LD(Classifier):
    def __init__(self, config, **kwargs):
        super().__init__(config, **kwargs)
        self.model = LogisticRegression(**self.param())

    @classmethod
    def cs_impl(cls):
        hps = {
            'solver': CatHP(choice, a = ['svd', 'lsqr', 'eigen']),
            'shrinkage': CatHP(choice, a = [None, 'auto']),
            'tol': RealHP(uniform, low = 1e-6, high = 0.5)
        }

        return ConfigSpace(name=cls.__name__, hps=hps)

    @classmethod
    # Creates a configuration of only default options
    def default(cls):
        config = {
            'solver': 'svd',
            'shrinkage': None,
            'tol': 1e-4
        }
        config['class'] = cls.__name__
        config['module'] = cls.__module__
        return config
