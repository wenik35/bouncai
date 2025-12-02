=====
Usage
=====

Running the Game
---------------

To play BouncAI after installation, make sure your virtual environment is activated first::

    # Activate virtual environment (Windows)
    venv\Scripts\activate

    # Activate virtual environment (macOS/Linux)
    source venv/bin/activate

    # Then run the game
    python -m bouncai

Game Controls
------------

- **A key**: Move left
- **D key**: Move right
- **Space bar**: Restart the game after Game Over
- **Close window**: Exit the game

Game Mechanics
-------------

1. **Character Movement**: The character automatically bounces upward when landing on platforms
2. **Platform Types**:
   - Regular platforms: Static and safe to land on
   - Moving platforms: Appear after 500 points and move horizontally
3. **Enemies**: Bird enemies appear after 1500 points and must be avoided
4. **Scoring**: Score increases as you climb higher
5. **Game Over**: Occurs when you fall off the bottom of the screen or collide with an enemy

High Score System
---------------

The game automatically saves your highest score to a file called `score.txt` in the game directory.

Using BouncAI as a Library
-------------------------

To use BouncAI in your own Python project (with your virtual environment activated)::

    from bouncai import bouncai

    # Run the game
    bouncai.run()

Remember that any project using BouncAI should also use a virtual environment to manage dependencies properly.
