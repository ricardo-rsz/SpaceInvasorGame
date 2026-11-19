import pygame
from config import *
from assets import load_image

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, image_name=LASER_IMAGE, speed=-10):
        super().__init__()
        self.image = load_image(image_name)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = speed
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.y += self.speed
        # Remove the laser if it goes off the screen
        if self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()