import pygame
import random

from bouncai.world.config import config

class Enemy(pygame.sprite.Sprite):
    """Enemy class that represents bird enemies in the game.

    This class handles enemy sprite animation, movement, and behavior.
    Enemies move horizontally across the screen and are affected by world scrolling.

    Attributes:
        animation_list (list): List of animation frames
        frame_index (int): Current animation frame index
        update_time (int): Time of last animation update
        direction (int): Direction of movement (-1 for left, 1 for right)
        flip (bool): Whether the sprite should be flipped horizontally
        image (pygame.Surface): Current sprite image
        rect (pygame.Rect): Rectangle for collision detection and positioning
    """
    def __init__(self, y, speed, sprite_sheet, scale):
        """Initialize an enemy.

        Args:
            y (int): Initial y-coordinate position
            sprite_sheet (SpriteSheet): Sprite sheet containing animation frames
            scale (float): Scale factor for the sprite images
        """
        pygame.sprite.Sprite.__init__(self)
        #define variables
        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.speed = speed
        self.direction = random.choice([-1, 1])
        if self.direction == 1:
            self.flip = True
        else:
            self.flip = False

        #load images from spritesheet
        animation_steps = 8
        for animation in range(animation_steps):
            image = sprite_sheet.get_image(animation, 32, 32, scale, (0, 0, 0))
            image = pygame.transform.flip(image, self.flip, False)
            image.set_colorkey((0, 0, 0))
            self.animation_list.append(image)

        #select starting image and create rectangle from it
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()

        if self.direction == 1:
            self.rect.x = 0
        else:
            self.rect.x = config["SCREEN_WIDTH"]
        self.rect.y = y

    def update(self, scroll):
        """Update enemy animation and position.

        Handles animation frame updates, horizontal movement,
        vertical scrolling, and removal when off-screen.

        Args:
            scroll (int): Amount to scroll the enemy vertically
        """
        #update image depending on current frame
        self.image = self.animation_list[self.frame_index]
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > config["ANIMATION_COOLDOWN"]:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #if the animation has run out then reset back to the start
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0

        #move enemy
        self.rect.x += self.direction * self.speed
        self.rect.y += scroll

        #check if gone off screen
        if self.rect.right < 0 or self.rect.left > config["SCREEN_WIDTH"] or self.rect.top > config["SCREEN_HEIGHT"]:
            self.kill()
