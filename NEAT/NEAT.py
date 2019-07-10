from Genes import Genome, Genepool, distill_genome
from Genes.core import breed
from Network import FeedForwardNetwork
from Species import Population

P = Population()

for n in range(10):
    P.generate_members(Genome(2, 2, 2, 1), 50)

print(breed(P, P.members[0], P.members[10]))


#To do - Breeding:
#
#          _/    1) topological comparison
#
#          _/    2) speciation
#
#          _/    3) crossing over
#
#             _/    a) Produce ability to build the whole Genome from only a distilled Genome
#
#                /  b) breeding algorithm based on http://nn.cs.utexas.edu/downloads/papers/stanley.ec02.pdf page 12, figure 4
#             _/ |
#                \  c) Genome1, Genome2 -> distilled -> breeder -> distilled -> Genome
#       
#             _/    d) adapt the algorithm for biases
#
#
# I DID IT! Genes.core.breed takes in a genepool, two genomes, and spits out a genome. The genome is not a child instance of the two first genomes, meaning that it can freely mutate. All problems have been avoided.
#           Also, it works with biases now too.
