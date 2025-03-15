from algorithms.sort_strategy_interface import SortStrategy

class SortContext:
    def __init__(self, strategy: SortStrategy):
        self.strategy = strategy
    
    def execute_sort(self, arr):
        self.strategy.sort(arr)