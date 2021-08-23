import matplotlib
import numpy as np
from random import randint

class Grid():

  # Couleur correspondant aux différentes cases
  BODY_COLOR = [
    np.array([0, .6, .2], dtype=np.float16),
    np.array([0., .357, .588], dtype=np.float16),
    np.array([0., .424, .424], dtype=np.float16),
  ]
  HEAD_COLOR = [
    np.array([0., .4, .2], dtype=np.float16), #serpent vert
    np.array([0.012, .223, .424], dtype=np.float16), #serpent bleu
    np.array([0., .298, .298], dtype=np.float16), #serpent marine
  ]
  APPLE_COLOR = np.array([1., 0.251, 0.251], dtype=np.float16)
  SPACE_COLOR = np.array([0.992, 0.961, 0.902], dtype=np.float16)
  TARGET_COLOR = np.array([1], dtype=np.float16)
  BACK_COLOR = np.array([0], dtype=np.float16)

  BODY_CODE = [1]
  HEAD_CODE = [2]
  APPLE_CODE = -1
  SPACE_CODE = 0

  def __init__(self, size = (15,15), unit_size=10, unit_gap=1):
    """Classe correspondant à une référence de l'état du jeu. 
    Gère l'appaparition d'une pomme et le rendu de la grille en image.

    Args:
        size (tuple, optional): Taille de la grille. Defaults to (15,15).
        unit_size (int, optional): Nombre de pixel equivalents à une case. Defaults to 10.
        unit_gap (int, optional): Nombre de pixel de séparation entre deux cases. Defaults to 1.
    """    
    self.unit_size = int(unit_size)
    self.unit_gap = unit_gap
    self.size=np.asarray(size, dtype=np.int)
    self.reset_board()
    self.apples = []

  def reset_board(self):
    """Réinitialise la grille à vide
    """    
    self.board=np.zeros(self.size)

  def update_board(self, snakes):
    """Mets à jour la grille en ajoutant des éléments sur la grille : les serpents et les pommes.

    Args:
        snakes (list<snake>): Liste des différents serpents de l'environnement.

    Returns:
        np.array: Grille actualisée avec les nouveaux éléments.
            0 : emplacement vide
            1 : corps du serpent
            2 : tête du serpent
            3 : pomme
    """    
    self.reset_board()
    # Ajout des pommes
    for apple in self.apples:
      self.board[apple[0]][apple[1]]=self.APPLE_CODE
    if len(snakes)==1:
      # Ajout des serpents
      for snake in snakes:
        if not snake.alive:
          continue
        # Ajout du corps
        for coord in snake.body :
          self.board[coord[0]][coord[1]]=self.BODY_CODE[0]
          # Ajout de la tête
        head=snake.head
        self.board[head[0]][head[1]]=self.HEAD_CODE[0]
    else :
      for snake in snakes:
        if not snake.alive:
          continue
        # Ajout du corps
        for coord in snake.body :
          self.board[coord[0]][coord[1]]=snake.id
          # Ajout de la tête
        
        head=snake.head
        self.board[head[0]][head[1]]=snake.id+1
    return self.board.copy()

  def spawn_apple(self):
    """Fais apparaître un pomme sur la grille. Ne peut apparaître que sur un emplacement vide.
    """    
    possible=np.where(self.board==0)
    if len(possible[0])!=0:
      index=np.random.randint(0,len(possible[0]))
      new_apple = np.asarray((possible[0][index],possible[1][index])).astype(int)
      self.apples.append(new_apple)
      # Ajout de la nouvelle pomme sur la grille
      self.board[new_apple[0]][new_apple[1]]=self.APPLE_CODE
      return new_apple
    else : 
      new_apple = np.array([0,0])
      self.apples.append(new_apple)
  
  def drop_apple(self, coordonate):
    """Retire un pomme de la liste des pommes

    Args:
        coordonate (np.array): coordonées de la pomme à retirer
    """    
    self.apples = [apple for apple in self.apples if (not np.array_equal(apple, coordonate))]

  def color_case(self, coordonate, color):
    """Color la case située à une coordonnée dans la grille dans l'affichage selon une couleur définie

    Args:
        coordonate (np.array): couple de coordonnées x,y à colorier
        color (list): couleur RBG de la case à colorier
    """    
    x, y = coordonate[0], coordonate[1]
    self.render[x:(x+1),
                y:(y+1)]=color


  def get_render(self,snakes):
    """Permet l'affichage de la grille en image.

    Args:
        snakes (list<snake>): Liste des serpents présents sur la grille

    Returns:
        np.array: Image de la grille
    """    
    # Coloration de l'arrière plan et des pommes
    height = self.size[1]
    width = self.size[0]
    self.render=np.zeros((height,width,4))
    self.render[:,:,:]=[0.,0.,0.,0.]
    for apple in self.apples : 
      self.color_case(apple, [1.,0.,0.,0.])
    # Coloration des serpents
    for i, snake in enumerate(snakes):
      if not snake.alive :
        continue
      
      for coord in snake.body:
        self.color_case(coord, [0.,1.,0.,0.])
      #self.link_body(snake.body, self.BODY_COLOR[i])
      self.color_case(snake.head, [0.,0.,1.-i,i])
    return self.render.copy()
  
  def get_render_without_apple(self,snakes):
    """Permet l'affichage de la grille en image.

    Args:
        snakes (list<snake>): Liste des serpents présents sur la grille

    Returns:
        np.array: Image de la grille
    """    
    # Coloration de l'arrière plan et des pommes
    height = self.size[1]*self.unit_size
    width = self.size[0]*self.unit_size
    self.render=np.zeros((height+self.unit_gap,width+self.unit_gap,3))
    self.render[:,:,:]=self.SPACE_COLOR
    for apple in self.apples : 
      self.color_case(apple, self.SPACE_COLOR)
    # Coloration des serpents
    for i, snake in enumerate(snakes):
      if not snake.alive :
        continue
      for coord in snake.body:
        self.color_case(coord, self.BODY_COLOR[i])
      self.color_case(snake.head, self.HEAD_COLOR[i])
    return self.render.copy()
  

  def get_target_render(self):
    """Permet l'affichage de l'image correspondant à l'objectif

    Returns:
        [type]: [description]
    """    
    height = self.size[1]*self.unit_size
    width = self.size[0]*self.unit_size
    self.render=np.zeros((height+self.unit_gap,width+self.unit_gap,1))
    self.render[:,:,:]=self.BACK_COLOR
    for apple in self.apples : 
      self.color_case(apple, self.TARGET_COLOR)
    return self.render.copy()

  def isfull(self):
    return not (-1 in self.board)|(0 in self.board)