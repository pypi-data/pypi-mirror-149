from __future__ import annotations

import json
import os
import pickle
from abc import ABC, abstractmethod
from typing import List

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, P):
            return obj.__dict__         # <-----
        return json.JSONEncoder.default(self, obj)

class AbstractSumary(ABC):
    @abstractmethod
    def get_desc(self) -> any:
        pass

    @abstractmethod
    def diff(self, other: AbstractSumary) -> any:
        pass

    def serialize(self):
        return json.dumps(self, cls=ComplexEncoder)

    def save(self,path_name,name):
        path_name+=os.sep
        if not os.path.isdir(path_name):
            os.makedirs(path_name)
        pickle.dump(self, open(path_name+name, "wb"))

    @staticmethod
    def read(name):
        return pickle.load(open(name, "rb"))



class AbstractFeature(ABC):
    """
    Each distinct product of a product family should have a base interface. All
    variants of the product must implement this interface.
    """

    @abstractmethod
    def detect(self, doc: AbstractSumary) -> AbstractSumary:
        pass

    @abstractmethod
    def detect_batch(self, docs: AbstractSumary) -> List[AbstractSumary]:
        pass