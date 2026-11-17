Two-Player Survival Game
Game description
This project is a two-player survival game developed with Python and Pygame. Both players must avoid the obstacles that fall from the top of the screen. Players earn points when obstacles pass off the bottom of the screen. As the shared score increases, the game becomes more difficult.

https://github.com/user-attachments/assets/1710876c-b08a-457b-920f-6c905980db86

The players share one score, but each player has their own position, lives, movement speed, and temporary effects.
Requirements and installation
You need Python 3 and the pygame-ce library.
1. Open a terminal in the SpaceInvadersGame folder.
2. Install the dependency:
   pip install -r requirements.txt
3. Start the game:
   python main.py
Controls
Action	Keys
Move Player 1	Arrow keys
Move Player 2	W, A, S, D
Increase normal movement speed	+ or =
Decrease normal movement speed	-
Pause or resume the game	Esc
Restart after Game Over	R
Enter a name on the high-score screen	Letters and numbers; Backspace deletes a character and Enter saves the score


The + and - keys change the normal speed of both players. A speed boost collected from a power-up is temporary and is applied on top of the player's normal speed.
Additional challenges implemented
Challenge 10: Lives System
What it does
- Each player starts the game with 3 lives.
- When an obstacle hits a player, that player loses one life instead of the game ending immediately.
- After being hit, the player is protected from further obstacle damage for 2 seconds. This prevents one collision from removing several lives.
- The game only ends when both players have lost all their lives. If one player loses all their lives first, the other player can continue playing.
- The remaining lives of both players are displayed on the screen.
How it is implemented

The lives system is implemented in the Player class in classes/player.py:
- The lives attribute stores the player's remaining lives. It is initialized with PLAYER_LIVES, which is set to 3 in config.py.
- is_alive() checks whether the player still has at least one life.
- take_hit() first checks whether the player is alive and whether they are already invulnerable. If the player can take damage, the method removes one life and sets the end time of the protection period.
- is_invulnerable() checks both types of protection: the 2-second protection after a hit and the temporary shield provided by a power-up.
- update_effects() clears protection states when their time has expired.
In main.py, colliderect() detects contact between a player's rectangle and an obstacle's rectangle. When a collision occurs, the game calls take_hit(). The game uses all() to check whether both players have run out of lives before setting the game-over state.

The hit-protection time is configured with HIT_INVULNERABILITY_MS = 2000 in config.py. The time values are measured in milliseconds.
Challenge 11: Power-ups
What it does

Collectible objects fall down the screen. A player can collect an object by touching it. There are three types:
Symbol	Power-up	Effect
S	Speed	Multiplies the player's normal movement speed by 1.7 for 5 seconds.
+	Life	Adds one life, up to a maximum of 5 lives.
I	Shield	Protects the player from obstacle damage for 5 seconds.


Only one power-up can be active on the screen at a time. The game attempts to create a new one every 9 seconds. If no player collects it, it disappears after leaving the bottom of the window. If both players touch the same power-up during the same update, the first player checked in the players list collects it.

How it is implemented

The separate PowerUp class was created in classes/powerUp.py. This class is responsible for:
- Choosing a random power-up type (speed, life, or shield).
- Creating the object's position, size, colour, and symbol.
- Moving it down the screen with move().
- Checking whether it has left the screen with is_off_screen().
- Drawing it with draw().
- Applying its effect to the player who collects it with apply_to().
The PowerUp class does not directly manage all of the player's data. When an object is collected, it calls the appropriate method from the Player class:
- activate_speed_boost() enables the temporary speed increase.
- add_life() restores one life if the player is below the maximum.
- activate_shield() enables temporary protection from obstacle damage.
The Player class stores the time when each temporary effect should end. update_effects() checks the current time and clears expired effects automatically. This means that the effects do not need to be removed manually.

In main.py, the game controls when power-ups appear, moves them, and checks for collisions with the players. When a player collects one, the game applies its effect and displays a short message.

The spawn interval, movement speed, effect durations, and maximum number of lives are configured in config.py using POWERUP_SPAWN_INTERVAL_MS, POWERUP_SPEED, SPEED_BOOST_MULTIPLIER, SPEED_BOOST_DURATION_MS, POWERUP_SHIELD_DURATION_MS, and MAX_PLAYER_LIVES.
Challenge 12: Save High Scores to a File
What it does
- High scores are saved in scores.txt, so they are still available after the game is closed.
- When a game ends, Pygame displays a text-entry prompt inside the game window.
- The player types a name and presses Enter to save the score. Backspace deletes the last character.
- Scores are sorted from highest to lowest. The five highest scores are displayed when the game starts and during gameplay.
Both players share one score in this game. For that reason, the game asks for one name at the end of the match and saves the shared score under that name.

How it is implemented

The ScoreManager class, defined in classes/saveScore.py, manages the score file:
- __init__() prepares the path to scores.txt and loads the saved results.
- load_scores() reads the file, converts scores to integers, and ignores lines that do not have a valid format.
- save_score(name, score) adds the new result, sorts the list, and writes the scores to the file.
- get_top_scores() returns the five highest scores.
Each line in scores.txt contains a name and a score separated by a comma. For example:
Alex,45
Sam,32
Taylor,20
In main.py, the entering_name and player_name variables control the text-entry process. Keyboard events allow the user to type, delete, or confirm the name. When Enter is pressed, score_manager.save_score() is called with the name and the match score. The Top 5 list is then updated.

The ScoreManager class stores all recorded scores in the file. The get_top_scores() method limits the list displayed on the screen to five results.
Project structure
SpaceInvadersGame/
├── main.py                 # Main game loop and coordination
├── config.py               # Window settings and configurable values
├── requirements.txt        # Python dependencies
├── scores.txt              # Saved high scores
├── README.md               # Project documentation
└── classes/
    ├── __init__.py         # Imports the classes in this package
    ├── player.py           # Player class: movement, lives, and effects
    ├── obstacle.py         # Obstacle class: falling obstacles
    ├── powerUp.py          # PowerUp class: collectible special objects
    ├── difficulty.py       # Difficulty class: score and difficulty level
    ├── pause.py            # Pause class: pause and resume the game
    ├── restart.py          # Restart class: reset the match
    └── saveScore.py        # ScoreManager class: load and save high scores
Main classes
- Player: represents one player. It stores the player's position, movement speed, and lives. It also controls movement, hit protection, and temporary power-up effects.
- Obstacle: creates, moves, and draws the obstacles that players must avoid.
- PowerUp: creates the special objects and applies the appropriate effect to the player who collects one.
- Difficulty: manages the shared score and increases the difficulty as points are earned. Every 10 points, it reduces the delay between obstacle spawns, down to a minimum delay of 150 milliseconds.
- Pause: pauses or resumes the game when Esc is pressed.
- Restart: restores the players to their initial state and removes the obstacles and power-ups from the previous match.
- ScoreManager: loads, sorts, and saves scores in scores.txt.
main.py coordinates these classes. It handles keyboard and window events, updates game objects, detects collisions, checks whether the game has ended, and draws the game information on the screen.
