# import wxPython
import wx
# import the floatcanvas module
import wx.lib.floatcanvas.floatcanvas2 as fc
from math import radians


def start(frame):
    ''' this function starts all canvas activities '''
    
    canvas = fc.NavCanvas( frame, backgroundColor = 'white', showStatusBar = True )

    # create the nodes
    node = canvas.create( 'Circle', 200, look = ('white', 'green'), name = 'Circle' )
    node2 = canvas.create( 'Text', 'My position, size and rotation do not change', look = fc.FontLook( 14 ), position = (0, -50) )
    node3 = canvas.create( 'Text', 'My position and size and do not change', look = fc.FontLook( 14 ), position = (0,0) )
    node4 = canvas.create( 'Text', 'My size does not change', look = fc.FontLook( 14 ), position = (0, +50), parent = node )
    node5 = canvas.create( 'Text', 'My position does not change', look = fc.FontLook( 14 ), position = (0, +100) )

    # capture their screen space transform
    controller = fc.ScreenRelativeController( canvas.camera )
    controller.addNode( node2 )
    controller.addNode( node3, ('position', 'scale') )
    controller.addNode( node4, ('scale',) )
    controller.addNode( node5, ('position',) )
    canvas.addController( controller )

       
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
