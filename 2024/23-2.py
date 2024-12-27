from collections import defaultdict

input = [str(x) for x in open("input/23-1.txt").read().splitlines()]
G = defaultdict(set)
C1 = []

def bors_kerbosch_v1(R, P, X, G, C):
    if len(P) == 0 and len(X) == 0:
        if len(R) > 2:
            C.append(sorted(R))
        return

    for v in P.union(set([])):
        bors_kerbosch_v1(R.union(set([v])), P.intersection(G[v]), X.intersection(G[v]), G, C)
        P.remove(v)
        X.add(v)

def add_edge(src: str, dst: str):
    G[src].add(dst)

# build graph
for edge in input:
    pcs = edge.split('-')
    for pc1, pc2 in [[pcs[0], pcs[1]], [pcs[1], pcs[0]]]:
        add_edge(pc1, pc2)
        add_edge(pc2, pc1)

bors_kerbosch_v1(set([]), set(G.keys()), set([]), G, C1)
max_i = C1.index(max(C1, key=len))
max_clique = sorted(C1[max_i])
print(','.join(max_clique))