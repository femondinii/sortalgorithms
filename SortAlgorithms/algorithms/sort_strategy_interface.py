from abc import ABC, abstractmethod

class SortStrategy(ABC):
    """Interface para estratégias de ordenação."""
    @abstractmethod
    def sort(self, arr):
        pass