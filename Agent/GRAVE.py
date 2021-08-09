import copy 
from math import sqrt, log
import random

class AMAF():
    def __init__(self):
        self.Side=5
        self.MaxCodeLegalMoves = 25*4
        self.MaxLegalMoves=4
        self.Tree = {}

    def playoutAMAF (self, environnment, played):
        """Applqiue l'algorithme AMAF sur le jeu 

        Args:
            board (Board): Etat du jeu
            played (list<int>): Liste encodée des mouvements déjà joués.

        Returns:
            float: Score de la partie jouée
        """    
        score=1
        while (True):
            moves = []
            moves = environnment.legalMoves ()
            if len (moves) == 0 or environnment.isdone ():
                print(score)
                return score
            n = random.randint (0, len (moves) - 1)
            played.append (moves [n].code ())
            score += environnment.step (moves [n].direction)[1]

    
    
    def addAMAF (self, environnment):
        """Ajoute les informations de AMAF pour un noeud

        Args:
            board (Board): Noeud/Etat du jeu à créer
        """    
        nplayouts = [0.0 for x in range (self.MaxLegalMoves)]
        nwins = [0.0 for x in range (self.MaxLegalMoves)]
        nplayoutsAMAF = [0.0 for x in range (self.MaxCodeLegalMoves)]
        nwinsAMAF = [0.0 for x in range (self.MaxCodeLegalMoves)]
        self.Tree [environnment.h] = [0, nplayouts, nwins, nplayoutsAMAF, nwinsAMAF]

    def updateAMAF (self, t, played, res):
        """Met à jour la table/l'arbre des noeuds sur les différents coups joués

        Args:
            t (np.array): Table / Arbre des noeuds
            played (list<int>): Liste de noeuds joués
            res (float): Résultats d'une partie.
        """    
        for i in range (len (played)):
            code = played [i]
            seen = False
            for j in range (i):
                if played [j] == code:
                    seen = True
            if not seen:
                t [3] [code] += 1
                t [4] [code] += res

    def look(self, environnment):
        return self.Tree.get (environnment.h, None)


class GRAVE():
    
    def __init__(self):
        self.AMAF = AMAF()

    def GRAVE (self, environnment, played, tref):
        """Permet de récursivement mettre à jour l'arbre des noeuds selon l'algorithme GRAVE

        Args:
            board (Board): Etat du jeu à compléter
            played (list): Liste des coups joués
            tref (np.array): Tableau/arbre des noeuds de reférence

        Returns:
            [type]: [description]
        """    
        if (environnment.isdone()):
            return environnment.score ()

        t = self.AMAF.look (environnment)
        
        if t != None:
            tr = tref
            if t [0] > 50:
                tr = t
            bestValue = -1000000.0
            best = 0
            moves = environnment.legalMoves ()
            bestcode = moves [0].code ()
            for i in range (0, len (moves)):
                val = 1000000.0
                code = moves [i].code ()
                if tr [3] [code] > 0:
                    beta = tr [3] [code] / (t [1] [i] + tr [3] [code] + 1e-3 * t [1] [i] * tr [3] [code])
                    Q_c = 1
                    if t [1] [i] > 0:
                        Q_c = t [2] [i] / t [1] [i]
                    AMAF_c = tr [4] [code] / tr [3] [code]
                    val = (1.0 - beta) * Q_c + beta * AMAF_c
 
                if val > bestValue:
                    bestValue = val
                    best = i
                    bestcode = code
            environnment.step (moves [best].direction)
            played.append (bestcode)
            res = self.GRAVE (environnment, played, tr)
            t [0] += 1
            t [1] [best] += 1
            t [2] [best] += res
            self.AMAF.updateAMAF (t, played, res)
            return res
        else:
            self.AMAF.addAMAF (environnment)
            return self.AMAF.playoutAMAF (environnment, played)

    def BestMove (self, environnment, n):
        """Permet d'obtenier le meilleur mouvement grâce à GRAVE

        Args:
            board (Board): Etat du jeu dont l'on souhaite le meilleur mouvement
            n (int): Nombre d'itérations pour estimer le score de chaqu noeud

        Returns:
            Move: Meilleur mouvement selon l'algorithme.
        """
        self.AMAF = AMAF()    
        self.AMAF.addAMAF (environnment)
        for i in range (n):
            t = self.AMAF.look (environnment)
            b1 = copy.deepcopy (environnment)
            res = self.GRAVE (b1, [], t)
        t = self.AMAF.look (environnment)
        print(t)
        moves = environnment.legalMoves ()
        best = moves [0]
        bestValue = t [1] [0]
        for i in range (1, len(moves)):
            if (t [1] [i] > bestValue):
                bestValue = t [1] [i]
                best = moves [i]
        return best.direction