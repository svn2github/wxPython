# import wxPython
import wx
# import the floatcanvas module
import wx.lib.floatcanvas.floatcanvas2 as fc
from math import radians


class LineDrawer(object):
    def __init__(self, canvas, parent, lineColour):
        self.line = None
        self.canvas = canvas
        self.parent = parent
        self.lineColour = lineColour

        parent.subscribe( self.onLineBegin, 'left_down' )
        parent.subscribe( self.onLineDrag, 'move' )
        parent.subscribe( self.onLineEnd, 'left_up' )

    def onLineBegin(self, evt):
        # grab the coordinate of the line in *local*, that is, long-lat space
        startPnt = evt.coords.local
        lineNode = self.lineNode = self.canvas.createLine( startPnt, startPnt, look = ( self.lineColour, None ), parent = self.parent, name = 'user-drawn line' )
        self.line = lineNode.model
        print 'begin line @ %s' % startPnt

    def onLineDrag(self, evt):
        if self.line is None:
            return
        self.line.endPoint = evt.coords.local
        
    def onLineEnd(self, evt):
        if self.line is None:
            return
        self.line.endPoint = evt.coords.local
        self.line = None
        print 'end line @ %s' % evt.coords.local


def start(frame):
    ''' this function starts all canvas activities '''
    
    canvas = fc.NavCanvas( frame, backgroundColor = 'white', showStatusBar = True )
    canvas.camera.zoom = (0.4, 0.4)
    # create the untransformed bitmap
    canvas.create( 'Bitmap', wx.Image('../../../../data/TestMap.png'), look = fc.NoLook, name = 'Bitmap' )

    # now create the group node which will hold all the nodes with a mercator transform
    group = canvas.createGroup( name = 'Mercator Group', transform = 'MercatorTransform' )
    # scale the group so its size is similar to that of the bitmap
    group.scale = (5, 2.75)
    
    # now add a few lines whose coordinates are long-lat to form a grid
    noLat = 10
    noLong = 10
    lines = []
    # calculate line coordinates from north to south
    for x in range(noLong+1):
        long = radians( x * 358.0 / noLong - 179 )
        lines += [ (long, radians(-89)), (long, radians(89)) ]

    # calculate line coordinates from west to east
    for y in range(noLat+1):
        lat = radians( y * 178.0 / noLat - 89 )
        lines += [ (radians(-179), lat), (radians(179), lat) ]

    # create the line node
    translucentGreen = (0,255,0,128)
    grid = canvas.createLineSegments( lines, parent = group, look = fc.LineLook( translucentGreen, 1, style = 'solid') )

    # create some untransformed text
    canvas.create( 'Text', 'Simply left-click and drag to create lines', look = fc.FontLook( size = 15, faceName = 'Arial', colour = 'black' ), name = 'label' )
    
    # finally create the tool to draw lines on the group in red
    translucentRed = (255,0,0,196)
    lineDrawer = LineDrawer(canvas, group, translucentRed)

       
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
