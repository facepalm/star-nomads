
from scipy import stats
import numpy as np

def population_genetics(planet=None):
    out = dict()
    out['culture'] = np.random.rand(20)
    out['biological needs'] = np.random.rand(8) #TODO fill in resource stuff # if planet is None else np.concatenate(planet.)
    out['biological needs'] /= np.sum(out['biological needs'])
    

def planet_attributes(planet):
    p = planet
    out_struct = dict()
    if p.type == 'Gas Giant':
        #all atmosphere, no terrain
        out_struct['atmosphere'] = np.sqrt(np.random.rand(4))
        out_struct['terrain'] = np.power(np.random.rand(4),2)
    elif p.type in ['Planetoid','Dwarf Planet']:
        #atmosphere limited or nonexistent
        out_struct['atmosphere'] = np.power(np.random.rand(4),2)
        out_struct['terrain'] = np.sqrt(np.random.rand(4))
    else:
        #"normal" planet
        out_struct['atmosphere'] = np.random.rand(4)
        out_struct['terrain'] = np.random.rand(4)
        
    resources_sum = np.sum(out_struct['atmosphere']) + np.sum(out_struct['terrain'])
    out_struct['atmosphere'] /= resources_sum
    out_struct['terrain'] /= resources_sum
    
    out_struct['area'] = test_planet.img_radius
    return out_struct    

if __name__ == "__main__":
    class stubPlanet(object): pass
    test_planet = stubPlanet()
    test_planet.type = 'Planetoid'
    test_planet.img_radius = 0.5
    
    print planet_attributes(test_planet)
