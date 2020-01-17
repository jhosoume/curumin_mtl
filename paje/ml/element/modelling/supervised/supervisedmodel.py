from abc import ABC

from paje.base.component import Component
from paje.ml.element.element import Element


class SupervisedModel(Element, ABC):
    def apply_impl(self, data):
        """
        If predictions on original data is really needed, it should be
        calculated by actual_output = component.use(original_data).
        :param data:
        :return:
        """
        # self.model will be set in the child class
        # print('classif.......', data)
        self.model.fit(*data.Xy)
        return self.use_impl(data)

    def use_impl(self, data):
        return data.updated(self, z=self.model.predict(data.X))

    def modifies(self, op):
        return ['Z']
