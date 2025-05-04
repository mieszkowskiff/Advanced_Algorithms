
def read_graph(filename):
    """
    Reads the graph from file and stores as dictionary of dictionaries.
    Checks if edges are integers.
    """
    graph = {}
    seen_edges = set()

    with open(filename, 'r') as file:
        for line in file:
            u, v, w = line.strip().split()
            try:
                w_int = int(float(w))
                if float(w) != w_int or w_int <= 0:
                    print(f"Invalid edge weight (not a positive integer): {u} -> {v} = {w}")
                    return None
                if (u, v) in seen_edges or (v, u) in seen_edges:
                    continue
                if u not in graph:
                    graph[u] = {}
                if v not in graph:
                    graph[v] = {}
                graph[u][v] = w_int
                graph[v][u] = w_int
                seen_edges.add((u, v))
            except ValueError:
                print(f"Failed to parse edge weight: {line.strip()}")
                return None
    return graph


def read_instance(filename):
    """
    Reads required leaf-to-leaf distances.
    Checks if paths are integers.
    """
    required_distances = {}
    with open(filename, 'r') as file:
        for line in file:
            u, v, d = line.strip().split()
            try:
                d_int = int(float(d))
                if float(d) != d_int or d_int < 0:
                    print(f"Invalid path distance (not a non-negative integer): {u} -> {v} = {d}")
                    return None
                if u not in required_distances:
                    required_distances[u] = {}
                required_distances[u][v] = d_int
            except ValueError:
                print(f"Failed to parse distance: {line.strip()}")
                return None
    return required_distances

def bfs_distance(graph, start):
    """
    BFS for finding the path in a tree.
    """
    distances = {}
    # remembering the previous visited node would be sufficient
    visited = set()
    queue = [(start, 0)]

    while queue:
        node, dist = queue.pop(0)
        if node in visited:
            continue
        visited.add(node)
        # we could easily check if the node is a leaf and remeber 
        # distances only between leaf_nodes  
        distances[node] = dist
        for neighbor in graph[node]:
            if neighbor not in visited:
                queue.append((neighbor, dist + graph[node][neighbor]))
                
    return distances

def validate_solution(graph, leaf_nodes, required_distances):
    # technically we dont have to perform the bfs for the last leaf
    for leaf in leaf_nodes:
        computed = bfs_distance(graph, leaf)
        for other_leaf, required_dist in required_distances[leaf].items():
            actual = computed.get(other_leaf, float('inf'))
            if actual != required_dist:
                print(f"Distance mismatch: {leaf} -> {other_leaf} | Expected: {required_dist}, Got: {actual}")
                return False
    return True

dic_name = "./instances/"
solution_file = dic_name + "solution_found.txt"
instance_file = dic_name + "instance.txt"

graph = read_graph(solution_file)

if graph is None:
    print("Invalid solution file. Aborting.")
else:
    required_distances = read_instance(instance_file)

    if required_distances is None:
        print("Invalid instance file. Aborting.")
    else:
        leaf_nodes = required_distances.keys()
        if validate_solution(graph, leaf_nodes, required_distances):
            print("The solution satisfies all instance constraints.")
        else:
            print("The solution does NOT satisfy the instance constraints.")
