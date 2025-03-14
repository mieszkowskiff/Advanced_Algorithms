from utils import load_from_file


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
        # d2 = (self.length - distance_to_start + distance_to_end) / 2
        d3 = (-self.length + distance_to_start + distance_to_end) / 2

        # validate distances here

        if d1 in self.children:
            self.children[d1].add_node(new_node, d3)
        else:
            if d1 == 0:
                self.children[d1] = Branch(self.start_node, new_node, d3, self.instance_matrix, self.queue_of_new_symbols)
            else:
                new_intersection_node = self.queue_of_new_symbols.pop(0)
                self.children[d1] = Branch(new_intersection_node, new_node, d3, self.instance_matrix, self.queue_of_new_symbols)

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

        
            
            

def solve(instance: dict[str: dict[str: int]]) -> dict[str: dict[str: int]]:
    """
    # Recreates the tree from the distance matrix between leaf nodes.
    """

    n = len(instance)
    if n in [0, 1, 2]:
        return instance
    
    leaves = list(instance.keys())

    queue_of_new_symbols = [f"INTERNAL_NODE_{i}" for i in range(n - 2)]
    root = Branch(leaves[0], leaves[1], instance[leaves[0]][leaves[1]], instance, queue_of_new_symbols)

    for leaf in leaves[2:]:
        root.add_node(leaf, instance[leaves[0]][leaf])
  
    adjacency_list = {
        leaves[0]: dict(),
    }

    root.fill_adjacency_list(adjacency_list)
    
    return adjacency_list

    

if __name__ == "__main__":
    instance = load_from_file("instance.json")
    adjacency_list = solve(instance)
    print(adjacency_list)

    
    