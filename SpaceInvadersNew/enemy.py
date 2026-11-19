import random

import pygame

from config import *
from laser import Laser
from assets import load_image


class Enemy(pygame.sprite.Sprite):
    """An enemy ship that moves down and fires at the players"""

    def __init__(self):
        super().__init__()
        # Exercise 6: Create an enemy ship that can fire at players.
        image_name = random.choice(ENEMY_IMAGES)
        self.image = load_image(image_name, width=ENEMY_WIDTH)
        x = random.randint(0, WIDTH - self.image.get_width())
        self.rect = self.image.get_rect(bottomleft=(x, 0))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = ENEMY_SPEED
        self.last_shot = -ENEMY_FIRE_DELAY

    def move(self):
        self.rect.y += self.speed

    def is_off_screen(self):
        return self.rect.top > HEIGHT

    def should_fire(self, now):
        if now - self.last_shot < ENEMY_FIRE_DELAY:
            return False
        self.last_shot = now
        return True

    def fire(self):
        return Laser(self.rect.centerx, self.rect.bottom, LASER_IMAGE2, 8)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
