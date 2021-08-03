from collections import deque

class HER():

    def __init__(self, env, off_policy, Strategy, Reward, Buffer=[]) -> None:
        self.off_policy=off_policy
        self.Strategy = Strategy
        self.Reward = Reward

        self.Buffer = Buffer

    
        