import subprocess
import re
import matplotlib.pyplot as plt

def test_instance_creation(nodes: int):
    # Uruchomienie create_instances.py z wymaganymi argumentami
    result = subprocess.run(
        ["python", "create_instances.py", str(nodes), "tree", "instance"],
        capture_output=True,
        text=True
    )
    output = result.stdout

    # Szukanie czasu z komunikatu "Finished in 0.00s"
    match = re.search(r"Finished in ([\d\.]+)s", output)
    if match:
        return float(match.group(1))
    else:
        print("Nie udało się znaleźć czasu w wyjściu programu create_instances.py.")
        print("Pełne wyjście:")
        print(output)
        return None

def solve_instance():
    # Uruchomienie solve.py z wymaganymi argumentami
    result = subprocess.run(
        ["python", "solve.py", "instance", "output"],
        capture_output=True,
        text=True
    )
    output = result.stdout

    # Szukanie czasu z komunikatu "Solution time: 0.00s"
    match = re.search(r"Solution time: ([\d\.]+)s", output)
    if match:
        return float(match.group(1))
    else:
        print("Nie udało się znaleźć czasu w wyjściu programu solve.py.")
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

        instance_creation_time[n].append(test_instance_creation(n))
        solving_time[n].append(solve_instance())

    # Przygotowanie danych do wykresów
    X = []
    Y1 = []
    Y2 = []

    for n, times in instance_creation_time.items():
        X.extend([n] * len(times))
        Y1.extend(times)

    for times in solving_time.values():
        Y2.extend(times)

    # Wykres 1 - czas tworzenia instancji
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
