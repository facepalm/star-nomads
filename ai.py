
import globalvars

class AI(object):
    def __init__(self,ship=None,role=None, owner=None):
        if not hasattr(self, 'role'): self.role = role
        self.ship = ship
        self.owner = owner #useful for remembering who we belong to, if anyone
        
        self.activity = None #specific, current activity
        self.goal = None #overarching plan. 



class StationAI(AI):
    '''Station AIs concentrate on building their own modules, and others.  They don't move around'''
    def __init__(self,**kwargs):
        AI.__init__(self,**kwargs)
        
        self.personality = kwargs['personality'] if personality in kwargs else 'Jack-of-all'
        
        
       
        
