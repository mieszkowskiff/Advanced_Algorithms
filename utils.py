import string
import json
import typing

def generate_labels(n: int, uppercase: bool = True) -> typing.List[str]:
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

def rename_nodes(dict) -> typing.Dict[str, typing.Dict[str, int]]:
    """
    # Renames the nodes of the tree.
    Renames the nodes of the tree to strings.
    """
    n = len(dict)
    labels = generate_labels(n)
    keys = list(dict.keys())
    mapping = {keys[i]: labels[i] for i in range(n)}
    return {mapping[key]: {mapping[node]: weight for node, weight in value.items()} for key, value in dict.items()}

def save_to_file(dict: typing.Dict[int, typing.Dict[int, int]], filename: str):
    """
    # Saves the tree or instance to a file.
    Saves the tree or instance to a file in JSON format."""
    with open(f"./instances/{filename}", "w") as file:
        json.dump(dict, file)

def load_from_file(filename: str) -> typing.Dict[int, typing.Dict[int, int]]:
    """
    # Loads the tree or instance from a file.
    Loads the tree or instance from a file in JSON format."""
    with open(f"./instances/{filename}", "r") as file:
        return json.load(file)
    
def read_graph_from_txt(file_path):
    graph = {}
    with open(file_path, 'r') as f:
        for line in f:
            src, dest, weight = line.strip().split()

            try:
                weight = int(weight)
            except:
                print("Input data is not valid. Provided weights are not positive integers.")
                return [], False
            
            if src not in graph:
                graph[src] = {src: 0}
            graph[src][dest] = weight
    return graph, True 

def save_graph_to_txt(adjacency_list, file_path):
    with open(file_path, 'w') as f:
        for src in adjacency_list:
            for dest, weight in adjacency_list[src].items():
                f.write(f"{src} {dest} {weight}\n")

def is_non_negative_whole_number(n):
    return (isinstance(n, int) or (isinstance(n, float) and n.is_integer())) and n >= 0

def initial_valid_check(d1, d2, d3):
    """
    This function performs an initial check. If all 3 values are natual numbers,
    the check is passed. 
    """
    if is_non_negative_whole_number(d1) and is_non_negative_whole_number(d2) and is_non_negative_whole_number(d3):
        return True
    else:
        return False
     