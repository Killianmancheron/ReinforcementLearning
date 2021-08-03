import numpy as np
from .move import Move
from .snake import Snake
from .grid import Grid

class Abstract_Controller():

  def __init__(self, grid_size=(15,15)):
    self.grid=Grid(grid_size)
    self.max_x=grid_size[0]-1
    self.max_y=grid_size[1]-1
    
    self.grid.spawn_apple()
    self.grid.update_board(self.snakes)

  def init_snakes(self):
    assert (self.nb_snakes<=0)|(self.nb_snakes>=10), "Nombre de serpents limités de 1 à 9"
    if self.nb_snakes==1:
      mid_grid=tuple([int(x/2) for x in self.grid_size])
      self.snakes=[Snake(init_coord=mid_grid)]
    else :
      spawn_points = self.get_spawn_points()
      self.snakes=[Snake(init_coord=coord) for coord in spawn_points]

  def is_output(self, coord):
    return (coord[0]<0 or coord[0]>self.max_x) or (coord[1]<0 or coord[1]>self.max_y)

  def get_spawn_points(self):
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

  def __init__(self, grid_size=(15,15), nb_snakes=1):
    Abstract_Controller.__init__(self, grid_size)
    self.nb_snakes = nb_snakes
    self.init_snakes()

  def get_reward(self, snake, direction):
    next_coord=Move(snake.head, direction).next_coord()
    reward=0
    #gestion de l'action hors de la grille
    if self.is_output(next_coord):
      snake.alive=False
      reward=-1
    else:
      # gestion pomme
      if np.array_equal(next_coord,self.grid.apple):
        self.grid.spawn_apple()
        reward=1
      else:
        #suppression de la queue
        snake.body.popleft()
        #gestion colision avec queue
        if any((next_coord == x).all() for x in snake.body):
          snake.alive=False
          reward=-1
    return reward

  def execute(self, directions):
    rewards = []
    for snake, direction in zip(self.select_alive_snakes(),directions) : 
      reward = self.get_reward(snake, direction)
      rewards.append(reward)
      if snake.alive :
        snake.action(direction)
    self.control_collision()
    rewards = self.harmonic(rewards)
    return self.get_board(), reward, self.is_alive()

  def control_collision(self, rewards, directions):
    for i, snake, direction in zip(range(self.nb_snakes), self.select_alive_snakes(), directions):
      next_coord=Move(snake.head, direction).next_coord()
      for other_snake in self.select_alive_snakes():
        if any((next_coord == x).all() for x in other_snake.body):
          rewards[i]=-1
          snake.alive=False
    return rewards

  def select_alive_snakes(self):
    return [snake for snake in self.snakes if snake.alive]

  def is_alive(self):
    return [snake.alive for snake in self.snakes]

  def is_done(self):
    nb_snakes=len(self.snakes)
    nb_alives=sum([snake.alive for snake in self.snakes])
    if (nb_snakes==1) and (nb_alives==0):
      return True
    if (nb_snakes>1) and (nb_alives==1):
      return True
    return False

  def harmonic(self, rewards):
    nb_snakes = len(rewards)
    new_rewards = np.zeros(nb_snakes)
    Bonus = sum([(reward==1) for reward in rewards])
    new_rewards+=np.where(np.array(rewards)==1,(nb_snakes-Bonus)/nb_snakes, -Bonus/nb_snakes)
    Malus = sum([(reward==-1) for reward in rewards])
    new_rewards+=np.where(np.array(rewards)==-1,(nb_snakes-Malus)/nb_snakes, -Malus/nb_snakes)
    return new_rewards
  
  # Getters
  def get_board(self):
    return self.grid.get_render(self.snakes)

  def get_target(self):
    return self.grid.get_target_render()
