
from scipy import stats
import numpy as np
import math

def population_genetics(planet=None):
    out = dict()
    out['culture'] = np.random.rand(20)
    out['biological needs'] = np.random.rand(8) if planet is None else planet.attributes['resources']
    out['biological needs'] /= np.sum(out['biological needs'])
    
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
    
    print stats.pearsonr(pop1['culture'],pop2['culture'])
