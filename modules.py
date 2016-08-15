
import util

class Module(object):
    def __init__(self,**kwargs):
        util.register(self)
        #super(Module, self).__init__(**kwargs)
        
        self.size = 1
        self.power = 0
        self.crew = 0
        
        self.active = False
        
        self.storage = {}
        self.recipe = {}
        
class Storage(Module):
    def __init__(self,**kwargs):
        Module.__init__(self,**kwargs)
        
    
        
