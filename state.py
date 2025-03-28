import numpy as np
from game import WIDTH, HEIGHT, Snake

def get_state(snake: Snake, food):
    head_x, head_y = snake.positions[0]
    food_x, food_y = food.position
    direction = snake.direction

    # Normalize position values to be between 0 and 1
    head_x /= WIDTH
    head_y /= HEIGHT
    food_x /= WIDTH
    food_y /= HEIGHT

    # Normalized differences between snake head and food
    delta_x = (food_x - head_x)
    delta_y = (food_y - head_y)

    # Distance to walls (already between 0 and 1)
    distance_up = head_y
    distance_down = 1 - head_y
    distance_left = head_x
    distance_right = 1 - head_x

    # One-hot encode direction (Up, Right, Down, Left)
    direction_one_hot = [0, 0, 0, 0]
    if direction == (0, -20):   # Up
        direction_one_hot[0] = 1
    elif direction == (20, 0):  # Right
        direction_one_hot[1] = 1
    elif direction == (0, 20):  # Down
        direction_one_hot[2] = 1
    elif direction == (-20, 0): # Left
        direction_one_hot[3] = 1

    # Combine all features into a single array
    state = np.array([
        head_x, head_y, 
        food_x, food_y, 
        delta_x, delta_y, 
        distance_up, distance_down, distance_left, distance_right
    ] + direction_one_hot)  # Add one-hot encoded direction

    return state
