lines = list(map(lambda l: l.split(': '), open('input/11.txt').read().splitlines()))
lines = list(map(lambda i: [i[0], tuple(i[1].split(' '))], lines))
network = {k: v for k, v in lines}
edges = {k: v for k, v in zip (network.keys(), [[] for i in range(0, len(network.keys()))])}
edges['out'] = []


for k in network.keys():
    keys = network[k]
    for j in keys:
        edges[j] += [k]

print(edges)

node_2_path_count = {k: v for k, v in zip(edges, [0] * len(edges))}
node_2_path_count['svr'] = 1

def topological_sort_graph():
    """ A topological sort of all the nodes"""
    _network = {k: v for k, v in lines}
    _topological_sorted = []
    while True:
        s = set(list(sum([_network[k] for k in _network.keys()], ())))
        k = set(_network.keys())
        tops = k.difference(s)
        print(tops)

        if len(tops) == 0:
            break
        _topological_sorted += [*tops]
        for top in tops:
            _network.pop(top)
            for edge in edges[top]:
                conns = node_2_path_count[edge]
                node_2_path_count[top] += conns
    return _topological_sorted

topological_sorted = topological_sort_graph()

print(network)

key_2_cnt = {}

for node in topological_sorted:

    successors = network[node]


    # print(successors)

print(node_2_path_count)
print(topological_sorted)
print(topological_sorted.index('fft'))
print(topological_sorted.index('dac'))

# 1 Find all nodes that do not have ancestors.
# 2 Put them into the resulting array.
# 3 Remove them from the graph.
# 4 Repeat until there are nodes in the graph.
# 5 If no nodes without ancestors exist, but there are still nodes in the graph, then there are cycles.


# Do a topological sort of all the nodes
#
# Set 'number of ways to reach' for whichever device we are counting from to 1, everything else to 0
#
# Go through devices in topological order, for each outgoing connection from current device a -> b increment 'number of ways to reach' for b by the value for a
#
# after we went through all the devices each has number of ways to reach it from initial one.
#
# For part 1 we do it from 'you' and check the value on 'out'
#
# For part 2 we do it for svr (get values for dac and fft), fft (dac, out), dac (fft,out) and multiply + add
#
# On the other hand we just are replacing DFS+Memo by topo sort (which guarantees we don't ever need to backtrack during DFS, so it just turns into iteration)


# edges = {k: v for k, v in zip([[x] * len(network[x]) for x in network.keys()], [network[y] for y in network.keys()])}

# print(edges)


# L ← Empty list that will contain the sorted elements
# S ← Set of all nodes with no incoming edge
#
#
# while S is not empty do
#     remove a node n from S
#     add n to L
#     for each node m with an edge e from n to m do
#         remove edge e from the graph
#         if m has no other incoming edges then
#             insert m into S
#
# if graph has edges then
#     return error   (graph has at least one cycle)
# else
#     return L   (a topologically sorted order)
