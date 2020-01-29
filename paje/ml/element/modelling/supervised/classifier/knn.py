from sklearn.kneighbors import KNeighborsClassifier

from paje.searchspace.hp import CatHP, IntHP, RealHP
from paje.searchspace.configspace import ConfigSpace
from numpy.random import choice, uniform
from paje.ml.element.modelling.supervised.classifier.classifier import Classifier


class KNN(Classifier):
    def __init__(self, config, **kwargs):
        super().__init__(config, **kwargs)
        self.model = KNeighborsClassifier(**self.param())

    @classmethod
    def cs_impl(cls):

        hps = {
            'n_neighbors': IntHP(uniform, low = 2, high = 1000),
            'weights': CatHP(choice, a = ['uniform', 'distance']),
            'algorithm': CatHP(choice, a = ['auto', 'ball_tree', 'kd_tree', 'brute']),
            'leaf_size': IntHP(uniform, low = 2, high = 1000),
            'p': IntHP(uniform, low = 1, high = 6)
        }

        return ConfigSpace(name=cls.__name__, hps=hps)

    @classmethod
    # Creates a configuration of only default options
    def default(cls):
        config = {
            'n_neighbors': 5,
            'weights': 'uniform',
            'algorithm': 'auto',
            'leaf_size': 30,
            'p': 2
        }
        config['class'] = cls.__name__
        config['module'] = cls.__module__
        return config
