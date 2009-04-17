# import wxPython
import wx
# import the floatcanvas module
import wx.lib.floatcanvas.floatcanvas2 as fc


class LineDrawer(object):
    def __init__(self, canvas):
        self.line = None
        self.canvas = canvas

        canvas.subscribe( self.onLineBegin, 'input.left_down' )
        canvas.subscribe( self.onLineDrag, 'input.move' )
        canvas.subscribe( self.onLineEnd, 'input.left_up' )

        canvas.updatePolicy.interval = 0.01

    def onLineBegin(self, evt):
        startPnt = evt.coords.world
        lineNode = self.canvas.createLine( startPnt, startPnt, look = ('red', 'blue') )
        self.line = lineNode.model
        print 'begin'

    def onLineDrag(self, evt):
        if self.line is None:
            return
        self.line.endPoint = evt.coords.world
        
    def onLineEnd(self, evt):
        if self.line is None:
            return
        self.line.endPoint = evt.coords.world
        self.line = None
        print 'end'


def start(frame):
    ''' this function starts all canvas activities '''
    
    canvas = fc.NavCanvas( frame, backgroundColor = 'white' )
    canvas.create( 'Text', 'Simply left-click and drag to create lines', look = fc.FontLook( size = 15, faceName = 'Arial', colour = 'black' ) )
    canvas.zoomToExtents()
    lineDrawer = LineDrawer(canvas)

       
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
