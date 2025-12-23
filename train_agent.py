import gymnasium as gym
from stable_baselines3 import DQN, PPO
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.vec_env import SubprocVecEnv, VecFrameStack, DummyVecEnv
from bouncai.env import BouncAIEnv
import os
import pygame
import torch as th

# Ensure assets exist
if not os.path.exists("assets"):
    print("Warning: assets directory not found!")

class RenderCallback(BaseCallback):
    """Callback for rendering episodes during training."""
    
    def __init__(self, render_env, render_freq=5000):
        super().__init__()
        render_env_base = BouncAIEnv(render_mode="human")
        self.render_env = VecFrameStack(DummyVecEnv([lambda: render_env_base]), n_stack=4)
        self.render_freq = render_freq
        self.last_render = 0
    
    def _on_step(self) -> bool:
        if self.num_timesteps - self.last_render >= self.render_freq:
            self.last_render = self.num_timesteps
            print(f"\n--- Rendering at {self.num_timesteps} timesteps ---")
            
            try:
                obs, _ = self.render_env.reset()
                done = False
                episode_reward = 0
                steps = 0
                
                while not done and steps < 2000:
                    action, _ = self.model.predict(obs, deterministic=True)
                    obs, reward, terminated, truncated, info = self.render_env.step(action)
                    self.render_env.render()
                    episode_reward += reward
                    done = terminated or truncated
                    steps += 1
                
                print(f"Episode reward: {episode_reward:.2f}, Score: {info.get('score', 0)}")
            except Exception as e:
                print(f"[ERROR] Rendering failed: {e}")
        
        return True

# Initialize pygame first
if not pygame.display.get_init():
    print("Initializing pygame display...")
    try:
        # Try to create a dummy display to ensure video mode is set
        pygame.init()
        pygame.mixer.init()
    except Exception as e:
        print(f"[ERROR] Failed to initialize pygame: {e}")

# Number of parallel environments
NUM_ENVS = 1

def make_env(rank):
    """Factory function to create environment instances for SubprocVecEnv."""
    def _init():
        env = BouncAIEnv(render_mode=None)
        return env
    return _init

# Initialize pygame first
if not pygame.display.get_init():
    print("Initializing pygame display...")
    try:
        # Try to create a dummy display to ensure video mode is set
        pygame.init()
        pygame.mixer.init()
    except Exception as e:
        print(f"[ERROR] Failed to initialize pygame: {e}")

if __name__ == "__main__":
    # Create parallel training environments
    print(f"Creating {NUM_ENVS} parallel training environments...")
    train_env = SubprocVecEnv([make_env(i) for i in range(NUM_ENVS)])
    train_env = VecFrameStack(train_env, n_stack=4)

    # Create render environment for visualization
    print("Creating render environment...")
    render_env = BouncAIEnv(render_mode="human")

    # Custom actor (pi) and value function (vf) networks
    # of two layers of size 32 each with Relu activation function
    # Note: an extra linear layer will be added on top of the pi and the vf nets, respectively
    policy_kwargs = dict(activation_fn=th.nn.ReLU,
                         net_arch=dict(pi=[128, 128], vf=[128, 128]))

    # Create or load model
    try:
        model = PPO.load("bouncai_model", env=train_env)
        print("Loaded existing model")
    except:
        print("Creating new model")
        model = PPO(
            "MlpPolicy",
            train_env,
    #        policy_kwargs=policy_kwargs,
            verbose=1,
            ent_coef = 0.005,
            learning_rate=3e-4,
            n_steps=8192,
            batch_size=64,
            n_epochs=10
        )

    # Train with rendering callback
    render_callback = RenderCallback(render_env, render_freq=5000000)

    try:
        model.learn(total_timesteps=1000000, callback=render_callback, progress_bar=True)
    except KeyboardInterrupt:
        print("\nTraining interrupted by user")
    except Exception as e:
        print(f"\n[ERROR] Training failed: {e}")
        import traceback
        traceback.print_exc()

    # Save model
    model.save("bouncai_model")
    print("Model saved as bouncai_model")

    train_env.close()
    render_env.close()
    pygame.quit()
