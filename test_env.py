import numpy as np
import matplotlib.pyplot as plt
from Environnment import Controller, snake

Game = Controller((5,5), nb_snakes=1)
Game.grid.apples = [np.array([1,2])]
print(Game.grid.board)
print(Game.grid.apples)
#plt.imshow(Game.get_board())
#plt.show()
render, rewards, is_alive = Game.execute([0])
print(rewards)
print(is_alive)
print(Game.grid.board)

print(Game.grid.apples)