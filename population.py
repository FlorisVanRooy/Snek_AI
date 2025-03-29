import random
from snake import Snake


class Population:
    def __init__(self, size):
        self.snakes = [Snake() for _ in range(size)]
        self.current_best_snake = Snake()
        self.max_score = 0
        self.gen = 0

    def update(self):
        for snake in self.snakes:
            if (snake.is_alive()):
                snake.look()
                snake.set_velocity()
                snake.move()

    def done(self):
        for snake in self.snakes:
            if (snake.is_alive()):
                return False
            
            return True
        
    def calc_fitness(self):
        for snake in self.snakes:
            snake.calc_fitness()

    def calc_max_score(self):
        for snake in self.snakes:
            score = snake.fitness
            if score > self.max_score:
                self.current_best_snake = snake
                self.max_score = score

    def natural_selection(self):
        new_snakes: list[Snake] = []

        self.calc_max_score()

        new_snakes.append(self.current_best_snake)

        for i in range(len(self.snakes)):
            parent1 = self.select_snake()
            parent2 = self.select_snake()

            child = parent1.crossover(parent2)
            child.mutate(0.05)

            new_snakes.append(child)

        self.snakes = [snake.clone() for snake in new_snakes]

        self.gen += 1
        self.current_best = 0

    def select_snake(self):
        """Selects a snake from the current population, with a higher chance for snakes with higher fitness."""
        # Calculate the total fitness of the population.
        total_fitness = sum(snake.fitness for snake in self.snakes)
        
        # If total fitness is 0 (which might happen initially), return a random snake.
        if total_fitness == 0:
            return random.choice(self.snakes)
        
        # Pick a random value between 0 and total_fitness.
        pick = random.uniform(0, total_fitness)
        
        # Iterate over the snakes and sum their fitness.
        current = 0
        for snake in self.snakes:
            current += snake.fitness
            # When the running sum exceeds the random pick, select that snake.
            if current >= pick:
                return snake