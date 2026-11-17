import pygame

from config import HEIGHT, WIDTH


class Pause:
    """Pause and resume the game with the Escape key."""

    def __init__(self, screen):
        self.screen = screen
        self.paused = False
        self.font = pygame.font.Font(None, 74)
        self.text = self.font.render("PAUSE", True, (255, 255, 255))
        self.text_rect = self.text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    def handle_event(self, event):
        """Toggle the pause state when Escape is pressed."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.paused = not self.paused

    def draw(self):
        """Show the pause message."""
        if self.paused:
            self.screen.blit(self.text, self.text_rect)
