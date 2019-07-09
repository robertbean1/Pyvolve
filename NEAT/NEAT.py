from Genes import Genome, Genepool, distill_genome
from Genes.core import genome_from_distilled, breed_from_distilled
from Network import FeedForwardNetwork
from Species import Population

P = Population()

for n in range(10):
    P.generate_members(Genome(2, 2, 2, 1), 50)

print(breed_from_distilled(P, distill_genome(P.members[0]), distill_genome(P.members[80])))

#To do - Breeding:
#
#          _/    1) topological comparison
#
#          _/    2) speciation
#
#          1/3   3) crossing over
#
#             _/    a) Produce ability to build the whole Genome from only a distilled Genome
#
#                /  b) breeding algorithm based on http://nn.cs.utexas.edu/downloads/papers/stanley.ec02.pdf page 12, figure 4
#             _/ |
#                \  c) Genome1, Genome2 -> distilled -> breeder -> distilled -> Genome
#       
#             X     d) adapt the algorithm for biases
#
# Working at stage c if I somehow find a way to screw up and make d and c mutually exclusive
# Future me: I sure did screw it up, Genes/genes.py line 161 - fix later. I need to disable biases for now.
# Future Future me: Yeah so I did c)
# 
# Genome to Network parser complete
