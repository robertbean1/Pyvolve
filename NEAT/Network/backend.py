import Topology.backend as T
from Network.activations import get_activation

def build_node_tree(connections, input_nodes, output_nodes, output_layer):
    node_tree = {}
    for input_node in input_nodes:
        for path in T.get_paths(connections, input_node):
            if path[-1].layer == output_layer:
                for conn in T.path_to_connections(path):
                    if not conn[-1] in node_tree:
                        node_tree[conn[-1]] = [conn[0]]
                    else:
                        if not conn[0] in node_tree[conn[-1]]:
                            node_tree[conn[-1]].append(conn[0])
    return node_tree

def build_activation_tree(topology, biases, buildout, tree={}, first=True):

    weight_dict = dict([((node1, node2), weight) for (node1, node2), weight in topology])

    if not first:
        complete = True
        for node in tree:
            node_complete = True
            for prev_node in tree[node]:
                if not prev_node[0]:
                    node_complete = False
            
            if node_complete:
                kernel = 0
                for prev_node in tree[node]:
                    kernel += buildout[prev_node[1]] * weight_dict[(prev_node[1], node)]
                buildout[node] = get_activation(node.activation)(kernel + biases[node])

            else:
                complete = False

        new_tree = {}
        for node in tree:
            new_tree[node] = tree[node]
            for i, prev_node in enumerate(tree[node]):
                if prev_node[1] in buildout:
                    new_tree[node][i] = [True, prev_node[1]]
                else:
                    new_tree[node][i] = [False, prev_node[1]]

        if not complete:
            return build_activation_tree(topology, biases, buildout, new_tree, False)

        else:
            return buildout
    
    else:
        new_tree = {}
        for node in tree:
            new_tree[node] = tree[node]
            for i, prev_node in enumerate(tree[node]):
                if prev_node in buildout:
                    new_tree[node][i] = [True, prev_node]
                else:
                    new_tree[node][i] = [False, prev_node]
        return build_activation_tree(topology, biases, buildout, new_tree, False)

    

                

    
        

            
            
