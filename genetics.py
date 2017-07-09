
from scipy import stats
import numpy as np
import math

def sample_pop(mean,std,size=10):
    samples = stats.norm.rvs(loc=mean,scale=std,size=size)
    samples[samples < 0] = 0
    samples[samples > 1] = 1
    return samples.mean(), samples.std()

def sampling_update(array,stdarray):
    tick = np.array( [sample_pop(array[a],stdarray[a]) for a in range(len(array))])
    array, stdarray = tick[:,0], tick[:,1]

    stdarray[stdarray< 0.005] = 0.05
        
    return array, stdarray

def population_genetics(planet=None):
    out = dict()
    out['culture'] = np.random.rand(20)
    out['culture std'] = np.random.rand(20)
    out['bio needs'] = np.random.rand(8) if planet is None else planet.attributes['resources']
    out['bio needs'] /= np.sum(out['bio needs'])
    out['bio needs std'] = np.multiply(np.random.rand(8),out['bio needs'])
    
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
    
    out_struct['area'] = test_planet.radius # not really AREA, but we can TODO that when we use it
    return out_struct    

if __name__ == "__main__":
    class stubPlanet(object): pass
    test_planet = stubPlanet()
    test_planet.type = 'Planetoid'
    test_planet.radius = 1000
    test_planet.attributes = planet_attributes(test_planet)
    
    print 'Planet resources', test_planet.attributes
    
    pop1 = population_genetics(test_planet)
    pop2 = population_genetics(test_planet)
    
    print pop1
    print pop2

    for c in range(len(pop1['culture'])):
        print stats.ttest_ind_from_stats(pop1['culture'][c],np.sqrt(pop1['culture std'][c]),10,pop2['culture'][c],np.sqrt(pop2['culture std'][c]),10)
    print stats.pearsonr(pop1['culture'],pop2['culture'])
    print
    for i in range(1000):
        print
        pop1['culture'],pop1['culture std'] = sampling_update(pop1['culture'],pop1['culture std'])
        print pop1['culture']
        print pop1['culture std']
