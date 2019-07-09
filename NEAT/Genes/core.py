from .genes import Genome
from Topology import Node

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
