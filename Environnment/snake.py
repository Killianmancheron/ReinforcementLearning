import numpy as np
from collections import deque
from random import randint
from .move import Move

class Snake():

  def __init__(self, init_coord, id, body_length=3, direction='top'):
    """Classe correspondant aux serpents et aux méthodes relatives.

    Args:
        init_coord (np.array): Coordonnées d'apparition du serpent 
        body_length (int, optional): Taille du corps (tête comprise). Defaults to 3.
    """    
    self.body=deque()
    self.alive=True
    self.id=id
    self.head = np.asarray(init_coord).astype(np.int)
    # Le corps est placé automatiquement de haut en bas
    print(direction)
    if direction=='top':
      for i in range(body_length-1, 0, -1):
          self.body.append(self.head+np.asarray([i,0]).astype(np.int))
    elif direction=='down':
      for i in range(body_length-1, 0, -1):
          self.body.append(self.head-np.asarray([i,0]).astype(np.int))
    # La tête du serpent sera toujours le dernier élément du deque
    print(self.body)
    self.body.append(self.head)
      
  def action(self, direction):
    '''
    Déplace le corps du serpent vers une direction
    '''
    self.head=Move(self.head, direction).next_coord()
    self.body.append(self.head)

