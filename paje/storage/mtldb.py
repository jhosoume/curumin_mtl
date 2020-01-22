from paje.storage.db_models.mtldbbase import MtLDBBase

from paje.storage.db_models.Classifier import Classifier
from paje.storage.db_models.ClfEval import ClfEval
from paje.storage.db_models.Dataset import Dataset
from paje.storage.db_models.Feature import Feature
from paje.storage.db_models.Metadata import Metadata
from paje.storage.db_models.Preprocess import Preprocess
from paje.storage.db_models.RegEval import RegEval
from paje.storage.db_models.Regressor import Regressor
from paje.storage.db_models.Score import Score

class MtLDB:
    def __init__(self, debug = False):
        db = MtLDBBase()
        self.debug = False
        self.models = [Classifier(), Dataset(), Feature(), Preprocess(), Regressor(), Score(), Metadata(), RegEval(), ClfEval()]
        self._open()

    def _open(self):
        try:
            self.query(f"SELECT * FROM clfevals;")
        except:
            if self.debug:
                print('Creating MtL Database...')
            self._setup()

    def _setup(self):
        for model in self.models:
            model.create_table()

    def _reset(self):
        for model in reversed(self.models):
            model.delete_table()
