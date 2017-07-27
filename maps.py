import random
import numpy as np
import uuid
import math

import util
import mapscreen
import event
import asteroid
import star
import gps
import globalvars

import time

EVENT_TC = 720.

M_TO_LY = 1000.

def tweak_coords(coords,dist=5):
    state = random.getstate()
    seed = coords[0]+1024*coords[1]
    random.seed(seed)

    randomness = 0.25
    off_r = random.gauss(0,dist/randomness)
    off_t = random.random()*2*3.14159
    new_coords = [int(coords[0] + off_r*math.cos(off_t)), int(coords[1] + off_r*math.sin(off_t))]

    random.setstate(state)
    return new_coords

class Map(object): #more or less just a container for all of the things that happen in space
    def __init__(self, ship=None, previous = None, coords = None, universe=None):
        util.register(self)
        self.registry={}

        self.universe = universe if universe else globalvars.universe
        self.coords_known = False

        self.map_coordinates = coords if coords else [500,500]
        self.galactic_coordinates = tweak_coords(self.map_coordinates)
        self.mapseed = self.galactic_coordinates[0] + 1024*self.galactic_coordinates[1]
        random.seed(self.mapseed)

        self.scale = 2

        #generate coordinate offset
        #off_r = random.random()*2 + 3
        #off_t = random.random()*2*3.14159
        #coords = previous.connections[self.mapseed]['Coords'] if previous else [500,500]

        #self.galactic_coordinates = [coords[0]+off_r*math.cos(off_t), coords[1]+off_r*math.sin(off_t)]

        #generate list of connected maps
        #self.connections = []
        #if previous:
        #    self.connections.append( {'Map':previous,'Coords':previous.galactic_coordinates} )

        self.connections = []
        pi = math.pi
        for i in range(6):
            off_r = 5
            off_t = i*pi/3.
            coords = [int(round(self.map_coordinates[0] + off_r*math.cos(off_t))), int(round(self.map_coordinates[1] + off_r*math.sin(off_t)))]
            if [coords, self.map_coordinates] in self.universe.map_edges:
                self.connections.append( [coords, self.map_coordinates] )
            else:
                if random.random() < 0.33:
                    #generate coordinate offset
                    self.universe.map_edges.append( [self.map_coordinates, coords] )
                    self.connections.append( [self.map_coordinates, coords] )
        print self.universe.map_edges


        self.events = [] #list for unpopped events - do we even need this here?
        self.objects = [] #popped events.  Mostly just little stuff like resource finds

        self.stars = {}

        self.ship = ship  #convenience link to get location information

        stars = self.universe.galaxy_stars[ self.galactic_coordinates[0], self.galactic_coordinates[1]]
        self.density = int(250 / (stars/255.)**1.05) #avg distance between stars (in meters), where 1 km == 1 ly
        self.dust = self.universe.galaxy_dust[ self.galactic_coordinates[0], self.galactic_coordinates[1]]
        print 'Star distance',self.density
        #quit()

        globalvars.map = self

        self.event_mgr = event.EventManager()

        self.display = mapscreen.MapScreen(map=self)
        #self.display.add_widget(self.ship.image)

        self.update_starmap()

    def __getstate__(self):
        odict = self.__dict__.copy() # copy the dict since we change it
        del odict['display']              # remove gui entry
        #if 'screen' in odict: del odict['screen']
        return odict

    def __setstate__(self,state):
        self.__dict__.update(state)   # update attributes
        self.display = mapscreen.MapScreen(map=self)
        for obj in self.registry:
            if hasattr(self.registry[obj], 'image'):
                print self.registry[obj]
                self.display.ids['mapscale'].add_widget(self.registry[obj].image)

    def register(self, obj, oid=''):
        new_id = oid if oid else str(uuid.uuid4())
        try:
            self.registry[new_id] = obj
            obj.id = new_id
        except:
            assert False, "global id collision!"
        return new_id

    def unregister(self, obj):
        if obj.id in self.registry:
            self.registry.pop(obj.id)

    def update(self,secs):
        timer = time.time()
        loc = None
        loc = gps.get_location()
        if gps.accuracy <= 25: self.display.location = loc
        self.display.update_location()
        self.display.update(secs)

        print 'display updated',time.time() - timer
        timer = time.time()

        self.update_starmap()
            #print self.systemcoord(loc)

        print 'starmap updated',time.time() - timer
        timer = time.time()

        #one event every hour or so?
        num = util.sround( random.random()*secs/EVENT_TC )
        for i in range(num):
            #new event at current location... ish
            new_event = self.event_mgr.new(loc)
            if new_event:
                #ping location
                self.display.ids['mapscale'].add_widget(new_event.image)
                #self.display.spawn_ping(location=new_event.location,extent=100.,color=new_event.color)

        if random.random() < 0.1:
            self.display.event_ping(extent=self.ship.sensor_strength(active=True))

        events = self.event_mgr.fetch_all(loc,self.ship.sensor_strength())
        for e in events:
            if not e.discovered: e.discover(curmap=self)

        print 'events updated',time.time() - timer
        timer = time.time()

        for obj in self.registry.values():
            if hasattr(obj,'update'):
                obj.update(secs)

        print 'objs updated',time.time() - timer
        timer = time.time()

    def update_starmap(self,loc=None,dist=3):
        if loc is None: loc = self.display.location
        #print loc, self.systemcoord(loc)
        loc = self.systemcoord(loc)

        for x in np.linspace(loc[0]-dist*self.density,loc[0]+dist*self.density,num=dist*2+1):
            for y in np.linspace(loc[1]-dist*self.density,loc[1]+dist*self.density,num=dist*2+1):
                newloc = (int(round(x)),int(round(y)))
                #print newloc
                if newloc not in self.stars:
                    print 'Adding new star at',newloc
                    self.stars[newloc] = star.initialize_star(newloc,self.density,int(abs(self.mapseed+y*x+x+y)),self.display.ids['mapscale'],self)
                    if self.stars[newloc]:
                        print self.stars[newloc].info()
                        #self.display.ids['mapscale'].add_widget(self.stars[newloc].primary_image())


    def which_system(self,loc=None):
        if loc is None: loc = self.display.location
        loc = self.systemcoord(loc)
        newloc = (int(round(loc[0])),int(round(loc[1])))
        closest = None
        best_dist = 0
        for x in np.linspace(loc[0]-self.density,loc[0]+self.density,num=3):
            for y in np.linspace(loc[1]-self.density,loc[1]+self.density,num=3):
                newloc = (int(round(x)),int(round(y)))
                if newloc not in self.stars:
                    self.update_starmap(loc=newloc,dist=1)
                if closest is None or (self.stars[newloc] and util.vec_dist(self.stars[newloc].location, np.array(self.display.location)) < best_dist):
                    closest = self.stars[newloc]
                    best_dist = util.vec_dist(self.stars[newloc].location, np.array(self.display.location)) if closest else 0
        #print closest.info(), best_dist / globalvars.M_TO_AU, closest.snow_line
        return closest

    def fetch_objects(self,loc,rad=10,exclude_player = True):
        firstlist = list(filter((lambda x: hasattr(x,'location') and util.simple_2vec_dist(x.location,loc) <= rad ), self.registry.values()))
        if exclude_player:
            return list(filter((lambda x: not hasattr(x,'player_ship') or not x.player_ship ), firstlist))
        else:
            return firstlist


    def new_player_ship(self,ship):
        #TODO remove old ship if present?

        self.ship = ship

        #hand to mapscreen
        self.display.ids['mapscale'].add_widget(self.ship.image)

    def spawn(self,item,loc,system=None):
        if system is None: system = self.which_system(loc)
        if item=='asteroid':
            print 'Spawning asteroid! '
            ast = asteroid.Asteroid(location=np.array(loc),star = system)
            self.objects.append(ast)
            self.display.ids['mapscale'].add_widget(ast.get_image())
        elif item is not None and not isinstance(item, basestring):
            #we're given something to spawn
            item.location = np.array(loc)
            if item not in self.objects: self.objects.append(item)
            self.display.ids['mapscale'].add_widget(item.get_image())

    def systemcoord(self,loc):
        nloc = self.density * (np.array(loc) // self.density)
        return nloc.round().tolist()
