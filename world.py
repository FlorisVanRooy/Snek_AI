from population import Population


class World:
    def __init__(self, species_number, pop_size):
        self.gen = 0  # The current generation
        self.top_score = 0
        
        # Initialize species: a list of Population objects.
        self.species = [Population(pop_size) for _ in range(species_number)]
        
    def update(self):
        for population in self.species:
            population.update()

    def genetic_algorithm(self):
        for population in self.species:
            population.calc_fitness()
            population.natural_selection()
            # population.mutate()
        self.gen += 1
        self.set_top_score()
        print("Generation", self.gen, "has a top score of", self.top_score)

    def done(self):
        for population in self.species:
            if not population.done():
                return False
            
        return True
    
    def set_top_score(self):
        for population in self.species:
            score = population.max_score
            print("Best score for this gen =", score)
            if (score > self.top_score):
                self.top_score = score
