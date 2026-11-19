import pygame
import random

from config import *
from assets import load_image

class Obstacle:
    """An obstacle that the player must avoid"""

    def __init__(self, x=None, y=None, image=None, speed=None, can_split=True):
        if image is None:
            size = random.randint(OBSTACLE_MIN_SIZE, OBSTACLE_MAX_SIZE)
            image_name = random.choice(METEOR_IMAGES)
            image = load_image(image_name)
            x = random.randint(0, WIDTH - size)
            self.rect = image.get_rect(bottomleft=(x, 0))
        else:
            self.rect = image.get_rect(center=(x, y))

        self.original_image = image
        self.image = self.original_image
        self.speed = random.randint(2, 7) if speed is None else speed
        self.can_split = can_split
        self.angle = 0
        self.rotation_speed = random.choice((-1, 1)) * OBSTACLE_ROTATION_SPEED
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        """Move the obstacle down the screen"""
        self.rect.y += self.speed
        center = self.rect.center
        self.angle = (self.angle + self.rotation_speed) % 360
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=center)
        self.mask = pygame.mask.from_surface(self.image)

    def split(self):
        """Create two smaller fragments when this meteorite can split"""
        if not self.can_split:
            return []

        width = max(OBSTACLE_MIN_SIZE, int(self.image.get_width() * 0.6))
        height = max(OBSTACLE_MIN_SIZE, int(self.image.get_height() * 0.6))
        fragment_image = pygame.transform.smoothscale(self.original_image, (width, height))
        center_x, center_y = self.rect.center
        offset = max(width // 2, 10)
        return [
            Obstacle(center_x - offset, center_y, fragment_image, self.speed + 1, False),
            Obstacle(center_x + offset, center_y, fragment_image, self.speed + 1, False),
        ]

    def is_off_screen(self):
        """Check if the obstacle has moved off the screen"""
        return self.rect.y > HEIGHT

    def draw(self, surface):
        """Draw the obstacle on the given surface"""
        surface.blit(self.image, self.rect)