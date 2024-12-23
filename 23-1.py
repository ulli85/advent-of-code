edges = [str(x) for x in open("input/23-1.txt").read().splitlines()]
pcnm = set()
sets = {}
uniques = set()
triplets = []


def add_edge(pc1: str, pc2: str):
    if pc1 not in pcnm:
        sets[pc1] = {pc2}
        pcnm.add(pc1)
    else:
        sets[pc1].add(pc2)


def add_triplet(triplet: [str]):
    triplet.sort()
    if len(list(filter(lambda x: x.startswith('t'), triplet))) > 0:
        unique = ''.join(triplet)
        if unique not in uniques:  # only triplets with t
            triplets.append(triplet)
            uniques.add(unique)


# make set for each pc
for edge in edges:
    pcs = edge.split('-')
    for pc1, pc2 in [[pcs[0], pcs[1]], [pcs[1], pcs[0]]]:
        add_edge(pc1, pc2)
        add_edge(pc2, pc1)

components = []
uniques = set()
for pc1 in sets.keys():
    for pc2 in sets[pc1]:
        if pc1 != pc2:
            for pc3 in sets[pc2]:
                if pc3 != pc1 and pc3 != pc2 and pc3 in sets[pc1]:
                    add_triplet([pc1, pc2, pc3])


print(f'tr{triplets}')
print(len(triplets))
