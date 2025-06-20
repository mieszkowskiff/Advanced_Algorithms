import random
import utils
import time
import typing
import sys
from collections import defaultdict


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





def build_adjacency(tree: typing.Dict[str, typing.Dict[str, int]]) -> typing.Dict[str, set]:
    adj = defaultdict(set)
    for src in tree:
        for dest in tree[src]:
            adj[src].add(dest)
            adj[dest].add(src)
    return adj

def assign_indices_with_leaves_first(adj: typing.Dict[str, set]) -> typing.Dict[str, int]:
    leaves = sorted([node for node in adj if len(adj[node]) == 1])
    others = sorted([node for node in adj if len(adj[node]) > 1])
    ordered_nodes = leaves + others
    label_to_index = {label: idx + 1 for idx, label in enumerate(ordered_nodes)}
    return label_to_index

def relabel_adjacency(adj: typing.Dict[str, set], label_to_index: typing.Dict[str, int]) -> typing.Dict[int, set]:
    new_adj = defaultdict(set)
    for old_node in adj:
        new_node = label_to_index[old_node]
        for neighbor in adj[old_node]:
            new_neighbor = label_to_index[neighbor]
            new_adj[new_node].add(new_neighbor)
    return new_adj

def save_adjacency_list(adj: typing.Dict[int, set], path: str):
    with open(path, 'w') as f:
        for node in sorted(adj):
            neighbors = sorted(adj[node])
            f.write(f"{node}\t{' '.join(str(n) for n in neighbors)}\n")

def save_leaf_distance_matrix(instance: typing.Dict[str, typing.Dict[str, int]],
                              label_to_index: typing.Dict[str, int],
                              tree: typing.Dict[str, typing.Dict[str, int]],
                              path: str):

    leaf_labels = [label for label in tree if len(tree[label]) == 1]

    leaf_labels_sorted = sorted(leaf_labels, key=lambda x: label_to_index[x])
    k = len(leaf_labels_sorted)

    with open(path, 'w') as f:
        for i in range(k):
            row = []
            for j in range(k):
                if i == j:
                    row.append('0')
                else:
                    u = leaf_labels_sorted[i]
                    v = leaf_labels_sorted[j]
                    try:
                        dist = instance[u][v]
                    except KeyError:
                        dist = instance[v][u]
                    row.append(str(dist))
            f.write(' '.join(row) + '\n')

def main():
    if len(sys.argv) != 4:
        print("Usage: python filename.py <node_number> <tree_file.txt> <instance_file.txt>")
        sys.exit(1)

    try:
        n = int(sys.argv[1])
        path_tree = sys.argv[2]
        path_instance = sys.argv[3]
    except ValueError:
        print("Error: node_number must be an integer.")
        sys.exit(1)

    random.seed(43)
    start_time = time.time()

    tree = generate_tree(n=n, gamma=0.8, max_weight=10)
    instance = create_instance(tree, original_names = True)

    adj = build_adjacency(tree)
    label_to_index = assign_indices_with_leaves_first(adj)
    relabeled_adj = relabel_adjacency(adj, label_to_index)

    save_adjacency_list(relabeled_adj, path_tree)
    save_leaf_distance_matrix(instance, label_to_index, tree, path_instance)

    print(f"Finished in {time.time() - start_time:.2f}s")
    print("Files saved successfully.")

if __name__ == "__main__":
    main()
