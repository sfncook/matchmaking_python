from abc import ABC, abstractmethod
from typing import List

class VectorStore(ABC):
    @abstractmethod
    def initialize(self):
        """Initialize the data store."""
        pass

    @abstractmethod
    def add_vector_data(self, uuid: str, vector: List[float]):
        """Adds a single vector to the index."""
        pass

    @abstractmethod
    def search_nearest(self, vector, limit):
        pass

    @abstractmethod
    def count(self):
        pass

    @abstractmethod
    def clear(self):
        """Delete all data from the index"""
        pass
