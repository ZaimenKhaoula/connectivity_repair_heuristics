import numpy as np
import networkx as nx
import networkx.algorithms.components as comp
import math
from scipy.spatial import distance
from networkx.utils import pairwise, not_implemented_for
from itertools import combinations, chain
import random


def compute_zones_positions(connections_between_positions, length):
    zones_positions = []
    for i in range(len(connections_between_positions)):
        zones_positions.append((i // length, i % length))
    return zones_positions


def get_most_centered_point_in_set_of_points(subset_of_zones, length):
    l = []
    for zone in subset_of_zones:
        c=[zone // length, zone % length]
        l.append(c)
    all_nodes =np.array(l)
    avg_dists = distance.squareform(distance.pdist(all_nodes)).mean(axis=1)
    m = list(all_nodes[avg_dists.argmin()])
    return m[0]*length+m[1]



def index_list_of_list(node,    D):
    i=0
    for l in list(D):
        if node in list(l):
            return i
        i=i+1
    return -1

def links_sets(node1, node2, D):

    return index_list_of_list(node1, D) != index_list_of_list(node2, D)

def check_connectivity(a,b, threshold, width):
    if distance.euclidean((a//width, a%width), (b//width, b%width))<=threshold:
        return True
    return False


def generate_list_connections_between_positions(nb_zones, threshold,length):
    l = [[] for x in range(nb_zones)]
    for i in range(nb_zones):
        for j in range(i + 1, nb_zones):
            if check_connectivity(i, j, threshold, length):
                l[i].append(j)
                l[j].append(i)

    return l


def generate_random_sensors_positions(length, nb_sensors):
    sensors_positions = []
    for i in range(nb_sensors):
        sensors_positions.append((random.randint(0,length), random.randint(0,length)))

def find_indices_of_deployed_sensors(individual):
    array = np.array(individual.deployment)
    indices = np.where(array == 1)[0]
    return list(indices)




def get_neighbors_positions_of_disjoints_connected_set(lst_disjoints_connected_set, lst_neighbors_per_zone):
    S = [[] for x in range(len(lst_disjoints_connected_set))]
    i=0
    for d in lst_disjoints_connected_set:
        s = []
        for p in d:
            s.extend(lst_neighbors_per_zone[p])
            s = [elem for elem in s if elem not in d]
        S[i] = list(set(s))
        i = i+1
    return S



def index_of(a, lst):
    for i in range(0, len(lst)):
        if lst[i] == a:
            return i
    return -1

def highest_occurence(lst):
    return max(lst, key=lst.count)

def metric_closure (G, weight='weight'):

    M = nx.Graph()
    Gnodes = set(G)

    # check for connected graph while processing first node
    all_paths_iter = nx.all_pairs_dijkstra(G, weight=weight)
    u, (distance, path) = next(all_paths_iter)
    if Gnodes - set(distance):
        msg = "G is not a connected graph. metric_closure is not defined."
        raise nx.NetworkXError(msg)
    Gnodes.remove(u)
    for v in Gnodes:
        M.add_edge(u, v, distance=distance[v], path=path[v])

    # first node done -- now process the rest
    for u, (distance, path) in all_paths_iter:
        Gnodes.remove(u)
        for v in Gnodes:
            M.add_edge(u, v, distance=distance[v], path=path[v])

    return M


def first_step_of_connectivity_repair(individual, disjoint_sets, lst_neighbors_per_zone, lst_neighbors_per_set):

    cont = True
    while cont:
        P = []
        for s in lst_neighbors_per_set:
            P = P + s
        l = highest_occurence(P)
        if l > 1:
            individual.deployment[l]=1
            merged_set = []
            merged_neighbors = []
            lis_index = []
            for i in range(0, len(lst_neighbors_per_set)):
                ind = index_of(l, lst_neighbors_per_set[i])
                if ind != -1:
                    lis_index.append(i)
            for k in lis_index:
                merged_set = merged_set + disjoint_sets[k]
                merged_neighbors.extend((lst_neighbors_per_set[k]))



            for k in reversed(lis_index):
                disjoint_sets.pop(k)
                lst_neighbors_per_set.pop(k)

            merged_set.append(l)
            disjoint_sets.append(merged_set)
            merged_neighbors.extend(lst_neighbors_per_zone[l])
            merged_neighbors = list(set(merged_neighbors))
            merged_neighbors.remove(l)
            lst_neighbors_per_set.append(merged_neighbors)
        else:
            cont = False



def steiner_tree(G, terminal_nodes, M):

    """ Return an approximation to the minimum Steiner tree of a graph.

    Parameters
    ----------
    G : NetworkX graph

    terminal_nodes : list
         A list of terminal nodes for which minimum steiner tree is
         to be found.

    Returns
    -------
    NetworkX graph
        Approximation to the minimum steiner tree of `G` induced by
        `terminal_nodes` .

    Notes
    -----
    Steiner tree can be approximated by computing the minimum spanning
    tree of the subgraph of the metric closure of the graph induced by the
    terminal nodes, where the metric closure of *G* is the complete graph in
    which each edge is weighted by the shortest path distance between the
    nodes in *G* .
    This algorithm produces a tree whose weight is within a (2 - (2 / t))
    factor of the weight of the optimal Steiner tree where *t* is number of
    terminal nodes.

    """
    # M is the subgraph of the metric closure induced by the terminal nodes of
    # G.

    # Use the 'distance' attribute of each edge provided by the metric closure
    # graph.
    H = M.subgraph(terminal_nodes)
    mst_edges = nx.minimum_spanning_edges(H, weight='distance', data=True)
    # Create an iterator over each edge in each shortest path; repeats are okay
    edges = chain.from_iterable(pairwise(d['path']) for u, v, d in mst_edges)
    T = G.edge_subgraph(edges)

    return T




def steiner_point(t, steiner_stree,length):
    dist = math.inf
    sp= None
    t1=(t[0] // length, t[0]%length )
    t2= (t[1] // length, t[1]%length )
    t3= (t[2] // length, t[2]%length )
    x= (t1[0]+ t2[0]+ t3[0]) / 3
    y= (t1[1]+ t2[1]+ t3[1]) / 3

    for e in list(steiner_stree.nodes):
        if distance.euclidean((x,y),(e // length, e% length)) < dist:
            sp = e

    return sp

def create_graph(connections_between_positions):
    graph = nx.Graph()
    i = 0
    for zones in connections_between_positions:
        for j in zones:
            if not graph.has_edge(i, j):
                graph.add_edge(i, j)
        i = i + 1
    return graph


def distinct_connected_components(graph):
    connected_nodes = []
    for connected_set in list(comp.connected_components(graph)):
        connected_nodes.append(list(connected_set))

    return connected_nodes


def in_same_set(node1, node2, list_disjoints_neighbors):
    ind = index_list_of_list(node1, list_disjoints_neighbors)
    if ind !=-1:
        return ind == index_list_of_list(node2, list_disjoints_neighbors)
    else:
        return False

