''' Source code for the FloatCanvas tutorial

    Part 9 - Cameras
'''

# import wxPython
import wx
# import the floatcanvas module
import wx.lib.floatcanvas.floatcanvas2 as fc
  
def start(frame):
    ''' this function starts all canvas activities '''
        
    canvas = fc.NavCanvas( frame, backgroundColor = 'white' )

    canvas.create( 'Circle', 75, name = 'my first circle', pos = (0, 0), look = ('white', 'black') )

    look =  fc.LinearGradientLook( 'purple', (0,0), 'white', (30, 0), 'pink' )
    canvas.createRectangle( (300, 300), pos = (0, 0), rotation = 45, look = look )
    
    # here come there camera parts
    print canvas.camera.position        # default position is (0, 0)
    print canvas.camera.rotation        # default 0
    print canvas.camera.zoom            # default 1
    
    print canvas.camera.transform.matrix    # a camera has a transform like any other nodee
    
    # you should almost never need these two properties:
    print canvas.camera.viewBox             # this is the part of the world that will be shown
    print canvas.camera.viewTransform       # the view-transform
    
    # now shift and rotate the camera a bit
    canvas.camera.rotation = 30
    canvas.camera.position += (100, 0)
    
    
    
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
