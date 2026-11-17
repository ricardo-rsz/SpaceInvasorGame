import pygame

from config import HEIGHT, WIDTH


class Restart:
    """Restart the game after the final score has been saved."""

    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 40)
        self.text = self.font.render(
            "GAME OVER - PRESS R TO RESTART", True, (255, 255, 255)
        )
        self.text_rect = self.text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    def handle_event(self, event, game_over, players, obstacles, powerups=None):
        """Reset players and clear falling objects when R is pressed."""
        if not game_over or event.type != pygame.KEYDOWN or event.key != pygame.K_r:
            return False

        for player in players:
            player.reset()

        obstacles.clear()
        if powerups is not None:
            powerups.clear()
        return True

    def draw(self):
        """Show the restart instruction."""
        self.screen.blit(self.text, self.text_rect)
