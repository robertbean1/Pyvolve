from Topology import random_topology, Node, Structure
import Topology.backend as T
import Network.backend as N
from Network import FeedForwardNetwork
import random, time, copy

class Genome:
    def __init__(self, inputs, outputs, nodes_bound=3, layers_bound=3, weights_mode='nonzero', biases_mode='nonzero', connection_density=0.5, hidden_func='sigmoid', output_func='sigmoid', randomized=True):

        self.configs = (inputs, outputs, nodes_bound, layers_bound, weights_mode, biases_mode, connection_density, hidden_func, output_func)
        
        self.inputs = inputs
        self.outputs = outputs

        if randomized:
            self.genes = self.random(nodes_bound, layers_bound, weights_mode, biases_mode, connection_density, hidden_func, output_func)
        
    def random(self, nodes_bound=3, layers_bound=3, weights_mode='nonzero', biases_mode='nonzero', connection_density=0.5, hidden_func='sigmoid', output_func='sigmoid'):
        self.structure = random_topology(self.inputs, self.outputs, nodes_bound, layers_bound, connection_density, hidden_func, output_func)
        self.topology = self.structure.active_connections
        self.weights = T.random_weights(self.topology, weights_mode)
        self.biases = {node:bias for node, bias in zip(self.structure.nodes, T.random_biases(self.structure, biases_mode))}
        self.disabled_genes = []
        self.n_nodes = max([conn[0].number for conn in self.topology] + [conn[1].number for conn in self.topology])
        return list(zip(self.topology, self.weights))

    def mutate_add_node(self):
        split = random.choice(list(enumerate(self.genes)))
        (node1, node2), weight = split[1]
        del self.genes[split[0]]
        
        new_layer = 'Inbetween(' + node1.layer + '-' + node2.layer + ')'

        new_node = Node(node2.number, new_layer)
        new_node.activate()
        
        n = 0
        for node in self.sort_nodes():
            if node == node2:
                n = 1
            node.number += n
        
        self.structure.layers.append(new_layer)

        self.structure.nodes.append(new_node)
        
        self.structure.connections.append([node1, new_node])
        self.structure.connections.append([new_node, node2])

        for n, conn in enumerate(self.structure.active_connections):
            if conn == [node1, node2]:
                del self.structure.active_connections[n]

        for n, gene in enumerate(self.genes):
            conn = gene[0]
            if conn == [node1, node2]:
                del self.genes[n]
        
        self.biases[new_node] = 0

        self.structure.active_connections.append([node1, new_node])
        self.structure.active_connections.append([new_node, node2])
        
        self.genes.insert(split[0], [[new_node, node2], weight])
        self.genes.insert(split[0], [[node1, new_node], 1])

        self.topology = list(zip(*self.genes))[0]
        self.weights = list(zip(*self.genes))[1]

        self.disabled_genes.append([[node1, node2], weight])

    def mutate_add_connection(self, stop_search_threshold=20):

        def __mac(_i=0):
            layers = [v for _, v in self.sort_layers().items()]
            layer1 = random.choice(list(enumerate(layers[:len(layers)-1]))) #Choices between Inputs to Outputs, excluding Outputs
            layer2 = random.choice(layers[layer1[0]+1:]) #Choices between layer1 and Outputs, including Outputs

            layer1 = layer1[1]
            
            node1 = random.choice(layer1)
            node2 = random.choice(layer2)

            if not [node1, node2] in self.structure.active_connections:
                self.structure.connections.append([node1, node2])
                if node1.is_active and node2.is_active:
                    self.structure.active_connections.append([node1, node2])
                    self.genes.append([[node1, node2], random.uniform(-2.718, 2.718)])
                    self.topology = list(zip(*self.genes))[0]
                    self.weights = list(zip(*self.genes))[1]

            elif _i < stop_search_threshold:
               __mac(_i+1)

        __mac()

    def mutate_weight(self, max_sub=0.1, max_add=0.1):
        n = random.randint(0, len(self.genes)-1)
        self.genes[n] = list(self.genes[n])
        self.genes[n][1] = self.genes[n][1] + random.uniform(max_sub, max_add)

    def mutate_bias(self, max_sub=0.1, max_add=0.1):
        subject_node = random.choice(tuple(self.biases))
        self.biases[subject_node] = self.biases[subject_node] + random.uniform(max_sub, max_add)

    def sort_nodes(self):
        return sorted(self.structure.nodes, key=lambda x: x.number)

    def sort_layers(self):
        layers = {}
        for node in self.sort_nodes():
            if not node.layer in layers:
                layers[node.layer] = [node]
            else:
                layers[node.layer].append(node)
        return layers

