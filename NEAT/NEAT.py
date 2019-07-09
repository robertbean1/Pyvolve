from Genes import Genome, Genepool
from Genes.backend import *
from Network import FeedForwardNetwork
from Species import Population

P = Population()
P.generate_members(Genome(2, 2), 50)

for member in P.members:
    Net = FeedForwardNetwork(member)
    print(Net.predict([0, 1]))

#To do - Breeding:
#
#          _/    1) topological comparison
#
#          _/    2) speciation
#
#          X     3) crossing over
#
#          ^ That's all that's left to do, and I'm done


