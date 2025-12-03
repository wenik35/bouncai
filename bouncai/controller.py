# Enum defining valid actions for the controller
from enum import Enum

import pygame
import random
import numpy as np
import os

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
    def __init__(self, model_path: str = "bouncai_model", deterministic: bool = True):
        self.model = None
        self.deterministic = deterministic
        self.model_path = model_path

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
        # If no model, return random action
        if self.model is None:
            return random.choice(list(Actions))

        # Convert state dict to observation array
        obs = state_to_obs(state)

        try:
            action, _ = self.model.predict(obs, deterministic=self.deterministic)
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

    Observation ordering (11 values):
    [player_x, player_y, player_vel_y,
     nearest_platform_x, nearest_platform_y, nearest_platform_width,
     nearest_enemy_x, nearest_enemy_y,
     nearest_wind_x, nearest_wind_y,
     score]
    """
    # Extract player rect
    player_rect = state.get('player')
    if player_rect is None:
        px = py = 0.0
    else:
        px = float(player_rect.x)
        py = float(player_rect.y)

    # Player velocity not provided by the state dict; assume 0
    pvel_y = 0.0

    # Nearest platform (prefer platforms below the player)
    platforms = state.get('platforms', [])
    nearest_platform = None
    min_distance = float('inf')
    for p in platforms:
        try:
            # p is a rect-like object
            dist = abs(p.y - py)
            if dist < min_distance and p.y > py:
                min_distance = dist
                nearest_platform = p
        except Exception:
            continue

    if nearest_platform is not None:
        np_x = float(nearest_platform.x)
        np_y = float(nearest_platform.y)
        np_w = float(getattr(nearest_platform, 'width', getattr(nearest_platform, 'w', 0)))
    else:
        np_x = 0.0
        np_y = float(state.get('screen_height', 0) or 600)
        np_w = 0.0

    # Nearest enemy
    enemies = state.get('enemies', [])
    nearest_enemy = None
    min_enemy_dist = float('inf')
    for e in enemies:
        try:
            dist = abs(e.x - px) + abs(e.y - py)
            if dist < min_enemy_dist:
                min_enemy_dist = dist
                nearest_enemy = e
        except Exception:
            continue

    if nearest_enemy is not None:
        ne_x = float(nearest_enemy.x)
        ne_y = float(nearest_enemy.y)
    else:
        ne_x = 0.0
        ne_y = -1000.0

    # Nearest wind
    winds = state.get('winds', [])
    nearest_wind = None
    min_wind_dist = float('inf')
    for w in winds:
        try:
            dist = abs(w.x - px) + abs(w.y - py)
            if dist < min_wind_dist:
                min_wind_dist = dist
                nearest_wind = w
        except Exception:
            continue

    if nearest_wind is not None:
        nw_x = float(nearest_wind.x)
        nw_y = float(nearest_wind.y)
    else:
        nw_x = 0.0
        nw_y = -1000.0

    score = float(state.get('score', 0.0))

    obs = np.array([
        px,
        py,
        pvel_y,
        np_x,
        np_y,
        np_w,
        ne_x,
        ne_y,
        nw_x,
        nw_y,
        score
    ], dtype=np.float32)

    # Many RL libs expect shape (n,) or (1, n). We'll return 1D array; callers
    # can reshape if needed.
    return obs
