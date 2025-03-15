import csv
from algorithms.bubble_sort import BubbleSort
from algorithms.bubble_sort_optimized import BubbleSortOptimized
from algorithms.counting_sort import CountingSort
from algorithms.insertion_sort import InsertionSort
from algorithms.selection_sort import SelectionSort
from algorithms.quick_sort import QuickSort
from algorithms.merge_sort import MergeSort
from algorithms.heap_sort import HeapSort
from algorithms.shell_sort import ShellSort
from algorithms.radix_sort import RadixSort
from algorithms.tim_sort import TimSort
from algorithms.sort_context import SortContext

def read_numbers(file):
    with open(file, 'r') as f:
        reader = csv.reader(f)
        return [int(num) for row in reader for num in row]

def save_numbers(file, numbers):
    with open(file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(numbers)

def choice_method():
    # Métodos de ordenação disponíveis
    methods = {
        '1': ('bubble_sort', BubbleSort()),
        '2': ('bubble_sort_optimized', BubbleSortOptimized()),
        '3': ('insertion_sort', InsertionSort()),
        '4': ('selection_sort', SelectionSort()),
        '5': ('quick_sort', QuickSort()),
        '6': ('merge_sort', MergeSort()),
        '7': ('heap_sort', HeapSort()),
        '8': ('shell_sort', ShellSort()),
        '9': ('counting_sort', CountingSort()),
        '10': ('radix_sort', RadixSort()),
        '11': ('tim_sort', TimSort())
    }

    print("Escolha o método de ordenação:")

    for key, (name, _) in methods.items():
        print(f"{key} - {name.replace('_', ' ').title()}")
    choice = input("Digite o número correspondente: ")
    return methods.get(choice, None)

if __name__ == "__main__":
    methods = choice_method()
    # Verifica se a escolha é válida
    if methods:
        name_method, strategy_instance = methods
        numbers = read_numbers('random_numbers.csv')
        context = SortContext(strategy_instance)
        context.execute_sort(numbers)
        save_numbers(f'results/{name_method}.csv', numbers)
        print(f"Arquivo {name_method}.csv gerado com sucesso!")
    else:
        print("Opção inválida!")