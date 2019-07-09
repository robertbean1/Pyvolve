from random import randint
from Topology.node import Node
from Topology.structure import Structure

def random_topology(inputs, outputs, nodes_bound, layers_bound, connection_density=0.5, hidden_func='sigmoid', output_func='sigmoid'):

    node_number = 0
    
    node_list = []
    
    for _ in range(inputs):
        node_list.append(Node(node_number, layer='Input', activation='Input'))
        node_number += 1

    for layer_n in range(randint(1, layers_bound)):
        for _ in range(randint(1, nodes_bound)):
            node_list.append(Node(node_number, layer='Hidden' + str(layer_n), activation=hidden_func))
            node_number += 1

    for _ in range(outputs):
        node_list.append(Node(node_number, layer='Output', activation=output_func))
        node_number += 1

    topology = Structure(node_list)
    topology.build(connection_density)

    return topology
    
