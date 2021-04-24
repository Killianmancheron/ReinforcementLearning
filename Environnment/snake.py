import numpy as np
from collections import deque

class Snake():

  UP=0
  LEFT=1
  RIGHT=2
  DOWN=3

  def __init__(self, init_coord= (7,7) ,body_length=3):
    self.body=deque()
    self.alive=True
    self.head = np.asarray(init_coord).astype(np.int)
    for i in range(body_length-1, 0, -1):
        self.body.append(self.head+np.asarray([i,0]).astype(np.int))
    # The head of the snake will always be the last item of the deque
    self.body.append(self.head)

  def move(self, coord, direction):
    '''
    Return a new coordonate from a direction and a coordonate
    '''
    assert direction<4 and direction>=0

    if direction == self.LEFT:
      return np.asarray([coord[0],coord[1]-1]).astype(int)
    elif direction == self.UP:
      return np.asarray([coord[0]-1,coord[1]]).astype(int)
    elif direction == self.RIGHT:
      return np.asarray([coord[0],coord[1]+1]).astype(int)
    elif direction == self.DOWN:
      return np.asarray([coord[0]+1,coord[1]]).astype(int)
    else :
      raise ValueError("Direction doesn't define, possible values : {0,1,2,3}")
    
  def action(self, direction):
    '''
    move the body of the snake to the direction
    '''
    self.head=self.move(self.head, direction)
    self.body.append(self.head)

