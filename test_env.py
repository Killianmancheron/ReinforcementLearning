import numpy as np
import matplotlib.pyplot as plt
from Environnment import Controller, snake
from Environnment import SnakeGame

env = SnakeGame((15,15),1)
state= env.reset()


dones = [False for _ in range(2)]
plt.imshow(state)
plt.show()
while not all(dones):

    state, rewards, dones = env.step([0,1])
    plt.imshow(state)
    plt.show()
    print(dones)
    print(rewards)

    # a faire:
    # tester model avec etat action => action (pas le choix à ce stade)
    # implémenter MARL DQN et le tester
    # en parallèle :
    # faire 5*5 DQN avec param optimaux et tester 15*15
    # faire HER 5*5, normalement HER doit réussir mieux
    # faire HER 15*15 normalement HER doit réussir mieux
    # IMPORTANT : RESOUDRE CE PROBLEME CAR SINON HORRIBLE
    # Regarder comment marl se comporte