import numpy as np
import random

class Grid():

  BODY_COLOR = np.array([0,1,0], dtype=np.uint8)
  HEAD_COLOR = np.array([1, 0, 0], dtype=np.uint8)
  APPLE_COLOR = np.array([0,0,1], dtype=np.uint8)
  SPACE_COLOR = np.array([0,0,0], dtype=np.uint8)

  def __init__(self, size = (15,15), unit_size=10, unit_gap=1):
    self.unit_size = int(unit_size)
    self.unit_gap = unit_gap
    self.size=np.asarray(size, dtype=np.int)
    self.height = self.size[1]*self.unit_size
    self.width = self.size[0]*self.unit_size
    self.reset_board()

  def reset_board(self):
    self.board=np.zeros(self.size)

  def update_board(self, snakes):
    self.reset_board()
    self.board[self.apple[0]][self.apple[1]]=3
    for snake in snakes:
      for coord in snake.body :
        self.board[coord[0]][coord[1]]=1
      head= snake.head
      self.board[head[0]][head[1]]=2
    return self.board.copy()

  def spawn_apple(self):
    possible=np.where(self.board==0)
    self.apple=np.asarray((random.choice(possible[0]),random.choice(possible[1]))).astype(int)
  
  def color_case(self, coordonate, color):
    x, y = coordonate[0], coordonate[1]
    self.render[x*self.unit_size+1:(x+1)*self.unit_size,
                y*self.unit_size+1:(y+1)*self.unit_size]=color

  def get_render(self,snakes):
    self.render = self.get_target_render()
    for snake in snakes:
      for coord in snake.body:
        self.color_case(coord, self.BODY_COLOR)
      self.color_case(snake.head, self.HEAD_COLOR)
    return self.render.copy()

  def get_target_render(self):
    self.render=np.zeros((self.height+self.unit_gap,self.width+self.unit_gap,3))
    self.render[:,:,:]=self.SPACE_COLOR
    self.color_case(self.apple, self.APPLE_COLOR)
    return self.render.copy()

  