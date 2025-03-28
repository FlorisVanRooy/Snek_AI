import numpy as np
import concurrent.futures
import signal
from action import get_action
from game import BLOCK_SIZE, SnakeGame
from model import build_model, input_size, output_size
from state import get_state

def simulate_game(model):
    game = SnakeGame()
    total_reward = 0
    while game.run:
        game.clock.tick(20)
        state = get_state(game.snake, game.food)
        action = get_action(model, state)
        game.update(action)
        
        head_x, head_y = game.snake.positions[0]
        food_x, food_y = game.food.position
        distance = abs(head_x - food_x) + abs(head_y - food_y)  
        total_reward += (5.0 / (distance + 1))

        if game.steps_without_food > 50:
            break

    if game.collided:
        total_reward -= 10
    return total_reward + game.score * 100 - game.steps_without_food * 0.1

def init_worker():
    # Allow worker to respond to Ctrl+C
    signal.signal(signal.SIGINT, signal.SIG_IGN)

if __name__ == '__main__':
    population_size = 36
    generations = 100
    mutation_rate = 0.1

    # Initialize population
    population = [build_model(input_size, output_size) for _ in range(population_size)]

    try:
        for gen in range(generations):
            print(f"Starting generation {gen}")
            with concurrent.futures.ProcessPoolExecutor(initializer=init_worker, max_workers=2) as executor:
                # Submit all tasks
                futures = [executor.submit(simulate_game, model) for model in population]
                # Wait for tasks to complete; you can add a timeout if desired.
                fitness_scores = [future.result() for future in concurrent.futures.as_completed(futures)]
            
            for i, score in enumerate(fitness_scores):
                print(f"Model {i} got a score of {score}")

            print(f"Generation {gen} - Best score: {max(fitness_scores)} - Average score: {np.average(fitness_scores)}")
            
            # Selection: keep top 10% (elitism)
            sorted_indices = np.argsort(fitness_scores)[::-1]
            survivors = [population[i] for i in sorted_indices[:population_size // 10]]
            
            # Breeding new population
            new_population = survivors.copy()
            while len(new_population) < population_size:
                parent1, parent2 = np.random.choice(survivors, 2, replace=False)
                child = build_model(input_size, output_size)
                child_weights = []
                for w1, w2 in zip(parent1.get_weights(), parent2.get_weights()):
                    child_w = w1 * 0.5 + w2 * 0.5  # Smooth blend of parent weights
                    mutation = np.random.randn(*child_w.shape) * mutation_rate
                    child_w += mutation
                    child_weights.append(child_w)
                child.set_weights(child_weights)
                new_population.append(child)
            
            population = new_population
    except KeyboardInterrupt:
        print("Training interrupted by user.")
