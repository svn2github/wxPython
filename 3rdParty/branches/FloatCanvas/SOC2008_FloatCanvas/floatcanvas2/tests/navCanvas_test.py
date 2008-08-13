''' Tests the NavCanvas and events (click on object, move cursor over small
    circle)
'''

import sys
import os.path
sys.path.append( os.path.abspath( '..' ) )

import wx
import floatcanvas as fc
from floatcanvas.canvas.navCanvas import NavCanvas
from floatcanvas.math.boundingBox import fromPoint
from floatcanvas.nodes.spatialQuery import QueryWithPrimitive

def onEvent(event):
    print '%s event on node %s @ %s' % ( event.__class__.__name__, event.nodes[0].name, event.coords )

def start():
    #  setup very basic window
    app = wx.App(0)
    frame = wx.Frame( None, wx.ID_ANY, 'FloatCanvas2 demo', size = (800, 600) )
    canvas = NavCanvas( frame, backgroundColor = 'white' )
    frame.Show()
        
    #canvas.dirty = False

    r1 = canvas.create( 'Rectangle', (100, 200), name = 'r1', pos = (0, 0), look = fc.SolidColourLook( line_colour = 'blue', fill_colour = 'red' )  )
    r2 = canvas.create( 'Rectangle', (200, 100), name = 'r2', pos = (100, 100), rotation = 20, look = fc.SolidColourLook( line_colour = 'blue', fill_colour = 'red' )  )    
    c1 = canvas.create( 'Circle', 200, name = 'c1', pos = (200, 200), rotation = 20, look = fc.SolidColourLook( line_colour = 'blue', fill_colour = 'red', line_width = 50 )  )    
    c2 = canvas.create( 'Circle', 20, name = 'c2', pos = (500, 200), rotation = 20, look = fc.SolidColourLook( line_colour = 'blue', fill_colour = 'red', line_width = 2 )  )    

    # the default cam, looking at 500, 500
    canvas.camera.position = (100, 73)
    #canvas.camera.rotation = 12
    canvas.camera.zoom = (0.5, 0.8)
    

    nodes = [ r1, r2, c1, c2, canvas ]
    events = [ 'left_down', 'left_dclick', 'left_up',
               'middle_down', 'middle_dclick', 'middle_up',
               'right_down', 'right_dclick', 'right_up',
               'wheel', 'key_down', 'key_up',
             ]
    
    # bind all events
    for node in nodes:
        for event in events:    
            node.subscribe( onEvent, event )
            
    # bind the motion event only to the mini circle so the event output doesn't
    #  litter everything
    c2.subscribe( onEvent, 'move' )
    
    app.MainLoop()


if __name__ == '__main__':
    start()
