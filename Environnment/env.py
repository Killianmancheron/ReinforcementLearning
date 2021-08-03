import matplotlib.pyplot as plt
import numpy as np
import gym
from gym import spaces
from Environnment import Controller

class SnakeGame():

  def __init__(self, grid_size=(15,15), nb_snakes=1):
    self.grid_size = grid_size
    self.nb_snakes = nb_snakes
    # Define action and observation space
    self.action_space = spaces.Discrete(4)
    self.viewer=None

  def step(self, action):
    if type(action)==int: # Action pour un seul serpent 
      self.board, reward, done=self.controller.execute(action)
      return self.board, reward, done
    else :
      self.board, reward, done = self.controller.execute_multiple(action)

  def reset(self):
    self.controller=Controller(self.grid_size, nb_snakes=self.nb_snakes)
    self.board=self.controller.get_board()
    return self.board

  def render(self, frame_speed=0.1):
    if self.viewer==None:
      self.fig = plt.figure()
      self.viewer = self.fig.add_subplot(111)
      plt.ion()
      self.fig.show()
    else:
      self.viewer.clear()
      self.viewer.imshow(self.board)
      plt.pause(frame_speed)
    self.fig.canvas.draw_idle()
