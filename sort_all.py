from abc import ABC, abstractmethod
import copy
import random
import time
import os
import logging
from prometheus_client import start_http_server, Summary, Counter

#########################
# Configuração de Logging
#########################
logging.basicConfig(
    filename="python_app.log",  # Arquivo onde os logs serão gravados
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logging.info("Iniciando o benchmark de algoritmos de ordenação.")

#########################
# Configuração do Prometheus
#########################
ALGORITHM_DURATION = Summary(
    "algorithm_duration_seconds", "Tempo gasto em segundos para ordenar", ["algorithm"]
)
ALGORITHM_COMPARISONS = Counter(
    "algorithm_comparisons_total", "Total de comparações realizadas", ["algorithm"]
)
ALGORITHM_SWAPS = Counter(
    "algorithm_swaps_total", "Total de trocas realizadas", ["algorithm"]
)


#########################
# Implementação dos Algoritmos
#########################
class SortResult:
    def __init__(self, sorted_data, comparisons, swaps):
        self.sorted_data = sorted_data
        self.comparisons = comparisons
        self.swaps = swaps


class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data):
        pass


class BubbleSort(SortStrategy):
    def sort(self, data):
        logging.info("Executando BubbleSort.")
        arr = copy.deepcopy(data)
        n = len(arr)
        comparisons = 0
        swaps = 0
        for i in range(n):
            for j in range(0, n - i - 1):
                comparisons += 1
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swaps += 1
        return SortResult(arr, comparisons, swaps)


class InsertionSort(SortStrategy):
    def sort(self, data):
        logging.info("Executando InsertionSort.")
        arr = copy.deepcopy(data)
        comparisons = 0
        swaps = 0
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0:
                comparisons += 1
                if arr[j] > key:
                    arr[j + 1] = arr[j]
                    swaps += 1
                    j -= 1
                else:
                    break
            arr[j + 1] = key
            swaps += 1
        return SortResult(arr, comparisons, swaps)


