=======
BouncAI
=======


.. image:: https://readthedocs.org/projects/bouncai/badge/?version=latest
        :target: https://bouncai.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status



An endless jumping game to develop AI agents for

Description
-----------

BouncAI is an endless jumping game where players control a character that automatically bounces upward when landing on platforms. The goal is to navigate the character as high as possible by bouncing from platform to platform without falling or colliding with enemies. The game progressively gets more challenging with moving platforms and flying enemies appearing as your score increases.

The game is designed to be a testbed for developing and evaluating AI agents, allowing users to implement and train their own algorithms to play the game autonomously. For starting, a manual control mode is provided where the human player can control the character using keyboard inputs.

The project is inspired by the tutorial series of GitHub user `russs123` and their Jumpy game: https://github.com/russs123/Jumpy

Getting Started
---------------

Dependencies
~~~~~~~~~~~~

- Python 3.6 or higher
- Pygame 2.0.0 or higher

Installing
~~~~~~~~~~

It's recommended to use a virtual environment to install BouncAI to avoid conflicts with other Python packages. The installation steps vary slightly depending on your operating system.

Prerequisites
^^^^^^^^^^^^^

Ensure you have Python 3.6 or higher and Git installed on your system.

Linux (Debian/Ubuntu)
^^^^^^^^^^^^^^^^^^^^^^

1. Install required system packages:

::

   # Update package list
   sudo apt update

   # Install Python, pip, and development tools
   sudo apt install python3 python3-pip python3-venv git

   # Install pygame dependencies (optional, for better performance)
   sudo apt install python3-dev libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev

2. Clone and install BouncAI:

::

   # Clone the repository
   git clone https://git.informatik.tu-freiberg.de/vorlesungen/bouncai.git
   cd bouncai

   # Create and activate a virtual environment
   python3 -m venv venv
   source venv/bin/activate

   # Install in development mode
   pip install -e .

Linux (Fedora/RHEL/CentOS)
^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Install required system packages:

::

   # For Fedora
   sudo dnf install python3 python3-pip python3-devel git

   # For RHEL/CentOS (with EPEL repository enabled)
   sudo yum install python3 python3-pip python3-devel git

   # Install pygame dependencies (optional)
   sudo dnf install SDL2-devel SDL2_image-devel SDL2_mixer-devel SDL2_ttf-devel  # Fedora
   # or
   sudo yum install SDL2-devel SDL2_image-devel SDL2_mixer-devel SDL2_ttf-devel  # RHEL/CentOS

2. Clone and install BouncAI:

::

   # Clone the repository
   git clone https://git.informatik.tu-freiberg.de/vorlesungen/bouncai.git
   cd bouncai

   # Create and activate a virtual environment
   python3 -m venv venv
   source venv/bin/activate

   # Install in development mode
   pip install -e .

Unix (macOS)
^^^^^^^^^^^^

1. Install prerequisites using Homebrew (recommended):

::

   # Install Homebrew if not already installed
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

   # Install Python and Git
   brew install python git

   # Install pygame dependencies (optional)
   brew install sdl2 sdl2_image sdl2_mixer sdl2_ttf

2. Clone and install BouncAI:

::

   # Clone the repository
   git clone https://git.informatik.tu-freiberg.de/vorlesungen/bouncai.git
   cd bouncai

   # Create and activate a virtual environment
   python3 -m venv venv
   source venv/bin/activate

   # Install in development mode
   pip install -e .

Alternative for macOS without Homebrew:

::

   # If using system Python or Python from python.org
   # Clone the repository
   git clone https://git.informatik.tu-freiberg.de/vorlesungen/bouncai.git
   cd bouncai

   # Create and activate a virtual environment
   python3 -m venv venv
   source venv/bin/activate

   # Install in development mode
   pip install -e .

Windows (PowerShell)
^^^^^^^^^^^^^^^^^^^^

