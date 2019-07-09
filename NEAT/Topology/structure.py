import Topology.backend as T
import random

class Structure:
    def __init__(self, nodes):
        self.nodes = nodes

        layer_names = []
        for node in nodes:
            if not node.layer in layer_names:
                layer_names.append(node.layer)

        self.hidden_layers = layer_names[1:-1]
        self.layers = layer_names

        self.connections = None
        self.active_connections = None

    def __str__(self):
        
        out_str = 'Structure('

        for node in self.nodes:
            out_str += '\n\t' + str(node)

        return out_str + '\n)'
    
    
    def random_hidden_hidden_connections(self): #Deprecated
        raise NotImplementedError('Deprecated')
        connections = []
        hiddens = self.hidden_nodes
        for n, node in enumerate(hiddens):
            choices = [node for i, node in enumerate(hiddens) if i != n]
            if len(choices) >= 1:
                connections.append([node, random.choice(choices)])
        return connections

    def random_hidden_output_connections(self): #Deprecated
        raise NotImplementedError('Deprecated')
        connections = []
        hiddens = self.hidden_nodes
        outputs = self.output_nodes
        used = []
        for n, node in enumerate(hiddens):
            if random.uniform(0, 1) < 0.5:
                out = random.choice(outputs)
                used.append(out)
                connections.append([node, out])

        for n, node in enumerate([node for node in outputs if not node in used]):
            connections.append([random.choice(hidden), node])
            
        return connections

    def sort_hidden_connections(self, connections): #Deprecated
        raise NotImplementedError('Deprecated')
        paths = []
        hiddens = self.hidden_nodes
        for node in hiddens:
            paths.append(T.get_path(connections, node, [node]))
        return paths
    
    def random_connections(self, density=0.5):
        # Right now these are layer to layer
        # It is neccessary to allow connections between-
        # -any 2 layers, but only from a layer to a later layer
        conns = []
        latest = self.get_nodes(1)       
        for layer in sorted(self.layers)[1:]:
            current = self.get_nodes(layer)
            conns += T.permute_link(latest, current, density)
            latest = current
        return conns

    def get_active_connections(self, connections):
        active_conns = []
        for input_node in self.input_nodes:
            for path in T.get_paths(connections, input_node):
                if path[-1].layer == max(self.layers):
                    active_conns += [conn for conn in T.path_to_connections(path) if not conn in active_conns]
                    
        return active_conns
    
    def build(self, connection_density=0.5):
        self.connections = self.random_connections(connection_density)
        self.active_connections = self.get_active_connections(self.connections)

        for conn in self.active_connections:
            conn[0].activate()
            conn[1].activate()
        
    def get_nodes(self, layer):
        layer_list = []
        for node in self.nodes:
            if node.layer == layer:
                layer_list.append(node)
        return layer_list

    @property
    def topological_genes(self):
        return [[[node1.layer, node1.number], [node2.layer, node2.number]] for node1, node2 in self.active_connections]

    @property
    def is_built(self):
        return self.connections and self.active_connections
    
    @property
    def hidden_nodes(self):
        hidden_list = []
        for node in self.nodes:
            if 1 < node.layer and node.layer < max(self.layers):
                hidden_list.append(node)
        return hidden_list

    @property
    def input_nodes(self):
        input_list = []
        for node in self.nodes:
            if node.layer == 1:
                input_list.append(node)
        return input_list

    @property
    def output_nodes(self):
        output_list = []
        for node in self.nodes:
            if node.layer == max(self.layers):
                output_list.append(node)
        return output_list
