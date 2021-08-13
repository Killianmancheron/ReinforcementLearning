import matplotlib.pyplot as plt
import numpy as np

from Environnment import Controller

class SnakeGame():

  def __init__(self, grid_size=(15,15), nb_snakes=1, nb_apples=1, goals=False, gridmode=False):
    self.grid_size = grid_size
    self.nb_snakes = nb_snakes
    self.nb_apples = nb_apples
    self.goals=goals
    self.gridmode=gridmode
    self.viewer=None
    self.total_score=0
    

  def step(self, actions):
    if self.nb_snakes==1: # Action pour un seul serpent 
      actions = [actions]
    self.board, rewards, dones=self.controller.execute(actions)
    self.target = self.controller.get_target()

    self.h =self.controller.h

    self.done = self.controller.is_done()
    self.total_score += rewards[0]

    if self.nb_snakes==1:
      if self.goals :
        return self.board, rewards[0], dones[0], self.target
      else :
        return self.board, rewards[0], dones[0]

    else :
      if self.goals :
        return self.board, rewards, dones, self.target
      else :
        return self.board, rewards, dones

  def reset(self):
    self.controller=Controller(self.grid_size, nb_snakes=self.nb_snakes, nb_apples=self.nb_apples, goals=self.goals, gridmode=self.gridmode)
    self.board=self.controller.get_board()
    self.target = self.controller.get_target()

    self.total_score = 0
    self.h =self.controller.h
    self.done = self.controller.is_done()

    if self.goals :
      return self.board, self.target
    else : 
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

  #============================================#

  def legalMoves(self):
    return self.controller.legalMoves()

  def isdone(self):
    return self.done

  def score(self):
    return min(self.total_score*2+1,1)

  def playout(self):   
    return self.controller.playout()