1. Install Python from https://www.python.org/downloads/ (ensure "Add Python to PATH" is checked)

2. Install Git from https://git-scm.com/download/win

3. Open PowerShell and run:

::

   # Clone the repository
   git clone https://gitlab.hrz.tu-chemnitz.de/vorlesungen/kuenstliche_intelligenz/ws25-26/bouncai.git
   cd bouncai

   # Create and activate a virtual environment
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   # If execution policy prevents script execution, run:
   # Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

   # Install in development mode
   pip install -e .

Windows (WSL - Windows Subsystem for Linux)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Install WSL2 with Ubuntu from the Microsoft Store

2. Open WSL terminal and follow the Linux (Debian/Ubuntu) instructions:

::

   # Update package list
   sudo apt update

   # Install Python, pip, and development tools
   sudo apt install python3 python3-pip python3-venv git

   # Clone the repository
   git clone https://gitlab.hrz.tu-chemnitz.de/vorlesungen/kuenstliche_intelligenz/ws25-26/bouncai.git
   cd bouncai

   # Create and activate a virtual environment
   python3 -m venv venv
   source venv/bin/activate

   # Install in development mode
   pip install -e .

Note for WSL: You may need to install an X server (like VcXsrv) on Windows to run GUI applications, or use WSL2 with WSLg support.

Verification
^^^^^^^^^^^^

After installation, verify that BouncAI is working correctly:

::

   # Test the installation
   bouncai --help

   # Generate a sample configuration
   bouncai --generate-config sample_config.json

   # Run the game
   bouncai

Executing program
~~~~~~~~~~~~~~~~~

Run the game with:

::

   bouncai

Command-line options:
- ``--config`` or ``-c``: Load a custom configuration file (JSON format)
- ``--generate-config`` or ``-g``: Generate a default configuration file

Examples:

::

   # Run with default settings
   bouncai

   # Generate a default configuration file
   bouncai --generate-config my_config.json

   # Run with custom configuration
   bouncai --config my_config.json

Game Controls:
- A/D: Move left/right
- Space: Restart game after Game Over
- Close window to exit the game




AI Development
~~~~~~~~~~~~~

Students interested in developing their own AI agent should start by modifying the ``AIController`` class in ``bouncai/controller.py``. This class has a ``control`` method that takes the game state as input and returns an action (LEFT or RIGHT) that the AI decides to take. Currently, this method just selects a random action, but you can replace this with your own AI algorithm:

.. code-block:: python

   class AIController:
       def __init__(self):
           pass
       def control(self, state):
           # This is where you implement your AI logic
           # The state parameter contains all relevant game information
           # Return either Actions.LEFT or Actions.RIGHT
           action = random.choice(list(Actions))  # Replace with your AI logic
           return action

The ``state`` parameter is a dictionary containing all the information your AI needs to make decisions:

- ``state['player']``: The player's rectangle (position and size)
- ``state['platforms']``: List of platform rectangles
- ``state['enemies']``: List of enemy rectangles
- ``state['winds']``: List of wind area rectangles
- ``state['score']``: Current player score

Using this information, your AI can analyze the game environment to make intelligent decisions, such as:

- Finding the nearest platform to land on
- Avoiding enemies in the path
- Adjusting movement based on wind effects
- Planning ahead based on platform and enemy positions
- Optimizing movement patterns as score/difficulty increases

NEAT-based AI Training
^^^^^^^^^^^^^^^^^^^^^^

BouncAI includes a built-in NEAT (NeuroEvolution of Augmenting Topologies) trainer that evolves neural networks to play the game automatically. NEAT is a genetic algorithm that evolves the structure and weights of neural networks over time.

**Training a NEAT Agent**

To train a new NEAT agent, use the ``--train-neat`` flag:

::

   bouncai --train-neat

Options for training:

- ``--neat-gens``: Number of generations to train (default: 10)
- ``--neat-save``: Path to save the best evolved genome (default: best_genome.pkl)

Examples:

