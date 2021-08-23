from agent import Agent
import gym
import torch
import random
import time


env = gym.make('LunarLander-v2')
env.seed(0)
print(env.action_space.n)
print(env.observation_space.shape[0])
agent = Agent(state_size=env.action_space.n,
              action_size=env.observation_space.shape[0], seed=0)

# load the weights from file
agent.qnetwork_local.load_state_dict(torch.load('checkpoint_per.pth'))

for i in range(10):
    state = env.reset()
    for j in range(200):
        action = agent.act(state)

        state, reward, done, _ = env.step(action)
        # env.render()
        if done:
            time.sleep(1)
            break

# for j in range(15):
#     for i in range(5):
#         state = env.reset()
#         for j in range(200):
#             action = agent.act(state)
#             env.render()
#             state, reward, done, _ = env.step(action)
#             if done:
#                 break
