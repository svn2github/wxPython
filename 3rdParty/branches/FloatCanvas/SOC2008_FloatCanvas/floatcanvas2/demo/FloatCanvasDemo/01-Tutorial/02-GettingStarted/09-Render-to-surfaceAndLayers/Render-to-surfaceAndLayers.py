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
    
    # Create a group with render_to_surface enabled. This means all of the group's
    # children will be rendered to a bitmap which is used in subsequent draws.
    group = canvas.create( 'Group', name = 'Parent of the group', render_to_surface = True, surface_size = ( 600, 300 ) )

    look =  fc.LinearGradientLook( 'purple', (-50,0), 'black', (50, 0), 'green' )
    # Create 100 circles here and add them to the group
    for i in range(100):
        circle = canvas.createCircle( 50, name = 'circle %d' % i, pos = (i * 10, i * 10), look = look, parent = group )
    
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
