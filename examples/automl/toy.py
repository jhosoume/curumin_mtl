import sys

from paje.automl.composer.seq import Seq
from paje.automl.composer.any import Any
from paje.automl.optimization.blind.random import RandomAutoML
from paje.base.data import Data
from paje.ml.element.modelling.supervised.classifier.dt import DT
from paje.ml.element.modelling.supervised.classifier.nb import NB
from paje.ml.element.modelling.supervised.classifier.nbp import NBP
from paje.ml.element.preprocessing.supervised.instance.sampler.over.ran_over_sampler import \
    RanOverSampler
from paje.ml.element.preprocessing.supervised.instance.sampler.under.ran_under_sampler import \
    RanUnderSampler
from paje.ml.element.preprocessing.unsupervised.feature.scaler.equalization import \
    Equalization
from paje.ml.element.preprocessing.unsupervised.feature.scaler.standard import \
    Standard
from paje.ml.metric.supervised.classification.mclassif import Metrics


def main():
    if len(sys.argv[1:]) < 1 or any(['=' not in k for k in sys.argv[1:]]):
        print('Usage: \npython toy.py data=/tmp/dataset.arff '
              '[iter=#] [seed=#] [cache=sqlite/amnesia] ['
              'db=dna] ')
    else:
        arg = {tupl.split('=')[0]: tupl.split('=')[1] for tupl in sys.argv[1:]}

        custom = Seq.cs(config_spaces=[Equalization.cs(), Standard.cs()])
        my_preprocessors = [custom,
                            Equalization.cs(),
                            Standard.cs(),
                            RanOverSampler.cs(),
                            RanUnderSampler.cs()]
        my_modelers = [Any.cs(config_spaces=[DT.cs(), NB.cs()])]
        #, NBP.cs()])] # <- requires non negative X

        for k, v in arg.items():
            print(f'{k}={v}')

        if 'cache' in arg:
            if arg['cache'] == 'sqlite':
                storage = {
                    'engine': 'sqlite',
                    'settings': {'db': arg['db']},
                    # 'nested': None,
                    # 'dump': False
                }
            elif arg['cache'] == 'mysql':
                storage = {
                    'engine': 'mysql',
                    'settings': {'db': arg['db']},
                    # 'nested': None,
                    # 'dump': False
                }
            elif arg['cache'] == 'amnesia':
                storage = {'engine': 'amnesia', 'settings': {}}
            else:
                raise Exception('Wrong cache', arg['cache'])
        else:
            storage = {'engine': 'amnesia', 'settings': {}}

        iterations = int(arg['iter']) if 'iter' in arg else 3
        random_state = int(arg['seed']) if 'seed' in arg else 0
        data = Data.read_arff(arg['data'], "class")

        trainset, testset = data.split(random_state=random_state)
        
        automl_rs = RandomAutoML(
            # preprocessors=default_preprocessors,
            # modelers=default_modelers,
            preprocessors=my_preprocessors,
            modelers=my_modelers,
            max_iter=iterations,
            pipe_length=2, repetitions=1,
            random_state=random_state,
            cache_settings_for_components=storage,
            config={}
        )
        automl_rs.apply(trainset)
        testout = automl_rs.use(testset)
        if testout is None:
            print('No working pipeline found!')
            exit(0)
        print("Accuracy score", Metrics.accuracy(testout))
        print()


if __name__ == '__main__':
    main()
