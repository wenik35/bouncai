from math import exp
import pygame
import random
from bouncai.world.platform import Platform
from bouncai.world.enemy import Enemy
from bouncai.world.config import config, initialize_fonts
from bouncai.world.wind import Wind

class World():
    """World class that manages the game environment.

    This class handles the game background, platforms, enemies, and game state.
    It manages the scrolling of the game world, score tracking, and game over state.

    Attributes:
        bg_image (pygame.Surface): Background image surface
        platform_image (pygame.Surface): Platform image surface
        enemy_sheet (SpriteSheet): Sprite sheet for enemy animations
        scroll (int): Current scroll amount
        bg_scroll (int): Background scroll amount
        game_over (bool): Flag indicating if the game is over
        score (int): Current player score
        fade_counter (int): Counter for fade effect during game over
        platform_group (pygame.sprite.Group): Group containing all platform sprites
        enemy_group (pygame.sprite.Group): Group containing all enemy sprites
    """
    def __init__(self, background_image, platform_image, enemy_sheet, wind_image):
        """Initialize the game world.

        Args:
            background_image (pygame.Surface): Background image surface
            platform_image (pygame.Surface): Platform image surface
            enemy_sheet (SpriteSheet): Sprite sheet for enemy animations
        """
        # Initialize fonts if not already initialized
        initialize_fonts()

        self.bg_image  = background_image
        self.platform_image = platform_image
        self.enemy_sheet = enemy_sheet
        self.wind_image = wind_image
        self.scroll = 0
        self.bg_scroll = 0
        self.game_over = False
        self.score = 0
        self.fade_counter = 0


        #create sprite groups
        self.platform_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.wind_group = pygame.sprite.Group()

        #create starting platform
        platform = Platform(config["SCREEN_WIDTH"] // 2 - 50, config["SCREEN_HEIGHT"] - 50, 100, False, self.platform_image)
        self.platform_group.add(platform)

        # store y-coordinate of the last platform for initial generation
        self.last_platform_y = platform.rect.y
        self.last_enemy_y = 0
        self.last_wind_y = 0

    def get_difficulty(self, delay=0.0):
        """Get the current difficulty level.

        Returns:
            float: Current difficulty level between 0.0 (easiest) and 1.0 (hardest)
        """
        # update difficulty based on score
        return exp(-1.0 * float(self.score) / (float(config["DIFFICULTY_INCREASE"])*(delay+1.0)))

    #function for drawing the background
    def draw_bg(self, screen):
        """Draw the scrolling background.

        Args:
            screen (pygame.Surface): Surface to draw the background on
        """
        screen.blit(self.bg_image, (0, 0 + self.bg_scroll))
        screen.blit(self.bg_image, (0, -600 + self.bg_scroll))

    def draw(self, screen):
        """Draw all game elements to the screen.

        Args:
            screen (pygame.Surface): Surface to draw all game elements on
        """
        self.draw_bg(screen)
        self.platform_group.draw(screen)
        self.enemy_group.draw(screen)
        self.wind_group.draw(screen)

    def update_background(self, scroll):
        """Update the background scroll position.

        Args:
            scroll (int): Amount to scroll the background by
        """
        #update background
        self.bg_scroll += scroll
        if self.bg_scroll >= 600:
            self.bg_scroll = 0

    def update_plattforms(self, scroll):
        """Update existing platforms and generate new ones as needed.

        Generates new platforms when fewer than MAX_PLATFORMS exist.
        Updates the position of all existing platforms.

        Args:
            scroll (int): Amount to scroll platforms by
        """

        #generate platforms
        if len(self.platform_group) < config["MAX_PLATFORMS"]:
            p_w = max(int(random.normalvariate(self.get_difficulty(config["PLATFORM_WIDTH_DIFFICULTY_DELAY"])*config["PLATFORM_WIDTH_MAX"], 5)), config["PLATFORM_WIDTH_MIN"])
            p_x = random.randint(0, config["SCREEN_WIDTH"] - p_w)
            # Convert the Group to a list to access the last platform
            platform_list = list(self.platform_group)
            p_y = self.last_platform_y - min(int(random.normalvariate((1.5-self.get_difficulty(config["PLATFORMS_DISTANCE_DIFFICULTY_DELAY"]))*config["PlATFORMS_DISTANCE_MAX"], 5)), config["PlATFORMS_DISTANCE_MAX"])
            self.last_platform_y = p_y
            p_moving_velocity = max(int(random.normalvariate((1.0-self.get_difficulty(config["PLATFORM_MOVING_DIFFICULTY_DELAY"]))*config["PLATFORM_MOVING_SPEED_MAX"], 0.025)), 0)
            platform = Platform(p_x, p_y, p_w, p_moving_velocity, self.platform_image)
            self.platform_group.add(platform)

        for platform in self.platform_group:
            platform.update(scroll)

        self.last_platform_y += scroll

    def update_enemies(self, scroll):
        """Update existing enemies and generate new ones as needed.

        Generates new enemies when none exist and the score is high enough.
        Updates the position of all existing enemies.

        Args:
            scroll (int): Amount to scroll enemies by
        """
        #generate enemies
        if len(self.enemy_group) < int((1.0-self.get_difficulty(config["ENEMY_DIFFICULTY_DELAY"]))*config["MAX_ENEMIES"]):

            if len(self.enemy_group) == 0:
                p_y = 150
            else:
                p_y = self.last_enemy_y - max(int(random.normalvariate(self.get_difficulty(config["ENEMY_DIFFICULTY_DELAY"])*config["ENEMY_DISTANCE_MIN"], 5)), 0)

            enemy = Enemy(p_y, (1.0-self.get_difficulty(config["ENEMY_DIFFICULTY_DELAY"]))*config["ENEMY_MOVING_SPEED_MAX"], self.enemy_sheet, 1.5)
            self.enemy_group.add(enemy)

        #update enemies
        self.enemy_group.update(scroll)

    def update_wind(self, scroll):
        """Update existing wind areas and generate new ones as needed.

        Generates new wind areas when none exist and the score is high enough.
        Updates the position of all existing wind areas.

        Args:
            scroll (int): Amount to scroll wind areas by
        """
        #generate wind areas
        if len(self.wind_group) < int((1.0-self.get_difficulty(config["WIND_DIFFICULTY_DELAY"]))*config["MAX_WIND_AREAS"]):

            if len(self.wind_group) == 0:
                p_y = 100
            else:
                p_y = self.last_wind_y - max(int(random.normalvariate(self.get_difficulty(config["WIND_DIFFICULTY_DELAY"])*config["WIND_DISTANCE_MIN"], 5)), 0)

            wind = Wind(p_y, (1.0-self.get_difficulty(config["WIND_DIFFICULTY_DELAY"]))*config["WIND_MOVING_SPEED_MAX"], self.wind_image)
            self.wind_group.add(wind)

        #update wind areas
        self.wind_group.update(scroll)

    def update(self, scroll):
        """Update all game elements.

        Calls individual update methods for background, platforms, and enemies.
        Updates the player score based on scroll amount.

        Args:
            scroll (int): Amount to scroll the game world by
        """
        self.update_background(scroll)
        self.update_plattforms(scroll)
        self.update_wind(scroll)
        self.update_enemies(scroll)

        #update score
        if scroll > 0:
            self.score += scroll
