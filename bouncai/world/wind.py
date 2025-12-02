import pygame
import random

from bouncai.world.config import config

class Wind(pygame.sprite.Sprite):
    """Wind class that represents a windy area in the game.
    """
    def __init__(self, y, wind_speed, image):
        """Initialize an enemy.

        Args:
            y (int): Y-coordinate position
            wind_speed (int): Speed of the wind effect
            image (pygame.Surface): Image representing the wind area
        """
        pygame.sprite.Sprite.__init__(self)
        #define variables
        self.wind_speed = wind_speed
        self.direction = random.choice([-1, 1])
        if self.direction == 1:
            self.flip = False
        else:
            self.flip = True

        self.image = pygame.transform.flip(image, self.flip, False)
        self.rect = self.image.get_rect()
        self.rect.y = y

        if self.direction == 1:
            self.rect.x = 0
        else:
            self.rect.x = config["SCREEN_WIDTH"] - self.rect.width


    def update(self, scroll):
        """Update enemy animation and position.

        Handles animation frame updates, horizontal movement,
        vertical scrolling, and removal when off-screen.

        Args:
            scroll (int): Amount to scroll the enemy vertically
        """
        #move area
        self.rect.y += scroll

        #check if gone off screen
        if self.rect.top > config["SCREEN_HEIGHT"]:
            self.kill()
