"""The model package defines machine learning models"""

from abc import ABC


class Model(ABC):
    def compile(self):
        raise NotImplementedError


class SupervisedModel(Model):
    def compile(self):
        raise NotImplementedError
