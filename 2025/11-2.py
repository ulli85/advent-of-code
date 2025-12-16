from functools import reduce

lines = list(map(lambda l: l.split(': '), open('input/11.txt').read().splitlines()))
lines = list(map(lambda i: [i[0], tuple(i[1].split(' '))], lines))
network = {}
node_2_input_nodes = {}
node_2_path_count = {}


def init_data():
    """Initialize all data structures"""
    global network
    global node_2_input_nodes
    global node_2_path_count
    network = {k: v for k, v in lines}
    node_2_input_nodes = {k: v for k, v in zip(network.keys(), [[] for i in range(0, len(network.keys()))])}
    network['out'] = ()
    node_2_input_nodes['out'] = []

    for k in network.keys():
        keys = network[k]
        for j in keys:
            node_2_input_nodes[j] += [k]
    node_2_path_count = {k: v for k, v in zip(node_2_input_nodes, [0] * len(node_2_input_nodes))}


def get_root_nodes(_network):
    """Returns nodes without incoming edge (root nodes) """
    s = set(list(sum([_network[k] for k in _network.keys()], ())))
    k = set(_network.keys())
    tops = k.difference(s)
    return tops


def count_connections(root_node):
    """Count connections as sum of all input edges to root_node. Adjust dictionary node_2_path_count"""
    for edge in node_2_input_nodes[root_node]:
        conns = node_2_path_count[edge]
        node_2_path_count[root_node] += conns


def topological_sort_graph(start_node='svr', end_node='out', topological_sorted_graph=[]):
    """ A topological sort of all the nodes"""
    init_data()
    node_2_path_count[start_node] = 1

    if len(topological_sorted_graph) > 0:
        start_idx = topological_sorted_graph.index(start_node)
        for node_2_dispose in topological_sorted_graph[0:start_idx]:
            network.pop(node_2_dispose)
        end_idx = topological_sorted_graph.index(end_node)
        for node_2_dispose in topological_sorted_graph[end_idx + 1:]:
           network.pop(node_2_dispose)

    topological_sorted = []
    while True:
        tops = get_root_nodes(network)

        if len(tops) == 0:
            break

        topological_sorted += [*tops]

        for top in tops:
            network.pop(top)
            count_connections(top)
    return topological_sorted


graph = topological_sort_graph()
dac_index = graph.index('dac')
fft_index = graph.index('fft')
first_after_start = 'dac' if dac_index < fft_index else 'fft'
second_after_start = 'dac' if first_after_start == 'fft' else 'fft'

paths = []
topological_sort_graph('svr', first_after_start, graph)
paths += [node_2_path_count[first_after_start]]

topological_sort_graph(first_after_start, second_after_start, graph)
paths += [node_2_path_count[second_after_start]]

topological_sort_graph(second_after_start, 'out', graph)
paths += [node_2_path_count['out']]
# All possible path as multiplication of all paths between (svr->fft) * (fft->dac) * (dac->out)
print(reduce(lambda a, b: a * b, paths))
