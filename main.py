import numpy as np
import matplotlib.pyplot as plt
from Environnment import Controller, snake

Game = Controller((15,15), nb_snakes=2)
print(Game.grid.board)
render, rewards, is_alive = Game.execute([0,1])
print(rewards)
print(is_alive)
print(Game.grid.board)
#plt.imshow(render)
#plt.show()
