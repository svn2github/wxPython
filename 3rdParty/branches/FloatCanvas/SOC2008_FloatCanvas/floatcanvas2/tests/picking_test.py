''' Tests picking (hit-testing) '''

import sys
import os.path
sys.path.append( os.path.abspath( '..' ) )

import wx
import floatcanvas as fc

def start():
    #  setup very basic window
    app = wx.App(0)
    frame = wx.Frame( None, wx.ID_ANY, 'FloatCanvas2 demo', size = (800, 600) )
    frame.Show()
        
    canvas = fc.FloatCanvas( window = frame, backgroundColor = 'green' )
    #canvas.dirty = False

    r1 = canvas.create( 'Rectangle', (100, 200), name = 'r1', pos = (0, 0), look = fc.SolidColourLook( line_colour = 'blue', fill_colour = 'red' )  )
    r2 = canvas.create( 'Rectangle', (200, 100), name = 'r2', pos = (100, 100), rotation = 20, look = fc.SolidColourLook( line_colour = 'blue', fill_colour = 'red' )  )    
    r2 = canvas.create( 'Circle', 200, name = 'c1', pos = (200, 200), rotation = 20, look = fc.SolidColourLook( line_colour = 'blue', fill_colour = 'red', line_width = 50 )  )
    

    crazyTransform = False
    if crazyTransform:
        canvas.camera.position = (100, 73)
        canvas.camera.rotation = 12
        canvas.camera.zoom = (0.5, 0.8)
    else:
        canvas.zoomToExtents()

    # the default cam, looking at 500, 500
    
    def doQuery( screen_pnt, exact ):
        pickedNodes = canvas.hitTest( screen_pnt, exact )
        for node in pickedNodes:
            print 'Picked: ', node.name
        print '-' * 20
        
    def onLeftClick(evt):
        doQuery( evt.GetPosition(), exact = False )

    def onRightClick(evt):
        doQuery( evt.GetPosition(), exact = True )
    
    frame.Bind( wx.EVT_LEFT_DOWN, onLeftClick )
    frame.Bind( wx.EVT_RIGHT_DOWN, onRightClick )
        
    app.MainLoop()

if __name__ == '__main__':
    start()
