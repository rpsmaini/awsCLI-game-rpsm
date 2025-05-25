# Kung Fu Game

A Nintendo-style kung fu game built with Pygame.

## Controls

- **Left Arrow**: Move left
- **Right Arrow**: Move right
- **Up Arrow**: Jump
- **Down Arrow**: Dodge/Crouch
- **Space**: Punch
- **R**: Restart game (when game over)

## Game Features

- Player character with jumping, punching, and dodging abilities
- Enemy AI with different behaviors (patrol, chase, attack)
- Health system and scoring
- Game over and restart functionality

## How to Run

```bash
cd kungfu_game
python3 run.py
```

Or make it executable and run directly:

```bash
cd kungfu_game
./run.py
```

## Game Structure

- `run.py`: Entry point to start the game
- `game.py`: Main game loop and management
- `player.py`: Player character class and mechanics
- `enemy.py`: Enemy AI and behavior
- `assets/`: Directory for game assets (currently using placeholder graphics)

## Future Improvements

- Add sprite animations and proper graphics
- Add sound effects and music
- Implement different enemy types
- Add power-ups and special moves
- Create multiple levels with increasing difficulty
