import json
from agent import Agent
import gym
import random
import torch
import numpy as np
from collections import deque
import matplotlib.pyplot as plt
from collections import namedtuple, deque
import random
import time
import argparse
from open_environment import Environment as open_env
from moving_environment import Environment as moving_env
from maze_environment import Environment as maze

parser = argparse.ArgumentParser(description='Env select')
parser.add_argument('-env', type=str, help='lunar / mount',
                    choices=['lunar', 'mount', 'open', 'moving', 'maze'])
# parser.add_argument('-seed', type=int, help='seed')
args = parser.parse_args()

if args.env == 'lunar':
    print('LunarLander environment selected')
    env = gym.make('LunarLander-v2')
elif args.env == 'mount':
    print('MountainCar environment selected')
    env = gym.make('MountainCar-v0')
elif args.env == 'open':
    print('Open grid environment selected')
    env = open_env()
elif args.env == 'moving':
    print('Moving target environment selected')
    env = moving_env()
elif args.env == 'maze':
    print('Maze environment selected')
    env = maze()

# s = args.seed
# print('seed ', s)

# env.seed(s)
# print('Action space: ', env.action_space.n)
# print('Action observation: ', env.observation_space.shape[0])
# agent = Agent(state_size=env.observation_space.shape[0],
#               action_size=env.action_space.n, seed=0)

# n_episodes = 10_000
# max_t = 200
# eps_start = 1.0
# eps_end = 0.01
# eps_decay = 0.9995


############### for grid world only ######################
agent = Agent(state_size=2, action_size=4, seed=3)

n_episodes = 100_000
max_t = 200
eps_start = 1.0
eps_end = 0.01
eps_decay = 0.99995  # 0.999936
############### for grid world only ######################


def per(n_episodes=n_episodes, max_t=max_t, eps_start=eps_start, eps_end=eps_end, eps_decay=eps_decay):
    """Deep Q-Learning using PER.

    Params
    ======
        n_episodes (int): maximum number of training episodes
        max_t (int): maximum number of timesteps per episode
        eps_start (float): starting value of epsilon, for epsilon-greedy action selection
        eps_end (float): minimum value of epsilon
        eps_decay (float): multiplicative factor (per episode) for decreasing epsilon
    """
    scores = []                        # list containing scores from each episode
    scores_window = deque(maxlen=100)  # last 100 scores
    eps = eps_start                    # initialize epsilon
    max_score = 150.0

    for i_episode in range(1, n_episodes+1):
        state = env.reset()
        score = 0
        for t in range(max_t):
            env.render()
            action = agent.act(state, eps)
            next_state, reward, done = env.step(action)
            agent.step(state, action, reward, next_state, done)
            state = next_state
            score += reward
            if done:
                break
        scores_window.append(score)       # save most recent score
        scores.append(score)              # save most recent score
        eps = max(eps_end, eps_decay*eps)  # decrease epsilon
        print('\rEpisode {}\tAverage Score: {:.2f}'.format(
            i_episode, np.mean(scores_window)), end="")
        if i_episode % 100 == 0:
            print('\rEpisode {}\tAverage Score: {:.2f}'.format(
                i_episode, np.mean(scores_window)))
            #elapsed_time = time.time() - start_time
            #print("Duration: ", elapsed_time)
        if np.mean(scores_window) >= max_score:
            max_score = np.mean(scores_window)
            print('\nEnvironment solved in {:d} episodes!\tAverage Score: {:.2f}'.format(
                i_episode-100, np.mean(scores_window)))
            torch.save(agent.qnetwork_local.state_dict(),
                       "checkpoint_per_"+str(args.env)+".pth")
    #elapsed_time = time.time() - start_time
    #print("Training duration: ", elapsed_time)
    return scores


start_time = time.time()
scores = per()
end_time = time.time()

scores_per_np = np.array(scores)
np.savetxt("scores_per_"+str(args.env)+".txt", scores_per_np)


def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "Execution time: %d hours : %02d minutes : %02d seconds" % (hour, minutes, seconds)


n = end_time-start_time
train_time = convert(n)
print(train_time)


train_info_dictionary = {'algorithm': 'PER', 'env': args.env, 'eps_start': eps_start, 'eps_end': eps_end,
                         'eps_decay': eps_decay, 'episodes': n_episodes, 'train_time': train_time}

train_info_file = open('train_info_'+str(args.env)+'.json', 'w')
json.dump(train_info_dictionary, train_info_file)
train_info_file.close()


def moving_average(a, n=100):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n


scores_ma_per = moving_average(scores, n=100)

# plot the scores
fig = plt.figure()
ax = fig.add_subplot(111)
plt.plot(np.arange(len(scores_ma_per)), scores_ma_per)
plt.ylabel('Score')
plt.xlabel('Episode #')
plt.savefig('graph_per_'+str(args.env)+'.png')
