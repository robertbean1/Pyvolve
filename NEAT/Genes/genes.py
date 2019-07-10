from Topology import random_topology, Node, Structure
import Topology.backend as T
import Network.backend as N
from .backend import distill_connection
import random, time, copy

class Genome(Structure):
    def __init__(self, inputs, outputs, nodes_bound=5, layers_bound=5, weights_mode='nonzero', biases_mode='nonzero', connection_density=0.5, hidden_func='sigmoid', output_func='sigmoid', randomized=True):

        self.configs = (inputs, outputs, nodes_bound, layers_bound, weights_mode, biases_mode, connection_density, hidden_func, output_func)
        
        self.inputs = inputs
        self.outputs = outputs

        if randomized:
            self.genes = self.random(nodes_bound, layers_bound, weights_mode, biases_mode, connection_density, hidden_func, output_func)
        
    def random(self, nodes_bound=3, layers_bound=3, weights_mode='nonzero', biases_mode='nonzero', connection_density=0.5, hidden_func='sigmoid', output_func='sigmoid'):
        self.nodes, self.layers = random_topology(self.inputs, self.outputs, nodes_bound, layers_bound, connection_density, hidden_func, output_func)
        self.build()
        self.weights = T.random_weights(self.active_connections, weights_mode)
        self.biases = {node:bias for node, bias in zip(self.nodes, self.random_biases(biases_mode))}
        self.disabled_genes = []
        self.n_nodes = max([conn[0].number for conn in self.active_connections] + [conn[1].number for conn in self.active_connections])
        return list(zip(self.active_connections, self.weights))
        
    def random_biases(structure, mode='nonzero'):
        biases = []
        
        for node in structure.nodes:
            if mode=='nonzero':
                biases.append(random.uniform(-1, 1))
            
            if mode=='zero':
                biases.append(0)

        return biases

    def mutate_add_node(self):
        
        split = random.choice(list(enumerate(self.genes)))
        (node1, node2), weight = split[1]
        new_layer = (node1.layer + node2.layer) / 2
        
        while new_layer == int(new_layer):
            split = random.choice(list(enumerate(self.genes)))
            (node1, node2), weight = split[1]
            new_layer = (node1.layer + node2.layer) / 2

        new_node = Node(self.n_nodes + 1, new_layer)
        self.n_nodes = self.n_nodes + 1
        new_node.activate()

        self.nodes.append(new_node)
        
        self.biases[new_node] = random.uniform(-1, 1)
        
        self.genes.insert(split[0], [[new_node, node2], weight])
        self.genes.insert(split[0], [[node1, new_node], 1])

        self.active_connections = list(zip(*self.genes))[0]
        self.weights = list(zip(*self.genes))[1]

        # Disabled Genes - You'll remember what this means, if not, read the paper

    def mutate_add_connection(self, stop_search_threshold=20):

        def __mac(_i=0):
            layers = [v for _, v in self.sort_layers().items()]
            layer1 = random.choice(list(enumerate(layers[:len(layers)-1]))) #Choices between Inputs to Outputs, excluding Outputs
            layer2 = random.choice(layers[layer1[0]+1:]) #Choices between layer1 and Outputs, including Outputs

            layer1 = layer1[1]
            
            node1 = random.choice(layer1)
            node2 = random.choice(layer2)

            if not [node1, node2] in self.active_connections:
                if node1.is_active and node2.is_active:
                    self.genes.append([[node1, node2], random.uniform(-2.718, 2.718)])
                    self.active_connections = list(zip(*self.genes))[0]
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
        return sorted(self.nodes, key=lambda x: x.number)

    def sort_layers(self):
        layers = {layer:self.get_nodes(layer) for layer in sorted(self.layers)}
        return layers

    def binary_fission(self, mutate_weight_chance=1, mutate_bias_chance=0.3, mutate_add_connection_chance=0.1, mutate_add_node_chance=0.1, max_weight_add=0.1, max_weight_sub=0.1, max_bias_add=0.1, max_bias_sub=0.1):
        daughter = copy.deepcopy(self)
        if random.uniform(0, 1) < mutate_weight_chance:
            daughter.mutate_weight(max_weight_add, max_weight_sub)
        if random.uniform(0, 1) < mutate_bias_chance:
            daughter.mutate_bias(max_bias_add, max_bias_sub)
        if random.uniform(0, 1) < mutate_add_connection_chance:
            daughter.mutate_add_connection()
        if random.uniform(0, 1) < mutate_add_node_chance:
            daughter.mutate_add_node()
        return daughter

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
                conn = distill_connection(conn)
                self.genes.add((conn, True))
            for conn, weight in genome.disabled_genes:
                conn = distill_connection(conn)
                self.genes.add((conn, False))
        
        for n, gene in enumerate(self.genes):
            self.innovation_table[gene] = n

        self.innovation_number += len(self.genes)
    
    def breakdown(self, genome):
        marking_list = []
        for gene in genome.genes:
            conn, weight = gene
            conn = distill_connection(conn)
            if (conn, True) in self.innovation_table:
                marking_list.append([conn, weight, self.innovation_table[(conn, True)]])
            else:
                marking_list.append([conn, weight, self.innovation_number])
                self.innovation_number += 1
        for gene in genome.disabled_genes:
            conn, weight = gene
            conn = distill_connection(conn)
            if (conn, False) in self.innovation_table:
                marking_list.append([conn, weight, self.innovation_table[(conn, False)]])
            else:
                marking_list.append([conn, weight, self.innovation_number])
                self.innovation_number += 1
        return marking_list

    def package_genome(self, genome):
        if not self.genes:
            self.genes = set()
            self.innovation_table = {}
        
        for conn, weight in genome.genes:
            conn = distill_connection(conn)
            if not (conn, True) in self.innovation_table:
                self.genes.add((conn, True))
                self.innovation_table[(conn, True)] = self.innovation_number
                self.innovation_number += 1
        
        for conn, weight in genome.disabled_genes:
            conn = distill_connection(conn)
            if not (conn, False) in self.innovation_table:
                self.genes.add((conn, False))
                self.innovation_table[(conn, False)] = self.innovation_number
                self.innovation_number += 1

    def compare_genomes(self, genome1, genome2):
        
        t_sim_table1 = {"disjoint":[], "excess":[], "matching":[]}
        t_sim_table2 = {"disjoint":[], "excess":[], "matching":[]}
        
        genes1 = self.breakdown(genome1)
        genes2 = self.breakdown(genome2)

        genes1innovations = list(zip(*genes1))[2]
        genes2innovations = list(zip(*genes2))[2]

        key=lambda x: x[2]
        genes1range = range(min(genes1, key=key)[2], max(genes1, key=key)[2]+1)
        genes2range = range(min(genes2, key=key)[2], max(genes2, key=key)[2]+1)

        for gene1, gene2 in zip(genes1, genes2):
            if gene1[2] in genes2innovations:
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
        
        
        E = len(comparison[0]["excess"])
        D = len(comparison[0]["disjoint"])
        M = len(comparison[0]["matching"])
        N = (E + D + M)
        Wbar = 0
        
        for gene1, gene2 in zip(comparison[0]["matching"], comparison[1]["matching"]):
            Wbar += abs(gene1[1] - gene2[1]) / M

        if not delta_t:
            return (c1 * E/N) + (c2 * D/N) + (c3 * Wbar)
        else:
            return (c1 * E/N) + (c2 * D/N) + (c3 * Wbar) < delta_t





        

        
