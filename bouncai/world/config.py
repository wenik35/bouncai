"""
Game configuration module for BouncAI.

This module provides centralized access to game configuration including physics values,
screen dimensions, colors, and other game settings. The configuration is stored in a
dictionary that can be modified at runtime.
"""

import pygame
import json
import os
from typing import Dict, Any, Optional

# Default configuration dictionary
config: Dict[str, Any] = {
    # Physics
    "GRAVITY": 0.5,

    # Screen dimensions
    "SCREEN_WIDTH": 400,
    "SCREEN_HEIGHT": 600,
    "SCROLL_THRESH": 200,

    # Asset paths
    "ASSET_PATH": "assets",

    # Audio settings
    "MUSIC_VOLUME": 0.6,
    "SOUND_VOLUME": 0.5,

    # Platform settings
    "MAX_PLATFORMS": 10,
    "MIN_PLATFORMS": 5,
    "PLATFORM_WIDTH_MIN": 10,
    "PLATFORM_WIDTH_MAX": 100,
    "PLATFORM_WIDTH_DIFFICULTY_DELAY": 4,
    "PlATFORMS_DISTANCE_MAX": 120,
    "PLATFORMS_DISTANCE_DIFFICULTY_DELAY": 6,
    "PLATFORM_MOVING_SPEED_MAX": 5,
    "PLATFORM_MOVING_DIFFICULTY_DELAY": 2,

    # Game settings
    "FPS": 60,
    "DIFFICULTY_INCREASE": 5000,  # score interval for increasing difficulty
    "ANIMATION_COOLDOWN": 50,

    # Enemy settings
    "MAX_ENEMIES": 5,
    "ENEMY_MOVING_SPEED_MAX": 5,
    "ENEMY_DISTANCE_MIN": 200,
    "ENEMY_DIFFICULTY_DELAY": 8,

    # Wind settings
    "MAX_WIND_AREAS": 5,
    "WIND_DISTANCE_MIN": 150,
    "WIND_MOVING_SPEED_MAX": 10,
    "WIND_DIFFICULTY_DELAY": 4,

    # Colors
    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0),
    "PANEL": (153, 217, 234),

    # Font placeholders
    "FONT_SMALL": None,
    "FONT_BIG": None,

    # Controller to use: "manual" or "ai"
    "CONTROLLER": "manual",
}

def initialize_fonts():
    """Initialize the fonts if pygame is initialized.

    This function attempts to initialize the font entries in the config if they
    haven't been set yet and pygame is properly initialized. If pygame isn't
    initialized, the function will silently fail and can be called again later.

    Returns:
        None
    """
    if config["FONT_SMALL"] is None:
        try:
            config["FONT_SMALL"] = pygame.font.SysFont('Lucida Sans', 20)
            config["FONT_BIG"] = pygame.font.SysFont('Lucida Sans', 24)
        except pygame.error:
            # Pygame not initialized yet, will try again later
            pass

def get_config():
    """Return the current configuration dictionary.

    Returns:
        dict: The current game configuration
    """
    return config.copy()  # Return a copy to prevent accidental modification

def update_config(new_settings: Dict[str, Any]) -> None:
    """Update the configuration with new settings.

    Args:
        new_settings (dict): Dictionary containing settings to update

    Returns:
        None
    """
    config.update(new_settings)


def save_config(filepath: str = "game_config.json") -> bool:
    """Save the current configuration to a JSON file.

    Args:
        filepath (str): Path where to save the configuration file

    Returns:
        bool: True if saved successfully, False otherwise

    Example:
        >>> save_config("my_settings.json")
        True
    """
    try:
        # Create a copy of the config to save
        saveable_config = config.copy()

        # Remove non-serializable items
        saveable_config.pop("FONT_SMALL", None)
        saveable_config.pop("FONT_BIG", None)

        with open(filepath, 'w') as f:
            json.dump(saveable_config, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving configuration: {e}")
        return False


def load_config(filepath: str = "game_config.json") -> bool:
    """Load configuration from a JSON file.

    Args:
        filepath (str): Path to the configuration file

    Returns:
        bool: True if loaded successfully, False otherwise

    Example:
        >>> load_config("my_settings.json")
        True
    """
    try:
        if not os.path.exists(filepath):
            return False

        with open(filepath, 'r') as f:
            loaded_config = json.load(f)

        # Update the current config with loaded values
        config.update(loaded_config)
        return True
    except Exception as e:
        print(f"Error loading configuration: {e}")
        return False


def get_setting(key: str, default: Optional[Any] = None) -> Any:
    """Get a specific configuration setting with an optional default value.

    Args:
        key (str): The configuration key to retrieve
        default (Any, optional): Default value if key doesn't exist

    Returns:
        Any: The configuration value or default

    Example:
        >>> get_setting("GRAVITY", 0.75)
        0.5
        >>> get_setting("NONEXISTENT", "default")
        'default'
    """
    return config.get(key, default)

def create_default_config(filepath: str = "default_config.json") -> bool:
    """Create a default configuration file.

    Generates a JSON file with the current default configuration settings.
    Useful for users to see all available options.

    Args:
        filepath (str): Path where to save the default configuration

    Returns:
        bool: True if created successfully, False otherwise
    """
    return save_config(filepath)
