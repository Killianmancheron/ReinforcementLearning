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
    # finir entrainement expert : recharger reward
    # faire courbe tl et identification des différents facteurs. 1/3
    # faire tl sur modèle plus peitt
    # regarder coupage de tête ~
    # régler problème GRAVE
    

    # => faire HER 5*5 en fonction de recompenses, sans reward et avec goal 
    # tester importance sampling dessus
    # Comparer perf en fonction du nombre d'objectif sample au bout d'un certain nombre d'itérations

    #     # en parallèle :
    # tester MARL DQN => reduire taille MARL 7x7
    # coder UCT MARL

     1515 regarder nombre de coups moyens par parties
    # faire HER 15*15 normalement HER doit réussir mieux
    # IMPORTANT : RESOUDRE CE PROBLEME CAR SINON HORRIBLE
    
    # pour diiapo :
    # animation de l'évolution des priorités selon les épisodes

    # a écrire :
    
    # faire resultat tl p2
    # faire prio dans partie à part aveanbt tl
    # incorporer resultat prio de DQN
    
    
    # voir tl model tete 