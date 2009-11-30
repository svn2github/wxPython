# import wxPython
import wx
# import the floatcanvas module
import wx.lib.floatcanvas.floatcanvas2 as fc
from math import radians


class MyMoveNodeMode(fc.guiMode.GUIModeMoveObjects):
    def __init__(self, nonSelectableNodes = []):
        self.nonSelectableNodes = nonSelectableNodes
        
    ''' Can be used to move objects on canvas.
    '''
    def on_move(self, event):
        ''' filters all static objects and moves the non-static ones '''
        moveable = getattr( self.node, 'moveable', True ) and self.node not in self.nonSelectableNodes
        if moveable:
            # call base class to move object
            fc.guiMode.GUIModeMoveObjects.on_move( self, event )


def start(frame):
    ''' this function starts all canvas activities '''
    
    canvas = fc.NavCanvas( frame, backgroundColor = 'white', showStatusBar = True )

    # setup the canvas
    look = fc.RadialGradientLook( 'red', (0,0), (255,0,0,128), (0,0), 150, (255,255,0,128) )
    look2 = fc.RadialGradientLook( None, (0,0), (0,255,255,128), (0,0), 250, (255,255,255,0) )
    
    poly = canvas.create( 'Polygon', [ (0,0), (137,12), (42,123), (50,70), (54,52) ], name = 'polygon', pos = (-40, -250), look = look2 )
    circle = canvas.create( 'Circle', 75, name = 'circle', pos = (100, 80), look = look )
    rect = canvas.createRectangle( (200, 200), name = 'rectangle', pos = (0, 0), rotation = 0, look = ('brown', (0,255,0,128)) )
    text = canvas.create( 'Text', "I can't be moved!", name = 'text', pos = (0, 0), look = fc.TextLook(14, colour = ( 0, 0, 0, 100 ), background_fill_look = fc.SolidColourLook(None, None)), parent = rect )
    rect.moveable = False

    canvas.zoomToExtents()

    # replace default move tool with our own
    for mode_description in canvas.mode_descriptions:
        if mode_description.name == 'Move':
            mode_description.guiMode = MyMoveNodeMode( [text] )

       
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
