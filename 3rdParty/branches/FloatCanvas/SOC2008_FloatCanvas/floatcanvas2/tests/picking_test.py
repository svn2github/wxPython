import sys
import os.path
sys.path.append( os.path.abspath( '../..' ) )

import wx
import floatcanvas2 as fc

def start():
    #  setup very basic window
    app = wx.App(0)
    frame = wx.Frame( None, wx.ID_ANY, 'FloatCanvas2 demo', size = (800, 600) )
    frame.Show()
        
    canvas = fc.canvas.SimpleCanvas( window = frame )
    #canvas.dirty = False

    r1 = canvas.create( 'Rectangle', (100, 200), name = 'r1', pos = (200, 400), look = fc.SolidColourLook( line_colour = 'blue', fill_colour = 'red' )  )
    r2 = canvas.create( 'Rectangle', (200, 100), name = 'r2', pos = (300, 300), rotation = 20, look = fc.SolidColourLook( line_colour = 'blue', fill_colour = 'red' )  )    

    # the default cam, looking at 500, 500
    canvas.camera.position = (0, 0)
    canvas.camera.zoom = (1.0, 1.0)
    
    def doQuery( (x, y), exact ):
        from floatcanvas2.boundingBox import fromPoint
        from floatcanvas2.sceneQuery import QueryWithPrimitive
        query = QueryWithPrimitive( primitive = fromPoint( (x, y) ), exact = exact )
        pickedNodes = canvas.performSpatialQuery( query )
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