class Genepool:
    def __init__(self):
        self.innovation_number = 0
        self.genes = None
        self.innovation_table = None
    
    def package_genomes(self, genomes):
        self.genes = set()
        self.innovation_table = {}
        for genome in genomes:
            for conn, weight in genome.genes:
                self.genes.add((tuple(conn), True))
            for conn, weight in genome.disabled_genes:
                self.genes.add((tuple(conn), False))
        
        for n, gene in enumerate(self.genes):
            self.innovation_table[gene] = n

        self.innovation_number += len(self.genes)
    
    def breakdown(self, genome):
        marking_list = []
        for gene in genome.genes:
            conn, weight = gene
            if (tuple(conn), True) in self.innovation_table:
                marking_list.append([conn, weight, self.innovation_table[(tuple(conn), True)]])
            else:
                marking_list.append([conn, weight, self.innovation_number])
                self.innovation_number += 1
        for gene in genome.disabled_genes:
            conn, weight = gene
            if (tuple(conn), False) in self.innovation_table:
                marking_list.append([conn, weight, self.innovation_table[(tuple(conn), False)]])
            else:
                marking_list.append([conn, weight, self.innovation_number])
                self.innovation_number += 1
        return marking_list

    def package_genome(self, genome):
        if not self.genes:
            self.genes = set()
            self.innovation_table = {}
        
        for conn, weight in genome.genes:
            if not (tuple(conn), True) in self.innovation_table:
                self.genes.add((tuple(conn), True))
                self.innovation_table[(tuple(conn), True)] = self.innovation_number
                self.innovation_number += 1
        
        for conn, weight in genome.disabled_genes:
            if not (tuple(conn), False) in self.innovation_table:
                self.genes.add((tuple(conn), False))
                self.innovation_table[(tuple(conn), False)] = self.innovation_number
                self.innovation_number += 1

    def compare_genomes(self, genome1, genome2):
        
        t_sim_table1 = {"disjoint":[], "excess":[], "matching":[]}
        t_sim_table2 = {"disjoint":[], "excess":[], "matching":[]}
        
        genes1 = self.breakdown(genome1)
        genes2 = self.breakdown(genome2)

        key=lambda x: x[2]
        genes1range = range(min(genes1, key=key)[2], max(genes1, key=key)[2]+1)
        genes2range = range(min(genes2, key=key)[2], max(genes2, key=key)[2]+1)

        for gene1, gene2 in zip(genes1, genes2):
            if gene1[2] == gene2[2]:
                t_sim_table1["matching"].append(gene1)
                t_sim_table2["matching"].append(gene2)
            else:
                if gene1 in genes2range:
                    t_sim_table1["disjoint"].append(gene1)
                else:
                    t_sim_table1["excess"].append(gene1)

                if gene2 in genes1range:
                    t_sim_table2["disjoint"].append(gene2)
                else:
                    t_sim_table2["excess"].append(gene2)
        
        return [t_sim_table1, t_sim_table2]
            
    def topological_similarity(self, genome1, genome2, c1=1, c2=1, c3=0.2, delta_t=None):
        #given by http://nn.cs.utexas.edu/downloads/papers/stanley.ec02.pdf, figure 1, 2 on page 13
        #compares genome1 to genome2
        #if delta_t is not None:
        #   returns false if compatibility is above delta_t, true if it is below delta_t
        #otherwise:
        #   returns the compatibility
        
        comparison = self.compare_genomes(genome1, genome2)
        
        N = max((len(genome1.genes), len(genome2.genes)))
        E = len(comparison[0]["excess"])
        D = len(comparison[0]["disjoint"])
        M = len(comparison[0]["matching"])
        Wbar = 0
        
        for gene1, gene2 in zip(comparison[0]["matching"], comparison[1]["matching"]):
            Wbar += abs(gene1[1] - gene2[1]) / M

        if not delta_t:
            return (c1 * E)/N + (c2 * D)/N + (c3 * Wbar)
        else:
            return (c1 * E)/N + (c2 * D)/N + (c3 * Wbar) < delta_t





        

        
