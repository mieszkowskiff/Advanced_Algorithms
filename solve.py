from create_instances import load_from_file


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

    def print(self, depth=0, index = ""):
        indent = "\t" * depth
        if index != "":
            index = f"{index}: "
        print(f"{indent}{index}Branch(\n{indent}\tstart_node={self.start_node},", end="") 
        print(f"end_node={self.end_node}, length={self.length}\n{indent}\tchildren: \n", end="")
        for distance, child in self.children.items():
            child.print(depth = depth + 1, index = distance)
        print(f"{indent})")
        
        







    

def solve(instance: dict[int: dict[int: int]]) -> dict[int: dict[int: int]]:
    """
    # Recreates the tree from the distance matrix between leaf nodes.
    """

    n = len(instance)
    if n in [0, 1, 2]:
        return instance
    
    leaves = list(instance.keys())

    queue_of_new_symbols = [i for i in range(100, 200)]
    root = Branch(leaves[0], leaves[1], instance[leaves[0]][leaves[1]], instance, queue_of_new_symbols)
    root.print()
    print("-" * 30)
    for leaf in leaves[2:]:
        root.add_node(leaf, instance[leaves[0]][leaf])
        root.print()
        print("-" * 30)
    

if __name__ == "__main__":
    instance = load_from_file("instance.json")
    solve(instance)

    
    