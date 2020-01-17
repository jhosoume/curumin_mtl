from sklearn.linear_model import ElasticNet

from paje.searchspace.hp import RealHP
from paje.searchspace.configspace import ConfigSpace
from numpy.random import uniform
from paje.ml.element.modelling.supervised.regressor.regressor import Regressor


class ENET(Regressor):
    def __init__(self, config, **kwargs):
        super().__init__(config, **kwargs)
        self.model = ElasticNet(**self.param())

    @classmethod
    def cs_impl(cls):
        hps = {'alpha': RealHP(uniform,low=1e-5,high=10.0),
        'l1_ratio': RealHP(uniform,low=1e-5,high=10.0)}

        return ConfigSpace(name='ENET', hps=hps)
