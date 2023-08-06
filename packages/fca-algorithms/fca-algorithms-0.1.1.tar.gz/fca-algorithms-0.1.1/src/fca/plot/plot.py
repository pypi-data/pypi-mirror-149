import networkx as nx
from collections import deque

from ..border_hasse import calculate_hasse
from matplotlib import pyplot as plt


def plot_from_hasse(hasse, concepts_by_id, show_plot=True, save_plot : str=None):
    G = nx.DiGraph()
    for u in range(len(hasse)):
        G.add_node(to_node(u, concepts_by_id))

    for u in range(len(hasse)):
        for w in hasse[u]:
            G.add_edge(to_node(u, concepts_by_id), to_node(w, concepts_by_id))
    
    pos = dict()
    distances, diameter = _compute_distances(hasse, from_node=len(hasse) - 1)
    middle = diameter / 2
    for i in range(len(distances)):
        level_i_len = len(distances[i])
        new_middle = level_i_len / 2
        for idx, node in enumerate(distances[i]):
            horizontal_position = idx / level_i_len
            pos[to_node(node, concepts_by_id)] = (horizontal_position * level_i_len - new_middle, i)
    
    pos[to_node(0, concepts_by_id)] = (pos[to_node(len(hasse) - 1, concepts_by_id)][0],
                                       len(distances) + (1 if len(distances[-1]) == 0 else 0))

    nx.draw_networkx_edges(G, pos, edge_color='blue', arrowsize=13, width=1.3)
    nx.draw_networkx_labels(G, pos, font_weight='bold')
    # plt.savefig('this.png')
    if show_plot:
        plt.show()

    if save_plot:
        nx.nx_pydot.write_dot(G, save_plot if save_plot.endswith(".dot") else f"{save_plot}.dot")


def _compute_distances(hasse, from_node=0):
    distances = [None for _ in range(len(hasse))]
    distances[from_node] = 0
    queue = deque([from_node])
    maximum_distance = 0
    while queue:
        u = queue.popleft()
        for w in hasse[u]:
            if distances[w] is None:
                distances[w] = distances[u] + 1
                maximum_distance = max(maximum_distance, distances[w])
                queue.append(w)
    res_distances = [[] for _ in range(maximum_distance + 1)]
    diameter = 0
    for node in range(len(hasse)):
        res_distances[distances[node]].append(node)
        diameter = max(diameter, len(res_distances[distances[node]]))
    return res_distances, diameter

def to_node(u, concepts_by_id):
    return str(concepts_by_id[u])
