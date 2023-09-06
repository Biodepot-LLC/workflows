import json
import sys

def add_item(tree, parts):
    node = tree
    for part in parts:
        node = node.setdefault(part, {})

def list_to_tree(paths):
    tree = {}
    for path in paths:
        parts = path.split('/')
        add_item(tree, parts)
    return tree

if __name__ == "__main__":
    paths = [line.strip() for line in sys.stdin]
    tree = list_to_tree(paths)
    print(json.dumps(tree, indent=2))