import pygame

from assets import load_image, load_sound
from background import draw_background
from config import *
from enemy import Enemy
from laser import Laser
from obstacle import Obstacle
from player import Player
from powerup import PowerUp
from scores import save_score, top_scores


class Game:
    """Owns the game state and coordinates the game loop."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Moving Player Game")
        self.clock = pygame.time.Clock()
        self.background = pygame.transform.scale(load_image(BACKGROUND_IMAGE, WIDTH), (WIDTH, HEIGHT))

        self.laser_sound = load_sound(LASER_SOUND)
        self.meteor_explosion_sound = load_sound(METEOR_EXPLOSION_SOUND)
        self.player_explosion_sound = load_sound(PLAYER_EXPLOSION_SOUND)
        self.powerup_activate_sound = load_sound(POWERUP_ACTIVATE_SOUND)
        self.powerup_deactivate_sound = load_sound(POWERUP_DEACTIVATE_SOUND)

        self.player = Player(375, 530)
        self.player2 = Player(445, 530, PLAYER_COLOR2, 2, PLAYER2_IMAGE, DAMAGE_PLAYER_IMAGE2)
        self.active_players = []
        self.num_players = 1

        self.obstacles = []
        self.enemies = []
        self.powerups = []
        self.laser = pygame.sprite.Group()
        self.enemy_lasers = pygame.sprite.Group()
        self.last_laser_fire_times = {
            self.player: -LASER_FIRE_DELAY,
            self.player2: -LASER_FIRE_DELAY,
        }

        self.selecting_players = True
        self.game_over = False
        self.paused = False
        self.entering_name = False
        self.player_name = ""
        self.running = True

        self.game_time = 0
        self.last_obstacle_spawn_time = 0
        self.last_enemy_spawn_time = 0
        self.last_powerup_spawn_time = 0
        self.survival_time = 0
        self.background_y1 = 0
        self.background_y2 = -HEIGHT
        self.background_speed = 5

        self.score = 0
        self.best_scores = top_scores()
        self.high_score = self.best_scores[0][1] if self.best_scores else 0
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 26)

    def run(self):
        """Run the game until the window is closed."""
        try:
            while self.running:
                dt = self.clock.tick(FPS)
                self.handle_events()
                self.update(dt)
                self.draw()
        finally:
            pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif self.selecting_players:
                self.handle_player_selection(event)
            elif self.entering_name:
                self.handle_name_entry(event)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and not self.game_over:
                self.paused = not self.paused
            elif event.type == pygame.KEYDOWN and not self.game_over and not self.paused:
                self.handle_game_key(event)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r and self.game_over:
                self.restart()

    def handle_player_selection(self, event):
        if event.type != pygame.KEYDOWN or event.unicode not in ("1", "2"):
            return
        self.num_players = int(event.unicode)
        self.active_players = [self.player, self.player2] if self.num_players == 2 else [self.player]
        self.selecting_players = False
        self.game_time = 0
        self.last_obstacle_spawn_time = 0
        self.last_enemy_spawn_time = 0
        self.last_powerup_spawn_time = 0

    def handle_name_entry(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            save_score(self.player_name.strip() or DEFAULT_PLAYER_NAME, self.score)
            self.best_scores = top_scores()
            self.entering_name = False
        elif event.key == pygame.K_BACKSPACE:
            self.player_name = self.player_name[:-1]
        elif event.unicode.isprintable() and event.unicode not in ("", ";") and len(self.player_name) < MAX_NAME_LENGTH:
            self.player_name += event.unicode

    def handle_game_key(self, event):
        if event.key in (pygame.K_PLUS, pygame.K_KP_PLUS) or event.unicode == "+":
            self.player.change_speed(PLAYER_SPEED_STEP)
            self.player2.change_speed(PLAYER_SPEED_STEP)
        elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS) or event.unicode == "-":
            self.player.change_speed(-PLAYER_SPEED_STEP)
            self.player2.change_speed(-PLAYER_SPEED_STEP)

    def restart(self):
        self.score = 0
        self.obstacles = []
        self.enemies = []
        self.powerups = []
        self.laser.empty()
        self.enemy_lasers.empty()
        self.last_laser_fire_times = {
            self.player: -LASER_FIRE_DELAY,
            self.player2: -LASER_FIRE_DELAY,
        }
        for each_player in (self.player, self.player2):
            each_player.reset_position()
            each_player.reset_lives()
            each_player.reset_effects()
        self.player.reset_speed()
        self.survival_time = 0
        self.game_over = False
        self.entering_name = False
        self.selecting_players = True

    def update(self, dt):
        if self.selecting_players or self.game_over or self.paused:
            return

        self.game_time += dt
        self.survival_time = self.game_time // 1000
        self.spawn_entities()
        alive_players = [player for player in self.active_players if player.is_alive()]
        self.update_player_effects(alive_players)
        self.update_powerups(alive_players)
        self.update_obstacles(alive_players)
        self.update_enemies(alive_players)
        self.update_players()
        self.fire_player_lasers(alive_players)

        if not any(player.is_alive() for player in self.active_players):
            self.game_over = True
            self.entering_name = True
            self.player_name = ""

    def spawn_entities(self):
        difficulty_level = self.score // POINTS_PER_DIFFICULTY_LEVEL
        spawn_delay = max(
            MIN_SPAWN_OBSTACLE_DELAY,
            SPAWN_OBSTACLE_DELAY - difficulty_level * SPAWN_DELAY_DECREASE,
        )
        if self.game_time - self.last_obstacle_spawn_time > spawn_delay:
            self.obstacles.append(Obstacle())
            self.last_obstacle_spawn_time = self.game_time
        if self.game_time - self.last_enemy_spawn_time > ENEMY_SPAWN_DELAY:
            self.enemies.append(Enemy())
            self.last_enemy_spawn_time = self.game_time
        if self.game_time - self.last_powerup_spawn_time > POWERUP_SPAWN_DELAY:
            self.powerups.append(PowerUp())
            self.last_powerup_spawn_time = self.game_time

    def update_player_effects(self, alive_players):
        for player in alive_players:
            if player.update_effects(self.game_time):
                self.powerup_deactivate_sound.play()

    def update_powerups(self, alive_players):
        remaining_powerups = []
        for powerup in self.powerups:
            powerup.move()
            collector = next(
                (player for player in alive_players if player.rect.colliderect(powerup.rect)),
                None,
            )
            if collector:
                powerup.apply(collector, self.game_time)
                self.powerup_activate_sound.play()
            elif not powerup.is_off_screen():
                remaining_powerups.append(powerup)
        self.powerups = remaining_powerups

    def update_obstacles(self, alive_players):
        for obstacle in self.obstacles:
            obstacle.move()
            for player in alive_players:
                if pygame.sprite.collide_mask(player, obstacle) and player.take_hit(self.game_time):
                    self.player_explosion_sound.play()

        self.laser.update()
        remaining_obstacles = []
        for obstacle in self.obstacles:
            hit_by_laser = False
            for shot in self.laser.sprites():
                if pygame.sprite.collide_mask(shot, obstacle):
                    shot.kill()
                    hit_by_laser = True
                    self.meteor_explosion_sound.play()
                    remaining_obstacles.extend(obstacle.split())
                    self.add_score(2)
                    break
            if not hit_by_laser and not obstacle.is_off_screen():
                remaining_obstacles.append(obstacle)
            elif not hit_by_laser:
                self.add_score(2)
        self.obstacles = remaining_obstacles

    def update_enemies(self, alive_players):
        for enemy in self.enemies:
            enemy.move()
            if enemy.should_fire(self.game_time):
                self.enemy_lasers.add(enemy.fire())
                self.laser_sound.play()

        self.enemy_lasers.update()
        for shot in self.enemy_lasers.sprites():
            for player in alive_players:
                if pygame.sprite.collide_mask(shot, player):
                    shot.kill()
                    if player.take_hit(self.game_time):
                        self.player_explosion_sound.play()
                    break

        remaining_enemies = []
        for enemy in self.enemies:
            hit_by_laser = False
            for shot in self.laser.sprites():
                if pygame.sprite.collide_mask(shot, enemy):
                    shot.kill()
                    hit_by_laser = True
                    self.meteor_explosion_sound.play()
                    self.add_score(3)
                    break
            if not hit_by_laser and not enemy.is_off_screen():
                remaining_enemies.append(enemy)
        self.enemies = remaining_enemies

    def update_players(self):
        if self.player.is_alive():
            self.player.moveArrows()
        if self.num_players == 2 and self.player2.is_alive():
            self.player2.moveWASD()

    def fire_player_lasers(self, alive_players):
        for player in alive_players:
            if self.game_time - self.last_laser_fire_times[player] >= LASER_FIRE_DELAY:
                self.laser.add(Laser(player.rect.centerx, player.rect.top))
                self.laser_sound.play()
                self.last_laser_fire_times[player] = self.game_time

    def add_score(self, points):
        self.score += points
        self.high_score = max(self.high_score, self.score)

    def draw(self):
        self.background_y1, self.background_y2 = draw_background(
            self.screen,
            self.background,
            self.background_y1,
            self.background_y2,
            self.background_speed,
        )
        if self.selecting_players:
            self.draw_player_selection()
            pygame.display.flip()
            return

        for player in self.active_players:
            if player.is_alive() or player.death_animation_active():
                player.draw(self.screen, self.game_time)
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        for shot in self.laser:
            self.screen.blit(shot.image, shot.rect)
        for shot in self.enemy_lasers:
            self.screen.blit(shot.image, shot.rect)
        for powerup in self.powerups:
            powerup.draw(self.screen, self.small_font)

        self.draw_hud()
        pygame.display.flip()

    def draw_player_selection(self):
        title_text = self.font.render("Number of players?", True, (255, 255, 255))
        options_text = self.font.render("Press 1 or 2", True, (255, 255, 255))
        self.screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - title_text.get_height()))
        self.screen.blit(options_text, (WIDTH // 2 - options_text.get_width() // 2, HEIGHT // 2 + 10))

        ranking_y = HEIGHT // 2 + 70
        ranking_title = self.font.render(f"TOP {TOP_SCORES_COUNT}", True, (255, 215, 0))
        self.screen.blit(ranking_title, (WIDTH // 2 - ranking_title.get_width() // 2, ranking_y))
        if not self.best_scores:
            empty_text = self.small_font.render("No scores yet", True, (200, 200, 200))
            self.screen.blit(empty_text, (WIDTH // 2 - empty_text.get_width() // 2, ranking_y + 40))
        for position, (name, saved_score) in enumerate(self.best_scores, start=1):
            entry_text = self.small_font.render(f"{position}. {name}  {saved_score}", True, (255, 255, 255))
            self.screen.blit(entry_text, (WIDTH // 2 - entry_text.get_width() // 2, ranking_y + 10 + position * 28))

    def draw_hud(self):
        score_text = self.font.render(f"Score: {self.score}    High Score: {self.high_score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        time_text = self.font.render(f"Time: {self.survival_time}s", True, (255, 255, 255))
        self.screen.blit(time_text, (10, 40))

        speed_label = f"Speed P1: {self.player.current_speed()}"
        if self.num_players == 2:
            speed_label += f"  P2: {self.player2.current_speed()}"
        self.screen.blit(self.font.render(speed_label, True, (255, 255, 255)), (10, 70))

        lives_y = 100
        for index, player in enumerate(self.active_players, start=1):
            lives_text = self.font.render(f"P{index} Lives: {player.lives}", True, player.color)
            self.screen.blit(lives_text, (10, lives_y))
            effects = []
            if player.speed_boost:
                effects.append(f"SPEED {(player.speed_boost_until - self.game_time) // 1000 + 1}s")
            if player.has_shield(self.game_time):
                effects.append(f"SHIELD {(player.shield_until - self.game_time) // 1000 + 1}s")
            if effects:
                effects_text = self.small_font.render("  ".join(effects), True, player.color)
                self.screen.blit(effects_text, (lives_text.get_width() + 25, lives_y + 4))
            lives_y += 30

        if self.game_over:
            self.draw_game_over()
        if self.paused:
            pause_text = self.font.render("PAUSE", True, (255, 255, 255))
            self.screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - pause_text.get_height() // 2))

    def draw_game_over(self):
        game_over_text = self.font.render("Game Over", True, (255, 0, 0))
        self.screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
        if self.entering_name:
            cursor = "_" if (pygame.time.get_ticks() // 500) % 2 == 0 else " "
            name_text = self.font.render(f"Enter your name: {self.player_name}{cursor}", True, (255, 255, 255))
            self.screen.blit(name_text, (WIDTH // 2 - name_text.get_width() // 2, HEIGHT // 2 + game_over_text.get_height()))
            hint_text = self.small_font.render("Press ENTER to save", True, (200, 200, 200))
            self.screen.blit(hint_text, (WIDTH // 2 - hint_text.get_width() // 2, HEIGHT // 2 + game_over_text.get_height() + 40))
        else:
            restart_text = self.font.render("Press R to restart", True, (255, 255, 255))
            self.screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + game_over_text.get_height()))