class QuickSort(SortStrategy):
    def sort(self, data):
        logging.info("Executando QuickSort.")
        arr = copy.deepcopy(data)
        self.comparisons = 0
        self.swaps = 0
        self._quick_sort(arr, 0, len(arr) - 1)
        return SortResult(arr, self.comparisons, self.swaps)

    def _quick_sort(self, arr, low, high):
        if low < high:
            pi = self._partition(arr, low, high)
            self._quick_sort(arr, low, pi - 1)
            self._quick_sort(arr, pi + 1, high)

    def _partition(self, arr, low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            self.comparisons += 1
            if arr[j] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                self.swaps += 1
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        self.swaps += 1
        return i + 1


class SelectionSort(SortStrategy):
    def sort(self, data):
        logging.info("Executando SelectionSort.")
        arr = copy.deepcopy(data)
        n = len(arr)
        comparisons = 0
        swaps = 0
        for i in range(n):
            min_index = i
            for j in range(i + 1, n):
                comparisons += 1
                if arr[j] < arr[min_index]:
                    min_index = j
            if min_index != i:
                arr[i], arr[min_index] = arr[min_index], arr[i]
                swaps += 1
        return SortResult(arr, comparisons, swaps)


class MergeSort(SortStrategy):
    def sort(self, data):
        logging.info("Executando MergeSort.")
        arr = copy.deepcopy(data)
        self.comparisons = 0
        self.swaps = 0
        self._merge_sort(arr, 0, len(arr))
        return SortResult(arr, self.comparisons, self.swaps)

    def _merge_sort(self, arr, left, right):
        if right - left > 1:
            mid = (left + right) // 2
            self._merge_sort(arr, left, mid)
            self._merge_sort(arr, mid, right)
            self._merge(arr, left, mid, right)

    def _merge(self, arr, left, mid, right):
        L = arr[left:mid]
        R = arr[mid:right]
        i = 0
        j = 0
        k = left
        while i < len(L) and j < len(R):
            self.comparisons += 1
            if L[i] <= R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            self.swaps += 1
            k += 1
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
            self.swaps += 1
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
            self.swaps += 1


class TimSort(SortStrategy):
    def sort(self, data):
        logging.info("Executando TimSort (simplificado).")
        arr = copy.deepcopy(data)
        self.comparisons = 0
        self.swaps = 0
        minrun = 32
        n = len(arr)
        for start in range(0, n, minrun):
            end = min(start + minrun, n)
            self._insertion_sort(arr, start, end)
        size = minrun
        while size < n:
            for left in range(0, n, 2 * size):
                mid = min(n, left + size)
                right = min(n, left + 2 * size)
                self._merge(arr, left, mid, right)
            size *= 2
        return SortResult(arr, self.comparisons, self.swaps)

    def _insertion_sort(self, arr, left, right):
        for i in range(left + 1, right):
            key = arr[i]
            j = i - 1
            while j >= left:
                self.comparisons += 1
                if arr[j] > key:
                    arr[j + 1] = arr[j]
                    self.swaps += 1
                    j -= 1
                else:
                    break
            arr[j + 1] = key
            self.swaps += 1

    def _merge(self, arr, left, mid, right):
        L = arr[left:mid]
        R = arr[mid:right]
        i = 0
        j = 0
        k = left
        while i < len(L) and j < len(R):
            self.comparisons += 1
            if L[i] <= R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            self.swaps += 1
            k += 1
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
            self.swaps += 1
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
            self.swaps += 1


class HeapSort(SortStrategy):
    def sort(self, data):
        logging.info("Executando HeapSort.")
        arr = copy.deepcopy(data)
        n = len(arr)
        self.comparisons = 0
        self.swaps = 0
        for i in range(n // 2 - 1, -1, -1):
            self._heapify(arr, n, i)
        for i in range(n - 1, 0, -1):
            arr[0], arr[i] = arr[i], arr[0]
            self.swaps += 1
            self._heapify(arr, i, 0)
        return SortResult(arr, self.comparisons, self.swaps)

    def _heapify(self, arr, heap_size, root_index):
        largest = root_index
        left = 2 * root_index + 1
        right = 2 * root_index + 2
        if left < heap_size:
            self.comparisons += 1
            if arr[left] > arr[largest]:
                largest = left
        if right < heap_size:
            self.comparisons += 1
            if arr[right] > arr[largest]:
                largest = right
        if largest != root_index:
            arr[root_index], arr[largest] = arr[largest], arr[root_index]
            self.swaps += 1
            self._heapify(arr, heap_size, largest)


class CountingSort(SortStrategy):
    def sort(self, data):
        logging.info("Executando CountingSort.")
        arr = copy.deepcopy(data)
        if not arr:
            return SortResult(arr, 0, 0)
        max_val = max(arr)
        count = [0] * (max_val + 1)
        for num in arr:
            count[num] += 1
        self.comparisons = 0
        self.swaps = 0
        index = 0
        for num, freq in enumerate(count):
            for _ in range(freq):
                arr[index] = num
                self.swaps += 1
                index += 1
        return SortResult(arr, self.comparisons, self.swaps)


class RadixSort(SortStrategy):
    def sort(self, data):
        logging.info("Executando RadixSort.")
        arr = copy.deepcopy(data)
        if not arr:
            return SortResult(arr, 0, 0)
        max_val = max(arr)
        exp = 1
        self.comparisons = 0  # Não utiliza comparações diretas
        self.swaps = 0  # Movimentações contabilizadas
        while max_val // exp > 0:
            self._counting_sort_by_digit(arr, exp)
            exp *= 10
        return SortResult(arr, self.comparisons, self.swaps)

    def _counting_sort_by_digit(self, arr, exp):
        n = len(arr)
        output = [0] * n
        count = [0] * 10
        for i in range(n):
            index = (arr[i] // exp) % 10
            count[index] += 1
        for i in range(1, 10):
            count[i] += count[i - 1]
        for i in range(n - 1, -1, -1):
            index = (arr[i] // exp) % 10
            output[count[index] - 1] = arr[i]
            count[index] -= 1
            self.swaps += 1
        for i in range(n):
            arr[i] = output[i]
            self.swaps += 1


class ShellSort(SortStrategy):
    def sort(self, data):
        logging.info("Executando ShellSort.")
        arr = copy.deepcopy(data)
        n = len(arr)
        comparisons = 0
        swaps = 0
        gap = n // 2
        while gap > 0:
            for i in range(gap, n):
                temp = arr[i]
                j = i
                while j >= gap:
                    comparisons += 1
                    if arr[j - gap] > temp:
                        arr[j] = arr[j - gap]
                        swaps += 1
                        j -= gap
                    else:
                        break
                arr[j] = temp
                swaps += 1
            gap //= 2
        return SortResult(arr, comparisons, swaps)


#########################
# Funções de Gerenciamento de Dados e Benchmark
#########################
def generate_data(file_name, size):
    data = [random.randint(0, 100000) for _ in range(size)]
    with open(file_name, "w") as f:
        f.write("\n".join(map(str, data)))
    logging.info(f"Dados com {size} números salvos em {file_name}.")


def load_data(file_name):
    with open(file_name, "r") as f:
        lines = f.read().splitlines()
    return [int(x) for x in lines]


def benchmark_sort(strategy, data, repetitions=3):
    total_time = 0
    total_comparisons = 0
    total_swaps = 0
    for _ in range(repetitions):
        start = time.time()
        result = strategy.sort(data)
        elapsed = time.time() - start  # tempo em segundos
        total_time += elapsed
        total_comparisons += result.comparisons
        total_swaps += result.swaps
    avg_time = total_time / repetitions
    avg_comparisons = total_comparisons / repetitions
    avg_swaps = total_swaps / repetitions
    return avg_time, avg_comparisons, avg_swaps


#########################
# Função Principal
#########################
def main():
    # Inicia o servidor HTTP do Prometheus na porta 8000
    start_http_server(8000)
    logging.info("Endpoint de métricas disponível em http://localhost:8000/metrics")

    data_file = "data.txt"
    if not os.path.exists(data_file):
        generate_data(data_file, 10000)
    data = load_data(data_file)

    strategies = {
        "BubbleSort": BubbleSort(),
        "InsertionSort": InsertionSort(),
        "SelectionSort": SelectionSort(),
        "QuickSort": QuickSort(),
        "MergeSort": MergeSort(),
        "TimSort": TimSort(),
        "HeapSort": HeapSort(),
        "CountingSort": CountingSort(),
        "RadixSort": RadixSort(),
        "ShellSort": ShellSort(),
    }

    # Executa o benchmark para cada algoritmo e atualiza as métricas do Prometheus
    for name, strategy in strategies.items():
        avg_time, avg_comparisons, avg_swaps = benchmark_sort(strategy, data)
        ALGORITHM_DURATION.labels(algorithm=name).observe(avg_time)
        ALGORITHM_COMPARISONS.labels(algorithm=name).inc(avg_comparisons)
        ALGORITHM_SWAPS.labels(algorithm=name).inc(avg_swaps)
        logging.info(
            f"{name}: Tamanho={len(data)}, Tempo médio={avg_time*1000:.2f} ms, Comparações={avg_comparisons}, Trocas={avg_swaps}"
        )
        print(
            f"{name}: Tamanho={len(data)}, Tempo médio={avg_time*1000:.2f} ms, Comparações={avg_comparisons}, Trocas={avg_swaps}"
        )

    # Mantém o programa em execução para que o Prometheus possa raspar as métricas
    print("Aguardando... Pressione Ctrl+C para encerrar.")
    while True:
        time.sleep(5)


if __name__ == "__main__":
    main()
