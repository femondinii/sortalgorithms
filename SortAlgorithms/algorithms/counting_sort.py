from algorithms.sort_strategy_interface import SortStrategy

class CountingSort(SortStrategy):
    def sort(self, arr):
        if not arr:
            return
        max_val = max(arr)
        count = [0] * (max_val + 1)
        for num in arr:
            count[num] += 1
        index = 0
        for i in range(len(count)):
            while count[i] > 0:
                arr[index] = i
                index += 1
                count[i] -= 1