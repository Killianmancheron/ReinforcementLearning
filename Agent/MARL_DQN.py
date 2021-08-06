import random
import keras
import numpy as np
from keras.models import Model
from collections import deque
import time

def one_hot(action, k=4):
  return [int(action==i) for i in range(k)]

class MARL_DeepQN():

  def __init__(self, model, joueur, gamma =.99, batch_size = 32):
    #model:
    self.model = model

    #constantes:
    self.gamma = gamma
    self.batch_size = batch_size
    self.joueur=joueur
    
    #etat:
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
    # le model target n'est utile que pour la copie,
    # le choix de l'optimizer ou de la loss ne sert à rien
    self.target_model = keras.models.clone_model(self.model)
    self.update_target_model()
    self.target_model.compile(optimizer='sgd', loss='mse')
    self.model.compile(optimizer=optimizer, loss='mse')
    self.compiled = True

  def one_hot(action):
    return [int(action==i) for i in range(4)]

  def Q_values(self, state, action):
    state = np.array(state).reshape((-1,)+state.shape)
    action = np.array(one_hot(action)).reshape(-1,4)
    return np.array([max(self.model([state,action])[0].numpy() for action in range(4))])

  def eval(self, states):
    values = []
    for state in states:
      state =  np.array(state).reshape((-1,)+state.shape)
      Q_values = np.zeros((4,4))
      for action in range(4):
        action_vect = np.array(one_hot(action)).reshape(-1,4)
        Q_values[action,:] = self.target_model([ state,action_vect ])[0].numpy()
      index = np.unravel_index(np.argmax(Q_values, axis=None), Q_values.shape)
      values.append(np.min(Q_values[index[0],:]))
    return values

  def update(self, batch): 
    if not self.compiled :
      raise ValueError("Compiler l'algorithme avant la mise à jour des poids")

    num_batch = len(batch)

    states=[]
    actions = []
    observations=[]
    for state, action, reward, observation, done in batch:
      states.append(list(state))
      actions.append(list(one_hot(a) for a in action))
      observations.append(list(observation))
    states = np.array(states).reshape((num_batch,)+observation.shape)
    observations = np.array(observations).reshape((num_batch,)+observation.shape)
    actions = np.array([actions]).reshape(num_batch,2,4)

    opposant = 1 - self.joueur
    targets = np.array(self.model([states,actions[:,opposant,:]]))
    observation_targets = np.array(self.eval(observations))

    for i, experience in enumerate(batch):
      state, action, reward, observation, done = experience
      target = targets[i]
      if done[0] :
        target[action[0]] = reward[0]
      else :
        target[action[0]] = reward[0] + observation_targets[i] *self.gamma

    self.model.fit([states,actions[:,opposant,:]], targets, epochs=1, verbose=0)
