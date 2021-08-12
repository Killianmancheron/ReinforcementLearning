from collections import deque
from random import sample
from numpy.random import choice
import numpy as np

class Buffer():

    def __init__(self, maxlen=20000, priority=False, alpha=0.6):
        self.maxlen = maxlen
        self.reset()
        self.alpha = alpha
        self.priority= priority
        self.sample_indices=[]

    def reset(self):
        self.memory = deque(maxlen=self.maxlen)
        self.priority_index = deque(maxlen=self.maxlen)

    def append(self, object, priority=None):
        self.memory.append(object)
        if self.priority :
            assert priority is not None
            self.priority_index.append(priority)

    def update_priority_batch(self, priorities):
        assert len(priorities)==len(self.sample_indices), 'format de densité : {} pour {} exemples'.format(len(p),len(self.sample_indices))
        for i,priority in zip(self.sample_indices,priorities):
            self.priority_index[i] = priority

    def get_priority_batch(self):
        result = []
        for i in self.sample_indices:
            result.append(self.priority_index[i])
        return result

    def density_priority(self):
        sum_priority=0
        for p in self.priority_index:
            sum_priority+=pow(p,self.alpha)
        return [pow(p,self.alpha)/sum_priority for p in self.priority_index]

    def sample_batch(self, batch_size=32):
        #selectionner un batch de memoire
        num_batch = min(batch_size,len(self.memory))
        if not self.priority:
            return sample(self.memory, num_batch)
        else :
            samples=[]
            self.sample_indices = choice(range(len(self.memory)), num_batch, p=self.density_priority(), replace=False)
            for i in self.sample_indices:
                samples.append(self.memory[i])
            return samples