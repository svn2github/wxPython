''' Source code for the FloatCanvas tutorial

    Part 10 - Groups
'''

# import wxPython
import wx
# import the floatcanvas module
import wx.lib.floatcanvas.floatcanvas2 as fc
  
def start(frame):
    ''' this function starts all canvas activities '''
        
    canvas = fc.NavCanvas( frame, backgroundColor = 'white' )

    group = canvas.create( 'Group', name = 'Parent of the group' )

    look =  fc.LinearGradientLook( 'purple', (-50,0), 'black', (50, 0), 'green' )
    rect = canvas.createRectangle( (50, 50), pos = (0, 0), rotation = 45, look = look, parent = group )
    circle1 = canvas.createCircle( 50, pos = (0, 0), rotation = 45, look = fc.OutlineLook('blue', style = 'long_dash'), parent = group )

    # rectangle and circle are in the group now. let's scale the group parent
    # which will scale circle and rectangle
    group.scale = (3, 0.5)
    print rect.localTransform.scale
    print rect.worldTransform.scale
    
    # instead of the "Group" node, any other kind of node can serve as a group
    # as well
    circle2 = canvas.createCircle( 5, pos = (30, 0), scale = (2, 1), look = look, parent = circle1 )
    
    # now the hierarchy looks like:
    #
    # canvas
    #  |__group
    #       |____rect
    #       |____circle 1
    #                |_____circle2
    
    print circle2.worldTransform.pos
    
    # check some of the tree-related functionality of the circle node2
    print circle2.root is canvas
    print circle1.children == [circle2]
    print circle2.parent == circle1
        
        
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
