class Node:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
    
    def get_depth(self):
        depth = 0
        curr = self
        while curr.parent != None:
            curr = curr.parent
            depth += 1
        return depth

    def get_parents(self):
        depth = 0
        parents = {}
        curr = self
        while curr.parent != None:
            curr = curr.parent
            parents[curr.name] = depth
            depth += 1
        return parents

# IO
a = [x.split(")") for x in open("input.txt").read().split("\n") if x and x[0]]
connections = { x[1]:x[0] for x in a}
orbited = set(connections.keys())
orbiting = set(connections.values())
nodes = {name : Node(name, None) for name in orbited | orbiting}
for n in nodes.values():
    parent_name = connections.get(n.name, None)
    if parent_name:
        n.parent = nodes[parent_name]


# 1st 
print(sum(n.get_depth() for n in nodes.values()))

# 2nd
you_parents = nodes["YOU"].get_parents()
san_parents = nodes["SAN"].get_parents()
shared_parents = [par for par in you_parents if par in set(you_parents.keys()) & set(san_parents.keys())]
closest = min(shared_parents, key=lambda n: you_parents[n])
dist = you_parents[closest] + san_parents[closest]
print(dist)