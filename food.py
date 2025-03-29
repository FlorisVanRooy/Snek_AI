import random

import pygame

from consts import BLOCK_SIZE, HEIGHT, RED, WIDTH


class Food:
    def __init__(self):
        self.respawn()

    def respawn(self):
        self.position = (random.randrange(0, WIDTH, BLOCK_SIZE),
                         random.randrange(0, HEIGHT, BLOCK_SIZE))
    
    def show(self, screen):
        red = (255, 0, 0)
        pygame.draw.rect(screen, red, (self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE))