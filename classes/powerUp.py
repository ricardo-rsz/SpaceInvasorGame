import random
import pygame

from config import (
    HEIGHT,
    POWERUP_SHIELD_DURATION_MS,
    POWERUP_SPEED,
    SPEED_BOOST_DURATION_MS,
    WIDTH,
)


class PowerUp:
    """A collectible object that gives a player a special effect."""

    TYPES = ("speed", "life", "shield")
    COLORS = {
        "speed": (255, 220, 0),
        "life": (0, 220, 100),
        "shield": (80, 200, 255),
    }
    LABELS = {"speed": "S", "life": "+", "shield": "I"}

    def __init__(self, kind=None):
        self.kind = kind if kind in self.TYPES else random.choice(self.TYPES)
        self.rect = pygame.Rect(random.randint(20, WIDTH - 44), -32, 32, 32)
        self.speed = POWERUP_SPEED
        self.color = self.COLORS[self.kind]
        self.font = pygame.font.Font(None, 24)

    def move(self):
        """Move the power-up down the screen."""
        self.rect.y += self.speed

    def is_off_screen(self):
        """Check whether the power-up has left the game window."""
        return self.rect.top > HEIGHT

    def apply_to(self, player, current_time):
        """Apply this power-up to the player who collected it."""
        if self.kind == "speed":
            player.activate_speed_boost(current_time, SPEED_BOOST_DURATION_MS)
            return "Speed boost!"

        if self.kind == "life":
            if player.add_life():
                return "Extra life!"
            return "Lives are already full"

        player.activate_shield(current_time, POWERUP_SHIELD_DURATION_MS)
        return "Shield activated!"

    def draw(self, surface):
        """Draw the power-up as a coloured circle with a short label."""
        center = self.rect.center
        pygame.draw.circle(surface, self.color, center, self.rect.width // 2)
        pygame.draw.circle(surface, (255, 255, 255), center, self.rect.width // 2, 2)
        label = self.font.render(self.LABELS[self.kind], True, (0, 0, 0))
        surface.blit(label, label.get_rect(center=center))
