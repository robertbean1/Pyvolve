from Network.activations import get_activation
import Network.backend as N
import copy

class FeedForwardNetwork:
    def __init__(self, genome):
        self.topology, self.weights = list(zip(*genome.genes))
        self.genome = genome
        self.structure = genome.structure
        self.biases = self.genome.biases

    def compile(self):
        self.tree = N.build_node_tree(self.topology, self.structure.input_nodes, self.structure.output_nodes)

    def predict(self, xs):

        self.compile()
        
        buildout = {}

        for node in self.structure.nodes:
            if node.layer == 'Input':
                buildout[node] = xs[node.number]

        buildout = N.build_activation_tree(self.genome.genes, self.biases, buildout, self.tree)

        self.node_activity = buildout

        outs = []
        for node in self.node_activity:
            if node.layer == 'Output':
                outs.append([node, self.node_activity[node]])

        outs = sorted(outs, key=lambda x: x[0].number)

        return [out[1] for out in outs]
