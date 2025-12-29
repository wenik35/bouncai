"""Main module for the BouncAI game.

This module contains the main game loop and initialization code for the BouncAI game.
It handles pygame setup, game window creation, music/sound loading, and the main game loop
that manages player interaction, rendering, and game state.
"""

#import libraries
import pygame
import random
import os

from bouncai.world.world import World
from bouncai.world.config import config, initialize_fonts
from bouncai.world.player import Player
from bouncai.world.platform import Platform

from pygame import mixer
from bouncai.world.spritesheet import SpriteSheet
from bouncai.world.enemy import Enemy

from bouncai.controller import Actions
from bouncai.controller import ManualController

def run():
    """Run the BouncAI game.

    This function initializes pygame, sets up the game window, loads assets,
    and runs the main game loop. It handles all game mechanics including:
    - Game initialization (pygame, display, audio)
    - Asset loading (images, sounds, music)
    - High score tracking
    - Main game loop execution
    - Game over screen and restart functionality
    - Event handling
    - Configuration management

    Returns:
        None
    """
    #initialise pygame
    mixer.init()
    pygame.init()
    random.seed(0)

    # Initialize fonts after pygame is initialized
    initialize_fonts()

    #create game window
    screen = pygame.display.set_mode((config["SCREEN_WIDTH"], config["SCREEN_HEIGHT"]))
    pygame.display.set_caption('BouncAI')

    #set frame rate
    clock = pygame.time.Clock()

    # Load music and sounds with volume from config
    asset_base_path = config.get("ASSET_PATH", "assets")
    music_volume = config.get("MUSIC_VOLUME", 0.6)
    sound_volume = config.get("SOUND_VOLUME", 0.5)

    pygame.mixer.music.load(f'{asset_base_path}/music.mp3')
    pygame.mixer.music.set_volume(music_volume)
    pygame.mixer.music.play(-1, 0.0)
    jump_fx = pygame.mixer.Sound(f'{asset_base_path}/jump.mp3')
    jump_fx.set_volume(sound_volume)
    death_fx = pygame.mixer.Sound(f'{asset_base_path}/death.mp3')
    death_fx.set_volume(sound_volume)

    if os.path.exists('score.txt'):
        with open('score.txt', 'r') as file:
            high_score = float(file.read())
    else:
        high_score = 0

    # Set asset paths - can be overridden in config
    asset_base_path = config.get("ASSET_PATH", "assets")

    #load images
    player_image = pygame.image.load(f'{asset_base_path}/jump.png').convert_alpha()
    background_image = pygame.image.load(f'{asset_base_path}/bg.png').convert_alpha()
    platform_image = pygame.image.load(f'{asset_base_path}/wood.png').convert_alpha()
    wind_image = pygame.transform.scale(pygame.image.load(f'{asset_base_path}/wind.png').convert_alpha(), (65, 65))
    #bird spritesheet
    bird_sheet_img = pygame.image.load(f'{asset_base_path}/bird.png').convert_alpha()
    bird_sheet = SpriteSheet(bird_sheet_img)

    #function for outputting text onto the screen
    def draw_text(text, font, text_col, x, y):
        """Render text onto the game screen.

        Args:
            text (str): The text to render
            font (pygame.font.Font): Font to use for rendering
            text_col (tuple): RGB color tuple for the text
            x (int): X-coordinate position for the text
            y (int): Y-coordinate position for the text
        """
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))

    #function for drawing info panel
    def draw_panel():
        """Draw the information panel at the top of the screen.

        Renders a panel with the current score and a dividing line.
        """
        pygame.draw.rect(screen, config["PANEL"], (0, 0, config["SCREEN_WIDTH"], 30))
        pygame.draw.line(screen, config["WHITE"], (0, 30), (config["SCREEN_WIDTH"], 30), 2)
        draw_text('SCORE: ' + str(world.score), config["FONT_SMALL"], config["WHITE"], 0, 0)

    # initialize world
    world = World(background_image, platform_image, bird_sheet, wind_image)

    #player instance
    player = Player(world, config["SCREEN_WIDTH"] // 2, config["SCREEN_HEIGHT"] - 150, player_image, jump_fx)

    # initialize controller
    if config["CONTROLLER"] == "manual":
        controller = ManualController()
    elif config["CONTROLLER"] == "ai":
        from bouncai.controller import AIController
        controller = AIController()
    else:
        # Default to manual controller if not specified
        controller = ManualController()

    #game loop
    run = True
    while run:
        clock.tick(config["FPS"])

        if world.game_over == False:
            # generate state
            state = {}
            state['player'] = player.rect # + other variables
            state['platforms'] = [p.rect for p in world.platform_group]
            state['enemies'] = [e.rect for e in world.enemy_group]
            state['winds'] = [w.rect for w in world.wind_group]
            state['score'] = world.score

            action = controller.control(state)
            scroll = player.move(action)
            world.update(scroll)

            #draw line at previous high score
            pygame.draw.line(screen, config["WHITE"], (0, world.score - high_score + config["SCROLL_THRESH"]), (config["SCREEN_WIDTH"], world.score - high_score + config["SCROLL_THRESH"]), 3)
            draw_text('HIGH SCORE', config["FONT_SMALL"], config["WHITE"], config["SCREEN_WIDTH"] - 130, world.score - high_score + config["SCROLL_THRESH"])

            #draw sprites
            world.draw(screen)
            player.draw(screen)

            #draw panel
            draw_panel()

            #check game over
            if player.rect.top > config["SCREEN_HEIGHT"]:
                world.game_over = True
                death_fx.play()
            #check for collision with enemies
            if pygame.sprite.spritecollide(player, world.enemy_group, False):
                if pygame.sprite.spritecollide(player, world.enemy_group, False, pygame.sprite.collide_mask):
                    world.game_over = True
                    death_fx.play()
        else:
            # game over screen only in manual mode. For AI controller, auto-restart
            # by resetting the world and player so the agent can continue training/runs.
            if config["CONTROLLER"] == "manual":
                if world.fade_counter < config["SCREEN_WIDTH"]:
                    world.fade_counter += 5
                    for y in range(0, 6, 2):
                        pygame.draw.rect(screen, config["BLACK"], (0, y * 100, world.fade_counter, 100))
                        pygame.draw.rect(screen, config["BLACK"], (config["SCREEN_WIDTH"] - world.fade_counter, (y + 1) * 100, config["SCREEN_WIDTH"], 100))
                else:
                    draw_text('GAME OVER!', config["FONT_BIG"], config["WHITE"], 130, 200)
                    draw_text('SCORE: ' + str(world.score), config["FONT_BIG"], config["WHITE"], 130, 250)
                    draw_text('PRESS SPACE TO PLAY AGAIN', config["FONT_BIG"], config["WHITE"], 40, 300)
                    #update high score
                    if world.score > high_score:
                        high_score = world.score
                        with open('score.txt', 'w') as file:
                            file.write(str(high_score))
                    key = pygame.key.get_pressed()
                    if key[pygame.K_SPACE]:
                        # reset
                        world = World(background_image, platform_image, bird_sheet, wind_image)
                        player = Player(world, config["SCREEN_WIDTH"] // 2, config["SCREEN_HEIGHT"] - 150, player_image, jump_fx)
            elif config["CONTROLLER"] == "ai":
                # Automatically reset the world and player for AI runs so the
                # agent immediately restarts after dying.
                if world.score > high_score:
                    high_score = world.score
                    with open('score.txt', 'w') as file:
                        file.write(str(high_score))
                world = World(background_image, platform_image, bird_sheet, wind_image)
                player = Player(world, config["SCREEN_WIDTH"] // 2, config["SCREEN_HEIGHT"] - 150, player_image, jump_fx)
            else:
                run = False

        #event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #update high score
                if world.score > high_score:
                    high_score = world.score
                    with open('score.txt', 'w') as file:
                        file.write(str(high_score))
                run = False

        #update display window
        pygame.display.update()

    pygame.quit()
    return world.score
