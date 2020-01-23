from os import listdir
from os.path import isfile, join
import pandas as pd
import numpy as np
from sklearn import preprocessing
from scipy.io import arff as arff_io
from pymfe.mfe import MFE
from paje.storage.db_models.Dataset import Dataset
from paje.storage.db_models.Feature import Feature
from paje.storage.db_models.Metadata import Metadata

class MetaFeatures:
    def __init__(self):
        self.mfe = MFE()
        self.le = preprocessing.LabelEncoder()

    def calculate(self, dataset_filename):
        # Reading dataset
        dataset = Dataset.get_or_insert(dataset_filename)
        if dataset.name.endswith("json"):
            data = pd.read_json(self.datasets_dir + dataset.name)
        elif dataset.name.endswith("arff"):
            data = arff_io.loadarff(self.datasets_dir + dataset.name)
            data = pd.DataFrame(data[0])
        # Getting target column
        target = data["class"].values
        # Dealing with object columns (non numeric)
        if target.dtype == np.object:
            self.le.fit(target)
            target = self.le.transform(target)
        # Separating from data from labels
        values = data.drop("class", axis = 1).values
        # Calculating metafeatures
        self.mfe.fit(values, target)
        try:
            ft = self.mfe.extract()
        except AttributeError:
            self.mfe.fit(values.astype(float), target)
            ft = self.mfe.extract()
        # Getting metafeatures names (labels) and the calculated values (results)
        labels = np.array(ft[0])
        results = np.array(ft[1])
        # Ignoring nan values (Removing columns - features - with nan values in datasets)
        nan_columns = np.isnan(results)
        not_nan = np.invert(nan_columns)
        labels = labels[not_nan].tolist()
        results = results[not_nan].tolist()
        for indx, (label, result) in enumerate(zip(labels, results)):
            # Sometimes the result is a complex number, use just the real part
            if isinstance(result, complex):
                results[indx] = result.real
                result = result.real
            # Saving meta knowledge in the database
            metadata = Metadata(dataset = dataset.name,
                                feature = str(label),
                                value = result).save()
        return (labels, results)

    def apply(self, datasets_fd = "mock_datasets/"):
        # Calculates metafeatures for every datasets in the datasets directory
        self.datasets_dir = datasets_fd
        # Getting list of datasets inside directory
        self.datasets = [f for f in listdir(self.datasets_dir)
            if ( isfile(join(self.datasets_dir, f)) and
               ( f.endswith("json") or f.endswith("arff") ) )]
        for dataset in self.datasets:
            self.calculate(dataset)
