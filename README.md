# Mini Boss Fight 

A 2D boss game made with Python and Pygame.
The player must move across platforms, collect the sandwich power-up, avoid the boss's bullets, and defeat the boss before losing all 3 lives.

---

## Game Pitch

Mini Boss Fight is a small 2D platformer style boss battle.
At the start, the player cannot attack. The goal is to survive long enough to reach the sandwich power-up, which unlocks shooting. After that, the player can fight back against the boss.

The game includes jumping, gravity, one-way platforms, solid platforms, boss patrol movement, shooting, healt system, and win/lose states.

---

## How to Run

### Requirements
- python 3.8 or newer
- Pygame

install Pygame with:

'''bash
pip install pygame

---
### Run the game 
python dist/main.py

---

## CONTROLS
| Key | Action |
|---|---| 
| A | Move Left |
| D | Move right |
| Space | Jump |
| J | Shoot | 
| R | Restart (after Game Over or Victory) |


--- 


## Main Mechanics

- The player can move, jump, and land on platforms
- One-way platforms can be landed on from above, but passed through from below
- Solid platforms block the player from all sides
- The player starts without shooting
- Collecting the sandwich unlocks the player’s attack
- The boss patrols in a fixed area and shoots at the player
- The player has 3 lives
- The boss has 10 HP
- If the player loses all 3 lives, the game ends
- If the boss reaches 0 HP, the player wins


---

## File Structure 

CP-GameProject/
├── README.md        # Project documentation 
├── demo.mp4        # Short gameplay demo video
├── src/         
│   ├── assets/       # Development assets such as sprites, textures, and images   
│   ├── main.py       # Development version of the game
│   ├── sprites.py       # Player and Boss classes used during development
│   └── utils.py       # Optional helper file
└── dist/          
    ├── assets/       # Final verified assets used by the game 
    ├── main.py       # Finale stable version of the game
    ├── sprites.py        # Final stable class definitions
    └── utils.py        # Optional helper file for final version


---

## OOP Breakdown

### Player
The Player class stores the player's:
- position 
- collision rectangle
- vertical velocity
- ground state
- facing direction 
- hit count
- shooting ability

it also includes methods such as:
- reset()
- take_hit()
- jump()
- apply_gravity()

### Boss
- The Boss class stores the boss's:
- collision rectangle
- HP
- patrol movement values
- shooting cooldown
- patrol limits

It also includes methods such as:
- reset()
- update_movement()
- take_damage()

This use of classes helped organize the code better by grouping game data and behavior into objects instead of keeping everything as separate variables.


---


## AI Usage Statement

- AI was used as a support tool for debugging, code organization, and checking the final version of the project.
- I also learned some ideas and techniques by watching Pygame tutorials on YouTube.


---


## Future Improvements

Future Improvements would include:
- better player animation
- more visual polish for platforms and UI
- more advanced boss behavior
- sound effects
- background music