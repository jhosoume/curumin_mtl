from sklearn.neighbors import KNeighborsRegressor

from paje.searchspace.hp import CatHP, IntHP
from paje.searchspace.configspace import ConfigSpace
from numpy.random import uniform,choice
from paje.ml.element.modelling.supervised.regressor.regressor import Regressor


class KNN(Regressor):
    def __init__(self, config, **kwargs):
        super().__init__(config, **kwargs)
        self.model = KNeighborsRegressor(**self.param())

    @classmethod
    def cs_impl(cls):
        hps = {'n_neighbors': IntHP(uniform,low=1,high=15),
        'weights': CatHP(choice,a=['uniform','distance']),
        'algorithm': CatHP(choice,a=['kd_tree','ball_tree']),
        'leaf_size': IntHP(uniform,low=15,high=100),
        'p': IntHP(uniform,low=1,high=5)} #default metric: 'minkowski'

        return ConfigSpace(name='KNN', hps=hps)
