import numpy as np



class Community(object):
    def __init__(self,dna=None,population= 0 ):
        if dna is None: 
            dna = np.random.rand(20)
        self.dna = dna #a set of variables representing various personality factors of the community        
        self.spawn_pop(population)
        
    def spawn_pop(self, new_pop = 0, dna=None ):
        if dna: self.dna = dna
        self.children = new_pop/3
        self.civilians = new_pop/4
        self.crew = new_pop/4
        self.pensioners = new_pop/6
                
    def population(self):
        return self.children+self.crew+self.civilians+self.pensioners
        
    def trained_crew(self):
        return self.crew                        
        
            
        
        
        
