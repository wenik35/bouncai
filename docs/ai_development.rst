=================
AI Agent Development
=================

This guide provides information on how to develop AI agents to play BouncAI autonomously.

Overview
--------

BouncAI is designed as a testbed for artificial intelligence agents. The game's simple mechanics and clear objectives make it an ideal environment for developing and testing various AI approaches, from rule-based systems to reinforcement learning algorithms.

Getting Started
--------------

To create an AI agent for BouncAI, you'll need to:

1. Set up a virtual environment for development
2. Understand the game environment
3. Define state representation
4. Implement action selection
5. Evaluate agent performance

Setting Up Your Development Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It's best practice to use a virtual environment for AI development:

.. code-block:: console

    # Clone the repository if you haven't already
    git clone https://git.informatik.tu-freiberg.de/vorlesungen/bouncai.git
    cd bouncai

    # Create and activate a virtual environment
    python -m venv ai-dev-env

    # On Windows
    ai-dev-env\Scripts\activate

    # On macOS/Linux
    source ai-dev-env/bin/activate

    # Install BouncAI in development mode
    pip install -e .

    # Install additional packages for AI development
    pip install numpy pandas matplotlib tensorflow scikit-learn

Game Environment
---------------

AI agents interact with the same game environment as human players but receive state information and provide actions programmatically instead of via keyboard input.

State Information
~~~~~~~~~~~~~~~~

The game state available to an AI agent includes:

- Player position (x, y coordinates)
- Player velocity (especially vertical velocity)
- Platform positions (list of all visible platforms)
- Enemy positions (list of all visible enemies)
- Current score
- Game dimensions and boundaries

Available Actions
~~~~~~~~~~~~~~~~

AI agents can perform the following actions:

- Move left
- Move right
- No movement (neutral)

Note that jumping is automatic when landing on platforms, so agents only control horizontal movement.

AI Agent Interface
-----------------

To create an AI agent, extend the base ``AIAgent`` class:

.. code-block:: python

   from bouncai.agents.base import AIAgent

   class MyCustomAgent(AIAgent):
       def __init__(self):
           super().__init__()
           # Initialize your agent's parameters here

       def get_action(self, game_state):
           # Process game state and decide on an action
           # Return one of: "left", "right", or "neutral"
           return "neutral"

Example Implementation
---------------------

Here's a simple rule-based agent example:

.. code-block:: python

   class SimpleRuleAgent(AIAgent):
       def get_action(self, game_state):
           player = game_state['player']
           platforms = game_state['platforms']

           # Find the nearest platform below the player
           nearest_platform = None
           nearest_distance = float('inf')

           for platform in platforms:
               # Only consider platforms below the player
               if platform.rect.y > player.rect.y:
                   dist = ((platform.rect.centerx - player.rect.x)**2 +
                          (platform.rect.y - player.rect.y)**2)**0.5
                   if dist < nearest_distance:
                       nearest_distance = dist
                       nearest_platform = platform

           # If a platform is found, move toward it
           if nearest_platform:
               if nearest_platform.rect.centerx < player.rect.x:
                   return "left"
               elif nearest_platform.rect.centerx > player.rect.x:
                   return "right"

           # Default behavior
           return "neutral"

Training with Reinforcement Learning
----------------------------------

For more advanced agents, you can implement reinforcement learning algorithms:

1. **State Representation**: Convert the game state into a vector representation
2. **Reward Function**: Define rewards (e.g., +1 for each point scored, -100 for game over)
3. **Algorithm Selection**: Choose an RL algorithm (DQN, PPO, etc.)
4. **Training Loop**: Create a training loop that:
   - Gets the current state
   - Selects an action using the agent's policy
   - Applies the action to the game
   - Observes the new state and reward
   - Updates the agent's policy

Example frameworks for RL agents:

- Stable Baselines 3
- Ray RLlib
- PyTorch or TensorFlow for custom implementations

Evaluation
---------

To evaluate your AI agent's performance:

1. **Average Score**: Run multiple episodes and calculate the average score
2. **Survival Time**: Measure how long the agent survives
3. **Learning Curve**: For learning agents, plot performance over training iterations
4. **Comparison**: Compare against baseline agents or human performance

Running Your Agent
-----------------

To integrate your custom AI agent with the game, you'll need to modify the main game loop to use your agent's decisions instead of keyboard input. Make sure your virtual environment is activated before running your agent.

.. code-block:: console

   # Activate your virtual environment
   source ai-dev-env/bin/activate  # On macOS/Linux
   ai-dev-env\Scripts\activate     # On Windows

Here's a conceptual example of integrating your agent:

.. code-block:: python

   from bouncai.bouncai import run
   from bouncai.agents import PlayerController
   from my_agents import MyCustomAgent

   # This is a conceptual example - actual implementation
   # would require modifying the game's main loop
   agent = MyCustomAgent()
   controller = PlayerController(agent)
   run(controller=controller)

Visualization
------------

During agent evaluation, you can visualize:

- Agent's current state representation
- Action probabilities or Q-values
- Attention maps (for neural network-based agents)
- Reward signals over time

This visualization helps in understanding the agent's decision-making process and debugging.

Tips for Successful Agents
------------------------

1. **Start Simple**: Begin with rule-based agents before moving to complex algorithms
2. **Prioritize Survival**: Focusing on not falling off the screen is more important than optimizing for maximum score
3. **Balance Exploration**: Ensure your agent tries different strategies, especially early in training
4. **Feature Engineering**: For rule-based agents, carefully design state features that capture relevant information
5. **Hyperparameter Tuning**: For learning agents, experiment with different hyperparameters

Managing Dependencies
-------------------

When developing AI agents, you'll likely need additional libraries:

1. **Record your dependencies**: After installing required packages in your virtual environment:

   .. code-block:: console

       pip freeze > requirements-ai.txt

2. **Share environment configuration**: Include your requirements file when sharing your agent to ensure reproducibility.

3. **Separate environments**: For experimenting with different AI approaches, consider creating separate virtual environments:

   .. code-block:: console

       python -m venv dqn-agent-env
       python -m venv rule-based-agent-env

Community
--------

Share your AI agents with the community! Submit your implementations, results, and insights to the project repository to help advance the field of game-playing AI. Always include setup instructions and environment requirements with your submissions.
