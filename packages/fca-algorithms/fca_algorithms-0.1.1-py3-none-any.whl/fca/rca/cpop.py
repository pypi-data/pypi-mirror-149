"""Closed partially-ordered patterns impl
"""
from collections import deque
from .rca import lattice_and_concept_idx


def get_index_offsets(lattices):
    lattice_idx_offsets = [0]  # lattice 0 has 0 offset
    for idx in len(len(lattices) - 1):
        lattice_idx_offsets.append(lattice_idx_offsets[-1] + len(lattices[idx].concepts))
    return lattice_idx_offsets


def create_cpop(lattices):
    """Returns a graph with the cpop.
    Note that indexes in the graph will always be `idx - previous_lattice_last_index`
    """
    lattice_idx_offsets = get_index_offsets(lattices)
    graph = create_graph(lattices, lattice_idx_offsets)
    # at this point, graph contains all the lattices unconected between them
    create_relational_edges(graph, lattices, lattice_idx_offsets)
    # here the graph is completed in the sense that its relational edges has already been added
    return graph


def get_subgraph_from_concept(graph, concept_idx) -> set:
    nodes_in_connected_component = set([concept_idx])
    visited = set()
    q = deque([concept_idx])
    while q:
        u = q.popleft()
        visited.add(u)
        for v, is_relational in graph[u]:
            if v not in visited and is_relational:
                nodes_in_connected_component.add(v)
                q.append(v)
    return nodes_in_connected_component


def create_graph(lattices, idx_offsets):
    graph_so_far = []
    for i, lattice in enumerate(lattices):
        for neighbours in lattice.hasse:
            # Edges are (node, bool) where bool is False if the edge is not relational and True otherwise
            # offset all neighbours
            graph_so_far.append([(idx_offsets[i] + neighbour, False) for neighbour in neighbours])
    return graph_so_far


def create_relational_edges(graph, lattices, lattice_idx_offsets):
    for i, lattice in enumerate(lattices):
        for c_idx, concept in enumerate(lattice.concepts):
            idx_in_graph = lattice_idx_offsets[i] + c_idx
            for attr in concept.A:
                if is_attr_relational(attr):
                    i_related, j = lattice_and_concept_idx(attr)
                    concept_idx_related = lattice_idx_offsets[i_related] + j
                    graph[concept_idx_related].append((concept_idx_related, True))  # These are always relational


def is_attr_relational(attr):
    return ':' in attr  # this can be highly improved


def is_edge_relational(edge):
    return edge[1]
