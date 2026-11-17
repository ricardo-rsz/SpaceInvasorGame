from config import SPAWN_OBSTACLE_DELAY


class Difficulty:
    """Increase the game difficulty as the shared score gets higher."""

    def __init__(self):
        self.score = 0
        self.spawn_obstacle_delay = SPAWN_OBSTACLE_DELAY
        self.level = 0

    def sum_score(self, points):
        """Add points and reduce the obstacle spawn delay at each level."""
        self.score += points
        new_level = self.score // 10

        if new_level > self.level:
            self.level = new_level
            new_delay = max(150, SPAWN_OBSTACLE_DELAY - self.level * 50)

            if new_delay < self.spawn_obstacle_delay:
                self.spawn_obstacle_delay = new_delay
                return True

        return False

    def reset(self):
        """Reset the score and difficulty for a new game."""
        self.score = 0
        self.spawn_obstacle_delay = SPAWN_OBSTACLE_DELAY
        self.level = 0


# Keep the original spelling available for existing imports.
Dificulty = Difficulty
