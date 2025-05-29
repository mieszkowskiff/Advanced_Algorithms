import subprocess
import time
import re
import matplotlib.pyplot as plt

def test_instance_creation(nodes: int):
    # Przygotowanie wejścia dla programu EXE
    input_data = f"{nodes}\ntesting\n"

    # Uruchomienie programu i przekazanie danych wejściowych
    process = subprocess.run(
        ["create_instance.exe"],
        input=input_data,
        capture_output = True,
        text=True
    )

    output = process.stdout

    # Szukanie czasu w wyjściu
    match = re.search(r"Instance creation time: ([\d\.]+)s", output)
    if match:
        creation_time = float(match.group(1))
        return creation_time
    else:
        print("Nie udało się znaleźć czasu w wyjściu programu.")
        print("Pełne wyjście:")
        print(output)
        return None


def solve_instance():
    # Przygotowanie wejścia: ścieżka do instancji i do pliku wyjściowego
    input_data = "testing\n_\n"

    # Uruchomienie solve.exe
    process = subprocess.run(
        ["solve.exe"],
        input=input_data,
        capture_output=True,
        text=True
    )

    output = process.stdout

    # Szukanie czasu w wyjściu
    match = re.search(r"Sollution time: ([\d\.]+)s", output)
    if match:
        solve_time = float(match.group(1))
        return solve_time
    else:
        print("Nie udało się znaleźć czasu w wyjściu programu.")
        print("Pełne wyjście:")
        print(output)
        return None



def main():
    instance_creation_time = dict()
    solving_time = dict()

    for n in range(100, 6001, 100):
        print(f"Testowanie dla {n} wierzchołków...")
        instance_creation_time[n] = []
        solving_time[n] = []
        for i in range(1):
            instance_creation_time[n].append(test_instance_creation(n))
            solving_time[n].append(solve_instance())

    plt.figure(figsize=(8, 5))

    # Seria 1 - czas tworzenia instancji
    X = []
    Y1 = []
    Y2 = []
    for n, times in instance_creation_time.items():
        X.extend([n] * len(times))
        Y1.extend(times)

    for n, times in solving_time.items(): 
        Y2.extend(times)

    plt.figure(figsize=(6, 4))
    plt.scatter(X, Y1, label="Czas tworzenia instancji", color='blue', marker='o')
    plt.xlabel("Liczba wierzchołków w grafie")
    plt.ylabel("Czas (s)")
    plt.title("Czas tworzenia instancji")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Wykres 2 - czas rozwiązywania instancji
    plt.figure(figsize=(6, 4))
    plt.scatter(X, Y2, label="Czas rozwiązywania instancji", color='red', marker='o')
    plt.xlabel("Liczba wierzchołków w grafie")
    plt.ylabel("Czas (s)")
    plt.title("Czas rozwiązywania instancji")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()



if __name__ == "__main__":
    main()
