=============
API Reference
=============

This section provides detailed documentation for the main modules and classes of the BouncAI game. It is intended for developers who want to understand the codebase, extend the game's functionality, or create AI agents to play the game. BouncAI is only available via git clone and local installation, not through PyPI.

Main Module
-----------

bouncai.bouncai
~~~~~~~~~~~~~~

.. py:function:: run()

   Run the BouncAI game.

   This function initializes pygame, sets up the game window, loads assets,
   and runs the main game loop. It handles all game mechanics including:

   - Game initialization (pygame, display, audio)
   - Asset loading (images, sounds, music)
   - High score tracking
   - Main game loop execution
   - Game over screen and restart functionality
   - Event handling

   :return: None

Game World
----------

bouncai.world.world
~~~~~~~~~~~~~~~~~~

.. py:class:: World(background_image, platform_image, enemy_sheet)

   World class that manages the game environment.

   This class handles the game background, platforms, enemies, and game state.
   It manages the scrolling of the game world, score tracking, and game over state.

   :param background_image: Background image surface
   :type background_image: pygame.Surface
   :param platform_image: Platform image surface
   :type platform_image: pygame.Surface
   :param enemy_sheet: Sprite sheet for enemy animations
   :type enemy_sheet: SpriteSheet

   .. py:method:: draw_bg(screen)

      Draw the scrolling background.

      :param screen: Surface to draw the background on
      :type screen: pygame.Surface

   .. py:method:: draw(screen)

      Draw all game elements to the screen.

      :param screen: Surface to draw all game elements on
      :type screen: pygame.Surface

   .. py:method:: update(scroll)

      Update all game elements.

      Calls individual update methods for background, platforms, and enemies.
      Updates the player score based on scroll amount.

      :param scroll: Amount to scroll the game world by
      :type scroll: int

Game Entities
------------

bouncai.world.player
~~~~~~~~~~~~~~~~~~~

.. py:class:: Player(world, x, y, player_image, jump_sound)

   Player class that manages the player character.

   This class handles player movement, gravity, collision detection with platforms,
   and rendering of the player sprite. It manages player jumping, horizontal movement,
   and interactions with the game world.

   :param world: Reference to the game world
   :type world: World
   :param x: Initial x-coordinate position
   :type x: int
   :param y: Initial y-coordinate position
   :type y: int
   :param player_image: Image for the player sprite
   :type player_image: pygame.Surface
   :param jump_sound: Sound effect for jumping
   :type jump_sound: pygame.mixer.Sound

   .. py:method:: move()

      Handle player movement and physics.

      Processes keyboard input for horizontal movement, applies gravity,
      handles platform collisions, and determines screen scrolling.

      :return: The amount the screen should scroll based on player position
      :rtype: int

   .. py:method:: draw(screen)

      Draw the player sprite on the screen.

      :param screen: Surface to draw the player on
      :type screen: pygame.Surface

bouncai.world.platform
~~~~~~~~~~~~~~~~~~~~~

.. py:class:: Platform(x, y, width, moving, platform_image)

   Platform class that represents the platforms the player can jump on.

   This class handles the creation and behavior of platforms in the game,
   including moving platforms that travel side to side.

   :param x: Initial x-coordinate position
   :type x: int
   :param y: Initial y-coordinate position
   :type y: int
   :param width: Width of the platform
   :type width: int
   :param moving: Whether the platform should move horizontally
   :type moving: bool
   :param platform_image: Image for the platform sprite
   :type platform_image: pygame.Surface

   .. py:method:: update(scroll)

      Update the platform position and movement.

      Handles horizontal movement for moving platforms and vertical
      scrolling for all platforms. Removes platforms that go off-screen.

      :param scroll: Amount to scroll the platform vertically
      :type scroll: int

bouncai.world.enemy
~~~~~~~~~~~~~~~~~~

.. py:class:: Enemy(SCREEN_WIDTH, y, sprite_sheet, scale)

   Enemy class that represents bird enemies in the game.

   This class handles enemy sprite animation, movement, and behavior.
   Enemies move horizontally across the screen and are affected by world scrolling.

   :param SCREEN_WIDTH: Width of the game screen
   :type SCREEN_WIDTH: int
   :param y: Initial y-coordinate position
   :type y: int
   :param sprite_sheet: Sprite sheet containing animation frames
   :type sprite_sheet: SpriteSheet
   :param scale: Scale factor for the sprite images
   :type scale: float

   .. py:method:: update(scroll, SCREEN_WIDTH)

      Update enemy animation and position.

      Handles animation frame updates, horizontal movement,
      vertical scrolling, and removal when off-screen.

      :param scroll: Amount to scroll the enemy vertically
      :type scroll: int
      :param SCREEN_WIDTH: Width of the game screen for boundary checking
      :type SCREEN_WIDTH: int

Utilities
---------

bouncai.world.constants
~~~~~~~~~~~~~~~~~~~~~~

.. py:class:: Constants

   Constants used throughout the BouncAI game.

   This class provides centralized access to game constants including physics values,
   screen dimensions, colors, and font references.

   .. py:attribute:: GRAVITY
      :type: float

      Gravity constant for player physics (0.5)

   .. py:attribute:: SCREEN_WIDTH
      :type: int

      Width of the game window in pixels (400)

   .. py:attribute:: SCREEN_HEIGHT
      :type: int

      Height of the game window in pixels (600)

   .. py:attribute:: SCROLL_THRESH
      :type: int

      Threshold for screen scrolling (200)

   .. py:attribute:: MAX_PLATFORMS
      :type: int

      Maximum number of platforms allowed at once (10)

   .. py:attribute:: FPS
      :type: int

      Frames per second for game loop (60)

   .. py:classmethod:: initialize_fonts()

      Initialize the fonts if pygame is initialized.

      This method attempts to initialize the font attributes if they haven't been
      set yet and pygame is properly initialized.

bouncai.world.spritesheet
~~~~~~~~~~~~~~~~~~~~~~~~

.. py:class:: SpriteSheet(image)

   A utility class for loading and parsing sprite sheets.

   :param image: The sprite sheet image
   :type image: pygame.Surface

   .. py:method:: get_image(frame, width, height, scale, colour)

      Extract a single image from the sprite sheet.

      :param frame: Frame index to extract
      :type frame: int
      :param width: Width of each frame
      :type width: int
      :param height: Height of each frame
      :type height: int
      :param scale: Scale factor to apply to the image
      :type scale: float
      :param colour: Color to set as transparent
      :type colour: tuple
      :return: The extracted and processed image
      :rtype: pygame.Surface
