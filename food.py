import random

import pygame

from consts import BLOCK_SIZE, HEIGHT, RED, WIDTH


class Food:
    def __init__(self):
        self.respawn()

    def respawn(self):
        self.position = (random.randrange(0, WIDTH, BLOCK_SIZE),
                         random.randrange(0, HEIGHT, BLOCK_SIZE))