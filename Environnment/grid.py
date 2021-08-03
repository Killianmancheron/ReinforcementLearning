import numpy as np
import random

class Grid():

  # Couleur correspondant aux différentes cases
  BODY_COLOR = np.array([0, 1., 0], dtype=np.uint8)
  HEAD_COLOR = np.array([1., 0, 0], dtype=np.uint8)
  APPLE_COLOR = np.array([0, 0, 1.], dtype=np.uint8)
  SPACE_COLOR = np.array([0, 0, 0], dtype=np.uint8)

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
    self.height = self.size[1]*self.unit_size
    self.width = self.size[0]*self.unit_size
    self.reset_board()
    self.apples = []

  def reset_board(self):
    """Réinitialise la grille à vide
    """    
    self.board=np.zeros(self.size)

  def update_board(self, snakes):
    """Mets à jour la grille en ajoutant des éléments sur la grille : les serpents et les pommes.

    Args:
        snakes (list<snake>): Liste des différents serpents encore en vie dans l'environnement.

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
      self.board[apple[0]][apple[1]]=3
    # Ajout des serpents
    for snake in snakes:
      # Ajout du corps
      for coord in snake.body :
        self.board[coord[0]][coord[1]]=1
        # Ajout de la tête
      head=snake.head
      self.board[head[0]][head[1]]=2
    return self.board.copy()

  def spawn_apple(self):
    """Fais apparaître un pomme sur la grille. Ne peut apparaître que sur un emplacement vide.
    """    
    possible=np.where(self.board==0)
    self.apples.append(np.asarray((random.choice(possible[0]),random.choice(possible[1]))).astype(int))
  
  def drop_apple(self, coord):
    """Retire un pomme de la liste des pommes

    Args:
        coord (np.array): coordonées de la pomme à retirer
    """    
    self.apples = [apple for apple in self.apples if np.array_equal(apple, coord)]

  def color_case(self, coordonate, color):
    """Color la case située à une coordonnée dans la grille dans l'affichage selon une couleur définie

    Args:
        coordonate (np.array): couple de coordonnées x,y à colorier
        color (list): couleur RBG de la case à colorier
    """    
    x, y = coordonate[0], coordonate[1]
    self.render[x*self.unit_size+1:(x+1)*self.unit_size,
                y*self.unit_size+1:(y+1)*self.unit_size]=color

  def get_render(self,snakes):
    """Permet l'affichage de la grille en image.

    Args:
        snakes (list<snake>): Liste des serpents présents sur la grille

    Returns:
        np.array: Image de la grille
    """    
    # Coloration de l'arrière plan et des pommes
    self.render = self.get_target_render()
    # Coloration des serpents
    for snake in snakes:
      for coord in snake.body:
        self.color_case(coord, self.BODY_COLOR)
      self.color_case(snake.head, self.HEAD_COLOR)
    return self.render.copy()

  def get_target_render(self):
    """Permet l'affichage de l'image correspondant à l'objectif

    Returns:
        [type]: [description]
    """    
    self.render=np.zeros((self.height+self.unit_gap,self.width+self.unit_gap,3))
    self.render[:,:,:]=self.SPACE_COLOR
    for apple in self.apples : 
      self.color_case(apple, self.APPLE_COLOR)
    return self.render.copy()

  