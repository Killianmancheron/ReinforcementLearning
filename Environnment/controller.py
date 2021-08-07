import numpy as np
import random
from .move import Move
from .snake import Snake
from .grid import Grid

class Abstract_Controller():

  def __init__(self, grid_size=(15,15), nb_snakes=1, nb_apples=1,seed=None):
    """Classe abstraite du controleur pour l'encapsulation de la grille

    Args:
        grid_size (tuple, optional): Taille de la grille. Defaults to (15,15).
        nb_snakes (int, optional): Nombre de serpents. Defaults to 1.
    """    
    self.grid_size = grid_size
    self.grid=Grid(grid_size, seed=seed)
    # Coordonnées maximales de la grille

    self.nb_apples = nb_apples
    self.nb_snakes = nb_snakes
    # Positionne les serpents sur la grille
    self.init_snakes()

    # On actualise la grille avec tous les éléments
    self.grid.update_board(self.snakes)

    # On fait appraître autant de pommes que de serpents
    for _ in range(nb_apples):
      self.grid.spawn_apple()


  def init_snakes(self):
    """Permet de faire apparaître les serpents sur la grille et les enregistre dans une liste
    """    
    assert (self.nb_snakes>0)|(self.nb_snakes<10), "Nombre de serpents limités de 1 à 9"
    mid_grid=tuple([int(x/2) for x in self.grid_size])
    if self.nb_snakes==1:
      
      self.snakes=[Snake(init_coord=mid_grid, id=1)]
    else :
      # spawn_points = self.get_spawn_points()
      self.snakes=[]
      for i in range(self.nb_snakes):
        direction ='top' if i==0 else 'down'
        spawn_coord = np.array([10-6*i,mid_grid[1]])
        self.snakes.append(Snake(init_coord=spawn_coord,id=2*i+1, direction=direction))
       

  def is_output(self, coord):
    """Permet de vérifier si des coordonnées sont hors de la grille ou non

    Args:
        coord (np.array): Coordonnées à vérifier

    Returns:
        Boolean: Vrai si les coordonnées sont valides
    """    
    max_x=self.grid_size[0]-1
    max_y=self.grid_size[1]-1
    return (coord[0]<0 or coord[0]>max_x) or (coord[1]<0 or coord[1]>max_y)

  def get_spawn_points(self):
    """Permet de récupérer l'ensembles des points où les têtes de serpents peuvent apparaître

    Returns:
        list(<np.array>): Liste des coordonnées servant de points d'apparition des têtes de serpents
    """    
    grid = np.zeros(self.grid_size)
    # à généraliser
    grid[np.arange(3,15,4),:]+=1
    grid[:,np.arange(2,15,5)]+=1
    list_x, list_y = np.where(grid==2)
    spawn_points = []
    for x, y in zip(list_x, list_y):
      spawn_points.append(np.array([x,y]))
    return spawn_points


  
