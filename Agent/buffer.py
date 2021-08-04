from collections import deque
from numpy.random import choice

class Buffer():

    def __init__(self, maxlen=20000):
        self.maxlen = maxlen
        self.reset()

    def reset(self):
        self.memory = deque(maxlen=self.maxlen)

    def append(self, object):
        self.memory.append(object)