import numpy as np

class EpsGreedy():

    def __init__(self,eps=.1):
        self.eps = eps

    def select_action(self, q_values):

        assert q_values.ndim == 1, 'q_values doit etre de dim 1'
        nb_actions = q_values.shape[0]
        if np.random.uniform()< self.eps :
            action = np.random.randint(0,nb_actions)
        else :
            action = np.random.choice(np.where(q_values==q_values.max())[0])
        return action

    def get_config(self):
        """Retourne la configuration de EpsGreedy
        # Returns
            Dictionnaire de la config
        """
        config = {}
        config['eps'] = self.eps
        return config
    
    def __name__(self):
        return "EpsGreedy with eps = {}".format(self.eps)
    