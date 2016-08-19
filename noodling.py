import matplotlib.pyplot as plt
import random
import numpy as np

seed = 234234

def get_skew(skew = 'linear'):
    if skew == 'linear':
        return random.gauss(0,0.25)
    return 0

def randcoord(x):
    random.seed(seed+x[0]*x[1]+x[1]+x[0])
    
    return (get_skew() + x[0],get_skew() + x[1])

length = 30



regular=[]

indices = np.ndindex((length-1,length-1))#zeros((length-1) **2)
for ind in indices:
    regular.append(ind)

linskew = [ randcoord(x) for x in regular]
#linskewy = [random.random() + x for x in regular]

#plt.scatter([x[0] for x in regular],[x[1] for x in regular],color='y')
plt.scatter([x[0] for x in linskew],[x[1] for x in linskew],color='k')

plt.show()


