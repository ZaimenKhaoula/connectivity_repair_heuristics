import Outils
import time

def second_step_of_connectivity_repair(list_disjoints_neighbors,length, graph, metric):
    terminals = []
    for s in list_disjoints_neighbors:
        terminals.append(Outils.get_most_centered_point_in_set_of_points(s, length))
    steiner = Outils.steiner_tree(graph, terminals, metric)
    borders = []
    for node in list(steiner.nodes):
        if steiner.degree(node) == 1:
            borders.append(node)
    removed_nodes=[]
    for b in borders:
        e =list(list(steiner.edges(b))[0])
        while Outils.in_same_set(e[0], e[1], list_disjoints_neighbors):
            if b == e[0]:
                k = e[1]
            else:
                k = e[0]
            removed_nodes.append(e[0])
            removed_nodes.append(e[1])
            #steiner.remove_edges_from([e])
            if steiner.degree(k) == 1:
                e = steiner.edges(k)
            else:
                break
    return steiner, removed_nodes



def connectivity_repair_heuristic(individual, M, length, graph, metric):
    nb_deployed = individual.deployment.count(1)
    time_start = time.time()
    disjoint_sets = Outils.distinct_connected_components(individual.deployment_graph)
    #M = generate_list_connections_between_positions(zones, threshold)
    S = Outils.get_neighbors_positions_of_disjoints_connected_set(disjoint_sets, M)
    Outils.first_step_of_connectivity_repair(individual,disjoint_sets, M, S)
    steiner_tree, removed_nodes = second_step_of_connectivity_repair(S,length , graph, metric)
    for i in list(set(steiner_tree.nodes)) :
        if i not in removed_nodes:
            individual.deployment[i] = 1

    time_start = time.time() - time_start
    print("exec time  of steiner tree based method")
    print(time_start)
    print()
    print()

    print("number of added sensors using steiner tree")
    print(individual.deployment.count(1) - nb_deployed)

