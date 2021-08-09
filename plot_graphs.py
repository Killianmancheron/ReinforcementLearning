import numpy as np
import matplotlib.pyplot as plt
from utils import open_rewards

means = []
mins=[]
maxs=[]
all_rewards=[]
for playout in [1,10,100]:#,1000,10000]:

    r = open_rewards(folder=r'.\Records\rewards\UCT', filename=r'\rewards (10, 10) {}'.format(playout))
    means.append(sum(r['rewards'])/len(r['rewards']))
    mins.append(sum(r['rewards'])/len(r['rewards'])-min(r['rewards']))
    maxs.append(max(r['rewards'])-sum(r['rewards'])/len(r['rewards']))
    all_rewards.append(r['rewards'])

    
print(means)
print(mins)
print(maxs)
y_error=[mins,maxs]
plt.boxplot(all_rewards)
# plt.errorbar([1,10,100,1000,10000],means,yerr=y_error,label = r['n_playout'], linestyle='--',
#              fmt='o')
#plt.xscale('log')
#plt.legend()
plt.xticks([1,2,3,4,5],[1,10,100,1000,10000])
plt.xlabel('Nombre de parties aléatoires par coup')
plt.ylabel('Score de fin de partie')
plt.title('Comparaison UCT en fonction de N sur une grille 5x5')
plt.show()