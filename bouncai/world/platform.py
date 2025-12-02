import pygame
import random

from bouncai.world.config import config

class Platform(pygame.sprite.Sprite):
    """Platform class that represents the platforms the player can jump on.

    This class handles the creation and behavior of platforms in the game,
    including moving platforms that travel side to side.

    Attributes:
        image (pygame.Surface): The platform sprite
        moving (bool): Whether the platform moves horizontally
        move_counter (int): Counter for tracking platform movement
        direction (int): Direction of movement (-1 for left, 1 for right)
        speed (int): Movement speed for moving platforms
        rect (pygame.Rect): Rectangle for collision detection and positioning
    """
    def __init__(self, x, y, width, velocity, platform_image):
        """Initialize a platform.

        Args:
            x (int): Initial x-coordinate position
            y (int): Initial y-coordinate position
            width (int): Width of the platform
            moving (bool): Whether the platform should move horizontally
            platform_image (pygame.Surface): Image for the platform sprite
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_image, (width, 10))
        self.direction = random.choice([-1, 1])
        self.speed = velocity
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, scroll):
        """Update the platform position and movement.

        Handles horizontal movement for moving platforms and vertical
        scrolling for all platforms. Removes platforms that go off-screen.

        Args:
            scroll (int): Amount to scroll the platform vertically
        """
        #moving platform side to side if it is a moving platform
        self.rect.x += self.direction * self.speed

        #change platform direction if it has moved fully or hit a wall
        if  self.rect.left < 0 or self.rect.right > config["SCREEN_WIDTH"]:
            self.direction *= -1

        #update platform's vertical position
        self.rect.y += scroll

        #check if platform has gone off the screen
        if self.rect.top > config["SCREEN_HEIGHT"]:
            self.kill()
