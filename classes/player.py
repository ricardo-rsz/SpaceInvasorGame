import pygame

from config import (
    HEIGHT,
    HIT_INVULNERABILITY_MS,
    MAX_PLAYER_LIVES,
    PLAYER_COLOR,
    PLAYER_LIVES,
    PLAYER_SPEED,
    SPEED_BOOST_MULTIPLIER,
    WIDTH,
)


class Player:
    """A player controlled with the keyboard, including lives and timed effects."""

    def __init__(self, x, y, color=PLAYER_COLOR, speed=PLAYER_SPEED):
        self.initial_position = (x, y)
        self.rect = pygame.Rect(x, y, 50, 50)
        self.color = color
        self.initial_speed = speed
        self.speed = speed
        self.lives = PLAYER_LIVES
        self.hit_invulnerable_until = 0
        self.speed_boost_until = 0
        self.shield_until = 0

    def is_alive(self):
        """Return whether this player still has lives."""
        return self.lives > 0

    def is_invulnerable(self, current_time=None):
        """Check hit protection from damage or a shield power-up."""
        if current_time is None:
            current_time = pygame.time.get_ticks()

        return (
            current_time < self.hit_invulnerable_until
            or current_time < self.shield_until
        )

    def take_hit(self, current_time=None):
        """Remove one life and start the two-second hit protection."""
        if current_time is None:
            current_time = pygame.time.get_ticks()

        if not self.is_alive() or self.is_invulnerable(current_time):
            return False

        self.lives -= 1
        self.hit_invulnerable_until = current_time + HIT_INVULNERABILITY_MS
        return True

    def add_life(self):
        """Restore one life, up to the configured maximum."""
        if self.lives < MAX_PLAYER_LIVES:
            self.lives += 1
            return True
        return False

    def activate_speed_boost(self, current_time, duration):
        """Enable a temporary movement speed increase."""
        self.speed_boost_until = max(self.speed_boost_until, current_time + duration)

    def activate_shield(self, current_time, duration):
        """Enable temporary protection from obstacle collisions."""
        self.shield_until = max(self.shield_until, current_time + duration)

    def update_effects(self, current_time):
        """Clear temporary effects when their time has expired."""
        if current_time >= self.speed_boost_until:
            self.speed_boost_until = 0
        if current_time >= self.shield_until:
            self.shield_until = 0
        if current_time >= self.hit_invulnerable_until:
            self.hit_invulnerable_until = 0

    def get_current_speed(self, current_time=None):
        """Return the normal speed or the boosted speed while active."""
        if current_time is None:
            current_time = pygame.time.get_ticks()

        if current_time < self.speed_boost_until:
            return self.speed * SPEED_BOOST_MULTIPLIER
        return self.speed

    def moveArrows(self, current_time=None):
        """Move the first player with the arrow keys."""
        if not self.is_alive():
            return

        if current_time is None:
            current_time = pygame.time.get_ticks()
        speed = self.get_current_speed(current_time)
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rect.x -= speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += speed
        if keys[pygame.K_UP]:
            self.rect.y -= speed
        if keys[pygame.K_DOWN]:
            self.rect.y += speed

        self._keep_inside_screen()

    def moveWASD(self, current_time=None):
        """Move the second player with the WASD keys."""
        if not self.is_alive():
            return

        if current_time is None:
            current_time = pygame.time.get_ticks()
        speed = self.get_current_speed(current_time)
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rect.x -= speed
        if keys[pygame.K_d]:
            self.rect.x += speed
        if keys[pygame.K_w]:
            self.rect.y -= speed
        if keys[pygame.K_s]:
            self.rect.y += speed

        self._keep_inside_screen()

    def _keep_inside_screen(self):
        """Keep the player rectangle inside the game window."""
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(WIDTH, self.rect.right)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(HEIGHT, self.rect.bottom)

    def change_speed(self, event):
        """Change the player's normal speed with the plus and minus keys."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_MINUS:
                self.speed = max(2, self.speed - 1)
            elif event.key in (pygame.K_PLUS, pygame.K_KP_PLUS, pygame.K_EQUALS):
                self.speed = min(12, self.speed + 1)

    def reset(self):
        """Restore the player's position, lives, speed and effects."""
        self.rect.topleft = self.initial_position
        self.speed = self.initial_speed
        self.lives = PLAYER_LIVES
        self.hit_invulnerable_until = 0
        self.speed_boost_until = 0
        self.shield_until = 0

    def draw(self, surface, current_time=None):
        """Draw the player and show a white outline while shielded."""
        if not self.is_alive():
            return

        if current_time is None:
            current_time = pygame.time.get_ticks()

        # Blinking makes the two-second hit protection visible.
        if self.is_invulnerable(current_time) and (current_time // 120) % 2 == 0:
            return

        pygame.draw.rect(surface, self.color, self.rect)
        if current_time < self.shield_until:
            pygame.draw.rect(surface, (255, 255, 255), self.rect, 3)
