# import wxPython
import wx
# import the floatcanvas module
import wx.lib.floatcanvas.floatcanvas2 as fc
from math import radians

   
def start(frame):
    ''' this function starts all canvas activities '''

    # set background to None, so the background will not be cleared as we draw it ourselves
    canvas = fc.NavCanvas( frame, backgroundColor = None, showStatusBar = True )

    # create the bitmap and enlarge it to whole screen
    background = canvas.create( 'Bitmap', wx.Image('../../../../data/background.png'), look = fc.NoLook, name = 'Bitmap' )
    canvas.zoomToExtents( padding_percent = 0, maintain_aspect_ratio = False )    

    # capture screen space transforn of the bitmap
    controller = fc.ScreenRelativeController( canvas.camera )
    controller.addNode( background, rescaleOnResize = True )
    canvas.addController( controller )

    # create regular foreground objects
    canvas.create( 'Circle', 10, look = ('black', (255,128,0,196)), position = (0, 0) )
    canvas.create( 'RoundedRectangle', (15, 5), 1, look = ('black', 'white'), position = (0, 0) )
    canvas.create( 'Text', 'Try to pan and zoom', look = fc.TextLook( 14, colour = (0,0,0,128), background_fill_look = fc.SolidColourLook(None, None) ), position = (0, 40) )

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
