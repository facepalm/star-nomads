
from scipy import stats
import numpy as np
import math

def population_genetics(planet=None):
    out = dict()
    out['culture'] = np.random.rand(20)
    out['biological needs'] = np.random.rand(8) # TODO should match homeworld
    out['biological needs'] /= np.sum(out['biological needs'])
    

def planet_attributes(planet):
    p = planet
    out_struct = dict()
    out_struct['resources'] = 10*np.random.rand(8) # 4 terrestrial, 4 atmosphere
    if p.type == 'Gas Giant':
        # all atmosphere, no terrain
        
        out_struct['resources'][4:] = np.power(10*np.random.rand(4),3)
        out_struct['resources'][:4] = np.power(10*np.random.rand(4),.3)
    elif p.type in ['Planetoid','Dwarf Planet']:
        # atmosphere limited or nonexistent
        out_struct['resources'][:4] = np.power(10*np.random.rand(4),3)
        out_struct['resources'][4:] = np.power(10*np.random.rand(4),.3)
           
    out_struct['resources'] /= np.sum(out_struct['resources']) # so one "resource draw" will pull this ratio
    
    out_struct['area'] = test_planet.radius # not really AREA, but we can TODO that when we use it
    return out_struct    

if __name__ == "__main__":
    class stubPlanet(object): pass
    test_planet = stubPlanet()
    test_planet.type = 'Planetoid'
    test_planet.radius = 1000
    
    print planet_attributes(test_planet)
