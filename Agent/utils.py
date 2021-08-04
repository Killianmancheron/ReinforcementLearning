import numpy as np
from Environnment.move import Move
from random import choices 


class Abstract_Goal_Gestion():

    def __init__(self) -> None:
        self.BACKGROUND_COLOR = [0., 0., 0.]
        self.GOAL_COLOR = [0., 0., 1.]
        self.HEAD_COLOR = [1., 0., 0.]

    def state_to_goal(self, state): # equivalent to function m
        # On suppose que les états sont des images et que la pomme soit l'ensemble de couleur strictement bleu
        goal = []
        for x in state:
            row=[]
            for y in x:
                if np.array_equal(y, self.GOAL_COLOR):
                    row.append(self.GOAL_COLOR)
                else : 
                    row.append(self.BACKGROUND_COLOR)
            goal.append(row)
        return np.array(goal).reshape(state.shape)


class Modified_Reward(Abstract_Goal_Gestion):

    def __init__(self, down_size=15, unit_size=10, unit_gap=1):
        Abstract_Goal_Gestion.__init__(self)
        self.down_size = down_size
        self.unit_size = int(unit_size)
        self.unit_gap = unit_gap 

    def downsize_image(self, image):
        filter_pixel = np.arange(1,self.down_size*self.unit_size+self.unit_gap,self.unit_size)
        return image[filter_pixel,:][:,filter_pixel]

    def get_head_loc(self, state):
        for i,x in enumerate(state):
            for j,y in enumerate(x):
                if np.array_equal(y,self.HEAD_COLOR):
                    return np.array((i,j))
        raise ValueError('Pas de tête de serpent trouvées')

    def get_goal_loc(self, goal):
        for i,x in enumerate(goal):
            for j,y in enumerate(x):
                if np.array_equal(y,self.GOAL_COLOR):
                    return np.array((i,j))
        raise ValueError("Pas d'objectif trouvées")

    def get_reward(self, state, action, goal):
        head_coord = self.get_head_loc(self.downsize_image(state))
        goal_coord = self.get_goal_loc(self.downsize_image(goal))
        next_coord = Move(head_coord, action).next_coord()
        return np.array_equal(goal_coord, next_coord)
        
        
class Strategy(Abstract_Goal_Gestion):

    def __init__(self, strategy="future",  nb_goals = 4) -> None:
        Abstract_Goal_Gestion.__init__(self)
        self.strategy = strategy
        self.nb_goals = nb_goals

    def get_goals(self, Episode_memory, t):
        goals = []
        if self.strategy == 'future' :
            if len(Episode_memory)>t+1:
                state = choices(Episode_memory[t+1:], k=self.nb_goals)[0] #[0] for select only state
                goals.append(self.state_to_goal(state))
        elif self.strategy == 'episode' :
            state = choices(Episode_memory[t+1:], k=self.nb_goals)[0] #[0] for select only state
            goals.append(self.state_to_goal(state))