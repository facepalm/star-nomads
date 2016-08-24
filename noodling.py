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

length = 300
'''
regular=[]

indices = np.ndindex((length-1,length-1))#zeros((length-1) **2)
for ind in indices:
    regular.append(ind)

linskew = [ randcoord(x) for x in regular]
#linskewy = [random.random() + x for x in regular]

#plt.scatter([x[0] for x in regular],[x[1] for x in regular],color='y')
plt.scatter([x[0] for x in linskew],[x[1] for x in linskew],color='k')

plt.show()'''

def planet_type(mass):
    if mass > 1E29: 
       return 'INVALID' #actually a sun.  Throw an error, this shouldnt happen
    elif mass > 1E28: 
       return 'Brown dwarf' #counting this as a planet, since they have negligible radiation    
    elif mass > 1E26:
       return 'Gas giant'         
    elif mass > 1E23:
       return 'Planet' #rocky world, but capable of retaining an atmosphere, even if barely
    elif mass > 1E21:
       return 'Dwarf planet' #larger moons and asteroids, rounded
    return 'Planetoid' #small moons, asteroids, rocks, etc



masses = 1E24*10**(np.random.random( size=length)*8 - 3)
names = [planet_type(x) for x in masses]
print names
#masses.append(mass)
    
plt.hist(masses,bins=100)
plt.show()    

print '%02.02e' % 0


