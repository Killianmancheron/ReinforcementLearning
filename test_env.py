import numpy as np
import matplotlib.pyplot as plt
from Environnment import Controller, snake
from Environnment import SnakeGame

env = SnakeGame((5,5),goals=False)
state= env.reset()


state=env.step(1)[0]
plt.imshow(state)
plt.show()
state=env.step(3)[0]
plt.imshow(state)
plt.show()
exit()
print(state)
dones = [False for _ in range(2)]
plt.imshow(state)
plt.show()
while not all(dones):

    plt.imshow(state)
    plt.show()
    print(dones)
    print(rewards)

    # a faire:
    # coder transfert learning DQN
    # (faire liaison serpent et incorporer bordure)
    
    # régler problème GRAVE
    
    #     # en parallèle :
    # tester MARL DQN => reduire taille MARL 7x7
    #=> faire HER 5*5, normalement HER doit réussir mieux
    # faire HER 15*15 normalement HER doit réussir mieux
    # IMPORTANT : RESOUDRE CE PROBLEME CAR SINON HORRIBLE
    