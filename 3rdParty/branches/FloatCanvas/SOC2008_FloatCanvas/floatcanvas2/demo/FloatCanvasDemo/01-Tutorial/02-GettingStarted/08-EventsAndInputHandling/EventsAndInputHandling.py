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
    
    # setup the canvas
    look = fc.RadialGradientLook( 'red', (0,0), (255,0,0,128), (0,0), 150, (255,255,0,128) )
    look2 = fc.RadialGradientLook( None, (0,0), (0,255,255,128), (0,0), 250, (255,255,255,0) )
    
    circle = canvas.create( 'Circle', 75, name = 'circle', pos = (200, 40), look = look )
    rect = canvas.createRectangle( (200, 200), name = 'rectangle', pos = (0, 0), rotation = 0, look = ('brown', (0,255,0,128)) )
    poly = canvas.create( 'Polygon', [ (0,0), (137,12), (42,123), (50,70), (54,52) ], name = 'polygon', pos = (-40, -250), look = look2 )
    text = canvas.create( 'Text', 'Click me!', name = 'text', pos = (0, 0), look = fc.TextLook(14, background_fill_look = fc.SolidColourLook(None, None)), parent = rect )
    
    # now we start all the event-related things

    # the event handler print some information and rotates the rectangle upon
    #  each click
    def onRectangleClicked(event):
        print event.coords, [node.name for node in event.nodes]
        print type(event.wx_event), event.wx_event.GetPosition()
        rect.rotation += 21
           
    # bind an event handler to the 'left_down' event of the rect shape
    rect.subscribe( onRectangleClicked, 'left_down' )

    # now bind all other kinds of events to the other nodes

    # a generic event handler, printing some info
    def onEvent(event):
        print '%s event on nodes %s @ %s' % ( event.__class__.__name__, [node.name for node in event.nodes], event.coords )    

    # nodes which we want to watch
    nodes = [ circle, rect, poly ]
    
    # events to bind (all except 'move')
    events = [ 'left_down', 'left_dclick', 'left_up',
               'middle_down', 'middle_dclick', 'middle_up',
               'right_down', 'right_dclick', 'right_up',
               'wheel', 'key_down', 'key_up',
             ]
    
    # bind all events
    for node in nodes:
        for event in events:    
            node.subscribe( onEvent, event )
            
    # bind the motion event only to the polygon so the event output doesn't
    #  litter everything
    poly.subscribe( onEvent, 'move' )

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
