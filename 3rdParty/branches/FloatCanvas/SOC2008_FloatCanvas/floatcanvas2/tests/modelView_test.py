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

    r1 = canvas.create( 'Rectangle', (100, 200), look = fc.SolidColourLook( line_colour = 'blue', fill_colour = 'red' )  )

    # the default cam, looking at 500, 500
    canvas.camera.position = (0, 0)
    canvas.camera.zoom = (1.0, 1.0)
    
    print 1, canvas.dirty, r1.dirty, r1.model.dirty
    #canvas.Render()
    print 2, canvas.dirty, r1.dirty, r1.model.dirty

    import time
    time.sleep(0.5)
    print 3, canvas.dirty, r1.dirty, r1.model.dirty
    r1.model.size = (200, 100)
    print 4, canvas.dirty, r1.dirty, r1.model.dirty
    
    def change():
        r1.model.size = (500, 500)
        
    wx.CallLater( 1000, change )
    
    app.MainLoop()

if __name__ == '__main__':
    start()
