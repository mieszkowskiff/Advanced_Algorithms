import random
import json

def generate_tree(n: int, gamma: float = 0.7) -> dict[int: dict[int: int]]:
    """
    # Generates a tree with `n` nodes.
    Generates a tree with `n` nodes, but without the nodes of degree 2 (all nodes are either leaves or "intersection" nodes).

    ## Parameters:

    ### `n`: *int*
    The number of nodes in the tree.

    ### `gamma`: *float*, optional
    The `gamma` paramter is used to control the probability of adding a leaf node or an "intersection" node.
    On average, `gamma * n = l`, where `l` is the number of leaf nodes in the tree.

    Range of `gamma`: `(0, 1]`, where `gamma = 1` means that the tree consists only of internal nodes of degree 3, 
    and `gamma` close to 0 means that the tree consists only of one internal node of degree `n - 1`.

    ## Returns:
    A dictionary that represents the adjacency list of the tree, where the value of internal dictionary is the weight of the edge.
    """
    if n < 2:
        raise ValueError("The tree must have at least 2 nodes.")
    if n == 3:
        raise ValueError("3 as the number of nodes is invalid.")
    
    initial_weight = random.randint(1, 100)
    adjacency_list = {
        1: {0: initial_weight},
        0: {1: initial_weight}
    }

    beta = 1 / gamma - 1

    node_number = 2

    while node_number < n:
        # in each iteration one leaf is added to the tree
        if (random.uniform(0, 1) < beta or node_number == n - 1) and node_number > 2:
            # We decided to add one new node (leaf)
            parent = random.randint(0, node_number - 1)
            while len(adjacency_list[parent]) == 1:
                parent = random.randint(0, node_number - 1)

            weight = random.randint(1, 100)
            adjacency_list[parent][node_number] = weight
            adjacency_list[node_number] = {parent: weight}

            node_number += 1
            
        else:
            # We decided to add two new nodes (leaf and internal node)
            parent1 = random.randint(0, node_number - 1)
            parent2 = random.choice(list(adjacency_list[parent1].keys()))

            adjacency_list[parent1].pop(parent2)
            adjacency_list[parent2].pop(parent1)

            weight1 = random.randint(1, 100)
            weight2 = random.randint(1, 100)
            weight3 = random.randint(1, 100)

            adjacency_list[parent1][node_number] = weight1
            adjacency_list[parent2][node_number] = weight2

            adjacency_list[node_number] = {
                parent1: weight1,
                parent2: weight2,
                node_number + 1: weight3
            }

            adjacency_list[node_number + 1] = {
                node_number: weight3
            }

            node_number += 2
    return adjacency_list


def save_tree_to_file(tree: dict[int: dict[int: int]], filename: str):
    """
    # Saves the tree to a file.
    Saves the tree to a file in JSON format."""
    with open(filename, "w") as file:
        json.dump(tree, file)


    

def main():
    n = 10
    adjacency_list = generate_tree(n)
    print("Adjacency list:")
    print(adjacency_list)

if __name__ == "__main__":
    main()