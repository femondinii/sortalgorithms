from algorithms.sort_strategy_interface import SortStrategy

class HeapSort(SortStrategy):
    def sort(self, arr):
        import heapq
        heapq.heapify(arr)
        arr[:] = [heapq.heappop(arr) for _ in range(len(arr))]