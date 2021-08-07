import numpy as np
import matplotlib.pyplot as plt
from Environnment import Controller, snake
from Environnment import SnakeGame

env = SnakeGame((15,15),2)
state= env.reset()

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
    # Refaire rewards et apple spaws (regler pb end game)
    # tester MARL DQN 

    # en parallèle :
    # aggréger courbe, gif model, screen state interessant
    # tester 15*15
    # faire HER 5*5, normalement HER doit réussir mieux
    # faire HER 15*15 normalement HER doit réussir mieux
    # IMPORTANT : RESOUDRE CE PROBLEME CAR SINON HORRIBLE
    # Regarder comment marl se comporte