class Controller(Abstract_Controller):

  def __init__(self, grid_size=(15,15), nb_snakes=1, nb_apples=1, goals=False):
    """Classe permettant le controle de la grille avec le serpent, de vérifier si des déplacements sont possibles, etc.

    Args:
        grid_size (tuple, optional): Taille de la grille. Defaults to (15,15).
        nb_snakes (int, optional): Nombre de serpents. Defaults to 1.
    """    
    Abstract_Controller.__init__(self, grid_size, nb_snakes, nb_apples=1,seed=None)
    self.goals =False

  def get_reward(self, snake, direction):
    """Permet de récupérer une récompense pour un serpent et une action.
    L'ensemble des règles est limité à un serpent, la collision n'est pas gérée.
    Une récompense est positive si le serpent se déplace sur une pomme
    Une récompense est négative si le serpent sort de la grille ou percute son corps
    Sinon la récompense est négative

    Args:
        snake (<Snake>): Serpent dont on souhaite connaître la valeur de son action
        direction (int): Direction à prendre pour le serpent (UP=0, LEFT=1, RIGHT=2, DOWN=3)

    Returns:
        int: récompense obtenue pour l'action éfectuée
    """    
    next_coord=Move(snake.head, direction).next_coord()
    # Gestion de l'action hors de la grille
    if self.is_output(next_coord):
      snake.alive=False
      if self.nb_snakes>1:
        return -10
      else:
        return -1
    # Gestion des pommes
    for apple in self.grid.apples :
      if np.array_equal(next_coord,apple):
        # On retire la pomme de la liste
        self.grid.drop_apple(apple)
        return 1
    # Suppression de la queue
    snake.body.popleft()
    # Gestion colision avec queue
    if any((next_coord == x).all() for x in snake.body):
      snake.alive=False
      if self.nb_snakes>1:
        return -10
      else :
        return -1
    return 0

  def execute(self, directions):
    """Execute l'ensemble des directions sur les serpents, gère les collisions, les actions, 
    les récompenses et les pommes. si un serpent meurt, son cadavre disparaît.

    Args:
        directions (list<int>): Ensembles des directions à prendre pour chaque serpent

    Returns:
        tuple: état du jeu, récompenses à chaque agent, liste des agents en vie
    """    
    rewards = []
    for snake, direction in zip(self.select_alive_snakes(),directions) : 
      # Récupération des récompenses individuelles
      reward = self.get_reward(snake, direction)
      rewards.append(reward)
      # Execution des actions pour chaque serpent
      if snake.alive :
        snake.action(direction)
    # Gestion de la collision sur tous les serpents
    self.control_collision(rewards)
    self.grid.update_board(self.snakes)
    # On souhaite autant de pommes que de serpents vivants
    while len(self.grid.apples)<self.nb_apples:
      self.grid.spawn_apple()

    if self.nb_snakes!=1:
      rewards = self.harmonic(rewards)

    if self.is_done():
      dones = [True for snake in self.snakes]
    else :
      dones = self.dones_snakes()
    return self.get_board(), rewards, dones

  def control_collision(self, rewards):
    """Gère les collisions entre serpents. S'appui sur les serpents en vie uniquement.
    (Donc si un serpetn se suicide ou sort de la grille, aucun serpent ne peut entrer en collision avec)

    Args:
        rewards (list<int>): Liste des récompenses à modifier (-1 si un serpent en percute un autre)

    Returns:
        list<int>: La liste des récompenses modifiées.
    """    
    for i, snake in enumerate(self.select_alive_snakes()):
      # Selection des autres serpents
      other_snakes = [s for j,s in enumerate(self.select_alive_snakes()) if j!=i]
      for other_snake in other_snakes:
        # Vérification si la tête du serpent se trouve dans le corps des autres serpents
        if any((snake.head == x).all() for x in other_snake.body):
          if self.nb_snakes>1:
            rewards[i]-=10
          else :
            rewards[i]-=1
          snake.alive=False
    return rewards

  def select_alive_snakes(self):
    """Sélectionne uniquement les serpents en vie

    Returns:
        list<Snake>: Liste des serpents vivants
    """    
    return [snake for snake in self.snakes if snake.alive]

  def dones_snakes(self):
    """Renvoie une liste des serpents de booléen avec True si un serpent est en vie

    Returns:
        List<boolean>: Liste informant si un serpent est vivant ou non
    """    
    return [(not snake.alive) for snake in self.snakes]

  def is_done(self):
    """Permet de savoir si la partie est finie ou non. 
    S'il n'y qu'un serpent, elle se termine s'il meurt.
    S'il y en a plusieurs, elle se termine lorsqu'il n'en reste plus qu'un.

    Returns:
        boolean: Partie finie ou non
    """    
    nb_snakes=len(self.snakes)
    nb_alives=sum([snake.alive for snake in self.snakes])
    if (nb_snakes==1) and (nb_alives==0):
      return True
    if (nb_snakes>1) and (nb_alives<=1):
      return True
    return False

  def harmonic(self, rewards):
    """Lorsque plusieurs serpents sont présents, les récompenses doivent être de somme nulle.
    Pour cela, on harmonise les récompenses. Ici deux harmonisations sont faites :
    - harmonisation des récompenses positives (bonus pour ceux ayant une récompense de 1, malus aux autres)
    - harmonisation des récompenses négatives (malus pour ceux ayant une récompense de -1, bonus aux autres)

    Args:
        rewards (list<int>): Liste des récompenses

    Returns:
        list<flaot>: Liste harmonique des récompenses.
    """    
    nb_snakes = len(rewards)
    new_rewards = np.zeros(nb_snakes)
    # Gestion des serpents avec une récompense de +1
    Bonus = sum([(reward==1) for reward in rewards])
    new_rewards+=np.where(np.array(rewards)==1,(nb_snakes-Bonus), -Bonus)
    # Gestion des serpents avec une récompense de -1
    Malus = sum([(reward==-10) for reward in rewards])
    new_rewards+=np.where(np.array(rewards)==-10,-(nb_snakes-Malus), Malus)
    return new_rewards
  
  # Getters
  def get_board(self):
    """Permet de récupérer l'image du jeu

    Returns:
        np.array : Image de la représentation de la grille
    """    
    if self.goals:
      return self.grid.get_render_without_apple(self.select_alive_snakes())
    else:
      return self.grid.get_render(self.select_alive_snakes())

  def get_target(self):
    """Permet de récupérer l'image des objectifs sur la grille

    Returns:
        np.array : Image de la représentation de la grille 
    """    
    return self.grid.get_target_render()
