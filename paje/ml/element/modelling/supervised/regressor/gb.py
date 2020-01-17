from sklearn.ensemble import GradientBoostingRegressor

from paje.searchspace.hp import CatHP, IntHP, RealHP
from paje.searchspace.configspace import ConfigSpace
from numpy.random import choice, uniform
from paje.ml.element.modelling.supervised.regressor.regressor import Regressor


class GB(Regressor):
    def __init__(self, config, **kwargs):
        super().__init__(config, **kwargs)
        self.model = GradientBoostingRegressor(**self.param())

    @classmethod
    def cs_impl(cls):

        hps = {
            'n_estimators': IntHP(uniform, low=2, high=1000),
            'criterion': CatHP(choice, a=['mse','mae','friedman_mse']),
            'max_features': CatHP(choice, a=['auto', 'sqrt', 'log2', None]),
            'max_depth': IntHP(uniform, low=2, high=100),
            'min_samples_split': RealHP(uniform, low=1e-6, high=0.5),
            'min_samples_leaf': RealHP(uniform, low=1e-6, high=0.5),
            'min_weight_fraction_leaf': RealHP(uniform, low=0.0, high=0.5),
            'min_impurity_decrease': RealHP(uniform, low=0.0, high=0.2),
            'loss': CatHP(choice, a=['ls','lad','huber','quantile']),
            'learning_rate': RealHP(uniform, low=1e-4, high=1e-1),
            'subsample': RealHP(uniform, low=0.1, high=0.9),
            'alpha': RealHP(uniform, low=0.1, high=0.9),  #ignored if loss != huber or quantile
            'validation_fraction': RealHP(uniform, low=0.1, high=0.9), # Using Early Stopping #
            'n_iter_no_change': IntHP(uniform,low=5,high=20)           #                      #
        }

        return ConfigSpace(name='GB', hps=hps)
