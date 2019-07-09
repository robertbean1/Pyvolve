from .genes import Genome
from Topology import Node
import random

def find_node_from_distilled(nodes, distilled):
    for node in nodes:
        if (node.number, node.layer, node.activation) == tuple(distilled):
            return node

def genome_from_distilled(distilled):

    nodes = distilled[0]
    genes = distilled[1]
    biases = distilled[2]

    output_layer = max(nodes, key=lambda x: x[1])[1]
    outputs = 0
    for node in nodes:
        if node[1] == output_layer:
            outputs += 1

    inputs = 0
    for node in nodes:
        if node[1] == 1:
            inputs += 1
    
    New_G = Genome(inputs, outputs, randomized=False)

    node_objs = sorted([Node(node[0], node[1], node[2]) for node in nodes], key=lambda node: node.number)

    New_G.nodes = node_objs
    New_G.layers = sorted(list(set([node[1] for node in nodes])))
    New_G.weights = list(zip(*genes))[1]
    New_G.connections = [(find_node_from_distilled(New_G.nodes, gene[0][0]), find_node_from_distilled(New_G.nodes, gene[0][1])) for gene in genes]
    New_G.biases = biases
    New_G.disabled_genes = []
    New_G.n_nodes = max(nodes, key=lambda x: x[0])[0]
    
    New_G.active_connections = New_G.get_active_connections(New_G.connections)

    for active_conn in New_G.active_connections:
        active_conn[0].activate()
        active_conn[1].activate()
    
    New_G.genes = genes

    return New_G

def breed_from_distilled(genepool, distilled1, distilled2):

    new_conns = []

    conns1 = list(zip(*distilled1[1]))[0]
    conns2 = list(zip(*distilled1[1]))[0]

    conns1weights = list(zip(*distilled1[1]))[1]
    conns2weights = list(zip(*distilled1[1]))[1]
    
    conns1innovations_dict = {genepool.innovation_table[(tuple(conn), True)]:conn for conn in conns1}
    conns2innovations_dict = {genepool.innovation_table[(tuple(conn), True)]:conn for conn in conns2}

    conns1innovations_weights_dict = {genepool.innovation_table[(tuple(conn), True)]:conn for conn in conns1}
    conns2innovations_weights_dict = {genepool.innovation_table[(tuple(conn), True)]:conn for conn in conns2}

    conns1innovations = [genepool.innovation_table[(tuple(conn), True)] for conn in conns1]
    conns2innovations = [genepool.innovation_table[(tuple(conn), True)] for conn in conns2]

    all_innovations = list(set(conns1innovations + conns2innovations))
    
    for innovation in all_innovations:
        if innovation in conns1innovations and innovation in conns2innovations:
            weight = random.choice([conns1innovations_weights_dict[innovation], conns2innovations_weights_dict[innovation]])
            conn = conns1innovations_dict[innovation]
            new_conns.append((conn, weight))
        
        elif innovation in conns1innovations:
            weight = conns1innovations_weights_dict[innovation]
            conn = conns1innovations_dict[innovation]
            new_conns.append((conn, weight))

    return new_conns






    
