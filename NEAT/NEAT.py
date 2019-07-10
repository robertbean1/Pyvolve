from Genes import Genome, Genepool, distill_genome
from Genes.core import breed
from Network import FeedForwardNetwork
from Species import Population

#ALL MEMBERS OF A POPULATION MUST START FROM A TEMPLATE, OR ELSE SOME WEIRD STUFF HAPPENS WITH INNOVATION NUMBERS AND NODE NUMBERS

P = Population()

for n in range(10):
    P.generate_members(Genome(2, 2, 2, 1), 50)

#Example of why distant breeding isn't nice, and why I was yelling up there ^
G1 = P.members[0]
G2 = P.members[60]
G = breed(P, G1, G2)

Net1 = FeedForwardNetwork(G1)
Net2 = FeedForwardNetwork(G2)
Net3 = FeedForwardNetwork(G)

print(Net1.predict([1, 1]))
print(Net2.predict([1, 1]))
print(Net3.predict([1, 1]))

print('')

#Example of why intraspecieal breeding is nice
G1 = P.members[0]
G2 = P.members[1]
G = breed(P, G1, G2) 


Net1 = FeedForwardNetwork(G1)
Net2 = FeedForwardNetwork(G2)
Net3 = FeedForwardNetwork(G)

print(Net1.predict([1, 1]))
print(Net2.predict([1, 1]))
print(Net3.predict([1, 1]))


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
#           Also, it works with biases now too.** see bugs



# I typed up 68KB of code in 3 days

# Bug report : Breed offspring's network has no tree

# Bug fix: Fixed Genes.core.py genome_from_distilled : New_G.genes was still a distilled object

# Bug report: Bias dictionary built from genome inside the network is iffy as to wether the bias exists for that node
