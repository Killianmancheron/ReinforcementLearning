import numpy as np
import matplotlib.pyplot as plt
from Environnment import Controller, snake
from Environnment import SnakeGame

env = SnakeGame((15,15),goals=True)
state, goal= env.reset()
print(goal.shape)
plt.imshow(state)
plt.show()
plt.imshow(goal)
plt.show()
exit()
print(state)
dones = [False for _ in range(2)]
plt.imshow(state)
plt.show()
while not all(dones):

    state, rewards, dones = env.step([0,3])
    plt.imshow(state)
    plt.show()
    print(dones)
    print(rewards)

    # a faire:
    # tester MARL DQN 
    # reduire taille MARL
    # 
    #     # en parallèle :
    #=> faire HER 5*5, normalement HER doit réussir mieux
    # faire HER 15*15 normalement HER doit réussir mieux
    # IMPORTANT : RESOUDRE CE PROBLEME CAR SINON HORRIBLE
    