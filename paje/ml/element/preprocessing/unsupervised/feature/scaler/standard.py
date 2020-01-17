from sklearn.preprocessing import StandardScaler

from paje.searchspace.configspace import ConfigSpace
from paje.ml.element.preprocessing.unsupervised.feature.scaler.scaler import \
    Scaler
from paje.searchspace.hp import CatHP
from paje.util.distributions import choice


class Standard(Scaler):
    def __init__(self, config, **kwargs):
        super().__init__(config, **kwargs)

        newconfig = self.param().copy()
        mean_std = newconfig.get('@with_mean/std')
        if mean_std is None:
            with_mean, with_std = True, True
        else:
            del newconfig['@with_mean/std']
            with_mean, with_std = mean_std
        self.model = StandardScaler(with_mean, with_std, **newconfig)

    @classmethod
    def cs_impl(cls, data=None):
        hps = {'@with_mean/std': CatHP(
            choice,
            items=[(True, False), (False, True), (True, True)]
        )}
        return ConfigSpace(name=cls.__name__, hps=hps)
