from Individual import Individual
import Outils
import time
import Connectivity_repair_ST as st
import Connectivity_repair_SP as sp
import ORC as orc

"""
For our tests, we have fixed the variable 'length' to X (X=80, 100, 120) for areas of (80x80 m2, 100x100 m2, 120x120 mm2) respectively
"""


def create_individual_and_fill_deployment(sensors_positions, length):
    ind = Individual(length*length)
    for l in sensors_positions:
        ind.deployment[l[0] * length + l[1]] = 1

    return ind


#This variable represents the number of sensors deployed in the deployment area, it is fixed randomly

nb_sensors = None
length = 80  # for the first scenario (area = 80x80 m2)
nb_zones = length * length
threshold = 7 # communication threshold, it represents communication range of sensors

"""
sensors positions are generated randomly in the deployment area.
For each scenario, we have adjusted the sensors positions to have the prefixed number of segments. (prefixed sengments 
number for our tests are 5, 8, 10, 13).

The considered scenarios in our tests are :

|-----------------------------------------|
|deployment area size|  Number of segments|  
|-----------------------------------------|  
|     80X80          |   5                |  
|-----------------------------------------|  
|     80X80          |    8               |  
|-----------------------------------------|  
|     80X80          |    10              |  
|-----------------------------------------|  
|     80X80          |    13              |  
|-----------------------------------------|  
|     100x100        |    5               |  
|-----------------------------------------|  
|     100x100        |     8              |  
|-----------------------------------------|  
|     100x100        |     10             |  
|-----------------------------------------|  
|     100x100        |     13             |  
|-----------------------------------------|  
|     120x120        |     5              |  
|-----------------------------------------|
|     120x120        |     8              |  
|-----------------------------------------|
|     120x120        |     10             |  
|-----------------------------------------|
|     120x120        |     13             |  
|-----------------------------------------|  

"""
sensors_positions= Outils.generate_random_sensors_positions(length, nb_sensors)
M = Outils.generate_list_connections_between_positions(nb_zones, threshold, length)
start=time.time()
graph = Outils.create_graph(M)
metric = Outils.metric_closure(graph, weight='weight')
print("time required to generate graph and metric closure for the current scenario is")
print(time.time()-start)

ind1 = create_individual_and_fill_deployment(sensors_positions, length)
ind2 = create_individual_and_fill_deployment(sensors_positions, length)
ind3 = create_individual_and_fill_deployment(sensors_positions, length)

ind1.create_deployment_graph(threshold, length)
ind2.create_deployment_graph(threshold, length)
ind3.create_deployment_graph(threshold, length)


sp.connectivity_repair_heuristic(ind1,M, length, graph)
st.connectivity_repair_heuristic(ind2,M, length, graph, metric)
orc.connectivity_repair(metric,graph,ind3,length)

