
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
    def __init__(self):
        pass
    def control(self, state):
        print("New")
        print(state['player'])
        print(state['platforms'])
        print(state['enemies'])
        print(state['winds'])
        print(state['score'])
        print("\n\n\n")
        # Use the AI model to predict the next action based on the current state
        action = random.choice(list(Actions))  # Placeholder for AI prediction
        return action
