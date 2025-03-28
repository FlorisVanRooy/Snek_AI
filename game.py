import random
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame


os.environ["SDL_VIDEODRIVER"] = "dummy"


# Initialize Pygame
pygame.init()

# Constants
DIRECTIONS = [(0, -20), (20, 0), (0, 20), (-20, 0)]  # Up, Right, Down, Left
WIDTH, HEIGHT = 600, 600
BLOCK_SIZE = 20
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# The Snake class remains largely unchanged.
class Snake:
    def __init__(self):
        # Start with two segments for demonstration
        self.positions = [(WIDTH // 2, HEIGHT // 2),
                          (WIDTH // 2 - BLOCK_SIZE, HEIGHT // 2)]
        self.direction = (0, -BLOCK_SIZE)  # Starting moving up

    def move(self):
        head_x, head_y = self.positions[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        self.positions.insert(0, new_head)
        self.positions.pop()  # Remove tail unless food is eaten

    def grow(self):
        # When the snake eats food, we add a segment by not removing the tail.
        self.positions.append(self.positions[-1])

    def draw(self, surface):
        for pos in self.positions:
            pygame.draw.rect(surface, GREEN, (pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))


class Food:
    def __init__(self):
        self.respawn()

    def respawn(self):
        self.position = (random.randrange(0, WIDTH, BLOCK_SIZE),
                         random.randrange(0, HEIGHT, BLOCK_SIZE))

    def draw(self, surface):
        pygame.draw.rect(surface, RED, (self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE))


# The SnakeGame class encapsulates the game loop and state.
class SnakeGame:
    def __init__(self, width=WIDTH, height=HEIGHT, block_size=BLOCK_SIZE):
        self.width = width
        self.height = height
        self.block_size = block_size
        self.steps_without_food = 0
        self.collided = False

        # Set up the display window.
        self.win = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()

        # Initialize or reset the game state.
        self.reset()

    def reset(self):
        """Initializes or resets the game state."""
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.run = True

    def snake_eats_food(self):
        """Returns True if the snake's head is on the food."""
        return self.snake.positions[0] == self.food.position

    def snake_collision(self):
        """Returns True if the snake collides with itself."""
        head = self.snake.positions[0]
        return head in self.snake.positions[1:]

    def wall_collision(self):
        """Returns True if the snake collides with the wall."""
        head_x, head_y = self.snake.positions[0]
        return head_x < 0 or head_x >= self.width or head_y < 0 or head_y >= self.height

    def update_direction(self, action):
        """
        Update the snake's direction if the new direction is not directly opposite.
        new_direction should be a tuple like (dx, dy).
        """
        # Calculate the opposite of the current direction.
        current_index = DIRECTIONS.index(self.snake.direction)
        if action == 0:  # Turn Left
            new_index = (current_index - 1) % 4  
        else:  # Turn Right
            new_index = (current_index + 1) % 4  
    
        self.snake.direction = DIRECTIONS[new_index]  # Update snake's direction

    def update(self, action=None):
        """
        Update the game state for one time step.
        If an action is provided (e.g., from an AI), update the direction accordingly.
        Otherwise, manual control can be used.
        """
        # If an action is given, use it to update the snake's direction.
        if action is not None and action != 1:
            self.update_direction(action)
        # Move the snake.
        self.snake.move()

        # Check if the snake eats food.
        if self.snake_eats_food():
            self.snake.grow()
            self.food.respawn()
            self.score += 1
            self.steps_without_food = 0

        # Check for collisions (with walls or itself).
        if self.wall_collision() or self.snake_collision():
            self.collided = True
            self.run = False  # Game over
        self.steps_without_food+=1
    def draw(self):
        """Draw the game state on the window."""
        self.win.fill(BLACK)
        self.snake.draw(self.win)
        self.food.draw(self.win)
        pygame.display.update()

    def game_loop(self):
        """The main game loop for manual play (or testing)."""
        while self.run:
            self.clock.tick(10)  # Control game speed (FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

            # Example manual controls (keyboard):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and self.snake.direction != (0, self.block_size):
                self.snake.direction = (0, -self.block_size)
            elif keys[pygame.K_DOWN] and self.snake.direction != (0, -self.block_size):
                self.snake.direction = (0, self.block_size)
            elif keys[pygame.K_LEFT] and self.snake.direction != (self.block_size, 0):
                self.snake.direction = (-self.block_size, 0)
            elif keys[pygame.K_RIGHT] and self.snake.direction != (-self.block_size, 0):
                self.snake.direction = (self.block_size, 0)

            self.update()  # Update game state (no AI action in this loop)
            self.draw()    # Draw the updated state

        pygame.quit()


# For manual testing, you can run the game loop like this:
if __name__ == "__main__":
    game = SnakeGame()
    game.game_loop()
