"""Gymnasium environment for BouncAI game."""

import gymnasium as gym
import numpy as np
from gymnasium import spaces
import pygame
import random

from bouncai.world.world import World
from bouncai.world.config import config, initialize_fonts
from bouncai.world.player import Player
from bouncai.world.spritesheet import SpriteSheet
from bouncai.controller import Actions
from pygame import mixer



class BouncAIEnv(gym.Env):
    """Custom Gymnasium environment for BouncAI game."""
    
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 60}

    std_params = {
        "death": 10,
        "survival": 0,
        "survival_start": 100,
        "bounce": 5,
        "save_path": "models/"
    }
    
    def __init__(self, render_mode=None, params=std_params, asset_path="assets"):
        super().__init__()
        
        self.render_mode = render_mode
        self.asset_path = asset_path
        self.params = params
        
        # Initialize pygame if not already done
        if not pygame.get_init():
            print("[DEBUG] Initializing pygame...")
            mixer.init()
            pygame.init()
        
        # Initialize fonts after pygame is initialized
        initialize_fonts()
        
        # Screen setup
        self.screen_width = config["SCREEN_WIDTH"]
        self.screen_height = config["SCREEN_HEIGHT"]
        self.screen = None
        self.clock = None
        
        # Initialize asset variables
        self.player_image = None
        self.background_image = None
        self.platform_image = None
        self.wind_image = None
        self.bird_sheet = None
        self.jump_fx = None
        self.death_fx = None
        
        # Load assets
        self._load_assets()
        
        # Action space: LEFT, RIGHT, or NO_ACTION
        self.action_space = spaces.Discrete(3)  # 0: LEFT, 1: RIGHT, 2: NO_ACTION
        
        # Observation space: [player_x, player_y,
        #                     nearest_platform_x, nearest_platform_y, nearest_platform_width, * 10
        #                     nearest_enemy_x, nearest_enemy_y,
        #                     nearest_wind_x, nearest_wind_y]
        # = 2 + 30 + 2 + 2 = 36 values
        self.max_platforms = config.get("MAX_PLATFORMS", 10)
        obs_size = 2 + self.max_platforms * 3 + 2 + 2  # 36

        self.observation_space = spaces.Box(
            low=-np.inf, 
            high=np.inf, 
            shape=(obs_size,),
            dtype=np.float32
        )
        
        self.world = None
        self.player = None
        self.high_score = 0
        self.steps = 0
        self.max_steps = 5000
        
        self._reset_game()
    
    def _load_assets(self):
        """Load game assets."""
        try:
            print(f"Loading assets from: {self.asset_path}")
            
            # Load images without convert_alpha initially
            player_img = pygame.image.load(f'{self.asset_path}/jump.png')
            if pygame.display.get_surface() is not None:
                player_img = player_img.convert_alpha()
            self.player_image = player_img
            print("  [OK] Loaded player image")
            
            bg_img = pygame.image.load(f'{self.asset_path}/bg.png')
            if pygame.display.get_surface() is not None:
                bg_img = bg_img.convert_alpha()
            self.background_image = bg_img
            print("  [OK] Loaded background image")
            
            platform_img = pygame.image.load(f'{self.asset_path}/wood.png')
            if pygame.display.get_surface() is not None:
                platform_img = platform_img.convert_alpha()
            self.platform_image = platform_img
            print("  [OK] Loaded platform image")
            
            wind_img = pygame.image.load(f'{self.asset_path}/wind.png')
            if pygame.display.get_surface() is not None:
                wind_img = wind_img.convert_alpha()
            self.wind_image = pygame.transform.scale(wind_img, (65, 65))
            print("  [OK] Loaded wind image")
            
            bird_sheet_img = pygame.image.load(f'{self.asset_path}/bird.png')
            if pygame.display.get_surface() is not None:
                bird_sheet_img = bird_sheet_img.convert_alpha()
            self.bird_sheet = SpriteSheet(bird_sheet_img)
            print("  [OK] Loaded bird spritesheet")
            
            # Load sounds
            try:
                self.jump_fx = pygame.mixer.Sound(f'{self.asset_path}/jump.mp3')
                self.jump_fx.set_volume(config.get("SOUND_VOLUME", 0.5))
                print("  [OK] Loaded jump sound")
            except:
                print("  [WARNING] Could not load jump sound")
            
            try:
                self.death_fx = pygame.mixer.Sound(f'{self.asset_path}/death.mp3')
                self.death_fx.set_volume(config.get("SOUND_VOLUME", 0.5))
                print("  [OK] Loaded death sound")
            except:
                print("  [WARNING] Could not load death sound")
            
            print("[SUCCESS] All assets loaded successfully")
        except FileNotFoundError as e:
            print(f"[ERROR] Asset file not found: {e}")
            raise
        except Exception as e:
            print(f"[ERROR] Error loading assets: {e}")
            raise
    
    def _reset_game(self):
        """Reset the game state."""
        self.world = World(
            self.background_image,
            self.platform_image,
            self.bird_sheet,
            self.wind_image
        )
        self.player = Player(
            self.world,
            self.screen_width // 2,
            self.screen_height - 150,
            self.player_image,
            self.jump_fx
        )
        self.steps = 0

    def _get_observation(self):
        """Get relative and normalized observation."""
        player_rect = self.player.rect
        obs_list = []

        # 1. Player State
        # Normalize X pos (0 to 1) just so it knows if it's near the edge
        obs_list.append(player_rect.x / self.screen_width)
        obs_list.append(player_rect.y / self.screen_height)
        
        # 2. Platform State (Relative & Normalized)
        # Get all platforms
        platforms = self.world.platform_group.sprites()
        
        # Sort platforms by distance to player to ensure consistency
        #platforms = [p for p in platforms if p.rect.y <= player_rect.y - 300]
        #platforms.sort(key=lambda p: player_rect.y - p.rect.y)
        
        for i in range(self.max_platforms):
            if i < len(platforms):
                p = platforms[i]
                # Relative X distance normalized (-1 to 1)
                rel_x = (p.rect.x - player_rect.x) / self.screen_width
                # Relative Y distance normalized (-1 to 1)
                rel_y = (p.rect.y - player_rect.y) / self.screen_height
                
                obs_list.append(rel_x)
                obs_list.append(rel_y)
                obs_list.append(p.rect.width / self.screen_width) # Normalized width
            else:
                # Padding for missing platforms
                obs_list.append(0.0) 
                obs_list.append(1.0) # Far below/away
                obs_list.append(0.0)

        # 3. Enemy State (Relative & Normalized)
        enemies = self.world.enemy_group.sprites()
        if enemies:
            # Find nearest enemy
            nearest_enemy = min(enemies, key=lambda e: (e.rect.x - player_rect.x)**2 + (e.rect.y - player_rect.y)**2)
            obs_list.append((nearest_enemy.rect.x - player_rect.x) / self.screen_width)
            obs_list.append((nearest_enemy.rect.y - player_rect.y) / self.screen_height)
        else:
            obs_list.append(0.0)
            obs_list.append(1.0) # Far away

        # 4. Wind State (Relative & Normalized)
        winds = self.world.wind_group.sprites()
        if winds:
            nearest_wind = min(winds, key=lambda w: (w.rect.x - player_rect.x)**2 + (w.rect.y - player_rect.y)**2)
            obs_list.append((nearest_wind.rect.x - player_rect.x) / self.screen_width)
            obs_list.append((nearest_wind.rect.y - player_rect.y) / self.screen_height)
        else:
            obs_list.append(0.0)
            obs_list.append(1.0)

        return np.array(obs_list, dtype=np.float32)
    
    def _calculate_reward(self, prev_score, prev_vel_y):
        """Calculate reward based on game state."""
        
        # Penalty for dying
        if self.world.game_over:
            return - self.params["death"]
        else:
            score_delta = self.world.score - prev_score
            #reward = score_delta / 100.0
            reward = 0.0

            # reward for bouncing
            curr_vel_y = float(self.player.vel_y)
            if prev_vel_y > 0 and curr_vel_y < 0:
                reward += self.params["bounce"]
            
            # reward for survival
            if self.world.score > self.params["survival_start"]:
                reward += self.params["survival"]

            return reward
    
    def step(self, action):
        """Execute one step of the environment."""
        prev_score = self.world.score
        
        prev_vel_y = float(self.player.vel_y)

        # Convert action to controller action
        if action == 0:
            controller_action = Actions.LEFT
        elif action == 1:
            controller_action = Actions.RIGHT
        else:
            controller_action = None
        
        # Update game
        scroll = self.player.move(controller_action)
        self.world.update(scroll)
        
        # Check game over conditions
        if self.player.rect.top > self.screen_height:
            self.world.game_over = True
        
        if pygame.sprite.spritecollide(self.player, self.world.enemy_group, False):
            if pygame.sprite.spritecollide(
                self.player, self.world.enemy_group, False, pygame.sprite.collide_mask
            ):
                self.world.game_over = True
        
        # Calculate reward
        reward = self._calculate_reward(prev_score, prev_vel_y)

        # Get observation
        observation = self._get_observation()
        
        # Check termination
        terminated = self.world.game_over
        
        # Check truncation (max steps)
        self.steps += 1
        truncated = self.steps >= self.max_steps
        
        # Info dictionary
        info = {
            "score": self.world.score,
            "steps": self.steps,
        }

        # If the episode terminated because the agent died, log the final score
        if terminated:
            try:
                from datetime import datetime
                #log_line = f"{datetime.utcnow().isoformat()}Z, score={self.world.score}, steps={self.steps}\n"
                log_line = f"{self.world.score}\n"
                with open(self.params["save_path"] + "scores_log.txt", "a+", encoding="utf-8") as f:
                    f.write(log_line)
            except Exception as e:
                # Don't let logging errors crash the environment
                print(f"[WARN] Failed to write score log: {e}")

        return observation, reward, terminated, truncated, info
    
    def reset(self, seed=None, options=None):
        """Reset the environment."""
        super().reset(seed=seed)
        self._reset_game()
        observation = self._get_observation()
        info = {}
        return observation, info
    
    def render(self):
        """Render the game."""
        if self.render_mode == "human":
            # Ensure screen is created on first render
            if self.screen is None:
                self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
                pygame.display.set_caption('BouncAI-Gymnasium')
                self.clock = pygame.time.Clock()
            
            try:
                # Fill screen with background first
                self.screen.fill((0, 0, 0))
                self.world.draw(self.screen)
                self.player.draw(self.screen)
                pygame.display.update()
                
                # Handle events to keep window responsive
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.world.game_over = True
                
                if self.clock:
                    self.clock.tick(config["FPS"])
            except pygame.error as e:
                print(f"[ERROR] Pygame render error: {e}")
                print(f"[DEBUG] Screen is None: {self.screen is None}")
                print(f"[DEBUG] Render mode: {self.render_mode}")
                raise
        elif self.render_mode == "rgb_array":
            # Convert pygame surface to numpy array
            if self.screen:
                return pygame.surfarray.array3d(self.screen)
            return None
    
    def close(self):
        """Close the environment."""
        if self.screen:
            pygame.quit()