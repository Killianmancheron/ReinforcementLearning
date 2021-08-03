import numpy as np
from collections import deque

from .move import Move

class Snake():

  def __init__(self, init_coord= (7,7) ,body_length=3):
    self.body=deque()
    self.alive=True
    self.head = np.asarray(init_coord).astype(np.int)
    for i in range(body_length-1, 0, -1):
        self.body.append(self.head+np.asarray([i,0]).astype(np.int))
    # The head of the snake will always be the last item of the deque
    self.body.append(self.head)
      
  def action(self, direction):
    '''
    move the body of the snake to the direction
    '''
    self.head=Move(self.head, direction).next_coord()
    self.body.append(self.head)

