import random
import keras
import numpy as np
from keras.models import Model
from collections import deque
import time


class AbstractDeepQN():

  def __init__(self, gamma =.99, batch_size = 32):
    #constantes:
    self.gamma = gamma
    self.batch_size = batch_size
    
    #etat:
    self.compiled = False

  def get_config(self):
    return {
        'gamma': self.gamma,
        'batch_size': self.batch_size
    }

class DeepQN(AbstractDeepQN):

  def __init__(self, model, *args, **kwargs):
    #on hérite des paramètres de la classe abstraite
    super(DeepQN, self).__init__(*args, **kwargs)


    self.model = model
    #etat :
    self.compiled = False

  def update_target_model(self):
    '''Copier les poids de Q dans Q_target
    '''
    self.target_model.set_weights(self.model.get_weights())

  def load_weights(self, filepath = None):
    '''charge les poids depuis un fichier et met à jour la poids de Q_target
    '''
    self.model.load_weights(filepath)
    self.update_target_model()

  def save_weights(self, filepath, overwrite=False):
    '''Sauvegarde les poids du model dans un fichier
    '''
    self.model.save_weights(filepath, overwrite=overwrite)  

  def compile(self, optimizer = 'sgd', metrics=[]):
    metrics += ['mse']  # register default metrics
    self.target_model = keras.models.clone_model(self.model)
    self.update_target_model()
    self.target_model.compile(optimizer='sgd', loss='mse')
    self.model.compile(optimizer=optimizer, loss='mse')
    self.compiled = True

  def Q_values(self, state):
    state = np.array(state).reshape((-1,state.shape[0],state.shape[1],state.shape[2]))
    return np.array(self.model([state])[0])

  def update(self, batch): # reward, done, observation
    if not self.compiled :
      raise ValueError("Compiler l'algorithme avant la mise à jour des poids")

    num_batch = len(batch)
    states=[]
    observations=[]
    for state, action, reward, observation, done in batch:
      states.append(list(state))
      observations.append(list(observation))
    states = np.array(states).reshape(num_batch,observation.shape[0],observation.shape[1],observation.shape[2])
    observations = np.array(observations).reshape(num_batch,observation.shape[0],observation.shape[1],observation.shape[2])

    targets = np.array(self.model(states))
    observation_targets = np.array(self.target_model(observations))
 
    for i, experience in enumerate(batch):
      state, action, reward, observation, done = experience
      target = targets[i]
      if done :
        target[action] = reward
      else :
        target[action] = reward + max(observation_targets[i]) * self.gamma

    self.model.fit(states, targets, epochs=1, verbose=0)
