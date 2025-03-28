import numpy as np

def get_action(model, state):
    # Reshape state for prediction
    state = np.reshape(state, [1, -1])
    prediction = model.predict(state, verbose=0)[0]
    action = np.argmax(prediction)
    return action  # 0: turn left, 1: straight, 2: turn right
