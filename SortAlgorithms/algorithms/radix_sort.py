from algorithms.sort_strategy_interface import SortStrategy

class RadixSort(SortStrategy):
    def sort(self, arr):
        max_num = max(arr)
        exp = 1
        while max_num // exp > 0:
            self.counting_sort(arr, exp)
            exp *= 10
    
    def counting_sort(self, arr, exp):
        n = len(arr)
        output = [0] * n
        count = [0] * 10
        for i in arr:
            index = i // exp % 10
            count[index] += 1
        for i in range(1, 10):
            count[i] += count[i - 1]
        i = n - 1
        while i >= 0:
            index = arr[i] // exp % 10
            output[count[index] - 1] = arr[i]
            count[index] -= 1
            i -= 1
        arr[:] = output