"""NEAT training utilities for BouncAI.

This module provides a small NEAT integration to evolve agents that play
the BouncAI game. It uses `neat-python` and the game's `World`/`Player`
classes to simulate episodes (headless). The training is kept intentionally
simple and minimal so it can be adapted.
"""
import os
import time
import pickle

import neat
import pygame

from bouncai.world.world import World
from bouncai.world.player import Player
from bouncai.world.spritesheet import SpriteSheet
from bouncai.world.config import config as game_config


def get_neat_config(path=None):
    """Return a `neat.Config` loaded from the package's `neat_config.ini`.

    If `path` is provided, it will be used instead.
    """
    if path is None:
        path = os.path.join(os.path.dirname(__file__), 'neat_config.ini')
    local_dir = os.path.dirname(__file__)
    return neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                       neat.DefaultSpeciesSet, neat.DefaultStagnation,
                       path)


class _DummySound:
    def play(self):
        return None


def _make_world():
    """Create a World and Player using minimal dummy surfaces.

    Returns (world, player)
    """
    # ensure pygame is initialized
    pygame.init()

    sw = game_config.get('SCREEN_WIDTH', 400)
    sh = game_config.get('SCREEN_HEIGHT', 600)

    # Set a hidden display mode (required by pygame even for headless training)
    # Use HIDDEN flag so no window appears
    pygame.display.set_mode((1, 1), flags=pygame.HIDDEN)

    bg = pygame.Surface((sw, sh)).convert_alpha()
    platform_img = pygame.Surface((100, 10)).convert_alpha()
    wind_img = pygame.Surface((65, 65)).convert_alpha()
    bird_sheet_img = pygame.Surface((64, 64)).convert_alpha()
    bird_sheet = SpriteSheet(bird_sheet_img)

    world = World(bg, platform_img, bird_sheet, wind_img)
    player = Player(world, sw // 2, sh - 150, pygame.Surface((45, 45)), _DummySound())
    return world, player


def _extract_inputs(player, platforms, max_platforms=10):
    """Convert a state into a feature vector for the network.

    Inputs: player x, y, vel_y, then for each of up to max_platforms:
            (platform_x, platform_y, platform_width) normalized to screen dimensions.
    
    If fewer platforms exist, pad with zeros.
    Total inputs: 3 (player) + max_platforms * 3 = 33 (for max_platforms=10)
    """
    sw = game_config.get('SCREEN_WIDTH', 400)
    sh = game_config.get('SCREEN_HEIGHT', 600)

    inputs = []
    
    # Player state (always 3 inputs)
    px = player.rect.x / float(sw)
    py = player.rect.y / float(sh)
    pv = player.vel_y / 50.0
    inputs.extend([px, py, pv])

    # All platforms (sorted by distance from player, closest first)
    sorted_platforms = sorted(
        platforms,
        key=lambda p: abs(p.rect.y - player.rect.y)
    )[:max_platforms]

    # Add platform data
    for p in sorted_platforms:
        platform_x = p.rect.x / float(sw)
        platform_y = p.rect.y / float(sh)
        platform_w = p.rect.width / float(sw)
        inputs.extend([platform_x, platform_y, platform_w])

    # Pad with zeros if fewer platforms than max
    for _ in range(len(sorted_platforms), max_platforms):
        inputs.extend([0.0, 0.0, 0.0])

    return inputs


def _run_episode_for_genome(genome, neat_config, max_steps=5000, debug=False):
    """Simulate an episode using `genome` and return a fitness value.

    The genome will be converted to a feed-forward network.
    Fitness is based primarily on score (height reached), with a small survival bonus.
    """
    from bouncai.controller import Actions
    
    try:
        net = neat.nn.FeedForwardNetwork.create(genome, neat_config)

        world, player = _make_world()

        steps = 0
        max_score = 0.0
        sh = game_config.get('SCREEN_HEIGHT', 600)
        # track jumps (bounces) as an auxiliary reward
        jumps = 0
        prev_vel = player.vel_y

        while steps < max_steps and not world.game_over:
            # Extract inputs from current state
            platforms_list = list(world.platform_group)
            inputs = _extract_inputs(player, platforms_list)

            # Get network output: [left_score, right_score]
            out = net.activate(inputs)
            
            # Interpret outputs: higher score wins
            if len(out) >= 2:
                if out[0] > out[1]:
                    action = Actions.LEFT
                else:
                    action = Actions.RIGHT
            else:
                # Fallback to right if output is malformed
                action = Actions.RIGHT

            # Apply the action and get scroll amount
            scroll = player.move(action)

            # detect bounce: player.vel_y becomes strongly negative after being >=0
            if prev_vel >= 0 and player.vel_y < -10:
                jumps += 1
            prev_vel = player.vel_y
            
            # Update world state
            world.update(scroll)

            steps += 1
            
            # Track best score achieved (primary fitness metric)
            if world.score > max_score:
                max_score = world.score

            # End if player fell off screen
            if player.rect.top > sh:
                break

        # Fitness = score achieved + bonus per successful bounce + small survival bonus
        # Bounce reward encourages landing on platforms rather than just surviving.
        fitness = float(max_score) + (jumps * 50.0) + (steps * 0.001)
        
        return fitness
    except Exception as e:
        # Silent fail for robustness
        return 0.0


def eval_genomes(genomes, neat_config):
    """NEAT-compatible genomes evaluator.

    Sets `genome.fitness` for each genome.
    """
    import random
    runs_per_genome = 3
    fitnesses = []
    for gid, genome in genomes:
        total = 0.0
        for run_idx in range(runs_per_genome):
            # vary RNG so environments differ across runs
            random.seed(gid * 7919 + run_idx)
            try:
                f = _run_episode_for_genome(genome, neat_config)
            except Exception:
                f = 0.0
            total += f
        fitness = total / float(runs_per_genome)
        genome.fitness = fitness
        fitnesses.append(fitness)

    # Print brief stats for this generation
    if fitnesses:
        print(f"  Gen fitness: min={min(fitnesses):.1f}, max={max(fitnesses):.1f}, avg={sum(fitnesses)/len(fitnesses):.1f}")


def train(generations=10, pop_size=50, neat_cfg_path=None, save_path='best_genome.pkl'):
    """Train NEAT for a number of generations and save the best genome.

    Returns the path to the saved genome.
    """
    cfg = get_neat_config(neat_cfg_path)
    p = neat.Population(cfg)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(lambda genomes, config: eval_genomes(genomes, cfg), generations)

    # save winner
    with open(save_path, 'wb') as f:
        pickle.dump(winner, f)

    return save_path


def run_best(genome_path):
    """Run a saved genome in a visible game window (for manual inspection).

    This function will launch the regular game loop but use the genome for control.
    """
    import bouncai.bouncai as game_main
    # set config so the game will try to load the genome
    game_config['AI_GENOME_PATH'] = genome_path
    game_config['CONTROLLER'] = 'ai'
    return game_main.run()
