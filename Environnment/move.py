import numpy as np

class Move():

    UP=0
    LEFT=1
    RIGHT=2
    DOWN=3

    def __init__(self, coord, direction):
        """Classe correspondant au mouvement effectué.

        Args:
            coord (np.array): Coordonnées initiales, avant le déplacement.
            direction (int): Direction souhaitée.
        """        
        self.coord = coord
        self.direction=direction
        
    def next_coord(self):    
        '''
        Retourne une nouvelle coordonnée à partir d'une direction et d'une position
        '''
        coord = self.coord
        direction = self.direction

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

    def code(self):
        return 4*(5*self.coord[0]+self.coord[1])+self.direction