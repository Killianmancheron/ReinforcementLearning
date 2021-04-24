

class SnakeGame():

  def __init__(self, grid_size=(15,15),):
    self.grid_size = grid_size
    # Define action and observation space
    self.viewer=None

  def step(self, action):
    self.board, reward, done=self.controller.action(self.snake,action)
    return self.board, reward, done

  def reset(self):
    self.controller=Controller(self.grid_size)
    self.snake=self.controller.snakes[0]
    self.board=self.controller.get_board()
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
