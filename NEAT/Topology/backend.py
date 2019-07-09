import random
import itertools

def is_sub_path(subject_path, master_path):
    raise NotImplementedError()

def get_path(connections, node, l=[]):
    for conn in connections:
        if conn[0] == node:
            next_node = conn[-1]
            if next_node in l:
                return l
            else:
                new_l = l + [next_node]
                return get_path(connections, next_node, new_l)
    return l

def path_to_connections(path):
    conns = []
    for node1, node2 in zip(path[:-1], path[1:]):
        conns.append([node1, node2])
    return conns

def get_paths(connections, starting_node=None, prev=[]):
    if starting_node != None:
        prev = [[starting_node]]

    new_prev = []
    terminate = True
    for path in prev:
        node = path[-1]
        path_terminates = True
        for conn in connections:
            if conn[0] == node:
                path_terminates = False
                terminate = False
                new_prev.append(path + [conn[-1]])
        if path_terminates:
            new_prev.append(path)
    
    if terminate:
        return new_prev

    else:
        return get_paths(connections, prev=new_prev)

def permute_link(list1, list2, chance):
    links = []
    for item2 in list2:
        links.append([random.choice(list1), item2])
        for item1 in list1:
            if (not [item1, item2] in links) and (random.uniform(0, 1) < chance):
                links.append([item1, item2])

    return links

def random_weights(topology, mode='nonzero'):
    weights = []
    
    for conn in topology:
        
        if mode=='nonzero':
            weights.append(random.uniform(-2.718, 2.718))

        if mode=='zero':
            weights.append(0)

    return weights

def random_biases(structure, mode='nonzero'):
    biases = []
    
    for node in structure.nodes:
        if mode=='nonzero':
            biases.append(random.uniform(-1, 1))
        
        if mode=='zero':
            biases.append(0)

    return biases

    
