# import wxPython
import wx
# import the floatcanvas module
import wx.lib.floatcanvas.floatcanvas2 as fc

  
def OnOpenFrame( evt ):
    frame = wx.Frame( None, -1, 'NavCanvas in wx.SplitterWindow', size = (700, 500) )
    splitter = wx.SplitterWindow( frame, -1, style = wx.SP_LIVE_UPDATE )
    panel_left = wx.Panel( splitter, -1 )
    panel_left.SetBackgroundColour( wx.RED )

    canvas = fc.NavCanvas( splitter, backgroundColor = 'white' )

    canvas.create( 'Circle', 150, name = 'my first circle', pos = (0, 0), look = ('white', 'black') )

    look =  fc.LinearGradientLook( 'purple', (0,0), 'white', (30, 0), 'pink' )
    canvas.createRectangle( (300, 300), pos = (0, 0), rotation = 45, look = look, where = 'back' )
       
    splitter.SplitVertically( panel_left, canvas.mainPanel, 10 )
    splitter.SetMinimumPaneSize( 50 )

    frame.Show()


def start(frame):
    ''' this function starts all canvas activities '''
    
    start_panel = wx.Panel( frame, -1 )
    
    btn = wx.Button( start_panel, -1, 'Open NavCanvas in wx.SplitterWindow!', (50, 50) )    
    btn.Bind( wx.EVT_BUTTON, OnOpenFrame )
    

    
    
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
