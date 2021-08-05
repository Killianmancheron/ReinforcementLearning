from collections import deque
from numpy.random import sample

class Buffer():

    def __init__(self, maxlen=20000):
        self.maxlen = maxlen
        self.reset()

    def reset(self):
        self.memory = deque(maxlen=self.maxlen)

    def append(self, object):
        self.memory.append(object)

    def sample_batch(self, batch_size=32):
        #selectionner un batch de memoire
        num_batch = min(batch_size,len(self.memory))
        experiences = sample(self.memory, num_batch)