import networkx as nx
from scipy.spatial import distance,ConvexHull, convex_hull_plot_2d
import steiner_tree as st
import Outils
import time



def orc_heuristic(M, graph, list_disjoints_sets, length):

   terminals=[]
   for l in list_disjoints_sets:
       terminals.append(l[0])
   zones_positions=[]
   zones_positions_copie=[]
   for p in terminals:
       zones_positions.append((p // length, p % length))
   zones_positions_copie.extend(zones_positions)
   tree = nx.Graph()
   inserted_terminals = []
   num_terminals=len(list_disjoints_sets)
   while not st.check_terminals_connected(tree, num_terminals, len(inserted_terminals)):
       current_terminals = []
       hull = ConvexHull(zones_positions, incremental=False, qhull_options=None)
       boundary_nodes = []
       for v in hull.vertices:
           boundary_nodes.append((zones_positions[v][0]*length+zones_positions[v][1]))
       boundary_segments = []
       for p in boundary_nodes:
           index = Outils.index_list_of_list(p, list_disjoints_sets)
           if index != -1:
               if index not in boundary_segments:
                   boundary_segments.append(index)
                   inserted_terminals.append(list_disjoints_sets[index][0])
           current_terminals.append(p)
       lst_three_points = []
       i = 0
       if len(current_terminals) >= 3:
           while i + 2 < len(current_terminals):
               triple = []
               triple.append(current_terminals[i])
               triple.append(current_terminals[i + 1])
               triple.append(current_terminals[i + 2])
               lst_three_points.append(triple)
               i = i + 1
           triple = []
           triple.append(current_terminals[len(current_terminals) - 2])
           triple.append(current_terminals[len(current_terminals) - 1])
           triple.append(current_terminals[0])
           lst_three_points.append(triple)
           triple = []
           triple.append(current_terminals[len(current_terminals) - 1])
           triple.append(current_terminals[0])
           triple.append(current_terminals[1])
           lst_three_points.append(triple)
           zones_positions = [zone for zone in zones_positions if zone[0] * length + zone[1] not in current_terminals]
           removed_points=[]
           removed_points.clear()
           for t in lst_three_points:
               steiner = Outils.steiner_tree(graph,t, M)
               steiner_point = Outils.steiner_point(t, steiner, length)
               current_terminals.append(steiner_point)
               zones_positions.append((steiner_point // length, steiner_point % length))
               for e in steiner.edges:
                   tree.add_edge(*e)
           zones_positions = list(set(zones_positions))

       else:
           steiner = Outils.steiner_tree(graph, current_terminals)
           for e in steiner.edges:
               tree.add_edge(*e)

   return tree


def connectivity_repair(metric, graph, individual, length):
    nb_deployed = individual.deployment.count(1)
    time_start =time.time()
    disjoint_sets = Outils.distinct_connected_components(individual.deployment_graph)
    steiner_tree = orc_heuristic(metric, graph, disjoint_sets, length)
    for i in list(set(steiner_tree.nodes)):
        individual.deployment[i] = 1
    time_start = time.time() - time_start
    print("exec time  of orc ")
    print(time_start)
    print()

    print("number of added sensors using orc")
    print(individual.deployment.count(1) - nb_deployed)

