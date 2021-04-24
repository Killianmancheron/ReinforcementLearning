from Environnment import Snake
from Environnment import Grid

class Controller():

  def __init__(self, grid_size=(15,15)):
    self.grid=Grid(grid_size)
    self.max_x=grid_size[0]-1
    self.max_y=grid_size[1]-1
    mid_grid=tuple([int(x/2) for x in grid_size])
    self.snakes=[Snake(init_coord=mid_grid)]
    self.grid.spawn_apple()
    self.grid.update_board(self.snakes)

  def get_board(self):
    return self.grid.render_board(self.snakes)

  def action(self, snake, direction):
    next_coord=snake.move(snake.head,direction)
    reward=0
    #gestion de l'action hors de la grille
    if (next_coord[0]<0 or next_coord[0]>self.max_x) or (next_coord[1]<0 or next_coord[1]>self.max_y):
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
        else:
          snake.action(direction)
    return self.get_board(), reward, self.isdone()

  def isdone(self):
    nb_snakes=len(self.snakes)
    nb_alives=sum([snake.alive for snake in self.snakes])
    if (nb_snakes==1) and (nb_alives==0):
      return True
    if (nb_snakes>1) and (nb_alives==1):
      return True
    return False