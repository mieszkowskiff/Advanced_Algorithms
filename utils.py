import string
import json

def generate_labels(n: int, uppercase: bool = True) -> list[str]:
    """
    # Generates array of excel-like labels.
    Generates array of excel-like labels of length `n`.
    """
    if uppercase:
        letters = string.ascii_uppercase
    else:
        letters = string.ascii_lowercase
    result = []
    index = 1
    
    while len(result) < n:
        label = ""
        temp = index
        while temp > 0:
            temp -= 1
            label = letters[temp % 26] + label
            temp //= 26
        result.append(label)
        index += 1
    
    return result

def rename_nodes(dict) -> dict[str: dict[str: int]]:
    """
    # Renames the nodes of the tree.
    Renames the nodes of the tree to strings.
    """
    n = len(dict)
    labels = generate_labels(n)
    keys = list(dict.keys())
    mapping = {keys[i]: labels[i] for i in range(n)}
    return {mapping[key]: {mapping[node]: weight for node, weight in value.items()} for key, value in dict.items()}

def save_to_file(dict: dict[int: dict[int: int]], filename: str):
    """
    # Saves the tree or instance to a file.
    Saves the tree or instance to a file in JSON format."""
    with open(f"./instances/{filename}", "w") as file:
        json.dump(dict, file)

def load_from_file(filename: str) -> dict[int: dict[int: int]]:
    """
    # Loads the tree or instance from a file.
    Loads the tree or instance from a file in JSON format."""
    with open(f"./instances/{filename}", "r") as file:
        return json.load(file)