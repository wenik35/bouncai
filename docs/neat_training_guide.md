# NEAT Training & Playback Guide

This guide explains how to train a NEAT-based AI agent and how to run it in the game.

## Quick Start

### Training a New Agent

```bash
# Train for 10 generations (fast, for testing)
bouncai --train-neat

# Train for 50 generations (better results, takes longer)
bouncai --train-neat --neat-gens 50 --neat-save my_agent.pkl

# Train for 100 generations (best results, very slow)
bouncai --train-neat --neat-gens 100 --neat-save my_best_agent.pkl
```

### Playing with a Trained Agent

```bash
# Watch your trained agent play
bouncai --ai-genome best_genome.pkl

# Run with a custom trained agent
bouncai --ai-genome my_agent.pkl
```

## Understanding NEAT

**NEAT** (NeuroEvolution of Augmenting Topologies) is a genetic algorithm that evolves neural networks. Instead of using hand-crafted rules, NEAT discovers what the network should look like (structure and weights) through natural selection.

### How It Works

1. **Initial Population**: Start with random, simple neural networks
2. **Evaluation**: Each network plays one complete game episode
3. **Fitness Scoring**: Networks are scored based on how high they got (score)
4. **Selection**: The best-performing networks are kept
5. **Mutation**: The kept networks are mutated and recombined to create the next generation
6. **Repeat**: Generations improve over time as the algorithm explores the space of possible networks

### Why NEAT is Good for BouncAI

- **Simplicity**: Works with minimal configuration
- **Adaptability**: Automatically discovers the right network complexity
- **Interpretability**: You can inspect the evolved networks
- **Effectiveness**: Often finds solutions humans might not design

## Training Details

### Input Features

The network receives 5 normalized inputs:

| Input | Range | Description |
|-------|-------|-------------|
| Player X | 0-1 | Horizontal position (0=left edge, 1=right edge) |
| Player Y | 0-1 | Vertical position (0=top, 1=bottom) |
| Velocity | -1 to 1 | Player's vertical speed |
| Nearest Platform ΔX | -1 to 1 | Horizontal distance to nearest platform |
| Nearest Platform ΔY | -1 to 1 | Vertical distance to nearest platform |

### Output Actions

The network produces 2 outputs:

| Output | Meaning |
|--------|---------|
| Left Score | How much to move left |
| Right Score | How much to move right |

The action with the **higher score** is selected at each step.

### Fitness Function

Fitness = **Score** (height reached) + **Survival bonus** (0.01 × steps survived)

Higher score = better fitness. Networks that get higher are rewarded more than those that survive longer.

## Training Parameters

All training parameters are in `bouncai/neat_config.ini`:

| Parameter | Default | Effect |
|-----------|---------|--------|
| `pop_size` | 50 | Number of networks per generation (larger = slower, better) |
| `max_stagnation` | 15 | Generations without improvement before stopping |
| `conn_add_prob` | 0.5 | Probability of adding a new connection (higher = more complex) |
| `node_add_prob` | 0.2 | Probability of adding a new node (higher = more complex) |
| `weight_mutate_rate` | 0.8 | How often weights change |

To customize training, edit `bouncai/neat_config.ini` before running `--train-neat`.

## Practical Examples

### Scenario 1: Quick Test (5 minutes)

Test your setup without heavy computation:

```bash
bouncai --train-neat --neat-gens 5 --neat-save test_genome.pkl
```

Then play with the result:

```bash
bouncai --ai-genome test_genome.pkl
```

### Scenario 2: Good Agent (20 minutes)

Train an agent that plays reasonably well:

```bash
bouncai --train-neat --neat-gens 30 --neat-save good_agent.pkl
```

### Scenario 3: Best Agent (1+ hour)

Train the best possible agent (for overnight runs):

```bash
bouncai --train-neat --neat-gens 150 --neat-save best_agent.pkl
```

## Tips & Tricks

1. **Start small**: Test with 5-10 generations first to ensure everything works
2. **Save different versions**: Use descriptive names like `agent_fast.pkl`, `agent_balanced.pkl`
3. **Monitor progress**: Console output shows fitness per generation; watch it improve
4. **Watch gameplay**: After training, always playback to verify the agent works
5. **Experiment with config**: Try different `pop_size` (50 to 200) for different trade-offs
6. **Track best scores**: Note which training runs produced the best agents

## Troubleshooting

### Training is too slow

- Reduce `--neat-gens` to 10-20
- Reduce `pop_size` in `neat_config.ini` (trade-off: may get worse results)
- Use a faster machine

### Agent plays poorly

- Train for more generations (try 50 instead of 10)
- Ensure `neat_config.ini` is not corrupted
- Try different seeds by running training multiple times

### `best_genome.pkl` not created

- Check that the training completed (look for final console message)
- Ensure the directory is writable
- Try specifying a full path: `--neat-save /full/path/to/agent.pkl`

## Advanced: Training Multiple Populations

You can run multiple training sessions in parallel:

```bash
# Terminal 1
bouncai --train-neat --neat-gens 50 --neat-save agent_1.pkl

# Terminal 2 (while Terminal 1 runs)
bouncai --train-neat --neat-gens 50 --neat-save agent_2.pkl

# Compare results
bouncai --ai-genome agent_1.pkl
bouncai --ai-genome agent_2.pkl
```

## Next Steps

- Experiment with different generation counts
- Try modifying `neat_config.ini` to explore different network topologies
- Consider adding more input features (e.g., enemy positions, wind effects)
- Implement a tournament mode to compare different agents
- Log training statistics for analysis
