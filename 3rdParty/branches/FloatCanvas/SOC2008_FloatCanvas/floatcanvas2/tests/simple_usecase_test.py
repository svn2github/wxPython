import sys
import os.path
sys.path.append( os.path.abspath( '../..' ) )

import wx
import floatcanvas2 as fc

class MapPoint(object):
    def __init__(self, name, pos):
        self.name = name
        self.pos = pos


def start():
    #  setup very basic window
    app = wx.App(0)
    frame = wx.Frame( None, wx.ID_ANY, 'FloatCanvas2 demo', size = (800, 600) )
    frame.Show()
        
    canvas = fc.canvas.SimpleCanvas( window = frame )

    r1 = canvas.create( 'Rectangle', (200, 200) )
    r2 = canvas.createRectangle( (200, 200), transform = (200, 200) )
    r3 = canvas.create( 'Rectangle', (200, 200), look = ( 'red', 'black' ), name = 'Rectangle 3' )
    r4 = canvas.createRectangle( (200, 200), look = fc.DefaultLook( 'red', 'black' ) )
    r4 = canvas.createRectangle( (200, 200), look = fc.DefaultLook( line_colour = 'red', fill_colour = 'black' ) )
    r5 = canvas.create( 'Rectangle', (200, 200), look = ( 'red', 'black' ), transform = (200, 200), parent = r2, name = 'Child' )

    canvas.addChild( r1 )
    canvas.addChild( r2, where = 'back' )

    # the default cam, looking at 500, 500
    canvas.camera.target = (500, 500)
    canvas.camera.zoom = (1.0, 1.0)

    app.MainLoop()

if __name__ == '__main__':
    start()
