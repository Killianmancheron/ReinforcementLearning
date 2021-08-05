import numpy as np
import matplotlib.pyplot as plt
from Environnment import Controller, snake

def diff(a, b):
    if a!=b:
        return -1
    else:
        return 1

def R(i, q):
    s1 = sum([ (q[j]!=1) if (1==q[i]) else (q[j]==1) for j in range(len(q))  ])
    s2 = sum([ (q[j]!=-1) if (-1==q[i]) else (q[j]==-1) for j in range(len(q))  ])
    # print(s1)
    # print(s2)
    return diff(1,q[i])*s1-diff(-1,q[i])*s2

def Q(i, q):
    if q[i]==1:
        tmp1 = q.copy()
        tmp1[i] = 0
        tmp2 = q.copy()
        tmp2[i]=-1
        return (tmp1, tmp2)
    elif q[i]==0:
        tmp1 = q.copy()
        tmp1[i] = 1
        tmp2 = q.copy()
        tmp2[i]=-1
        return (tmp1, tmp2)
    else :
        tmp1 = q.copy()
        tmp1[i] = 0
        tmp2 = q.copy()
        tmp2[i]=1
        return (tmp1, tmp2)




q = [-1,-1,-1]
for i in range(len(q)):
    somme = 0
    s=[R(i,q)]
    for lst in Q(i, q):
        s.append(-R(i,lst))
    print(s)
    somme = sum(s)
    print(somme)

# Game = Controller((15,15), nb_snakes=3)
# print(Game.grid.board)
# print(Game.grid.apples)
# plt.imshow(Game.get_board())
# plt.show()
# plt.imshow(Game.get_target())
# plt.show()
# # render, rewards, is_alive = Game.execute([0])
# # print(rewards)
# # print(is_alive)
# # print(Game.grid.board)

