''' Source code for the FloatCanvas tutorial
'''

# import wxPython
import wx
# import the floatcanvas module
import wx.lib.floatcanvas.floatcanvas2 as fc
 
def start(frame):
    ''' this function starts all canvas activities '''
        
    # Let's create a canvas, in this case a NavCanvas
    canvas = fc.NavCanvas( frame, backgroundColor = 'white' )
    
    settings = [         
                 ( 5, (5, 5), (5, 5) ),
                 ( 1, (5, 5), (5, 5) ),
                 ( 5, (20, 20), (5, 5) ),
                 ( 20, (20, 20), (5, 5) ),
                
                 ( 5, (5, 5), (10, 10) ),
                 ( 1, (5, 5), (10, 10) ),
                 ( 5, (20, 20), (10, 10) ),
            
               ]
            
    for i, setting in enumerate( settings ):
        sigma, kernel_size, offset = setting
    
        x = i * 200
    
        # create the filters
        blurFilter = fc.GaussianBlurFilter( sigma = sigma, kernel_size = kernel_size, surface_size = (100, 100) )
        shadowFilter = fc.ShadowFilter( sigma = sigma, kernel_size = kernel_size, offset = offset, shadow_colour = (0,0,0,128), surface_size = (100, 100) )
        greenShadowFilter = fc.ShadowFilter( sigma = sigma, kernel_size = kernel_size, offset = offset, shadow_colour = (0,128,255,128), surface_size = (100, 100) )
        glowFilter = fc.GlowFilter( sigma = 100, kernel_size = (10, 10), glow_colour = (255,255,0,128), scale = (1.3, 1.3), surface_size = (100, 100) )
        threeDFilter = fc.ThreeDFilter(  sigma = 100, kernel_size = (10, 10), offset = (-3,-3), scale = (0.95, 0.95), surface_size = (100, 100), shadow_colour = (0,0,0,128) )
        pixelizeFilter = fc.PixelizeFilter( block_size = (5, 5), surface_size = (100, 100) )
        
        radialLook = fc.RadialGradientLook( 'red', (0,0), 'red', (0,0), 100, 'yellow' )
        blue_red = fc.SolidColourLook( line_colour = 'blue', fill_colour = 'red' )
    
        r1 = canvas.create( 'Rectangle', (100, 100), name = 'r1', pos = (x, 0), look = blue_red, filter = blurFilter  )
        rr1 = canvas.create( 'RoundedRectangle', (100, 100), 30, name = 'rr1', pos = (x, 150), look = blue_red, filter = shadowFilter  )
        e1 = canvas.create( 'Ellipse', (100, 70), name = 'e1', pos = (x, 300), look = ( 'black', 'black' ), filter = greenShadowFilter  )
        c1 = canvas.create( 'Circle', 50, name = 'c1', pos = (x, 450), look = radialLook, filter = glowFilter  )
        rr2 = canvas.create( 'RoundedRectangle', (100, 100), 30, name = 'rr2', pos = (x, 600), look = (None, 'red'), filter = threeDFilter  )
        t1 = canvas.create( 'Polygon', [ (-50,50), (50, 50), (0, -50) ], name = 't1', pos = (x, 750), rotation = 45, look = blue_red, filter = pixelizeFilter  )
    
    canvas.zoomToExtents()
    
def run_standalone():
    # create the wx application
    app = wx.App(0)
    
    # setup a very basic window
    frame = wx.Frame( None, wx.ID_ANY, 'FloatCanvas2 tutorial', size = (500, 500) )

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
