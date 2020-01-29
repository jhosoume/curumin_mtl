from sklearn.linear_model import LogisticRegression

from paje.searchspace.hp import CatHP, IntHP, RealHP
from paje.searchspace.configspace import ConfigSpace
from numpy.random import choice, uniform
from paje.ml.element.modelling.supervised.classifier.classifier import Classifier


class LR(Classifier):
    def __init__(self, config, **kwargs):
        super().__init__(config, **kwargs)
        self.model = LogisticRegression(**self.param())

    @classmethod
    def cs_impl(cls):
        hps = {
            'penalty': CatHP(choice, a = ['l1', 'l2', 'elasticnet', 'none']),
            'dual': CatHP(uniform, a = [True, False]),
            'tol': RealHP(uniform, low = 1e-6, high = 0.5),
            'C': RealHP(uniform, low = 0.0, high = 10000.0),
            'fit_intercept': CatHP(uniform, a = [True, False]),
            'solver': CatHP(choice, a = ['newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga']),
            'max_iter': IntHP(uniform, low = 1, max = 10000)
        }

        return ConfigSpace(name=cls.__name__, hps=hps)

    @classmethod
    # Creates a configuration of only default options
    def default(cls):
        config = {
            'penalty': 'l2',
            'dual': False,
            'tol': 1e-4,
            'C': 1.0,
            'fit_intercept': True,
            'solver': 'lbfgs',
            'max_iter': 100
        }
        config['class'] = cls.__name__
        config['module'] = cls.__module__
        return config
