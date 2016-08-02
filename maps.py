
import util

class Map(object): #more or less just a container for all of the things that happen in space
    def __init__(self, ship=None):
        self.id = util.register(self)
        self.events = [] #list for unpopped events - do we even need this here?
        self.objects = [] #popped events.  Mostly just little stuff like resource finds
        
        self.ship = ship #convenience link to get location information

    def update(self,secs):
        pass        
