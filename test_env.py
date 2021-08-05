import numpy as np
import matplotlib.pyplot as plt
from Environnment import Controller, snake

Game = Controller((5,5), nb_snakes=1)
print(Game.grid.board)
print(Game.grid.apples)
#plt.imshow(Game.get_board())
#plt.show()