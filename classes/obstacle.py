import random

import pygame

from config import HEIGHT, OBSTACLES_COLORS, WIDTH


class Obstacle:
    """A falling object that players must avoid."""

    def __init__(self):
        size = random.randint(20, 70)
        x = random.randint(0, WIDTH - size)
        self.rect = pygame.Rect(x, -size, size, size)
        self.color = random.choice(OBSTACLES_COLORS)
        self.speed = random.randint(2, 7)

    def move(self):
        """Move the obstacle down the screen."""
        self.rect.y += self.speed

    def is_off_screen(self):
        """Check whether the obstacle has left the game window."""
        return self.rect.top > HEIGHT

    def draw(self, surface):
        """Draw the obstacle."""
        pygame.draw.rect(surface, self.color, self.rect)
