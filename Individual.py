import Outils
import numpy as np
import networkx as nx


class Individual:

    def __init__(self,nb_zones):
        self.deployment = [0] * nb_zones
        self.deployment_graph = []
        self.adjacency = []


    def create_deployment_graph(self, threshold, width):
        self.generate_adjacency_matrix(threshold, width)
        index_of_deployed_sensors = [i for i in range(len(self.deployment)) if self.deployment[i] == 1]
        self.deployment_graph = nx.Graph()
        for i in index_of_deployed_sensors:
            self.deployment_graph.add_node(i)
        for i in range(len(index_of_deployed_sensors)):
            for j in range(i + 1, len(index_of_deployed_sensors)):
                if self.adjacency[i][j] == 1:
                    self.deployment_graph.add_edge(list(self.deployment_graph.nodes)[i], list(self.deployment_graph.nodes)[j])


    def generate_adjacency_matrix(self, threshold, width):
        index_of_deployed_sensors= [i for i in range(len(self.deployment)) if self.deployment[i]==1]
        self.adjacency = np.zeros((len(index_of_deployed_sensors),len(index_of_deployed_sensors)), dtype=int)
        for i in range(len(index_of_deployed_sensors)):
            for j in range(i+1, len(index_of_deployed_sensors)):
                if Outils.check_connectivity(index_of_deployed_sensors[i], index_of_deployed_sensors[j], threshold, width):
                    self.adjacency[i][j]=1
