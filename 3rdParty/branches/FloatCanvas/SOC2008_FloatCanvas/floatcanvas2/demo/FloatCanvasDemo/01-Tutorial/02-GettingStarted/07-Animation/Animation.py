''' Source code for the FloatCanvas tutorial

    Part 5 - A simple example
'''

# import wxPython
import wx
# import the floatcanvas module
import wx.lib.floatcanvas.floatcanvas2 as fc
 
def start(frame):
    ''' this function starts all canvas activities '''
        
    # Let's create a canvas, in this case a NavCanvas
    canvas = fc.NavCanvas( frame, backgroundColor = 'white' )

    # setup our canvas    
    circle = canvas.create( 'Circle', 75, name = 'my first circle', look = ('white', (0,0,0,96)) )

    look =  fc.LinearGradientLook( 'purple', (-150,-150), (0,255,0,128), (150, 150), (255,0,0,128) )
    rect = canvas.createRectangle( (300, 300), look = look )
        
    # define a function which does some erratic movements, scaling and rotations
    def onMove():
        from math import sin, cos, fmod
        import time
        time = fmod( time.time(), 100 ) / 100 * 2 - 0.5
        circle.pos = ( cos(time * 20) * 100, sin(time * 40) * 150 )
        circle.scale = ( sin(time * 17) * 3, sin(time * 33) * 2 )
        rect.pos = ( sin(time * 60) * 180, cos(time * 20) * 150 )
        rect.rotation = time * 5000
        timer.Restart( interval )
        
    # we could also animate the camera to fly through a scenery
        
    # setup the timer
    interval = 50       # move object every 50 ms
    timer = wx.CallLater( interval, onMove )
    
    # stop the timer if the canvas gets destroy
    def onDestroy(evt):
        timer.Stop()
        
    canvas.Bind( wx.EVT_WINDOW_DESTROY, onDestroy )
    
    
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
