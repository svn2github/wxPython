''' Source code for the FloatCanvas tutorial

    Part 7 - Looks
'''

# import wxPython
import wx
# import the floatcanvas module
import wx.lib.floatcanvas.floatcanvas2 as fc
  
def start(frame):
    ''' this function starts all canvas activities '''
        
    canvas = fc.NavCanvas( frame, backgroundColor = 'white' )

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
    
    # create primitives with looks on the,
    for i, look in enumerate(looks):
        r = canvas.create( 'Rectangle', (100, 100), name = 'r%d' % i, pos = (i * 110, 0), look = look  )
        rr = canvas.create( 'RoundedRectangle', (100, 100), 30, name = 'r%d' % i, pos = (i * 110, 200), look = look  )
        c = canvas.create( 'Circle', 50, name = 'r%d' % i, pos = (i * 110, 400), look = look  )
        e = canvas.create( 'Ellipse', (100, 75), name = 'r%d' % i, pos = (i * 110, 600), look = look  )
        l = canvas.create( 'Lines', thingy, name = 'r%d' % i, pos = (i * 110, 800), look = look  )
        p = canvas.create( 'Polygon', thingy, name = 'r%d' % i, pos = (i * 110, 1000), look = look  )

    def setRandomLookWhenClicked(event):
        import random
        event.node.look = random.choice( looks )
        
    for obj in canvas.children:
        obj.subscribe( setRandomLookWhenClicked, 'left_down' )

    canvas.zoomToExtents()
        
        
def run_standalone():
    # create the wx application
    app = wx.App(0)
    
    # setup a very basic window
    frame = wx.Frame( None, wx.ID_ANY, 'FloatCanvas2 tutorial', size = (700, 600) )

    # starts all canvas-related activities
    start( frame )

    # show the window
    frame.Show()
    
    # run the application
    app.MainLoop()


def run_demo(app, panel):
    start( panel )


if __name__ == '__main__':
    run_standalone()
