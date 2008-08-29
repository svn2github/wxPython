''' Tests a bunch of different looks '''

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
        
    canvas = fc.FloatCanvas( window = frame, backgroundColor = 'white' )
    #canvas.dirty = False
    
    looks = \
    [
        # some looks
        fc.RadialGradientLook( 'red', (0,0), 'red', (0,0), 50, 'yellow' ),
        fc.LinearGradientLook( 'purple', (0,0), 'white', (50,50), 'pink' ),
        fc.OutlineLook( line_colour = 'blue', width = 10, style = 'user_dash', dashes = [1,1] ),
        fc.SolidColourLook( line_colour = 'green', fill_colour = 'red' ),        

        # no lines and some transparent colors
        fc.RadialGradientLook( None, (0,0), (0,255,255,128), (0,0), 50, (255,255,255,0) ),
        fc.LinearGradientLook( None, (-50,-50), (0,0,255,255), (50,50), (128,128,255,0) ),
        fc.SolidColourLook( line_colour = None, fill_colour = 'red' ),        
        fc.SolidColourLook( line_colour = 'green', fill_colour = None ),
        
        # some more exotic lines
        fc.RadialGradientLook( 'pink', (0,0), (0,255,0,128), (0,0), 150, (255,0,255,200), line_style = 'dot', line_width = 10, line_cap = 'butt', line_join = 'bevel' ),
        fc.LinearGradientLook( 'red', (-5,-5), 'orange', (5,5), 'blue', line_style = 'long_dash', line_width = 5 ),
        fc.SolidColourLook( line_colour = 'green', fill_colour = 'red', line_style = 'solid', line_width = 13, line_cap = 'projecting', line_join = 'miter' ),        
        fc.SolidColourLook( line_colour = 'black', fill_colour = 'red', line_style = 'solid', line_width = 13, line_cap = 'projecting', line_join = 'round' ),        
    ]
    
    thingy = [ (0,50), (50,0), (-50,0), (0, -50) ]
    
    # create 1000 rectangles
    for i in range(0, len(looks)):
        look = looks[ i % len(looks) ]
        r = canvas.create( 'Rectangle', (100, 100), name = 'r%d' % i, pos = (i * 110, 0), look = look  )
        rr = canvas.create( 'RoundedRectangle', (100, 100), 30, name = 'r%d' % i, pos = (i * 110, 200), look = look  )
        c = canvas.create( 'Circle', 50, name = 'r%d' % i, pos = (i * 110, 400), look = look  )
        e = canvas.create( 'Ellipse', (100, 75), name = 'r%d' % i, pos = (i * 110, 600), look = look  )
        l = canvas.create( 'Lines', thingy, name = 'r%d' % i, pos = (i * 110, 800), look = look  )
        p = canvas.create( 'Polygon', thingy, name = 'r%d' % i, pos = (i * 110, 1000), look = look  )
        a = canvas.create( 'Arc', 50, 0, 2.14, True, name = 'a%d' % i, pos = (i * 110, 1200), look = look  )
        #r._debugDrawBoundingBoxes = True

    # the default cam, looking at 0, 0
    canvas.camera.position = (600, 500)
    canvas.camera.zoom = (0.4, 0.4)
    
    canvas.zoomToExtents()
       
    wx.CallLater( 1000, canvas.saveScreenshot, 'look_test_screenshot.png' )
                
    app.MainLoop()

if __name__ == '__main__':
    #import cProfile
    #cProfile.run('start()', 'profiling_data_cProfile')
    start()
