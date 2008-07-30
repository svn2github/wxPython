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

    r1 = canvas.create( 'Rectangle', (100, 200), look = fc.SolidColourLook( line_colour = 'blue', fill_colour = 'red' )  )
    semiTransparentGradientLook = fc.RadialGradientLook( 'blue', (0,0), (255,0,0,64), (0,0), 200, (0,0,255,128) )
    r2 = canvas.createRectangle( (200, 100), position = (100, 100), look = semiTransparentGradientLook )
    r3 = canvas.create( 'Rectangle', (20, 20), look = ( 'red', 'black' ), name = 'Rectangle 3', where = 'front' )
    linearGradientLook = fc.LinearGradientLook( 'green', (-100,-100), (255,255,0,64), (100,100), (0,255,0,128) )
    r5 = canvas.create( 'Rectangle', (150, 150), look = linearGradientLook, position = (200, 200), rotation = 45, scale = (2, 1), parent = r2, name = 'Child', where = 'front' )
    #mr = canvas.createPoints( [(70, 70)], transform = 'MercatorTransform', look = semiTransparentGradientLook, name = 'mercator' )
    #mr.scale = (1, 100)

    # the default cam, looking at 500, 500
    canvas.camera.position = (0, 0)
    canvas.camera.zoom = (1.0, 1.0)
    
    import time
    for i in range(0, 200):
        canvas.camera.position = (0, 0)
        canvas.camera.rotation = i
        zoom = 1 + abs(i - 50) / 50.0
        canvas.camera.zoom = ( zoom, zoom )
        canvas.Render()
        time.sleep(0.01)

    app.MainLoop()

if __name__ == '__main__':
    start()
