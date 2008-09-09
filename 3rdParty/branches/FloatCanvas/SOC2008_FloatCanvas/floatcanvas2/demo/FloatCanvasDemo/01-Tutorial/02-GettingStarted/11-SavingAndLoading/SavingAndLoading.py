''' Source code for the FloatCanvas tutorial

    Part 15 - Saving and loading
'''

# import wxPython
import wx
# import the floatcanvas module
import wx.lib.floatcanvas.floatcanvas2 as fc
 
def start(frame):
    ''' this function starts all canvas activities '''
        
    # Let's create a canvas, in this case a NavCanvas
    canvas = fc.NavCanvas( frame, backgroundColor = 'white' )
    
    # setup the canvas
    look = fc.RadialGradientLook( 'red', (0,0), (255,0,0,128), (0,0), 150, (255,255,0,128) )
    look2 = fc.RadialGradientLook( None, (0,0), (0,255,255,128), (0,0), 250, (255,255,255,0) )
    
    circle = canvas.create( 'Circle', 75, name = 'circle', pos = (200, 40), look = look )
    rect = canvas.createRectangle( (200, 200), name = 'rectangle', pos = (0, 0), rotation = 0, look = ('brown', (0,255,0,128)) )
    poly = canvas.create( 'Polygon', [ (0,0), (137,12), (42,123), (50,70), (54,52) ], name = 'polygon', pos = (-40, -250), look = look2 )
    
    canvas.zoomToExtents()
    
    # render hereso we get something on screen
    canvas.Render()
    
    # save the canvas to the native format
    # The save to /load from disk calls are commented here, because the demo
    # should not write unconditionally to your disk. If you want to save
    # something, use the save button of the navCanvas. It uses the same
    # mechanisms as shown here internally.
    
    fcsf_data = canvas.serialize( 'fcsf' )
    svg_data = canvas.serialize( 'svg' )
    jpg_data = canvas.getScreenshot( 'jpg' )
    #canvas.serializeToFile( 'saved_canvas.fcsf' )
    #canvas.serializeToFile( 'example.svg' )
    #canvas.saveScreenshot( 'screenshot.png' )    
    
    # the two loading function
    canvas.unserialize( fcsf_data, 'fcsf' )
    #canvas.serializeFromFile( 'saved_canvas.fcsf' )
    
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
