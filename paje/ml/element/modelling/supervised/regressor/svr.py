import sklearn.svm

from paje.searchspace.hp import CatHP, IntHP, RealHP
from paje.searchspace.configspace import ConfigSpace
from numpy.random import uniform,choice
from paje.ml.element.modelling.supervised.regressor.regressor import Regressor


class SVR(Regressor):
    def __init__(self, config, **kwargs):
        super().__init__(config, **kwargs)
        self.model = sklearn.svm.SVR(**self.param())

    @classmethod
    def cs_impl(cls):
        hps = {'kernel': CatHP(choice,a=['linear','poly','rbf','sigmoid']),
        'degree': IntHP(uniform,low=1,high=5), #ignored if kernel != poly
        'gamma': RealHP(uniform,low=1e-3,high=1.0), #ignored if kernel != rbf or sigmoid
        'C': RealHP(uniform,low=1e-1,high=1e4),
        'epsilon': RealHP(uniform,low=1e-1,high=1e-4),
        'max_iter': IntHP(uniform,low=100,high=1000)}

        return ConfigSpace(name='SVR', hps=hps)
