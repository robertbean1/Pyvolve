from Genes import Genome, Genepool
from Genes.backend import *

class Population(Genepool):
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        
        self.members = []
        
    def add_members(self, members):
        self.package_genomes(members)
        for member in members:
            self.members.append(member)

    def add_member(self, member):
        self.package_genome(member)
        self.members.append(member)

    def generate_members(self, ancestor, size, *args, **kwargs):
        for _ in range(size):
            self.members.append(ancestor.binary_fission(*args, **kwargs))

    def adjust_fitness(self, fitness, subject_member, delta_t, c1=1, c2=1, c3=0.1):
        n = 1
        for member in self.members:
            if self.topological_similarity(subject_member, member, c1, c2, c3, delta_t):
                n+=1
        
        return fitness / n
            
