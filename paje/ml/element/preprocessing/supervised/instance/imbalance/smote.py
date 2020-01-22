from imblearn.over_sampling import SMOTE
from paje.searchspace.hp import CatHP
from paje.searchspace.configspace import ConfigSpace
from paje.ml.element.preprocessing.supervised.instance.imbalance.imbalance import Imbalance
from paje.util.distributions import choice


class SMOTE(Imbalance):
    def __init__(self, config, **kwargs):
        super().__init__(config, **kwargs)
        self.model = SMOTE(**self.param())

    @classmethod
    def cs_impl(cls):
        hps = {
            'sampling_strategy': CatHP(
                choice,
                items=['not minority', 'not majority', 'all', 'minority']
            ),
            'k_neighbours': IntHP(uniform, low=2, high=1000)
        }
        return ConfigSpace(name=cls.__name__, hps=hps)
