""" Scaler Module
"""
from abc import ABC

from paje.ml.element.element import Element

class Imbalance(Element, ABC):
    def apply_impl(self, data):
        # self.model will be set in the child class
        X, y = self.model.fit_resample(*data.Xy)
        return data.updated(self, X = X, y = y)

    def use_impl(self, data):
        return data

    @classmethod
    def isdeterministic(cls):
        return False

    def modifies(self, op):
        return ['X', 'Y']
