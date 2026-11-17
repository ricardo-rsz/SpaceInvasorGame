import pygame

from config import (
    BACKGROUND_COLOR,
    FPS,
    HEIGHT,
    PLAYER_COLOR2,
    POWERUP_SPAWN_INTERVAL_MS,
    WIDTH,
)
from classes import *


# Initialize Pygame and create the game window.
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Two Player Survival Game")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 30)
small_font = pygame.font.Font(None, 24)

# Create the two keyboard-controlled players.
player = Player(375, 530)
player2 = Player(530, 530, PLAYER_COLOR2)
players = [player, player2]

obstacles = []
powerups = []

# Create the game managers.
pause = Pause(screen)
restart = Restart(screen)
difficulty = Difficulty()
score_manager = ScoreManager()
top_scores = score_manager.get_top_scores()
best_score = top_scores[0][1] if top_scores else 0

survival_time = 0.0
game_over = False
entering_name = False
score_saved = False
player_name = ""

current_time = pygame.time.get_ticks()
last_obstacle_spawn_time = current_time
last_powerup_spawn_time = current_time
last_timer_tick = current_time
difficulty_message_until = 0
powerup_message = ""
powerup_message_until = 0


# GAME LOOP
running = True
while running:
    current_time = pygame.time.get_ticks()

    # Handle keyboard and window events.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            continue

        # The name is entered directly in the Pygame window.
        if entering_name:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    score_manager.save_score(
                        player_name if player_name else "Player",
                        difficulty.score,
                    )
                    top_scores = score_manager.get_top_scores()
                    best_score = top_scores[0][1] if top_scores else 0
                    entering_name = False
                    score_saved = True
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                elif (
                    len(player_name) < 15
                    and event.unicode.isprintable()
                    and event.unicode not in ",\r\n"
                ):
                    player_name += event.unicode
            continue

        if not game_over:
            player.change_speed(event)
            player2.change_speed(event)
            pause.handle_event(event)
        elif score_saved and restart.handle_event(
            event, game_over, players, obstacles, powerups
        ):
            # Start a new game and reset all timers and temporary messages.
            game_over = False
            entering_name = False
            score_saved = False
            player_name = ""
            difficulty.reset()
            survival_time = 0.0
            pause.paused = False

            current_time = pygame.time.get_ticks()
            last_obstacle_spawn_time = current_time
            last_powerup_spawn_time = current_time
            last_timer_tick = current_time
            difficulty_message_until = 0
            powerup_message_until = 0
            powerup_message = ""

    current_time = pygame.time.get_ticks()

    # Update the game only when it is active and not paused.
    if not game_over and not pause.paused:
        survival_time += (current_time - last_timer_tick) / 1000

        for current_player in players:
            current_player.update_effects(current_time)

        # Spawn falling obstacles at the current difficulty rate.
        if current_time - last_obstacle_spawn_time >= difficulty.spawn_obstacle_delay:
            obstacles.append(Obstacle())
            last_obstacle_spawn_time = current_time

        # Spawn one power-up at regular intervals.
        if (
            not powerups
            and current_time - last_powerup_spawn_time >= POWERUP_SPAWN_INTERVAL_MS
        ):
            powerups.append(PowerUp())
            last_powerup_spawn_time = current_time

        # Move obstacles and remove one life on a valid collision.
        for obstacle in obstacles:
            obstacle.move()
            for current_player in players:
                if current_player.rect.colliderect(obstacle.rect):
                    current_player.take_hit(current_time)

        # Remove obstacles after they leave the screen and update the score.
        visible_obstacles = []
        for obstacle in obstacles:
            if not obstacle.is_off_screen():
                visible_obstacles.append(obstacle)
            elif difficulty.sum_score(1):
                difficulty_message_until = current_time + 2000
        obstacles = visible_obstacles

        # Move power-ups and apply their effect to the first player who collects them.
        visible_powerups = []
        for powerup in powerups:
            powerup.move()
            collected = False

            for current_player in players:
                if (
                    current_player.is_alive()
                    and current_player.rect.colliderect(powerup.rect)
                ):
                    powerup_message = powerup.apply_to(current_player, current_time)
                    powerup_message_until = current_time + 2000
                    collected = True
                    break

            if not collected and not powerup.is_off_screen():
                visible_powerups.append(powerup)
        powerups = visible_powerups

        # Both players must lose all their lives before the game ends.
        if all(not current_player.is_alive() for current_player in players):
            game_over = True

        # Move the players who still have at least one life.
        if not game_over:
            player.moveArrows(current_time)
            player2.moveWASD(current_time)

    last_timer_tick = current_time

    # Ask for a name once, after both players have run out of lives.
    if game_over and not score_saved and not entering_name:
        entering_name = True

    # DRAW EVERYTHING
    screen.fill(BACKGROUND_COLOR)

    for obstacle in obstacles:
        obstacle.draw(screen)
    for powerup in powerups:
        powerup.draw(screen)

    for current_player in players:
        current_player.draw(screen, current_time)

    # Show the shared score, best score, lives and player speeds.
    score_text = font.render(
        f"Score: {difficulty.score}  |  Best: {best_score}",
        True,
        (255, 255, 255),
    )
    screen.blit(score_text, (10, 10))

    lives_text = font.render(
        f"P1 Lives: {player.lives}     P2 Lives: {player2.lives}",
        True,
        (255, 255, 255),
    )
    screen.blit(lives_text, (10, 45))

    speed_text = small_font.render(
        f"Speed P1: {player.get_current_speed(current_time):.1f}  "
        f"P2: {player2.get_current_speed(current_time):.1f}",
        True,
        (200, 200, 200),
    )
    screen.blit(speed_text, (10, 80))

    time_text = font.render(
        f"Survival: {int(survival_time)} s", True, (255, 255, 255)
    )
    screen.blit(time_text, (500, 10))

    # Explain the symbols used by the three power-up types.
    legend = small_font.render(
        "Power-ups: S Speed   + Life   I Shield", True, (200, 200, 200)
    )
    screen.blit(legend, (10, HEIGHT - 28))

    # Show short messages when the difficulty changes or a power-up is collected.
    if current_time < difficulty_message_until:
        message = font.render("Increased difficulty!", True, (255, 255, 255))
        screen.blit(message, message.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 35)))

    if current_time < powerup_message_until:
        message = font.render(powerup_message, True, (255, 230, 80))
        screen.blit(message, message.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 5)))

    # Show the five highest saved scores.
    title = font.render("TOP 5", True, (255, 215, 0))
    screen.blit(title, (WIDTH - 170, 60))
    for index, (name, points) in enumerate(top_scores):
        text = small_font.render(f"{index + 1}. {name}: {points}", True, (255, 255, 255))
        screen.blit(text, (WIDTH - 190, 95 + index * 30))

    if entering_name:
        prompt = font.render("Enter name: " + player_name, True, (255, 255, 255))
        screen.blit(prompt, prompt.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        hint = small_font.render("Press ENTER to save the score", True, (200, 200, 200))
        screen.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 35)))
    elif game_over and score_saved:
        restart.draw()

    if pause.paused and not game_over:
        pause.draw()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
