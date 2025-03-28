import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
import tensorflow as tf
from tensorflow.keras.models import Sequential # type: ignore
from tensorflow.keras.layers import Dense # type: ignore
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="keras")


def build_model(input_size, output_size):
    model = Sequential([
        Dense(16, input_dim=input_size, activation='relu'),
        Dense(16, activation='relu'),
        Dense(output_size, activation='softmax')
    ])
    return model

# Example usage:
input_size = 14  # Adjust based on how many state features you include
output_size = 3  # [turn left, straight, turn right]
model = build_model(input_size, output_size)