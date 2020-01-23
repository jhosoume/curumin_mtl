import numpy as np
from pymfe.mfe import MFE
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

        self.mfe = MetaFeatures()
        # self.mfe.apply(self.train_datasets)

        self.clfeval = ClassifiersEval(self.preprocessors, self.classifiers)
        self.clfeval.apply()

        self.regressors = {}
        self.reg_models["decision_tree"] = tree.DecisionTreeRegressor()
        self.reg_models["random_forest"] = ensemble.RandomForestRegressor()

        self.regeval = RegressorsEval(regressors = self.regressors)
        self.regeval.apply()

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
        return Seq(self.best_pipe)

    def get_current_eval(self):
        """ TODO the docstring documentation
        """
        return self.curr_eval

    def get_best_eval(self):
        """ TODO the docstring documentation
        """
        return self.best_eval

    def eval(self, pip_config, data):
        return pip, (datapp.s, datause.s)

    def apply_impl(self, data):
        """ TODO the docstring documentation
        """
        self.all_eval_results = []

        for iteration in range(1, self.max_iter + 1):
            self.current_iteration = iteration
            if self.verbose:
                print("####------##-----##-----##-----##-----##-----####")
                print("Current iteration = ", self.current_iteration)


            # This attribute save all results
            self.all_eval_results.append(eval_result)

            self.process_step(eval_result)
            if self.verbose:
                print("Current ...............: ", self.get_current_eval())
                print("Best ..................: ", self.get_best_eval())
                print("Locks/fails/successes .: {0}/{1}/{2}".format(
                    self.locks, self.fails, self.successes))
                print("-------------------------------------------------\n")
