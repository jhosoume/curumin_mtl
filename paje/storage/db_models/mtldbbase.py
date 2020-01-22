import sys
import mysql

from paje.storage.mysqlconverter import NumpyMySQLConverter
from paje.storage.mysql_config import config

class MtLDBBase:
    def __init__(self):
        # Opening connection to mysql database according to informaiton in
        # configuration files
        db_config = config['mysql']
        try:
            # If database is already created
            self._con = mysql.connector.connect(
                host = db_config['host'],
                user = db_config['user'],
                password = db_config['password'],
                database = db_config['database'],
                use_pure = True
            )
        except mysql.connector.Error as err:
            # Create database
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                print("Creating database {}...".format(db_config['database']))
                self._con = mysql.connector.connect(
                    host = db_config['host'],
                    user = db_config['user'],
                    password = db_config['password'],
                )
                self._cursor = self._con.cursor()
                self._cursor.execute("""CREATE DATABASE {};""".format(db_config['database']))
                self._cursor.execute("""USE {};""".format(db_config['database']))
                self._con.commit()
            # Case any other error occur
            else:
                raise err
        self._con.set_converter_class(NumpyMySQLConverter)
        self._cursor = self._con.cursor()

    def query(self, sql_string, args = None):
        if args is None:
            args = []
        msg = self._interpolate(sql_string, args)
        try:
            self._cursor.execute(sql_string, args)
        except Exception as ex:
            # From a StackOverflow answer...
            import sys
            import traceback
            # Gather the information from the original exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            # Format the original exception for a nice printout:
            traceback_string = ''.join(traceback.format_exception(
                exc_type, exc_value, exc_traceback))
            # Re-raise a new exception of the same class as the original one
            raise type(ex)(
                "%s\norig. trac.:\n%s\n" % (msg, traceback_string))

    @staticmethod
    def _interpolate(sql, args):
        lst = [str(arg)[:100] for arg in args]
        zipped = zip(sql.replace('%s', '"%s"').split('%s'), map(str, lst + ['']))
        return ''.join(list(sum(zipped, ()))).replace('"None"', 'NULL')
