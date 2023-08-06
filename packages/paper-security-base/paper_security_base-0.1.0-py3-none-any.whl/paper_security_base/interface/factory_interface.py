from __future__ import annotations
from abc import ABC, abstractmethod

from paper_security_base.interface import AbstractFeature


class AbstractFactory(ABC):
    """
    The Abstract Factory interface declares a set of methods that return
    different abstract products. These products are called a family and are
    related by a high-level theme or concept. Products of one family are usually
    able to collaborate among themselves. A family of products may have several
    variants, but the products of one variant are incompatible with products of
    another.
    """
    @abstractmethod
    def create_feature(self) -> AbstractFeature:
        pass

    @abstractmethod
    def create_matched(self) -> any:
        pass

    @abstractmethod
    def create_clusted(self) -> any:
        pass

    @abstractmethod
    def create_graph(self) -> any:
        pass

    @abstractmethod
    def getPathFeature(self)->any:
        pass