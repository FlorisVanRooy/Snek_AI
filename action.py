import numpy as np

from consts import DIRECTIONS

def get_action(model, state):
    # Reshape state for prediction
    state = np.reshape(state, [1, -1])
    prediction = model.predict(state, verbose=0)[0]
    action = np.argmax(prediction)
    return action  # 0: turn left, 1: straight, 2: turn right

def set_action(action, current_direction):
    current_index = DIRECTIONS.index(current_direction)
    if action == 0:  # Turn Left
        new_index = (current_index - 1) % 4  
    else:  # Turn Right
        new_index = (current_index + 1) % 4
    
    return DIRECTIONS[new_index]
