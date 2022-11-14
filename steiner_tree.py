import networkx as nx
import networkx.algorithms.components as comp


def get_paths(graph,source,target):
    return list(nx.all_simple_paths(graph,source,target))


def get_path_cost(path):
    cost = 0
    for node in path:
        cost=cost+1
    return cost


def get_least_cost_path(graph,paths):
    min_cost_path = None
    min_cost = float("inf")
    for path in paths:
        cost = get_path_cost(graph, path)
        if cost < min_cost:
            min_cost = cost
            min_cost_path = path
    return min_cost_path,min_cost


def check_terminals_connected(tree, nb_insetred_terminals, nb_terminals):
    return len(list(comp.connected_components(tree)))==1 and nb_insetred_terminals==nb_terminals



def search_least_cost_paths(graph, terminal1, terminal2):
    print((terminal1, terminal2))
    paths = get_paths(graph, terminal1, terminal2)
    least_cost_path, least_cost = get_least_cost_path(graph, paths)
    print(least_cost_path)
    path = dict()
    path['cost'] = least_cost
    path['path'] = least_cost_path
    path['src'] = terminal1
    path['dest'] = terminal2
    print
    "Path" + str(path['path'])
    print((terminal1, terminal2))
    return path

"""

def approximate_steiner(disjoint_sets,connections_between_positions, terminals):
    graph = nx.Graph()
    i=0
    for zones in connections_between_positions:
        for j in zones:
            if not graph.has_edge(i,j):
                graph.add_edge(i,j)
        i=i+1
    print("graph generated")
    print(nx.is_connected(graph))
    plt.figure()
    nx.draw(graph, with_labels=True)
    plt.show()
    steiner_tree = nx.Graph()
    print("list of terminals")
    print(terminals)
    num_terminals = len(terminals)
    all_terminal_paths = list()
    items=[]
    for i in range(0,num_terminals):
        for j in range(i+1,num_terminals):
            print("terminal i and j")
            items.append((graph,terminals[i], terminals[j]))
    print("create pool")
    pool = Pool(cpu_count())
    for result in pool.starmap(search_least_cost_paths, items):
        all_terminal_paths.append(result)
    pool.close()
    print("create pool")
    inserted_terminals=[]
    all_terminal_paths.sort(key=lambda x:x['cost'])

    for t_path in all_terminal_paths:
        nx.add_path(steiner_tree, t_path['path'])
        inserted_terminals.append(t_path['src'])
        inserted_terminals.append(t_path['dest'])
        if check_terminals_connected(steiner_tree,len(set(inserted_terminals)),num_terminals):
            break
         
    conn_components = list(comp.connected_components(steiner_tree))
    while len(conn_components) > 1:
        print('enter while conn components')
        comp1 = list(conn_components[0])
        comp2 = list(conn_components[1])
        for j in range(0,len(comp1)):
            for k in range(0,len(comp2)):
                if graph.has_edge(comp1[j],comp2[k]):
                    steiner_tree.add_edge(comp1[j],comp2[k])
                    break
   
    while True:
        try:
            cycle = nx.find_cycle(steiner_tree)
            edge = cycle[0]
            steiner_tree.remove_edge(edge[0],edge[1])
        except:
            break
    
    weights = nx.get_node_attributes(graph,'weight')
    steiner_cost = 0
    for node in list(steiner_tree.nodes):
        steiner_cost = steiner_cost + weights[node]

    return steiner_tree   
"""