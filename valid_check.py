import sys
from collections import defaultdict, deque

def read_tree(path: str) -> dict:
    adj = defaultdict(list)
    with open(path, 'r') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split()
                node = int(parts[0])
                neighbors = list(map(int, parts[1:]))
                for n in neighbors:
                    adj[node].append(n)
    return adj

def find_centers(adj: dict) -> list:
    n = len(adj)
    degree = {node: len(adj[node]) for node in adj}
    leaves = deque([node for node in adj if degree[node] <= 1])
    removed = 0

    while removed < n - 2:
        new_leaves = deque()
        for leaf in leaves:
            removed += 1
            for neighbor in adj[leaf]:
                degree[neighbor] -= 1
                if degree[neighbor] == 1:
                    new_leaves.append(neighbor)
        leaves = new_leaves

    return list(leaves)

def rooted_tree_coding(node: int, parent: int, adj: dict) -> str:
    labels = []
    for neighbor in adj[node]:
        if neighbor != parent:
            labels.append(rooted_tree_coding(neighbor, node, adj))
    labels.sort()
    return "(" + "".join(labels) + ")"

def canonical_form(adj: dict) -> str:
    centers = find_centers(adj)
    forms = [rooted_tree_coding(center, -1, adj) for center in centers]
    return min(forms)

def main():
    if len(sys.argv) != 3:
        print("Usage: python valid_check.py <tree1.txt> <tree2.txt>")
        sys.exit(1)

    tree1 = read_tree(sys.argv[1])
    tree2 = read_tree(sys.argv[2])

    canon1 = canonical_form(tree1)
    canon2 = canonical_form(tree2)

    print(str(canon1 == canon2).lower())

if __name__ == "__main__":
    main()
