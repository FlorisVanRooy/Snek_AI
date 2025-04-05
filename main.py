import pygame
from action import get_action
from consts import HEIGHT, WIDTH
from snake import Snake
from world import World

# Initialize Pygame
pygame.init()

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake AI")

# Define speed and mutation rate
speed = 20
clock = pygame.time.Clock()
global_mutation_rate = 0.05

def draw(screen, world: "World", speed, global_mutation_rate):
    """Updates and evolves the snake population."""
    screen.fill((40, 40, 40))  # Background color
    # draw_data(screen, world, speed, global_mutation_rate)  # Draw the info panel

    if not world.done():
        world.update(screen)  # Update snakes if any are still alive
    else:
        world.genetic_algorithm()  # Apply evolution when all are dead

    pygame.display.flip()  # Refresh screen

# Create the world
world = World(1, 50)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw(screen, world, speed, global_mutation_rate)
    clock.tick(speed)

pygame.quit()