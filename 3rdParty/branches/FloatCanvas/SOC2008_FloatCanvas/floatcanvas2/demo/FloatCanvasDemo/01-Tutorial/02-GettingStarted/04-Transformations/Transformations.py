''' Source code for the FloatCanvas tutorial

    Part 8 - Transformations
'''

# import wxPython
import wx
# import the floatcanvas module
import wx.lib.floatcanvas.floatcanvas2 as fc

def start(frame):
    ''' this function starts all canvas activities '''
        
    # Let's create a canvas, in this case a NavCanvas
    canvas = fc.NavCanvas( frame, backgroundColor = 'white' )
    
    circle = canvas.create( 'Circle', 75, name = 'my first circle', pos = (2, 0), scale = (5, 3), rotation = 30, look = ('white', 'pink') )

    # show how to access the different transform properties
    
    print circle.pos
    print circle.position
    print circle.translation
    print circle.rotation
    print circle.scale
    print circle.transform
    print circle.transform.matrix
    
    circle.pos = (4, 5)
    circle.position = ( 9, 7 )
    circle.translation = ( 1, 2 )
    circle.rotation = 12
    circle.scale = (2, 2)
    
    print circle.pos
    print circle.position
    print circle.translation
    print circle.rotation
    print circle.scale
    print circle.transform
    print circle.transform.matrix
    

    pi = 3.14
    half_pi = pi / 2.0
    lines = canvas.create( 'Lines', [ (0, -half_pi), (-half_pi, 0), (0, half_pi), (half_pi, 0), (0, -half_pi) ], name = 'mercator test', transform = 'MercatorTransform', look = ('black', None), where = 'front' )
    print lines.transform
    lines.scale = (1, 0.2)
    
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
