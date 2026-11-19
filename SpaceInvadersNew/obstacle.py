import pygame
import random

from config import *
from assets import load_image

class Obstacle:
    """An obstacle that the player must avoid"""

    def __init__(self):
        size = random.randint(OBSTACLE_MIN_SIZE, OBSTACLE_MAX_SIZE)  # Random size in pixels
        image_name = random.choice(METEOR_IMAGES)  # Random meteor image
        self.original_image = load_image(image_name)  # Load the meteor image
        self.image = self.original_image
        x = random.randint(0, WIDTH - size)
        self.rect = self.image.get_rect(bottomleft=(x, 0))  # Position the obstacle at a random x and above the screen
        self.speed = random.randint(2, 7)  # Random speed for the obstacle
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

    def is_off_screen(self):
        """Check if the obstacle has moved off the screen"""
        return self.rect.y > HEIGHT

    def draw(self, surface):
        """Draw the obstacle on the given surface"""
        surface.blit(self.image, self.rect)