from .activations import get_activation
from .backend import *
import copy

class FeedForwardNetwork:
    def __init__(self, genome):
        self.topology, self.weights = list(zip(*genome.genes))
        self.genome = genome
        self.biases = genome.biases

    def compile(self):
        self.tree = build_node_tree(self.topology, self.genome.input_nodes, self.genome.output_nodes, max(self.genome.layers))

    def predict(self, xs):

        self.compile()
        
        buildout = {}

        for node in self.genome.nodes:
            if node.layer == 1:
                buildout[node] = xs[node.number]

        buildout = build_activation_tree(list(zip(self.topology, self.weights)), self.biases, buildout, self.tree)

        self.node_activity = buildout

        outs = []
        for node in self.node_activity:
            if node.layer == max(self.genome.layers):
                outs.append([node, self.node_activity[node]])

        outs = sorted(outs, key=lambda x: x[0].number)

        return [out[1] for out in outs]
