from collections import deque
from .reward import Modified_Reward
from keras.layers import concatenate

class HER():

    def __init__(self, off_policy, Strategy, Reward) -> None:
        self.off_policy=off_policy
        self.Strategy = Strategy
        if Reward is None :
            Reward = Modified_Reward()
        self.Reward = Reward

    def set_goal(self, goal):
        self.goal = goal

    def forward(self, observation):
        concatenate([observation, self.goal],axis=-1)
        action = self.off_policy.forward()
        return action

    def experience_replay(self, Episode_memory, Buffer):
        for t in range(len(Episode_memory)):
            state, action, _, observation, done = Episode_memory[t]
            reward = self.Reward.get_reward(state, action, self.goal)
            state_goal = concatenate([state, self.goal],axis=-1)
            observation_goal = concatenate([observation, self.goal],axis=-1)
            Buffer.append([state_goal, action, reward, observation_goal, done])
            Goal_replay = self.Strategy.get_goals(Episode_memory, t)
            for goal in Goal_replay:
                reward = self.Reward.get_reward(state, action, goal)
                state_goal = concatenate([state, goal],axis=-1)
                observation_goal = concatenate([observation, goal],axis=-1)
                Buffer.append([state_goal, action, reward, observation_goal, done])
        return Buffer

    def backward(self, Buffer):
        self.off_policy.backward(Buffer)
