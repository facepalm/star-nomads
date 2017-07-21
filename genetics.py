
#from scipy import stats
import numpy as np
import random
import math

def sample_pop(mean,std,size=10):
    samples = np.random.normal(loc=mean,scale=std,size=size)
    samples[samples < 0] = 0
    samples[samples > 1] = 1
    return samples.mean(), samples.std()

def sampling_update(array,stdarray):
    tick = np.array( [sample_pop(array[a],stdarray[a]) for a in range(len(array))])
    array, stdarray = tick[:,0], tick[:,1]

    stdarray[stdarray< 0.005] = 0.05
        
    return array, stdarray


def random_population(planet=None,init_pop=False):
    out = dict()
    out['population'] = 10000 * random.random() if init_pop else 0
    out['culture'] = np.random.rand(20)
    out['culture std'] = np.random.rand(20)
    out['bio needs'] = np.random.rand(8) if planet is None else planet.attributes['resources']
    out['bio needs'] /= np.sum(out['bio needs'])
    out['bio needs std'] = np.random.rand(8)
    out['energy needs'] = np.random.rand() #fraction of needs that can be satisfied with pure energy
    
    return out
    

def planet_attributes(planet):
    p = planet
    out_struct = dict()
    out_struct['resources'] = 10*np.random.rand(8) # 4 terrestrial, 4 atmosphere
    if p.type == 'Gas Giant':
        # all atmosphere, no terrain
        
        out_struct['resources'][4:] = np.power(10*np.random.rand(4),2)
        out_struct['resources'][:4] = np.power(10*np.random.rand(4),.5)
    elif p.type in ['Planetoid','Dwarf Planet']:
        # atmosphere limited or nonexistent
        out_struct['resources'][:4] = np.power(10*np.random.rand(4),2)
        out_struct['resources'][4:] = np.power(10*np.random.rand(4),.5)
           
    out_struct['resources'] /= np.sum(out_struct['resources']) # so one "resource draw" will pull this ratio
    
    return out_struct    


def compare_traits(trt1,trt2,std1,std2,pop1=10,pop2=10,method='harmonic'):
    outt = np.empty(len(trt1),np.float32)
    for c in range(len(trt1)):
        s1,s2 = std1[c]**2, std2[c]**2
        t = abs((trt1[c] - trt2[c]) / np.sqrt(pow(s1,2)/pop1 + pow(s2,2)/pop2 )) # welch's t-test
        #df = (pow(s1,2)/pop1 + pow(s2,2)/pop2)**2 / (pow(s1,4)/((pop1-1)*pop1**2) + pow(s2,4)/((pop2-1)*pop2**2))
        outt[c] =  max(np.exp(-0.5*t**2),0.001)
        print t,outt[c]
    if method == 'multiply':
        out = reduce((lambda x, y: x * y), outt)
    elif method == 'geometric':
        out = pow( reduce( (lambda x,y: x * y ), outt), 1./len(outt) )
    elif method == 'harmonic':
        out = pow( 1.*reduce( (lambda x,y: pow( x, -1) + pow( y, -1) ), outt)/len(outt), -1 )
    else:
        out = 1.0
    return out


class Population():
    def __init__(self,planet=None):
        self.planet=planet
        self.factions=[]           
        
    def total_pop(self):
        return np.sum([ f['population'] for f in self.factions ] ) 
        
    def spawn_on(self,planet=None):    
        # seeds a small (random) population on a planet
        if planet is None: planet = self.planet
        if self.planet is None: self.planet = planet
        if self.factions == []:        
            self.factions.append(random_population(planet=planet))
        
    def evolve_on(self,planet=None):
        # seeds a small (random) population on a planet and tweaks values until death or adaptation
        # technology is not factored in -> evolution, remember?
        if self.planet is None: self.planet = planet
        if planet is None: planet = self.planet
        if self.factions == []:        
            self.factions.append(random_population())
        for f in self.factions:
            comp = compare_traits(f['bio needs'],planet.attributes['resources'],f['bio needs std'],0.25*np.random.rand(8),10,10)
            if random.random() < comp:
                #population survived!
                f['bio needs'] = planet.attributes['resources']                                
                
                #calculate density
                parea = planet.surface_area() / 1000000 #km^2                                
                pop_density = 1. # souls per km^2
                
                f['population'] = parea * pop_density
            
        


if __name__ == "__main__":
    class stubPlanet(object): pass
    test_planet = stubPlanet()
    test_planet.type = 'Planetoid'
    test_planet.radius = 1000
    test_planet.attributes = planet_attributes(test_planet)
    
    print 'Planet resources', test_planet.attributes
    
    pop1 = random_population(test_planet)
    pop2 = random_population()
    
    print pop1
    print pop2

    '''for c in range(len(pop1['culture'])):
        print stats.ttest_ind_from_stats(pop1['culture'][c],np.sqrt(pop1['culture std'][c]),10,pop2['culture'][c],np.sqrt(pop2['culture std'][c]),10)'''
    print compare_traits(pop2['bio needs'],test_planet.attributes['resources'],pop2['bio needs std'],0.25*np.random.rand(8),10,10)
    print np.corrcoef(pop2['bio needs'],test_planet.attributes['resources'])
    print
    for i in range(1):
        print
        pop1['culture'],pop1['culture std'] = sampling_update(pop1['culture'],pop1['culture std'])
        print pop1['culture']
        print pop1['culture std']
