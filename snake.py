import numpy as np
import pygame
from action import get_action, set_action
from consts import ALL_DIRECTIONS, BLOCK_SIZE, DIRECTIONS, GREEN, HEIGHT, WIDTH
from food import Food
from model import build_model
from tensorflow.keras.models import Sequential # type: ignore


class Snake:
    def __init__(self):
        self.head = [WIDTH // 2, HEIGHT // 2]
        self.tail_positions = [
            [WIDTH // 2 - BLOCK_SIZE, HEIGHT // 2],
            [WIDTH // 2 - 2 * BLOCK_SIZE, HEIGHT // 2],
            [WIDTH // 2 - 3 * BLOCK_SIZE, HEIGHT // 2]
        ]
        self.direction = DIRECTIONS[1]
        self.brain: Sequential = build_model(24, 3)
        self.alive = True 
        self.food = Food()
        self.vision = []
        self.lifetime = 0
        self.left_to_live = 200
        self.fitness = 0
        self.length = 4

    def is_alive(self):
        """Returns whether the snake is alive."""
        return self.alive
    
    def look(self):
        """Looks in 8 directions (left, left/up, up, up/right, right, right/down, down, down/left)
        and collects vision data (food, tail, wall distance) into self.vision.
        """
        self.vision = []  # Reset vision for this look call

        # For each direction, obtain three values and extend the vision list.
        for direction in ALL_DIRECTIONS:
            vision_in_direction = self.look_in_direction(direction)
            self.vision.extend(vision_in_direction)

    def look_in_direction(self, direction):
        """
        Checks in one direction until a wall is hit.
        Returns a list of 3 floats:
         - [0]: 1 if food is found along this line, else 0.
         - [1]: A value (1/distance) if the snake's tail is seen.
         - [2]: A value (1/distance) representing how far the wall is.
        """
        # Prepare a list to hold the vision information in this direction.
        vision_in_direction = [0.0, 0.0, 0.0]
        # Copy the current head position
        position = self.head
        food_found = False
        tail_found = False
        distance = 0

        # Move one step in the direction before starting the loop.
        position = (position[0] + direction[0], position[1] + direction[1])
        distance += 1

        # Keep looking until a wall is reached.
        # Here, the walls are defined by 0 <= x < WIDTH and 0 <= y < HEIGHT.
        while 0 <= position[0] < WIDTH and 0 <= position[1] < HEIGHT:
            # Check if the food is found at the current position.
            if not food_found and position == self.food.position:
                vision_in_direction[0] = 1
                food_found = True

            # Check if the snake's tail is at the current position.
            if not tail_found and self.is_on_tail(position):
                vision_in_direction[1] = 1 / distance
                tail_found = True

            # Step further in the same direction.
            position = (position[0] + direction[0], position[1] + direction[1])
            distance += 1

        # Once a wall is hit, record the distance information.
        vision_in_direction[2] = 1 / distance

        return vision_in_direction

    def is_on_tail(self, pos):
        """Checks if the given position is part of the snake's tail."""
        return any(segment == pos for segment in self.tail_positions)

    def set_velocity(self):
        action = get_action(self.brain, self.vision)
        if action != 1:
            self.direction = set_action(action, self.direction)

    def move(self):
        self.lifetime += 1
        self.left_to_live -= 1
        if self.left_to_live <= 0:
            self.alive = False
        if self.gonna_die():
            self.alive = False
        if self.head == self.food:
            self.eat()
        else:
            self.tail_positions.insert(0, self.head)
            self.tail_positions.pop()
            self.head[0] += self.direction[0]
            self.head[1] += self.direction[1]

    def eat(self):
        self.food = Food()
        while any(self.food.position == segment for segment in self.tail_positions):
            self.food = Food()
        self.left_to_live += 100
        self.grow()

    def grow(self):
        self.tail_positions.insert(0, self.head)
        self.head[0] += self.direction[0]
        self.head[1] += self.direction[1]
        self.length += 1

    def gonna_die(self):
        if self.head[0] < 0 or self.head[0] >= WIDTH or self.head[1] < 0 or self.head[1] >= HEIGHT:
            return True

        return self.is_on_tail(self.head)
    
    def calc_fitness(self):
        if self.length < 10:
            self.fitness = np.floor(self.lifetime * self.lifetime * pow(2, np.floor(self.length)))
        else:
            self.fitness = self.lifetime * self.lifetime
            self.fitness *= pow(2, 10)
            self.fitness *= (self.length-9)

    def clone(self):
        clone = Snake()
        clone.brain = self.brain
        clone.alive = True
        return clone
    
    def crossover(self, wife: "Snake") -> "Snake":
        # Create a child snake instance.
        child = Snake()

        # Retrieve the weights from both parents' brains.
        weights_self = self.brain.get_weights()
        weights_wife = wife.brain.get_weights()

        new_weights = []
        # For each corresponding weight array, combine them.
        for w_self, w_wife in zip(weights_self, weights_wife):
            # Create a mask with the same shape as the weight matrix,
            # where each element is True or False randomly.
            mask = np.random.rand(*w_self.shape) > 0.5
            # Use the mask to pick weights from either parent.
            child_weights = np.where(mask, w_self, w_wife)
            new_weights.append(child_weights)

        # Set the new weights in the child's brain.
        child.brain.set_weights(new_weights)
        return child
    
    def mutate(self, mutation_rate: float):
        """
        Mutates the brain of this snake by randomly adjusting its weights.
        
        Each weight in the brain has a chance (mutation_rate) to be perturbed by adding
        a small random noise, often sampled from a normal distribution.
        """
        weights = self.brain.get_weights()  # get the current weights as a list of numpy arrays
        new_weights = []
        for w in weights:
            # Create a mutation mask: True where mutation occurs.
            mutation_mask = np.random.rand(*w.shape) < 0.75
            # Create noise: small random changes from a normal distribution.
            noise = np.random.randn(*w.shape) * mutation_rate
            # Only mutate where the mask is True.
            w_new = w + mutation_mask * noise
            new_weights.append(w_new)
        self.brain.set_weights(new_weights)