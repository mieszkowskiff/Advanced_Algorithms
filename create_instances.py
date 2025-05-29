import random
import utils
import time
import typing

def generate_tree(n: int, gamma: float = 0.8, max_weight: int = 10) -> typing.Dict[int, typing.Dict[int, int]]:
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
    
    initial_weight = random.randint(1, max_weight)
    adjacency_list = {
        0: {1: initial_weight},
        1: {0: initial_weight}
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

            weight = random.randint(1, max_weight)
            adjacency_list[parent][node_number] = weight
            adjacency_list[node_number] = {parent: weight}

            node_number += 1
            
        else:
            # We decided to add two new nodes (leaf and an internal node)
            parent1 = random.randint(0, node_number - 1)
            parent2 = random.choice(list(adjacency_list[parent1].keys()))

            adjacency_list[parent1].pop(parent2)
            adjacency_list[parent2].pop(parent1)

            weight1 = random.randint(1, max_weight)
            weight2 = random.randint(1, max_weight)
            weight3 = random.randint(1, max_weight)

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
    return utils.rename_nodes(adjacency_list)


def BFS(tree: typing.Dict[int, typing.Dict[int, int]], start: int) -> typing.Dict[int, int]:
    """
    # Breadth-first search.
    Breadth-first search algorithm is used to find the distances between leaf nodes of the tree.

    ## Parameters:
    ### `tree`: *dict[int: dict[int: int]]*
    The tree is represented as an adjacency list.

    ### `start`: *int*
    The starting node of the BFS.

    ## Returns:
    A dictionary where the keys are the leaf nodes of the tree and the values are the distances between the starting node and the leaf nodes.
    """
    distances = {start: 0}
    visited = {start}
    queue = [start]

    while queue:
        node = queue.pop(0)
        for neighbour in tree[node].keys():
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)
                distances[neighbour] = distances[node] + tree[node][neighbour]
    return distances

def create_instance(tree: typing.Dict[int, typing.Dict[int, int]], original_names: bool = False) -> typing.Dict[int, typing.Dict[int, int]]: 
    """
    # Creates an instance from the tree.
    An instance is matrix of the distances between leaf nodes of the tree.

    """
    distances_list = {}
    for nodeA in tree:
        if len(tree[nodeA]) == 1:
            distances = BFS(tree, nodeA)
            distances_list[nodeA] = {nodeB: weight for nodeB, weight in distances.items() if len(tree[nodeB]) == 1}
    if original_names:
        return distances_list
    return utils.rename_nodes(distances_list)


def main():
    random.seed(43)
    n = int(input("Enter number of nodes:"))
    start_time = time.time()
    tree = generate_tree(n = n, gamma = 0.8, max_weight = 10)
    instance = create_instance(tree)
    print(f"Instance creation time: {time.time() - start_time}s")
    
    with open(input("Enter the path to save the instance file (.txt file): "), 'w') as f:
        for src in instance:
            for dest, weight in instance[src].items():
                f.write(f"{src} {dest} {weight}\n")
    
    print("Files saved successfully")
    

if __name__ == "__main__":
    main()