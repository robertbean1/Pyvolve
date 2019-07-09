from random import randint
from Topology.node import Node
from Topology.structure import Structure

def random_topology(inputs, outputs, nodes_bound, layers_bound, connection_density=0.5, hidden_func='sigmoid', output_func='sigmoid'):

    node_number = 0
    
    node_list = []

    for _ in range(inputs):
        node_list.append(Node(node_number, layer=1, activation='Input'))
        node_number += 1

    for layer_n in range(1, randint(1, layers_bound)+1):
        for _ in range(randint(1, nodes_bound)):
            node_list.append(Node(node_number, layer=layer_n+1, activation=hidden_func))
            node_number += 1

    for _ in range(outputs):
        node_list.append(Node(node_number, layer=layer_n+2, activation=output_func))
        node_number += 1

    layer_list = list(range(1, layer_n+3))
    
    return node_list, layer_list
    
