from Genes import Genome, Genepool

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

#Problem (Fixed: No): Creating a Genome from another Genome makes them share the same node objects-
#                    -which in turn means that any mutation to one genome will produce side effects to the nodes of ancestors and relatives

