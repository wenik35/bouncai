# Enum defining valid actions for the controller
import collections
from enum import Enum

import pygame
import random
import numpy as np
import os
import sys
import time
from datetime import datetime

# Define valid actions
class Actions(Enum):
    LEFT = 0
    RIGHT = 1

class ManualController:
    def __init__(self):
        pass

    def control(self, state):
        # process keypresses
        key = pygame.key.get_pressed()
        action = None  # Default action
        if key[pygame.K_a]:
            action = Actions.LEFT
        if key[pygame.K_d]:
            action = Actions.RIGHT
        return action  # Return the action instead of not using it

class AIController:
    """AI controller that loads a pretrained RL model for display runs.

    If a Stable-Baselines3 model is available at `model_path` the controller
    will use it (deterministic by default). If the model or the
    package is not available it falls back to random actions.
    """
    def __init__(self, model_path: str = "models/death100_survival0_bounce10/model", deterministic: bool = True):
        self.model = None
        self.deterministic = deterministic
        self.model_path = model_path

        self.obs = collections.deque(maxlen=144)
        self.obs.append(np.zeros((144,), dtype=np.float32))

        # Frame capture buffer (store RGB numpy arrays)
        self.frames = []
        self.save_threshold = 100000  # score threshold to decide save/discard
        self.fps = 60

        # Try to load a Stable-Baselines3 model if available
        try:
            from stable_baselines3 import PPO  # noqa: F401
            if os.path.exists(model_path) or os.path.exists(model_path + ".zip"):
                try:
                    from stable_baselines3 import PPO
                    self.model = PPO.load(model_path)
                    print(f"[AIController] Loaded model from '{model_path}'")
                except Exception as e:  # loading failed
                    print(f"[AIController] Failed loading model '{model_path}': {e}")
                    self.model = None
            else:
                print(f"[AIController] Model file not found at '{model_path}', falling back to random actions")
        except Exception:
            # stable_baselines3 not installed
            print("[AIController] stable_baselines3 not available; falling back to random actions")

    def control(self, state):
        """Return an action (Actions.LEFT / Actions.RIGHT / None).

        Args:
            state (dict): game state as provided by the main loop
        """
        # Capture current screen to memory (RGB numpy array)
        try:
            surf = pygame.display.get_surface()
            if surf is not None:
                arr = pygame.surfarray.array3d(surf)
                # surfarray returns (width, height, 3) — transpose to (height, width, 3)
                arr = np.transpose(arr, (1, 0, 2)).astype(np.uint8)
                self.frames.append(arr.copy())
        except Exception:
            # If display not available yet, skip capture
            pass

        if self.model is None:
            return random.choice(list(Actions))

        # Convert state dict to observation array
        self.obs.extend(state_to_obs(state)) 

        try:
            action, _ = self.model.predict(self.obs, deterministic=self.deterministic)
        except Exception as e:
            print(f"[AIController] Model.predict failed: {e}")
            return random.choice(list(Actions))

        # Model may return numpy scalar/array
        try:
            a = int(action)
        except Exception:
            try:
                a = int(np.asarray(action).ravel()[0])
            except Exception:
                return random.choice(list(Actions))

        if a == 0:
            return Actions.LEFT
        elif a == 1:
            return Actions.RIGHT
        else:
            return None

    def on_episode_end(self, score: int):
        """Handle end of an episode.

        - If the score is below `save_threshold`: discard captured frames and
            return so the next run starts automatically.
        - If the score is >= `save_threshold`: write captured frames to a
            video file in the model path and post a QUIT event to end the
            simulation (so the user can inspect the high-scoring run).
        """
        # If no frames captured, nothing to do
        if not self.frames:
            return

        # If the run is below threshold, discard frames and continue
        if score < self.save_threshold:
            self.frames = []
            return

        # Otherwise save frames as a video (high-scoring run)
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        base = self.model_path
        out_dir = os.path.dirname(base) or base or 'models'
        os.makedirs(out_dir, exist_ok=True)
        out_file = os.path.join(out_dir, f'run_success_{timestamp}.mp4')

        saved = False
        # Try OpenCV first
        try:
            import cv2
            h, w, _ = self.frames[0].shape
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            writer = cv2.VideoWriter(out_file, fourcc, float(self.fps), (w, h))
            for f in self.frames:
                # frames are in RGB; convert to BGR
                try:
                    bgr = cv2.cvtColor(f, cv2.COLOR_RGB2BGR)
                except Exception:
                    bgr = f[:, :, ::-1]
                writer.write(bgr)
            writer.release()
            saved = True
        except Exception:
            # Fallback to imageio if cv2 not available
            try:
                import imageio
                imageio.mimwrite(out_file, self.frames, fps=self.fps)
                saved = True
            except Exception:
                saved = False

        if saved:
            print(f"[AIController] Saved high-run video to '{out_file}' (score={score})")
            # Post QUIT so the simulation ends for inspection
            try:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            except Exception:
                pass
        else:
            print(f"[AIController] Failed to save video for high run; saving frames as PNGs in '{out_dir}'")
            try:
                from PIL import Image
                for i, f in enumerate(self.frames):
                    Image.fromarray(f).save(os.path.join(out_dir, f'frame_{i:06d}.png'))
                # still request quit so user can inspect
                try:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                except Exception:
                    pass
            except Exception as e:
                print(f"[AIController] Failed fallback PNG save: {e}")
                # Clearing frames and continue (avoid stalling)
        # Clear frames buffer
        self.frames = []

