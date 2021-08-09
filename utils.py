import matplotlib.pyplot as plt
from os.path import exists
from os import mkdir
from pickle import dump, load
from Environnment import SnakeGame

def save_episoide(size, Agent, n_playout, folder):
    if not exists(folder):
        mkdir(folder)

    env = SnakeGame(size)
    state = env.reset()
    done=False
    num_fig = 0

    plt.imshow(state)
    plt.savefig(folder+'\{} {} {}.png'.format(n_playout, size, num_fig))

    while not done :
        action = Agent.BestMove(env, n_playout)
        observation, reward, done  = env.step(action)

        state = observation
        num_fig +=1
        plt.imshow(state)
        plt.savefig(folder+'\{} {} {}.png'.format(n_playout, size, num_fig))
        print(env.controller.grid.board)

def save_rewards(rewards, filename, folder):
    if not exists(folder):
        mkdir(folder)


    with open(folder+filename+'.pickle', 'wb') as handle:
        dump(rewards, handle)

def open_rewards(filename, folder):
    with open(folder+filename+'.pickle', 'rb') as handle:
        return load(handle)