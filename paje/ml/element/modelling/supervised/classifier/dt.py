from sklearn.tree import DecisionTreeClassifier

from paje.searchspace.hp import CatHP, IntHP, RealHP
from paje.searchspace.configspace import ConfigSpace
from numpy.random import choice, uniform
from paje.ml.element.modelling.supervised.classifier.classifier import Classifier


class DT(Classifier):
    def __init__(self, config, **kwargs):
        super().__init__(config, **kwargs)
        self.model = DecisionTreeClassifier(**self.param())

    @classmethod
    def cs_impl(cls):
        # Sw
        # cs = ConfigSpace('Switch')
        # st = cs.start()
        # st.add_children([a.start, b.start, c.start])
        # cs.finish([a.end,b.end,c.end])

        hps = {
            'criterion': CatHP(choice, a=['gini', 'entropy']),
            'splitter': CatHP(choice, a=['best', 'random']),
            'class_weight': CatHP(choice, a=[None, 'balanced']),
            'max_features': CatHP(choice, a=['auto', 'sqrt', 'log2', None]),

            'max_depth': IntHP(uniform, low=2, high=1000),

            'min_samples_split': RealHP(uniform, low=1e-6, high=0.3),
            'min_samples_leaf': RealHP(uniform, low=1e-6, high=0.3),
            'min_weight_fraction_leaf': RealHP(uniform, low=0.0, high=0.3),
            'min_impurity_decrease': RealHP(uniform, low=0.0, high=0.2)
        }

        return ConfigSpace(name='DT', hps=hps)

    @classmethod
    # Creates a configuration of only default options
    def default(cls):
        config = {
            'criterion': 'gini',
            'splitter': 'best',
            'class_weight': None,
            'max_features': None,
            'max_depth': None,
            'min_samples_split': 2,
            'min_samples_leaf': 1,
            'min_weight_fraction_leaf': 0.0,
            'min_impurity_decrease': 0.0
        }
        config['class'] = cls.__name__
        config['module'] = cls.__module__
        return config