class GymController:
    """Controller that uses a Gymnasium-trained model."""
    
    def __init__(self, model=None):
        self.model = model
    
    def control(self, state):
        if self.model is None:
            return random.choice(list(Actions))
        
        # Convert state dict to observation array
        obs = state_to_obs(state)
        action, _ = self.model.predict(obs)
        
        if action == 0:
            return Actions.LEFT
        elif action == 1:
            return Actions.RIGHT
        else:
            return None
    
    @staticmethod
    def _state_to_obs(state):
        # kept for backward compatibility; delegate to shared helper
        return state_to_obs(state)


def state_to_obs(state):
    """Convert the `state` dict (from bouncai.py) into the observation array
    format used by the Gym environment.
    """

    obs_list = []
    screen_width = 400
    screen_height = 600
    max_platforms = 10

    # 1. Player State
    # Normalize X pos (0 to 1) just so it knows if it's near the edge
    player_rect = state.get('player')
    obs_list.append(player_rect.x / screen_width)
    obs_list.append(player_rect.y / screen_height)

    # 2. Platform State (Relative & Normalized)
    # Get all platforms
    platforms = state.get('platforms')
    
    # Sort platforms by distance to player to ensure consistency
    #platforms = [p for p in platforms if p.rect.y <= player_rect.y - 300]
    #platforms.sort(key=lambda p: player_rect.y - p.rect.y)
    
    for i in range(max_platforms):
        if i < len(platforms):
            p = platforms[i]
            # Relative X distance normalized (-1 to 1)
            rel_x = (p.x - player_rect.x) / screen_width
            # Relative Y distance normalized (-1 to 1)
            rel_y = (p.y - player_rect.y) / screen_height
            
            obs_list.append(rel_x)
            obs_list.append(rel_y)
            obs_list.append(p.width / screen_width) # Normalized width
        else:
            # Padding for missing platforms
            obs_list.append(0.0) 
            obs_list.append(1.0) # Far below/away
            obs_list.append(0.0)
    
    # 3. Enemy State (Relative & Normalized)
    enemies = state.get('enemies')
    if enemies:
        # Find nearest enemy
        nearest_enemy = min(enemies, key=lambda e: (e.x - player_rect.x)**2 + (e.y - player_rect.y)**2)
        obs_list.append((nearest_enemy.x - player_rect.x) / screen_width)
        obs_list.append((nearest_enemy.y - player_rect.y) / screen_height)
    else:
        obs_list.append(0.0)
        obs_list.append(1.0) # Far away

    # 4. Wind State (Relative & Normalized)
    winds = state.get('winds')
    if winds:
        nearest_wind = min(winds, key=lambda w: (w.x - player_rect.x)**2 + (w.y - player_rect.y)**2)
        obs_list.append((nearest_wind.x - player_rect.x) / screen_width)
        obs_list.append((nearest_wind.y - player_rect.y) / screen_height)
    else:
        obs_list.append(0.0)
        obs_list.append(1.0)

    return np.array(obs_list, dtype=np.float32)