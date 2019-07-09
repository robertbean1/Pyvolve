def distill_connection(conn):
    return ((conn[0].number, conn[0].layer, conn[0].activation), (conn[1].number, conn[1].layer, conn[1].activation))
