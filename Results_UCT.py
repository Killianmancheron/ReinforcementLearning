import numpy as np
import matplotlib.pyplot as plt
from Environnment import Controller, snake
from Environnment import SnakeGame
from Agent.UCT import UCT
from Agent.GRAVE import GRAVE
from utils import save_episoide, save_rewards

# size = (5,5)
# n_playout=10000
# folder = r'.\Records\UCT'
# agent = UCT()
# save_episoide(size, agent, n_playout, folder)

def get_rewards(size, nb_episodes, n_playout, Agent):
    env = SnakeGame(size)
    total_rewards = []
    for n in range(nb_episodes):
        print('episode : {}'.format(n))
        sum_rewards = 0
        env.reset()
        done=False
        while not done :
            action = Agent.BestMove(env, n_playout)
            _, reward, done  = env.step(action)
            sum_rewards += reward
        total_rewards.append(sum_rewards)
        records = {'n_playout':n_playout, 'size':size, 'rewards':total_rewards}
        save_rewards(records, folder=folder, filename=r'\rewards {} {}'.format(size,n_playout))
    return total_rewards

size = (5,5)
agent = UCT()
folder = r'.\Records\rewards\UCT'

def save_records_playouts(nb_episodes = 20):
    for n_playout in [10000]:#1,10,100,1000,
        get_rewards(size, nb_episodes, n_playout, agent)

save_records_playouts(nb_episodes = 20)