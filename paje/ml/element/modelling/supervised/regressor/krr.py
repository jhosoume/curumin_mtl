from sklearn.kernel_ridge import KernelRidge

from paje.searchspace.hp import CatHP, RealHP, IntHP
from paje.searchspace.configspace import ConfigSpace
from numpy.random import uniform,choice
from paje.ml.element.modelling.supervised.regressor.regressor import Regressor


class KRR(Regressor):
    def __init__(self, config, **kwargs):
        super().__init__(config, **kwargs)
        self.model = KernelRidge(**self.param())

    @classmethod
    def cs_impl(cls):
        hps = {'alpha': RealHP(uniform,low=1e-5,high=10.0),
        'kernel': CatHP(choice,a=['linear','polynomial','rbf','sigmoid']),
        'gamma': RealHP(uniform,low=1e-5,high=10.0), #ignored if kernel = linear
        'degree': IntHP(uniform,low=1,high=5)}  #ignored if kernel != polynomial


        return ConfigSpace(name='KRR', hps=hps)
