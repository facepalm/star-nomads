import json

ids=dict()

config = {
    'TIME FACTOR' : 3600,
    'ZOOM' : 15,
    'GRAPHICS' : 'pyglet',
    'AUTOLOAD': True,
}

def save_config():
    outfile = file('config.txt','w')
    json.dump( config, outfile, indent = 4, separators = (',', ': ') )
    outfile.close()
   
def load_config():
    try:
        outfile = file('config.txt','r')
    except:
        save_config()
        outfile = file('config.txt','r')
    global config
    config = json.load( outfile )
    outfile.close()
    
save_config()    
load_config()

scenario = None
universe = None
root = None
mousedown=False
