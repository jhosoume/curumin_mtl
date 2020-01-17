from imblearn.over_sampling import RandomOverSampler

from paje.searchspace.configspace import ConfigSpace
from paje.ml.element.preprocessing.supervised.instance.sampler.resampler import \
    Resampler
from paje.searchspace.hp import CatHP
from paje.util.distributions import choice


class RanOverSampler(Resampler):
    def __init__(self, config, **kwargs):
        super().__init__(config, **kwargs)
        self.model = RandomOverSampler(**self.param())

    @classmethod
    def cs_impl(cls, data=None):
        hps = {'sampling_strategy': CatHP(
            choice,
            items=['not minority', 'not majority', 'all']
        )}
        return ConfigSpace(name=cls.__name__, hps=hps)
