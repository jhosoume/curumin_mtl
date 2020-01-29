import numpy as np
import pandas as pd
from operator import attrgetter
from paje.automl.automl import AutoML
from paje.automl.composer.iterator import Iterator
from paje.automl.composer.seq import Seq
from paje.base.cache import Cache
from paje.ml.element.posprocessing.metric import Metric
from paje.ml.element.posprocessing.summ import Summ
from paje.ml.element.preprocessing.supervised.instance.sampler.cv import CV
from paje.automl.meta.metafeatures import MetaFeatures
from paje.automl.meta.classifiers_eval import ClassifiersEval
from paje.automl.meta.regressors_eval import RegressorsEval
from paje.storage.db_models.Metadata import Metadata

class MtLAutoML(AutoML):

    def __init__(self,
                 preprocessors,
                 modelers,
                 pipe_length,
                 repetitions,
                 random_state,
                 train_datasets = None,
                 cache_settings_for_components = None,
                 **kwargs):
        """
        AutoML
        :param preprocessors: list of modules for balancing,
            noise removal, sampling etc.
        :param modelers: list of modules for prediction
            (classification or regression etc.)
        :param repetitions: how many times can a module appear
            in a pipeline
        :param max_iter: maximum number of pipelines to evaluate
        :param max_depth: maximum length of a pipeline
        :param static: are the pipelines generated always exactly
            as given by the ordered list preprocessors + modelers?
        :param fixed: are the pipelines generated always with
            length max(max_depth, len(preprocessors + modelers))?
        :param random_state: TODO
        :return:
        """

        AutoML.__init__(self,
                        components=preprocessors + modelers,
                        **kwargs)


        # These attributes identify uniquely AutoML.
        # This structure is necessary because the AutoML is a Component and it
        # could be used into other Components, like the Pipeline one.
        # build_impl()
        self.repetitions = repetitions
        self.pipe_length = pipe_length
        # __init__()


        if not isinstance(modelers, list) or \
                not isinstance(preprocessors, list):
            print(modelers)
            print(preprocessors)
            raise TypeError("The modelers/preprocessors must be list.")

        if not modelers:
            raise ValueError("The list length must be greater than one.")

        self.classifiers = modelers
        self.preprocessors = preprocessors
        self.train_datasets = train_datasets

        self.metafe = MetaFeatures()
        self.metafe.apply(self.train_datasets)

        self.clfeval = ClassifiersEval(self.preprocessors, self.classifiers)
        self.clfeval.apply()


        self.regeval = RegressorsEval()
        self.trained_regs = self.regeval.apply()

        # Getting means of all the calculated features to fill Nan values
        # of MFE
        self.metadata = Metadata.get_matrix()
        self.metadata_means = {feature: np.mean(self.metadata[feature]) for feature in self.metadata.columns if feature != "name"}

        # Other class attributes.
        # These attributes can be set here or in the build_impl method. They
        # should not influence the AutoML final result.
        self.storage_settings_for_components = cache_settings_for_components

        # Class internal attributes
        # Attributes that were not parameterizable
        self.best_eval = float('-Inf')
        self.best_pipe = None
        self.curr_eval = None
        self.curr_pipe = None

        self.random_state = random_state
        np.random.seed(self.random_state)

        # Creation of all possible pipelines to be evaluated (may be useless)
        pipelines = []
        for preprocesses in [None] + self.preprocessors:
            for clf in self.classifiers:
                pipelines = [preprocesses] + [clf]

    def next_pipelines(self, data):
        """ TODO the docstring documentation
        """
        pass


    def process_step(self, eval_result):
        """ TODO the docstring documentation
        """
        self.curr_eval = eval_result[0][1] or 0
        if self.curr_eval is not None \
                and self.curr_eval > self.best_eval:
            self.best_eval = self.curr_eval
            self.best_pipe = self.curr_pipe

    def get_best_pipeline(self):
        """ TODO the docstring documentation
        """
        return self.best_pipe

    def get_current_eval(self):
        """ TODO the docstring documentation
        """
        return self.curr_eval

    def get_best_eval(self):
        """ TODO the docstring documentation
        """
        return self.best_eval

    def eval(self, data):
        return pip, (datapp.s, datause.s)

    # Data should be a train set
    def apply_impl(self, data):
        """ TODO the docstring documentation
        """
        # Initialize array that will save the preprocessors to be applied in data
        preprocessors_pipeline = []
        # Make iterations to find the best preprocessors pipeline
        for iteration in range(1, self.max_iter + 1):
            # Get input data
            values, target = data.Xy
            # Calculates metafeatures of the input data
            features = self.metafe.metafeatures(values, target)
            # Reshapes features to reflect that it is only one example
            mfe_values = np.array(features[1]).reshape(1, len(features[1]))
            features = pd.DataFrame(mfe_values, columns = features[0])
            # Some metafeatures may not be calculated, so the Nan values will
            # be substituted for the mean
            features.fillna(value = self.metadata_means, inplace = True)
            results = []
            for regressor in self.trained_regs:
                # Use regressor to predict performance for a combination of preprocessor and classifier
                result = regressor['model'].predict(features)
                regressor['result'] = result
                results.append(regressor)
            # Get best result among the ones calculated
            best_result = max(results, key = lambda prediction: prediction['result'])
            # Get classifier instance to be returned
            classifier = next(clf for clf in self.classifiers if clf["class"] == best_result["clf"])
            # If the best pipeline does not include a preprocessor, there is
            # no need to make new itartions since the data will not be modified
            if best_result["preprocess"] != "None":
                # If the best pipeline has a preprocessor, applies to data and verifies new
                # scores (metafeatures are recalculated and scores are predicted)
                pproc = next(preprocess for preprocess in self.preprocessors if preprocess["class"] == best_result["preprocess"])
                preprocessors_pipeline.append(pproc)
                pproc_pipeline = Seq(
                    config = {"configs": [Seq.cfg(configs = [pproc], random_state = self.random_state)],
                              "random_state": self.random_state
                    }
                )
                pproc_pipeline.apply(data)
                pproc_pipeline.use(data)

            else:
                # Check if the data was modified before. Every preprocessement applied
                # to the data is incorporeted in the pipeline
                if preprocessors_pipeline:
                    # Structure pipelines
                    self.best_pipe = Seq(
                        config = {"configs": [Seq.cfg(configs = [preprocessors_pipeline.append(classifier)], random_state = self.random_state)],
                                  "random_state": self.random_state
                        }
                    )
                else:
                    self.best_pipe = Seq(
                        config = {"configs": [Seq.cfg(configs = [classifier], random_state = self.random_state)],
                                  "random_state": self.random_state
                        }
                    )
                # Does not need to make more iterations
                break
            # Defines best pipeline
            self.best_pipe = Seq(
                config = {"configs": [Seq.cfg(configs = [preprocessors_pipeline.append(classifier)], random_state = self.random_state)],
                          "random_state": self.random_state
                }
            )
        # If max iteration is reached, returns the best pipeline so far
        self.model = self.get_best_pipeline()
        if self.verbose:
            print("Best pipeline found:")
            print(self.model)

        return self.model.apply(data)
