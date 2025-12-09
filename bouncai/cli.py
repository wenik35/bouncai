"""Console script for bouncai.

This module provides the command-line interface (CLI) for launching the BouncAI game.
It uses the Click library to handle command-line arguments and calls the main game
function from the bouncai module. It also provides an option to load custom game
configuration from a file.
"""
import sys
import os
import click
import bouncai.bouncai as bouncai
from bouncai.world.config import load_config, create_default_config
import bouncai.world.config as config_module
import bouncai.bouncai as game_main
from bouncai import neat_agent

@click.command()
@click.option('--config', '-c', type=click.Path(exists=True, dir_okay=False, readable=True),
              help='Path to a JSON configuration file to customize game settings.')
@click.option('--generate-config', '-g', type=click.Path(dir_okay=False, writable=True),
              help='Generate a default configuration file at the specified path.')
@click.option('--manual', '-m', is_flag=True,
              help='Use manual control for the player (default is AI control).')
@click.option('--train-neat', is_flag=True,
              help='Run a NEAT training session (requires neat-python).')
@click.option('--neat-gens', default=10, show_default=True,
              help='Number of generations to evolve when training NEAT.')
@click.option('--neat-save', default='best_genome.pkl', show_default=True,
              help='Path to save the best genome from NEAT training.')
@click.option('--ai-genome', type=click.Path(exists=True, dir_okay=False, readable=True),
              help='Path to a saved genome to run in the game.')
def main(config=None, generate_config=None, args=None, manual=False, train_neat=False, neat_gens=10, neat_save='best_genome.pkl', ai_genome=None):
    """Console script for launching the BouncAI game.

    This function serves as the entry point for the CLI. When executed,
    it starts the BouncAI game by calling the run function from the
    bouncai module.

    Args:
        config: Path to a configuration file (JSON format)
        generate_config: Path where to generate a default configuration file
        manual: Flag to enable manual control of the player
        args: Command line arguments (not currently used)

    Returns:
        int: Return code 0 for successful execution
    """
    # Generate default configuration if requested
    if generate_config:
        if create_default_config(generate_config):
            click.echo(f"Default configuration generated at '{generate_config}'")
            return 0
        else:
            click.echo(f"Error: Failed to generate configuration at '{generate_config}'")
            return 1

    # Load custom configuration if provided
    if config:
        if not os.path.exists(config):
            click.echo(f"Error: Configuration file '{config}' not found.")
            return 1

        if not load_config(config):
            click.echo(f"Error: Failed to load configuration from '{config}'.")
            return 1

        click.echo(f"Loaded configuration from '{config}'")

    # Set control mode
    if manual:
        config_module.config["CONTROLLER"] = "manual"

    # If ai_genome provided, instruct game to use it
    if ai_genome:
        config_module.config["AI_GENOME_PATH"] = ai_genome
        config_module.config["CONTROLLER"] = "ai"

    # If training requested, run NEAT trainer and exit
    if train_neat:
        click.echo(f"Starting NEAT training for {neat_gens} generations...")
        try:
            path = neat_agent.train(generations=neat_gens, save_path=neat_save)
            click.echo(f"Training complete. Best genome saved to {path}")
        except Exception as e:
            click.echo(f"Error during NEAT training: {e}")
            return 1
        return 0

    # Otherwise run the game normally
    score = game_main.run()
    print(f"Final Score: {score}")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
