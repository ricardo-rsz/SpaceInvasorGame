# Space Invaders PyGame

A 2D space arcade game built with [Pygame](https://www.pygame.org/). The game combines meteorite avoidance, automatic player weapons, enemy ships, power-ups, lives, sound effects, and a persistent high-score table.

## Game overview

- The game window is 800x600 pixels and runs at 60 FPS.
- At the start of each round, players choose one or two local players.
- Player 1 uses the blue ship and the arrow keys.
- Player 2 uses a different orange ship model and the WASD keys.
- Both players fire lasers automatically while they are alive.
- Meteorites fall from the top of the screen and rotate as they move.
- Enemy ships appear during the round and fire red lasers downward.
- The game ends when every active player loses all lives.

## Main features

### Background and movement

- A space background is scaled to the game window.
- Two copies of the background scroll vertically to create a continuous moving effect.
- Players are kept inside the screen boundaries.

### Meteorites

- Meteorites spawn at random horizontal positions.
- Their speed and rotation direction are randomized.
- Pixel masks provide precise collisions based on visible pixels.
- A player laser destroys a meteorite and awards bonus points.
- A destroyed meteorite splits into two smaller fragments.
- Fragments keep moving and rotating but cannot split again.
- Meteorites that leave the bottom of the screen award survival points.

### Player weapons

- Each living player fires automatically at regular intervals.
- Player lasers travel upward.
- Player lasers can destroy meteorites, fragments, and enemy ships.
- Laser collisions use pixel masks instead of only rectangular bounds.

### Enemy ships

- Enemy ships use different enemy sprites selected at random.
- They enter from the top of the screen and move downward.
- Each enemy fires red lasers at regular intervals.
- Enemy laser collisions can remove player lives.
- Player lasers can destroy enemy ships for additional points.

### Lives and damage

- Each player starts with three lives.
- A collision removes one life unless the player is invulnerable.
- Players become temporarily invulnerable after taking damage.
- Invulnerable players blink.
- When a player loses the last life, the death sprites are shown in this order:
  `3 -> 2 -> 1`.
- The game ends only when all active players are out of lives.

### Power-ups

Power-ups appear periodically and are collected by the first living player that touches them.

| Power-up | Effect |
|---|---|
| Speed | Increases speed temporarily. |
| Life | Restores one life, up to the maximum. |
| Shield | Makes the player temporarily invulnerable. |

Power-up timers are displayed next to the players' lives. Effects stop counting during a pause.

### Sound effects

The game includes sounds for:

- Player and enemy laser shots.
- Meteorite and enemy explosions.
- Player damage.
- Power-up activation.
- Power-up expiration.

### Score and difficulty

- Dodging a meteorite awards survival points.
- Destroying a meteorite awards bonus points.
- Destroying an enemy ship awards additional points.
- The current score and high score are shown in the HUD.
- Meteorites spawn more frequently as the score increases.
- The spawn delay has a minimum limit.

### Pause and restart

- Press `ESC` to pause or resume the game.
- The game clock, entity movement, spawning, and temporary effects stop while paused.
- After Game Over, press `R` to reset the round.
- Restarting clears entities, restores players, resets lives and effects, and returns to player selection.

### Saved scores

- After Game Over, the player can enter a name.
- Press `ENTER` to save the score.
- The top five scores are shown on the player-selection screen.
- Scores are stored in `scores.txt`.
- `scores.txt` is ignored by Git because it contains local player data.

## Requirements and installation

- Python 3.8 or newer.
- Pygame.

Install Pygame:

```bash
pip install pygame
```

Run the game from the `SpaceInvadersNew` directory:

```bash
python main.py
```

## Controls

| Action | Player 1 | Player 2 |
|---|---|---|
| Move up | Up arrow | W |
| Move down | Down arrow | S |
| Move left | Left arrow | A |
| Move right | Right arrow | D |
| Increase speed | `+` | `+` |
| Decrease speed | `-` | `-` |
| Pause/resume | `ESC` | `ESC` |
| Restart after Game Over | `R` | `R` |
| Select one or two players | `1` / `2` | - |
| Enter the score name | Keyboard + `ENTER` | - |
| Quit | Close the window | - |

The lasers do not require a firing key because both players fire automatically.

## Project structure

| File | Description |
|---|---|
| `main.py` | Application entry point. |
| `game.py` | Game state, event handling, updates, collisions, rendering, and HUD. |
| `config.py` | Central game constants and asset names. |
| `background.py` | Scrolling background helper. |
| `assets.py` | Image and sound loading with caching. |
| `player.py` | Player movement, speed, lives, power-up effects, masks, and death animation. |
| `laser.py` | Upward player lasers and downward enemy lasers. |
| `obstacle.py` | Rotating meteorites, pixel masks, movement, and fragments. |
| `enemy.py` | Enemy ships, movement, masks, and firing behavior. |
| `powerup.py` | Speed, life, and shield power-ups. |
| `scores.py` | High-score loading, sorting, and saving. |
| `assets/` | Images, sounds, fonts, and other game resources. |

## Exercises and implemented challenges

### Exercise 1: Game background

The background image is loaded, scaled to the window size, and drawn behind the game entities.

### Exercise 2: Player lasers and bonus points

Players fire automatically. A laser that hits a meteorite destroys it and awards bonus points.

### Exercise 3: Sound effects

Sound effects are used for shots, meteorite explosions, player damage, and power-up activation or expiration.

### Exercise 4: Rotating meteorites and precise collisions

Meteorites rotate while moving. Pixel masks are refreshed after rotation so transparent pixels do not count as collisions.

### Exercise 5: Splitting meteorites

A meteorite hit by a player laser splits into two smaller fragments. Fragments cannot split again.

### Exercise 6: Enemy ships that fire

Enemy ships appear during the game and fire red lasers downward. Player lasers can destroy them.

### Exercise 7: Moving background

Two background images move vertically and wrap around to produce a continuous scrolling effect.

### Additional implemented systems

The project also includes:

1. Screen boundaries for both players.
2. Random meteorite sizes and speeds.
3. Two-player collision handling.
4. Pause and resume behavior.
5. In-game restart flow.
6. Survival time tracking.
7. Progressive meteorite difficulty.
8. Adjustable player speed.
9. In-memory and saved high scores.
10. One- or two-player selection.
11. Player lives, invulnerability, blinking, and death animation.
12. Speed, life, and shield power-ups.
13. Name entry and persistent top-five scores.

## Scoring rules

| Event | Points |
|---|---:|
| Meteorite leaves the screen | +2 |
| Player destroys a meteorite | +2 |
| Player destroys an enemy ship | +3 |

The score values are defined by the game logic in `game.py` and can be adjusted there if needed.
