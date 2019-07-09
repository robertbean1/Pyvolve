from Topology import random_topology, Node, Structure
import Topology.backend as T
import Network.backend as N
from Network import FeedForwardNetwork
import random, time

random.seed(time.time())

class Genome:
    def __init__(self, inputs, outputs, nodes_bound=3, layers_bound=3, weights_mode='nonzero', biases_mode='nonzero', connection_density=0.5, hidden_func='sigmoid', output_func='sigmoid', previous=None):
        #if previous:
            #self.genes = previous.mutate()
        #else:
            #self.genes = self.random()
        
        self.inputs = inputs
        self.outputs = outputs

        self.genes = self.random(nodes_bound, layers_bound, weights_mode, biases_mode, connection_density, hidden_func, output_func)

        self.n_nodes = max([conn[0].number for conn in self.topology] + [conn[1].number for conn in self.topology])

    def random(self, nodes_bound=3, layers_bound=3, weights_mode='nonzero', biases_mode='nonzero', connection_density=0.5, hidden_func='sigmoid', output_func='sigmoid'):
        self.structure = random_topology(self.inputs, self.outputs, nodes_bound, layers_bound, connection_density, hidden_func, output_func)
        self.topology = self.structure.active_connections
        self.weights = T.random_weights(self.topology, weights_mode)
        self.biases = {node:bias for node, bias in zip(self.structure.nodes, T.random_biases(self.structure, biases_mode))}
        return list(zip(self.topology, self.weights))

    def mutate_add_node(self):
        split = random.choice(list(enumerate(self.genes)))
        (node1, node2), weight = split[1]
        del self.genes[split[0]]

        new_layer = 'Inbetween(' + node1.layer + '-' + node2.layer + ')'
        new_node = Node(self.n_nodes+1, new_layer)
        new_node.activate()
        
        self.structure.layers.append(new_layer)

        self.structure.nodes.append(new_node)
        
        self.structure.connections.append([node1, new_node])
        self.structure.connections.append([new_node, node2])

        for n, conn in enumerate(self.structure.active_connections):
            if conn == [node1, node2]:
                del self.structure.active_connections[n]

        self.biases[new_node] = 0

        self.structure.active_connections.append([node1, new_node])
        self.structure.active_connections.append([new_node, node2])
        
        self.genes.insert(split[0], [[new_node, node2], weight])
        self.genes.insert(split[0], [[node1, new_node], 1])

        self.topology = self.structure.active_connections
        self.weights = list(zip(*self.genes))[1]

if __name__ == '__main__':
    G = Genome(2, 1, nodes_bound=2, layers_bound=1, connection_density=0.85, hidden_func='tanh', output_func='sigmoid')
    G.mutate_add_node()

    net = FeedForwardNetwork(G)

    print(net.predict([0, 0]))
    print(net.predict([0, 1]))
    print(net.predict([1, 0]))
    print(net.predict([1, 1]))



