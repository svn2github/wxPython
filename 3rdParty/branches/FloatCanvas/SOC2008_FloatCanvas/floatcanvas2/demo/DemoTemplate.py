# import wxPython
import wx
# import the floatcanvas module
import wx.lib.floatcanvas.floatcanvas2 as fc
 
def start(frame):
    ''' this function starts all canvas activities '''
        
    # Let's create a canvas, in this case a NavCanvas
    canvas = fc.NavCanvas( frame, backgroundColor = 'white' )
    
    # Add a circle with radius 150 to the canvas, give it a name and set its
    # position to (0,0). Then make the outline white and the inner part black.
    canvas.create( 'Circle', 150, name = 'my first circle', pos = (0, 0), look = ('white', 'black') )

    # Create a look to make our next shape a bit prettier.
    # Don't worry if you don't understand the parameters here. The "Looks" part
    # of the tutorial will explain this in detail.
    look =  fc.LinearGradientLook( 'purple', (0,0), 'white', (30, 0), 'pink' )

    # Now we'll add a rectangle of size (300, 300). That's actually a square.
    # The center of the rectangle will be placed at (0,0).
    # Additionally the rectangle will be rotated by 45 degrees and the look
    # we've created in the line above will be assigned.
    canvas.createRectangle( (300, 300), pos = (0, 0), rotation = 45, look = look )
    
    
def run_standalone():
    # create the wx application
    app = wx.App(0)
    
    # setup a very basic window
    frame = wx.Frame( None, wx.ID_ANY, 'FloatCanvas2 demo', size = (500, 500) )

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
