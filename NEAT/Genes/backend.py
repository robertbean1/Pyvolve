def distill_genome(genome):
    return [[distill_node(node) for node in genome.nodes], [(distill_connection(conn), w) for conn, w in zip(genome.active_connections, genome.weights)], [(distill_node(node), v) for node, v in genome.biases.items()]]

def distill_connection(conn):
    return ((conn[0].number, conn[0].layer, conn[0].activation), (conn[1].number, conn[1].layer, conn[1].activation))

def distill_node(node):
    return (node.number, node.layer, node.activation)


