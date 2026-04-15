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
- If the player loses all lives, the game ends
- If the boss reaches 0 HP, the player wins
