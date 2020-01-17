import sys
import mysql

from paje.storage.mysqlconverter import NumpyMySQLConverter
from paje.storage.mysql_config import config

class MtLDB:
    def __init__(self):
        # Opening connection to mysql database according to informaiton in
        # configuration files
        db_config = config['mysql']
        self._con = mysql.connector.connect(
            host = db_config['host'],
            user = db_config['user'],
            password = db_config['password'],
            database = db_config['database'],
            use_pure = True
        )
        self._con.set_converter_class(NumpyMySQLConverter)
        self._cursor = self._con.cursor()

        # Preparing MySQL to be used
        self._open()

    def _open(self):
        self._setup()

    def _setup(self):
        pass

    def _create_datasets_table(self):
        pass

    def _create_feature_table(self):
        pass

    def _create_classifier_table(self):
        pass

    def _create_scores_table(self):
        pass

    def _create_preprocessors_table(self):
        pass

    def _create_metadata_table(self):
        pass
