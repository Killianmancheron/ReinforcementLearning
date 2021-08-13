import numpy as np
import matplotlib.pyplot as plt
from Environnment import Controller, snake
from Environnment import SnakeGame
from Agent.UCT import UCT
from Agent.GRAVE import GRAVE
from utils import save_episoide, save_rewards


size = (5,5)
n_playout=5000
# folder = r'.\Records\UCT'
agent = GRAVE()
# save_episoide(size, agent, n_playout, folder)

env = SnakeGame(size)
total_rewards = []
sum_rewards = 0
env.reset()
done=False
while not done :
    action = agent.BestMove(env, n_playout)
    _, reward, done  = env.step(action)
    sum_rewards += reward
    print(env.controller.grid.board)
total_rewards.append(sum_rewards)
records = {'n_playout':n_playout, 'size':size, 'rewards':total_rewards}
# save_rewards(records, folder=folder, filename=r'\rewards {} {}'.format(size,n_playout))


# size = (5,5)
# agent = UCT()
# folder = r'.\Records\rewards\UCT'

# def save_records_playouts(nb_episodes = 20):
#     for n_playout in [10000]:#1,10,100,1000,
#         get_rewards(size, nb_episodes, n_playout, agent)

# save_records_playouts(nb_episodes = 20)