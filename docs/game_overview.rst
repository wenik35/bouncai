=============
Game Overview
=============

BouncAI is an endless vertical jumping game where players control a character that automatically bounces from platform to platform while avoiding obstacles and enemies. The game is designed as a testbed for AI agent development.

Game Objective
-------------

The main objective is to achieve the highest possible score by guiding the character as far up as possible without:

1. Falling off the bottom of the screen
2. Colliding with enemies (birds)

Game Components
--------------

Character
~~~~~~~~~

- Automatically bounces upward when landing on platforms
- Controlled horizontally by the player (A/D keys)
- Cannot go beyond the screen edges
- Has gravity constantly pulling it downward

Platforms
~~~~~~~~~

- Randomly generated as the player progresses upward
- Vary in width (40-60 pixels) and horizontal position
- Two types:
  - Static platforms: Standard non-moving platforms
  - Moving platforms: Appear after reaching 500 points, move horizontally back and forth

Enemies
~~~~~~~

- Bird enemies appear after reaching 1500 points
- Fly horizontally across the screen
- Animated sprites with 8 animation frames
- Contact with an enemy results in game over

Scoring System
~~~~~~~~~~~~~

- Score increases proportionally to how high the player climbs
- High score is saved between game sessions in a score.txt file
- Current score and high score are displayed on screen

Game Progression
---------------

1. **Starting Phase (0-500 points)**:
   - Only static platforms
   - Focus on basic movement and jumping

2. **Intermediate Phase (500-1500 points)**:
   - Moving platforms introduced
   - Increased difficulty in landing

3. **Advanced Phase (1500+ points)**:
   - Bird enemies appear
   - Requires careful timing and positioning to avoid collisions

Game Over
---------

The game ends when either:
- The player falls below the bottom of the screen
- The player collides with a bird enemy

After game over:
- The screen fades to black
- Game Over screen appears showing final score
- Press Space to restart the game
- High score is updated if current score exceeds previous record

Game Interface
-------------

- Score panel at the top of the screen
- High score line displayed as a visual reference
- Game window dimensions: 400x600 pixels
- 60 FPS game loop for smooth gameplay
- High score is saved to a local file named 'score.txt'

Technical Details
----------------

- Built with Pygame
- Game physics include gravity (0.5 units per frame) and vertical velocity
- Sprite-based collision detection
- Pixel-perfect collision masking for enemies
- Installation via git clone and local pip installation only
