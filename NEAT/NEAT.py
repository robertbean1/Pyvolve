from Genes import Genome, Genepool
from Genes.backend import *
from Network import FeedForwardNetwork

class Species(Genepool):
    def __init__(self, ancestor, *args, **kwargs):
        
        super().__init__(*args, **kwargs)

        self.ancestor = ancestor
        self.members = []
        self.add_member(self.ancestor)
        
        
    def add_members(self, members):
        self.package_genomes(members)
        for member in members:
            self.members.append(member)

    def add_member(self, member):
        self.package_genome(member)
        self.members.append(member)
    
    def is_member(self, potential_member, delta_t, *args, **kwargs):
        return self.topological_similarity(self.ancestor, potential_member, *args, delta_t=delta_t, **kwargs)

    def mean_topological_similarity(self, potential_member, *args, **kwargs):
        similarity = 0
        for member in self.members:
            similarity += self.topological_similarity(member, potential_member, *args, **kwargs)
        return similarity / len(self.members)

    def generate_members(self, size):
        for _ in range(size):
            self.members.append(self.ancestor.binary_fission(1, 0.2, 0.2, 0.2))

class Population:
    def __init__(self, species, species_members, inputs, outputs):
        self.niches = []
        for _ in range(species):
            niche = Species(Genome(inputs, outputs))
            niche.generate_members(species_members)
            self.niches.append(niche)

S = Species(Genome(2, 1))
S.generate_members(50)

for member in S.members:
    Net = FeedForwardNetwork(member)
    print(Net.predict([0, 1]))

print(S.mean_topological_similarity(Genome(2, 1)))

#To do - Breeding:
#
#          _/    1) topological comparison
#
#          0.5_/ 2) speciation (We're halfway there, ooooh oh, we're living on a prayer)
#
#          X     3) crossing over
#
#          ^ That's all that's left to do, and I'm done


