from sklearn.tree import DecisionTreeRegressor

from paje.searchspace.hp import CatHP, IntHP, RealHP
from paje.searchspace.configspace import ConfigSpace
from numpy.random import choice, uniform
from paje.ml.element.modelling.supervised.regressor.regressor import Regressor


class RT(Regressor):
    def __init__(self, config, **kwargs):
        super().__init__(config, **kwargs)
        self.model = DecisionTreeRegressor(**self.param())

    @classmethod
    def cs_impl(cls):

        hps = {
            'criterion': CatHP(choice, a=['mse','mae','friedman_mse']),
            'splitter': CatHP(choice, a=['best','random']),
            'max_features': CatHP(choice, a=['auto', 'sqrt', 'log2', None]),
            'max_depth': IntHP(uniform, low=2, high=1000),
            'min_samples_split': RealHP(uniform, low=1e-6, high=0.5),
            'min_samples_leaf': RealHP(uniform, low=1e-6, high=0.5),
            'min_weight_fraction_leaf': RealHP(uniform, low=0.0, high=0.5),
            'min_impurity_decrease': RealHP(uniform, low=0.0, high=0.2)
        }

        return ConfigSpace(name='RT', hps=hps)
