import random
import csv

numbers = [random.randint(1, 1000000) for _ in range(10000)]

# Gera os números aleatórios e salva em um arquivo CSV
with open('random_numbers.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(numbers)