import pygame
from bouncai.world.config import config
from bouncai.world.world import World

from bouncai.controller import Actions

#player class
class Player():
    """Player class that manages the player character.

    This class handles player movement, gravity, collision detection with platforms,
    and rendering of the player sprite. It manages player jumping, horizontal movement,
    and interactions with the game world.

    Attributes:
        image (pygame.Surface): The player character sprite
        jump_sound (pygame.mixer.Sound): Sound effect played when player jumps
        world (World): Reference to the game world
        width (int): Player hitbox width
        height (int): Player hitbox height
        rect (pygame.Rect): Rectangle for collision detection
        vel_y (float): Vertical velocity of the player
        flip (bool): Whether the player sprite should be flipped horizontally
    """
    def __init__(self, world: World, x, y, player_image, jump_sound):
        """Initialize the player character.

        Args:
            world (World): Reference to the game world
            x (int): Initial x-coordinate position
            y (int): Initial y-coordinate position
            player_image (pygame.Surface): Image for the player sprite
            jump_sound (pygame.mixer.Sound): Sound effect for jumping
        """
        self.image = pygame.transform.scale(player_image, (45, 45))
        self.jump_sound = jump_sound
        self.world = world
        self.width = 25
        self.height = 40
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.vel_y = 0
        self.vel_x = 0
        self.flip = False


    def move(self, action: Actions):
        """Handle player movement and physics.

        Processes keyboard input for horizontal movement, applies gravity,
        handles platform collisions, and determines screen scrolling.

        Args:
            action (Actions): The action to perform

        Returns:
            int: The amount the screen should scroll based on player position
        """
        #reset variables
        scroll = 0
        dx = 0
        dy = 0

        #only act on valid actions
        if action == Actions.LEFT:
            dx = -10
            self.flip = True

        if action == Actions.RIGHT:
            dx = 10
            self.flip = False

        #check if we are in a wind area
        for wind in self.world.wind_group:
            # check collision only in y direction
            if self.rect.colliderect(wind.rect.x, wind.rect.y + scroll, config["SCREEN_WIDTH"], wind.rect.height):
                dx += wind.wind_speed * wind.direction


        #gravity
        self.vel_y += config["GRAVITY"]
        dy += self.vel_y

        #ensure player doesn't go off the edge of the screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > config["SCREEN_WIDTH"]:
            dx = config["SCREEN_WIDTH"] - self.rect.right


        #check collision with platforms
        for platform in self.world.platform_group:
            #collision in the y direction
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                #check if above the platform
                if self.rect.bottom < platform.rect.centery:
                    if self.vel_y > 0:
                        self.rect.bottom = platform.rect.top
                        dy = 0
                        self.vel_y = -20
                        self.jump_sound.play()

        #check if the player has bounced to the top of the screen
        if self.rect.top <= config["SCROLL_THRESH"]:
            #if player is jumping
            if self.vel_y < 0:
                scroll = -dy

        #update rectangle position
        self.rect.x += dx
        self.rect.y += dy + scroll

        self.vel_x = dx

        #update mask
        self.mask = pygame.mask.from_surface(self.image)

        return scroll

    def draw(self, screen):
        """Draw the player sprite on the screen.

        Args:
            screen (pygame.Surface): Surface to draw the player on
        """
        screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 12, self.rect.y - 5))
