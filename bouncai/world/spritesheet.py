import pygame

class SpriteSheet():
    """A class for handling sprite sheets.

    This class provides functionality for extracting individual sprite frames
    from a sprite sheet image. It handles the cutting, scaling, and color key
    setting for sprite animation frames.

    Attributes:
        sheet (pygame.Surface): The sprite sheet image containing multiple frames
    """
    def __init__(self, image):
        """Initialize the sprite sheet.

        Args:
            image (pygame.Surface): The sprite sheet image containing multiple frames
        """
        self.sheet = image

    def get_image(self, frame, width, height, scale, colour):
        """Extract a single frame from the sprite sheet.

        Args:
            frame (int): The frame index to extract (0-based)
            width (int): Width of each frame in the sprite sheet
            height (int): Height of each frame in the sprite sheet
            scale (float): Scale factor to resize the extracted frame
            colour (tuple): RGB color tuple to use as transparency key

        Returns:
            pygame.Surface: The extracted and processed frame image
        """
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        image.set_colorkey(colour)

        return image
