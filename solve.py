from utils import read_graph_from_txt, save_graph_to_txt, initial_valid_check
import time
import typing

class Branch:
    def __init__(self, start_node, end_node, length, instance_matrix, queue_of_new_symbols):
        self.start_node = start_node
        self.end_node = end_node
        self.instance_matrix = instance_matrix
        self.length = length
        self.children = dict()
        self.queue_of_new_symbols = queue_of_new_symbols

    def add_node(self, new_node, distance_to_start):
        distance_to_end = self.instance_matrix[self.end_node][new_node]

        d1 = (self.length + distance_to_start - distance_to_end) / 2
        d2 = (self.length - distance_to_start + distance_to_end) / 2
        d3 = (-self.length + distance_to_start + distance_to_end) / 2
        
        # d1 can be equal to 0, this means that current node is a start node for 
        # a new Branch 
        # if d2 == 0 then d1 == self.length and d3 == distance_to_end which also semms to
        # be wrong, because the end_node has to be a leaf
        # d3 cannot be equal to 0, d3 is a length of a new Branch
        if not initial_valid_check(d1, d2, d3) or (d2 == 0) or (d3 == 0):
            print("initial_valid_check FAILED")
            # recurssion failed at some point, valid check failed 
            return False
        
        d1 = int(d1)
        d2 = int(d2)
        d3 = int(d3)

        if d1 in self.children:
            # return the check status to the previous recursion calls
            return self.children[d1].add_node(new_node, d3)
        else:
            if d1 == 0:
                self.children[d1] = Branch(self.start_node, new_node, d3, self.instance_matrix, self.queue_of_new_symbols)
            else:
                new_intersection_node = self.queue_of_new_symbols.pop(0)
                self.children[d1] = Branch(new_intersection_node, new_node, d3, self.instance_matrix, self.queue_of_new_symbols)
            # recurssion made it to the end without trigerring the check
            return True

    def fill_adjacency_list(self, adjacency_list):
        # TODO: this sort below would be redundant in binary tree dictionary
        indexes = sorted(list(self.children.keys()))

        if len(indexes) == 0:
            adjacency_list[self.start_node][self.end_node] = self.length
            adjacency_list[self.end_node] = {self.start_node: self.length}
            return
        if indexes[0] != 0:
            adjacency_list[self.start_node][self.children[indexes[0]].start_node] = indexes[0]
            adjacency_list[self.children[indexes[0]].start_node] = {self.start_node: indexes[0]}
        self.children[indexes[0]].fill_adjacency_list(adjacency_list)

        for child_index in range(1, len(indexes)):
            previous_child = self.children[indexes[child_index - 1]]
            actual_child = self.children[indexes[child_index]]

            adjacency_list[previous_child.start_node][actual_child.start_node] = indexes[child_index]- indexes[child_index - 1]
            adjacency_list[actual_child.start_node] = {previous_child.start_node: indexes[child_index] - indexes[child_index - 1]}
            actual_child.fill_adjacency_list(adjacency_list)

        adjacency_list[self.children[indexes[-1]].start_node][self.end_node] = self.length - indexes[-1]
        adjacency_list[self.end_node] = {self.children[indexes[-1]].start_node: self.length - indexes[-1]}
        return
    
    def print(self, depth=0, index = ""):
        indent = "\t" * depth
        if index != "":
            index = f"{index}: "
        print(f"{indent}{index}Branch(\n{indent}\tstart_node={self.start_node},", end="") 
        print(f"end_node={self.end_node}, length={self.length}\n{indent}\tchildren: \n", end="")
        for distance, child in self.children.items():
            child.print(depth = depth + 1, index = distance)
        print(f"{indent})")

        
def solve(instance: typing.Dict[str, typing.Dict[str, int]]) -> typing.Dict[str, typing.Dict[str, int]]:
    """
    # Recreates the tree from the distance matrix between leaf nodes.
    """

    n = len(instance)
    if n in [0, 1, 2]:
        return instance
    
    leaves = list(instance.keys())

    queue_of_new_symbols = [f"INTERNAL_NODE_{i}" for i in range(n - 2)]
    root = Branch(leaves[0], leaves[1], instance[leaves[0]][leaves[1]], instance, queue_of_new_symbols)

    valid_check = True
    for leaf in leaves[2:]:
        if not root.add_node(leaf, instance[leaves[0]][leaf]):
            valid_check = False
            break

    if valid_check:
        adjacency_list = {
            leaves[0]: dict(),
        }

        root.fill_adjacency_list(adjacency_list)
        
        return adjacency_list, valid_check
    else:   
        return [], valid_check
import sys
import time

def read_instance_matrix(path: str) -> dict:
    instance = {}
    with open(path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    n = len(lines)
    for i, line in enumerate(lines):
        row = list(map(int, line.split()))
        instance[str(i + 1)] = {}
        for j, val in enumerate(row):
            if i != j:
                instance[str(i + 1)][str(j + 1)] = val
    return instance

def write_adjacency_list(adj: dict, path: str):
    leaf_nodes = sorted([node for node in adj if node.isdigit()], key=lambda x: int(x))
    next_index = max(int(x) for x in leaf_nodes) + 1

    label_to_index = {leaf: int(leaf) for leaf in leaf_nodes}
    for node in adj:
        if node not in label_to_index:
            label_to_index[node] = next_index
            next_index += 1

    relabeled_adj = {}
    for node in adj:
        new_node = label_to_index[node]
        neighbors = [label_to_index[nei] for nei in adj[node]]
        relabeled_adj[new_node] = sorted(neighbors)

    with open(path, 'w') as f:
        for node in sorted(relabeled_adj):
            neighbors = relabeled_adj[node]
            f.write(f"{node}\t{' '.join(map(str, neighbors))}\n")


def main():
    if len(sys.argv) != 3:
        print("Usage: python solve.py <path_to_instance.txt> <path_to_output.txt>")
        sys.exit(1)

    path_instance = sys.argv[1]
    path_output = sys.argv[2]

    instance = read_instance_matrix(path_instance)
    print("Instance loaded.")

    # Rozwiązywanie
    start_time = time.time()
    adjacency_list, valid_check = solve(instance)
    print(f"Solution time: {time.time() - start_time:.2f}s")

    if valid_check:
        write_adjacency_list(adjacency_list, path_output)
        print("File saved successfully.")
    else:
        print("Input data is not valid. Initial validity check failed.")

if __name__ == "__main__":
    main()
