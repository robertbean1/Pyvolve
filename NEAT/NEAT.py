from Genes import Genome, Genepool
from Genes.backend import *
from Network import FeedForwardNetwork
import copy

class Species(Genepool):
    def __init__(self, ancestor, *args, **kwargs):
        self.ancestor = ancestor
        super().__init__(*args, **kwargs)
        self.add_member(self.ancestor)
        
    def add_members(self, members):
        self.package_genomes(members)

    def add_member(self, member):
        self.package_genome(member)
    
    def is_member(self, potential_member, delta_t, *args, **kwargs):
        return self.topological_similarity(self.ancestor, potential_member, *args, delta_t=delta_t, **kwargs)

class Population:
    def __init__(self, species, species_members, max_topological_mutations, max_parametric_mutations):
        for _ in range(species):
            for _ in range(species_members):
                pass

#To do - Breeding:
#
#          _/ 1) topological comparison
#
#          X  2) speciation
#
#          X  3) crossing over

#          ^ That's all that's left to do, and I'm done


