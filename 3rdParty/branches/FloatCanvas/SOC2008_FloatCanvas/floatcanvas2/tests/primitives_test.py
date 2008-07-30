import sys
import os.path
sys.path.append( os.path.abspath( '..' ) )
sys.path.append( os.path.abspath( '../misc' ) )

import wx
import floatcanvas as fc
from loadWorldData import points as mapPoints


def start():
    #  setup very basic window
    app = wx.App(0)
    frame = wx.Frame( None, wx.ID_ANY, 'FloatCanvas2 demo', size = (800, 600) )
    frame.Show()
        
    canvas = fc.SimpleCanvas( window = frame )
    #canvas.dirty = False
    
    kinds = [ ('Rectangle', (100, 100)), ('Circle', 125), ('Ellipse', (100, 150)), ('Text', 'wxPython') ]
    
    # create 1000 rectangles
    for i in range(0, 100):
        kind, sizes = kinds[ i % len(kinds) ]
        if kind != 'Text':
            look = fc.SolidColourLook( line_colour = 'blue', fill_colour = 'red' )
        else:
            semiTransparentGradientLook = fc.RadialGradientFillLook( (0,0), (0,255,0,128), (0,0), 150, (255,0,255,200) )
            look = fc.TextLook( size = 20, faceName = 'Arial', background_fill_look = semiTransparentGradientLook )
            
        r = canvas.create( kind, sizes, name = 'r%d' % i, pos = (i * 100, 0), look = look  )
        #r._debugDrawBoundingBoxes = True
        
    #pts = canvas.create( 'Points', mapPoints, name = 'Map', pos = (0, 0), look = ( 'blue', 'red' ), transform = 'Mercator'  )

    # the default cam, looking at 0, 0
    canvas.camera.position = (0, 0)
    canvas.camera.zoom = (1.0, 1.0)
    
    def print_culled_nodes():
        try:
            print 'rendered %d nodes' % ( len(canvas.renderPolicy.renderedNodes), )
            #print r.boundingBox
            #for node in canvas.renderPolicy.renderedNodes:
            #    print node.name
        except AttributeError:
            pass
    
    rotate = True
    if rotate:
        import time
        for i in range(0, 361):
            canvas.camera.rotation = i
            zoom = 1.0 / (i+1) * 25
            canvas.camera.zoom = ( zoom, zoom )
            canvas.Render()
            print_culled_nodes()
            #time.sleep(0.01)
        
    wx.CallLater( 1000, print_culled_nodes )
    
    app.MainLoop()

if __name__ == '__main__':
    #import cProfile
    #cProfile.run('start()', 'profiling_data_cProfile')
    start()
