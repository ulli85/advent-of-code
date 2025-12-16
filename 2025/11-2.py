from functools import reduce

lines = list(map(lambda l: l.split(': '), open('input/11.txt').read().splitlines()))
lines = list(map(lambda i: [i[0], tuple(i[1].split(' '))], lines))
node_2_outputs = {}
node_2_inputs = {}
node_2_path_count = {}


def init_data():
    """Initialize all data structures"""
    global node_2_outputs
    global node_2_inputs
    global node_2_path_count
    node_2_outputs = {k: v for k, v in lines}
    node_2_outputs['out'] = ()
    node_2_inputs = {k: v for k, v in zip(node_2_outputs.keys(), [[] for i in range(0, len(node_2_outputs.keys()))])}
    node_2_inputs['out'] = []

    for input in node_2_outputs.keys():
        outputs = node_2_outputs[input]
        for output in outputs:
            node_2_inputs[output] += [input]
    node_2_path_count = {k: v for k, v in zip(node_2_inputs, [0] * len(node_2_inputs))}


def get_root_nodes(_network):
    """Returns nodes without incoming edge (root nodes) """
    s = set(list(sum([_network[k] for k in _network.keys()], ())))
    k = set(_network.keys())
    roots = k.difference(s)
    return roots


def count_connections(root_node):
    """Count connections as sum of all input edges to root_node. Adjust dictionary node_2_path_count"""
    for edge in node_2_inputs[root_node]:
        conns = node_2_path_count[edge]
        node_2_path_count[root_node] += conns


def cut_off_nodes_not_between_inclusive(start_node, end_node, topologically_sorted_nodes):
    """Cut off all nodes from graph not between start_node and end_node. start_node and end_node are not cut off."""
    start_idx = topologically_sorted_nodes.index(start_node)
    for node_2_dispose in topologically_sorted_nodes[0:start_idx]:
        node_2_outputs.pop(node_2_dispose)
    end_idx = topologically_sorted_nodes.index(end_node)
    for node_2_dispose in topologically_sorted_nodes[end_idx + 1:]:
        node_2_outputs.pop(node_2_dispose)


def topological_sort_graph(start_node, end_node, topologically_sorted_nodes=[]):
    """ A topological sort of all the nodes"""
    init_data()
    node_2_path_count[start_node] = 1

    if len(topologically_sorted_nodes) > 0:
        cut_off_nodes_not_between_inclusive(start_node, end_node, topologically_sorted_nodes)


    topological_sorted = []
    roots = get_root_nodes(node_2_outputs)
    while roots:
        topological_sorted += [*roots]

        for root in roots:
            node_2_outputs.pop(root)
            count_connections(root)
        roots = get_root_nodes(node_2_outputs)
    return topological_sorted


topological_sorted_nodes = topological_sort_graph('svr', 'out')
dac_index = topological_sorted_nodes.index('dac')
fft_index = topological_sorted_nodes.index('fft')
first_after_start = 'dac' if dac_index < fft_index else 'fft'
second_after_start = 'dac' if first_after_start == 'fft' else 'fft'

paths = []
topological_sort_graph('svr', first_after_start, topological_sorted_nodes)
paths += [node_2_path_count[first_after_start]]

topological_sort_graph(first_after_start, second_after_start, topological_sorted_nodes)
paths += [node_2_path_count[second_after_start]]

topological_sort_graph(second_after_start, 'out', topological_sorted_nodes)
paths += [node_2_path_count['out']]
# All possible path as multiplication of all paths between (svr->fft) * (fft->dac) * (dac->out)
print(reduce(lambda a, b: a * b, paths))
