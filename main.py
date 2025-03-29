from action import get_action
from snake import Snake
from world import World

world = World(1, 5)

while world.gen < 5:
    if not world.done():
        world.update()
    else:
        world.genetic_algorithm()