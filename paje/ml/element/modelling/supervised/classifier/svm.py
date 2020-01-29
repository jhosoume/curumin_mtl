from sklearn.svm import SVC

from paje.searchspace.hp import CatHP, IntHP, RealHP
from paje.searchspace.configspace import ConfigSpace
from numpy.random import choice, uniform
from paje.ml.element.modelling.supervised.classifier.classifier import Classifier


class SVM(Classifier):
    def __init__(self, config, **kwargs):
        super().__init__(config, **kwargs)
        self.model = SVC(**self.param())

    @classmethod
    def cs_impl(cls):
        hps = {
            'C': RealHP(uniform, low = 0.0, high = 10000.0),
            'kernel': CatHP(choice, a = ['linear', 'poly', 'rbf', 'sigmoid']),
            'degree': IntHP(uniform, low = 0, high = 1000),
            'gamma': CatHP(choice, a = ['scale', 'auto']),
            'coef0': RealHP(uniform, low = 0.0, high = 1000.0),
            'shrinking': CatHP(choice, a = [True, False]),
            'probability': CatHP(choice, a = [True, False]),
            'tol': RealHP(uniform, low = 1e-6, high = 0.5),
            'max_iter': IntHP(uniform, low = -1, max = 10000),
            'decision_function_shape': CatHP(choice, a = ['ovo', 'ovr'])
        }

        return ConfigSpace(name=cls.__name__, hps=hps)

    @classmethod
    # Creates a configuration of only default options
    def default(cls):
        config = {
            'C': 1.0,
            'kernel': 'rbf',
            'degree': 3,
            'gamma': 'scale',
            'coef0': 0.0,
            'shrinking': True,
            'probability': False,
            'tol': 1e-3,
            'max_iter': -1,
            'decision_function_shape': 'ovr'
        }
        config['class'] = cls.__name__
        config['module'] = cls.__module__
        return config
