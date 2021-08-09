import copy 
from math import sqrt, log

class UCT():


    def add_node_tree(self, environnment):
        nplayouts = [0.0 for x in range (4)]
        nwins = [0.0 for x in range (4)]
        self.Tree [environnment.h] = [0, nplayouts, nwins]

    def look(self, environnment):
        return self.Tree.get (environnment.h, None)

    def Update_Tree (self, environnment):
        """Algorithme récursif UCT permettant empiriquement d'évaluer un noeud/état du board 

        Args:
            board (Board): Etat du jeu à compléter

        """    
        if environnment.isdone ():
            return environnment.score ()
        t = self.look(environnment)

        if t != None:
            bestValue = -1000000.0
            best = 0
            moves = environnment.legalMoves ()
            for i in range (0, len (moves)):
                val = 1000000.0
                if t [1] [i] > 0:
                    Q = t [2] [i] / t [1] [i]
                    val = Q + 0.4 * sqrt (log (t [0]) / t [1] [i])
                if val > bestValue:
                    bestValue = val
                    best = i
            environnment.step (moves [best].direction)
            res = self.Update_Tree (environnment)
            t [0] += 1
            t [1] [best] += 1
            t [2] [best] += res
            return res
        else:
            self.add_node_tree (environnment)
            return environnment.playout()

    def BestMove (self, environnment, n):
        """Applique l'estimation UCT pour choisir le meilleur mouvement

        Args:
            board (Board): Etat du jeu dont on souhaite le meilleur mouvement
            n (int): Nombre de parties à jouer que l'on souhaite par noeud

        Returns:
            Move: meilleur mouvement selon l'algorithme.
        """    
        environnment.total_score=0
        self.Tree = {}
        for i in range (n):
            b1 = copy.deepcopy (environnment)
            res = self.Update_Tree (b1)
        t = self.look(environnment)
        
        moves = environnment.legalMoves ()
        best = moves [0]
        bestValue = t [1] [0]
        for i in range (1, len(moves)):
            if (t [1] [i] > bestValue):
                bestValue = t [1] [i]
                best = moves [i]
        return best.direction

