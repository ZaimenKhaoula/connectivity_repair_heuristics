import networkx as nx
from scipy.spatial import distance
import Outils
import time

def second_step_of_connectivity_repair(list_disjoints_neighbors, length, graph):

    terminals = []
    tree = nx.Graph()
    for s in list_disjoints_neighbors:
        terminals.append(Outils.get_most_centered_point_in_set_of_points(s, length))
    num_terminals = len(terminals)
    distance_between_terminals=[]
    for i in range(num_terminals):
        for j in range(i+1, num_terminals):
            pair=dict()
            pair['src']= terminals[i]
            pair['dest'] = terminals[j]
            pair['dis'] = distance.euclidean((terminals[i] // length, terminals[i] % length) , (terminals[j] // length, terminals[j] % length))
            pair['inserted']= False
            distance_between_terminals.append(pair)

    distance_between_terminals = sorted(distance_between_terminals, key=lambda d: d['dis'])
    inserted_terminals = []
    i = 0
    while distance_between_terminals[i]['src'] not in inserted_terminals or distance_between_terminals[i]['dest'] not in inserted_terminals:
        least_cost_path = nx.shortest_path(graph, source=distance_between_terminals[i]['src'], target=distance_between_terminals[i]['dest'])
        nx.add_path(tree, least_cost_path)
        if distance_between_terminals[i]['src'] not in inserted_terminals:
            inserted_terminals.append(distance_between_terminals[i]['src'])
        if distance_between_terminals[i]['dest'] not in inserted_terminals:
            inserted_terminals.append(distance_between_terminals[i]['dest'])
        distance_between_terminals[i]['inserted'] = True
        i =i+1
        if i==len(distance_between_terminals):
            break
    D = Outils.distinct_connected_components(tree)
    not_added_paths = [elem for elem in distance_between_terminals if elem['inserted'] == False]
    for elem in not_added_paths:
        if Outils.links_sets(elem['src'], elem['dest'], D):
            least_cost_path = nx.shortest_path(graph, source=elem['src'], target=elem['dest'])
            nx.add_path(tree, least_cost_path)
            if elem['src'] not in inserted_terminals:
                inserted_terminals.append(elem['src'])
            if elem['dest'] not in inserted_terminals:
                inserted_terminals.append(elem['dest'])
        D = Outils.distinct_connected_components(tree)
        if len(D) == 1:
            break
    borders = []
    for node in list(tree.nodes):
        if tree.degree(node) == 1:
            borders.append(node)
    removed_nodes=[]
    for b in borders:
        e =list(list(tree.edges(b))[0])
        while Outils.in_same_set(e[0], e[1], list_disjoints_neighbors):
            if b == e[0]:
                k = e[1]
            else:
                k = e[0]
            removed_nodes.append(e[0])
            removed_nodes.append(e[1])
            #tree.remove_edge(*e)
            if tree.degree(k) == 1:
                e = tree.edges(k)
            else:
                break
    return tree, removed_nodes

def connectivity_repair_heuristic(individual,M, length, graph):

    nb_deployed = individual.deployment.count(1)
    time_start = time.time()
    disjoint_sets = Outils.distinct_connected_components(individual.deployment_graph)
    #M = generate_list_connections_between_positions(zones, threshold)
    S = Outils.get_neighbors_positions_of_disjoints_connected_set(disjoint_sets, M)
    Outils.first_step_of_connectivity_repair(individual,disjoint_sets, M, S)
    steiner_tree, removed_nodes = second_step_of_connectivity_repair(S, length, graph)

    for i in list(set(steiner_tree.nodes)):
        if i not in removed_nodes:
            individual.deployment[i] = 1

    time_start = time.time() - time_start
    print("exec time  of short path based algorithm")
    print(time_start)
    print("number of added sensors using short path based algorithm")
    print(individual.deployment.count(1) - nb_deployed)
