import random
import keras
import numpy as np
from keras.models import Model
from collections import deque
from Policies import EpsGreedy
import time


class AbstractDeepQN():

  def __init__(self, nb_actions, gamma =.99, batch_size = 32):
    #constantes:
    self.nb_actions = nb_actions
    self.gamma = gamma
    self.batch_size = batch_size
    
    #objets:
    self.memory = deque(maxlen=20000)

    #etat:
    self.compiled = False

  def random_batch_choice(self, memory):
    index = np.random.choice(range(len(self.memory)),min(self.batch_size,len(self.memory)),replace=False)
    batch = [memory[i] for i in index]
    return batch

  def get_config(self):
    return {
        'nb_actions': self.nb_actions,
        'gamma': self.gamma,
        'batch_size': self.batch_size,
        'memory length': len(self.memory)
    }

class DeepQN(AbstractDeepQN):

  def __init__(self, model, policy = None, *args, **kwargs):
    #on hérite des paramètres de la classe abstraite
    super(DeepQN, self).__init__(*args, **kwargs)

    if model.output.shape.as_list() != [None, self.nb_actions]:
      raise ValueError("Le model doit avoir un output avec autant d'actions possibles")

    if policy is None :
      policy = EpsGreedy()
    
    self.policy = policy
    self.model = model
    
    #etat :
    self.reset_states()

  def reset_states(self):
    self.compiled = False
    self.last_action = None
    self.state = None

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

  def forward(self, observation):

    observation = np.array(observation).reshape((-1,observation.shape[0],observation.shape[1],observation.shape[2]))
    q_values = np.array(self.model([observation])[0])
    action = self.policy.select_action(q_values = q_values) 
    #enregistrement de l'etat d'entree et de l'action choisi
    self.last_action = action
    self.state = observation[0]
    return action
  
  def backward(self, reward, done, observation):
    if not self.compiled :
      raise ValueError("Compiler l'algorithme avant le backward")

    #enregistrer l'etat et le resultat courant dans la memoire
    self.memory.append([self.state, self.last_action, reward, observation, done])
    
    #selectionner un batch de memoire
    num_batch = min(self.batch_size,len(self.memory))
    experiences = random.sample(self.memory,num_batch)
        
    #copier les poids du model
    #self.update_target_model()
    #
    states=[]
    observations=[]
    for state, action, reward, observation, done in experiences:
      states.append(list(state))
      observations.append(list(observation))
    states = np.array(states).reshape(num_batch,observation.shape[0],observation.shape[1],observation.shape[2])
    observations = np.array(observations).reshape(num_batch,observation.shape[0],observation.shape[1],observation.shape[2])

    targets = np.array(self.model(states))
    observation_targets = np.array(self.target_model(observations))

 
    for i, experience in enumerate(experiences):
      state, action, reward, observation, done = experience
      target = targets[i]
      if done :
        target[action] = reward
      else :
        target[action] = reward + max(observation_targets[i]) * self.gamma

    self.model.fit(states, targets, epochs=1, verbose=0)
