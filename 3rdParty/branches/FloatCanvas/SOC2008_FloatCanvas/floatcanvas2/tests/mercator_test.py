# set this one to True if you want to render the world map to a surface
use_layer = False
    
import sys
import os.path
sys.path.append( os.path.abspath( '..' ) )
sys.path.append( os.path.abspath( '../misc' ) )

import wx
import floatcanvas as fc

  
def start():
    #  setup very basic window
    app = wx.App(0)
    frame = wx.Frame( None, wx.ID_ANY, 'FloatCanvas2 demo', size = (800, 600) )
    canvas = fc.NavCanvas( frame, backgroundColor = 'white' )
    frame.Show()
           
    from loadWorldData import mapPointsAsLineList
    
    # Create the world by drawing individual longer lines
    currentPos = 0
    look = fc.OutlineLook( 'blue' )

    
    # create one huge list. would be better to subdivide it into a few so one can benefit from culling when zooming in.
    lines = canvas.create( 'LinesList', mapPointsAsLineList, name = 'Map', pos = (0, 0), look = look, transform = 'MercatorTransform', scaled = False, render_to_surface = use_layer, surface_size = (2048, 2048)  )
    #lines2 = canvas.create( 'LinesList', mapPointsAsLineList, name = 'Map', pos = (100, 100), look = look, transform = 'MercatorTransform', scaled = False, render_to_surface = True, surface_size = (2048, 2048)  )

    # the default cam, looking at 0, 0
    canvas.zoomToExtents()
    #canvas.camera.position = (10, 100)
    #canvas.camera.rotation = 180
    canvas.camera.zoom = (1.0, -1.0)
    #
    #def print_culled_nodes():
    #    try:
    #        print 'rendered %d nodes' % ( len(canvas.renderPolicy.renderedNodes), )
    #    except AttributeError:
    #        #print 'forced render'
    #        pass
    #
    #import math
    #animate = True
    #if animate:
    #    import time
    #    for i in range(0, 300):
    #        canvas.camera.zoom = ( 1 + i/50.0, 1 + i/50.0 )
    #        canvas.Render( backgroundColor = 'white' )
    #        print_culled_nodes()
    #    
    #wx.CallLater( 1000, print_culled_nodes )
    
    app.MainLoop()

if __name__ == '__main__':
    #import cProfile
    #cProfile.run('start()', 'profiling_data_cProfile')
    start()
