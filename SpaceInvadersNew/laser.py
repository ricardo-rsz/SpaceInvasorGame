import pygame
from config import *
from assets import load_image

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load_image(LASER_IMAGE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        # Remove the laser if it goes off the screen
        if self.rect.bottom < 0:
            self.kill()