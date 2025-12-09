
# Enum defining valid actions for the controller
from enum import Enum

import pygame
import random

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
    def __init__(self, net=None):
        """AI Controller that uses a neural network to decide actions.

        Args:
            net: A callable network with .activate(inputs) that returns output list.
                 If None and `bouncai.world.config.config["AI_GENOME_PATH"]` is set,
                 the controller will try to load a pickled genome and create a
                 compatible network at runtime. The network is expected to be a
                 neat.nn.FeedForwardNetwork or similar with an `activate` method.
        """
        self.net = net

    def control(self, state):
        """Return an action based on the current `state` using the provided network.

        The network should output two values (left_score, right_score). The
        larger value determines the action. If no network is available, the
        controller falls back to a random action.
        """
        # build a small feature vector from the state
        try:
            player = state.get('player')
            platforms = state.get('platforms', [])
            # Normalize by screen width/height from config to keep inputs small
            from bouncai.world.config import config as cfg
            sw = cfg.get("SCREEN_WIDTH", 400)
            sh = cfg.get("SCREEN_HEIGHT", 600)

            px = player.x / sw
            py = player.y / sh
            # approximate vertical velocity if available
            pv = getattr(player, 'vel_y', 0) / 50.0

            # nearest platform (by vertical distance)
            nearest_dx = 0.0
            nearest_dy = 1.0
            if platforms:
                # platforms are rects; find one with smallest positive dy (above player)
                best = None
                best_dy = None
                for p in platforms:
                    dy = (p.y - player.y)
                    if best is None or abs(dy) < abs(best_dy):
                        best = p
                        best_dy = dy
                if best is not None:
                    nearest_dx = (best.x - player.x) / sw
                    nearest_dy = (best.y - player.y) / sh

            inputs = [px, py, pv, nearest_dx, nearest_dy]

            if self.net is None:
                # lazy-load network if path provided in config
                genome_path = cfg.get("AI_GENOME_PATH")
                if genome_path:
                    try:
                        import pickle
                        import neat
                        with open(genome_path, 'rb') as f:
                            genome = pickle.load(f)
                        # build a temporary config for the genome that matches default
                        from bouncai import neat_agent
                        neat_config = neat_agent.get_neat_config()
                        self.net = neat.nn.FeedForwardNetwork.create(genome, neat_config)
                    except Exception:
                        self.net = None

            if self.net is not None:
                out = self.net.activate(inputs)
                # expect two outputs: left_score, right_score
                if len(out) >= 2:
                    if out[0] > out[1]:
                        return Actions.LEFT
                    else:
                        return Actions.RIGHT
        except Exception:
            # if anything goes wrong fallback to random
            pass

        # fallback random action
        return random.choice(list(Actions))
