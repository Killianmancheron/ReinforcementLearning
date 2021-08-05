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

  def step(self, actions):
    if self.nb_snakes==1: # Action pour un seul serpent 
      actions = [actions]
    self.board, rewards, dones=self.controller.execute(actions)
    self.target = self.controller.get_target()
    if self.nb_snakes==1:
      return self.board, rewards[0], dones[0], self.target
    else :
      return self.board, rewards, dones, self.target

  def reset(self):
    self.controller=Controller(self.grid_size, nb_snakes=self.nb_snakes)
    self.board=self.controller.get_board()
    self.target = self.controller.get_target()
    return self.board, self.target

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