::

   # Train for 50 generations and save to my_best_agent.pkl
   bouncai --train-neat --neat-gens 50 --neat-save my_best_agent.pkl

   # Train for 100 generations with default save location
   bouncai --train-neat --neat-gens 100

**How NEAT Training Works**

1. A population of random neural networks is created
2. Each network plays the game for up to 5000 steps
3. Networks are evaluated based on the score they achieve
4. The best performers are kept and mutated to create the next generation
5. New connections and nodes are added to successful networks
6. This process repeats for the specified number of generations
7. The best genome is saved as a pickled file for later use

The NEAT agent uses a simple feature vector as input:

- Normalized player X position (0-1)
- Normalized player Y position (0-1)
- Player vertical velocity (normalized)
- Relative X distance to nearest platform (normalized)
- Relative Y distance to nearest platform (normalized)

The network outputs two values: a score for moving left and a score for moving right. The action with the higher score is selected.

**Running a Trained Agent**

To play with a previously trained agent, use the ``--ai-genome`` option:

::

   bouncai --ai-genome best_genome.pkl

This will launch the game window where you can watch your trained agent play. The agent will automatically make decisions based on what it learned during training.

Examples:

::

   # Run with the default trained genome
   bouncai --ai-genome best_genome.pkl

   # Run with a custom saved genome
   bouncai --ai-genome my_best_agent.pkl

**Training Tips**

- Start with small generation counts (10-20) to test your setup
- Increase ``--neat-gens`` to 50+ for better results (this will take longer)
- Monitor the console output during training to see fitness scores improving
- Save genomes with descriptive names (e.g., ``genome_gen50.pkl``, ``genome_fast.pkl``)
- You can run multiple training sessions and compare the genomes
- Training is CPU-intensive; use reasonable generation counts on slower machines

Game Features
~~~~~~~~~~~~~

- Automatically bouncing character controlled by left and right movement
- Randomly generated platforms with increasing difficulty
- Moving platforms that appear as difficulty increases
- Flying bird enemies that appear as score increases
- Wind areas that affect player movement
- High score tracking between game sessions
- Smooth scrolling background
- Game over screen with restart option
- Customizable game configuration via JSON files

Configuration
------------

BouncAI supports customization through JSON configuration files. You can adjust various game parameters including:

- Screen dimensions and FPS
- Physics settings (gravity, scrolling threshold)
- Difficulty parameters (platform sizes, enemy speeds)
- Audio volumes
- Colors and visual elements

To create a configuration file:

::

   # Generate a default configuration
   bouncai --generate-config my_config.json

   # Edit the file with your preferred settings
   # Then run the game with your configuration
   bouncai --config my_config.json

Help/Troubleshooting
--------------------

Common Issues:

- If the game fails to start, ensure Pygame is properly installed
- For audio issues, verify that your system has working audio drivers
- If the high score doesn't save, check if the game has write permissions in its directory
- If configuration loading fails, verify your JSON file is properly formatted

For more help, open an issue on the project repository.

Contributing
------------

.. include:: ./CONTRIBUTING.rst


Authors
-------

.. include:: ./AUTHORS.rst

Version History
---------------

.. include:: ./HISTORY.rst


* Free software: MIT license
* Documentation: See docs directory for local documentation.


Acknowledgments
---------------

Inspiration, code snippets, etc. \* `Project this template is based
on <https://gist.github.com/DomPizzie/7a5ff55ffa9081f2de27c315f5018afc>`__
\* `awesome-readme <https://github.com/matiassingers/awesome-readme>`__
\*
`PurpleBooth <https://gist.github.com/PurpleBooth/109311bb0361f32d87a2>`__
\* `dbader <https://github.com/dbader/readme-template>`__ \*
`zenorocha <https://gist.github.com/zenorocha/4526327>`__ \*
`fvcproductions <https://gist.github.com/fvcproductions/1bfc2d4aecb01a834b46>`__

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
