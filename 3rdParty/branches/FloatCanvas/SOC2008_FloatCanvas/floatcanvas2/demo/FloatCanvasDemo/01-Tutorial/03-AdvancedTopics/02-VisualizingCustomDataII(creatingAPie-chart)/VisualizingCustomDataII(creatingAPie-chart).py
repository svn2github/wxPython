''' Source code for the FloatCanvas tutorial

    Part 5 - A simple example
'''

# import wxPython
import wx
# import the floatcanvas module
import wx.lib.floatcanvas.floatcanvas2 as fc
 

class PieChart(object):
    def __init__(self, radius, values):
        self.radius = radius
        self.values = values
        
ObservablePieChart = fc.canvas.observables.createObservableClass( PieChart, ( 'radius', 'values' ) )
 
class PieChartVisualizer(object):
    def __init__(self, piechart, parentNode, looks, labelLook = None, labelFilter = None, drawLabels = True):
        self.parentNode = parentNode
        self.piechart = piechart
        self.nodes = []
        self.looks = looks
        self.labelLook = labelLook
        self.labelFilter = labelFilter
        self.drawLabels = drawLabels

        def onModelChanged(event):
            self.rebuild()
        self.piechart.subscribe( onModelChanged, 'attribChanged' )

        self.rebuild()
        
    def rebuild(self):
        from math import pi, sin, cos
        
        piechart = self.piechart
        
        values_sum = float( sum( piechart.values ) )
        normalizedValues = [ value / values_sum for value in piechart.values ]
        
        canvas = self.parentNode.root
        self.parentNode.removeChildren( self.nodes )
        self.nodes = []
        
        current_position = 0
        for i, value in enumerate(normalizedValues):
            next_position = current_position + value
            
            name = 'piechart piece %d, value %f' % ( i, value )
            
            look = self.looks[ i % len(self.looks) ]
            
            angle1, angle2 = current_position * 2 * pi, next_position * 2 * pi
            
            arc = canvas.createArc( piechart.radius, angle1, angle2, True, name = name, look = look, parent = self.parentNode )
            self.nodes.append( arc )

            coords1 = ( cos(angle1) * piechart.radius, sin(angle1) * piechart.radius )
            coords2 = ( cos(angle2) * piechart.radius, sin(angle2) * piechart.radius )
            coords3 = ( cos((angle2+angle1)/2) * piechart.radius / 1.5, sin((angle2+angle1)/2) * piechart.radius / 1.5 )

            if abs(angle1-angle2) < pi:
                poly = canvas.createLines( [ coords1, (0,0), coords2 ], name = name, look = look, parent = self.parentNode )
                self.nodes.append( poly )

            if self.labelLook and self.drawLabels:
                textShadow = fc.ShadowFilter(  sigma = 3, kernel_size = (8, 8), offset = (1.5,1.5), surface_size = (100, 100), shadow_colour = (0,0,0,128) )
                text = canvas.createText( '%.1f%%' % (value * 100), pos = coords3, name = name, look = self.labelLook, filter = textShadow, parent = self.parentNode, where = 'front' )
                self.nodes.append( text )

            current_position = next_position
            
        piechart.dirty = False
 
def start(frame):
    ''' this function starts all canvas activities '''
        
    # Let's create a canvas, in this case a NavCanvas
    #from wx.lib.floatcanvas.floatcanvas2.floatcanvas.canvas.renderPolicies import DefaultRenderPolicy
    #canvas = fc.NavCanvas( frame, backgroundColor = 'white', renderPolicy = DefaultRenderPolicy() )
    canvas = fc.NavCanvas( frame, backgroundColor = 'white' )

    colors = [ 'red', 'green', 'blue', 'yellow', 'cyan', 'magenta' ]
    looks = [ fc.RadialGradientLook( (128,128,128,128), (10,0), (255,255,255,160), (50,0), 300, color, line_width = 0.2 ) for color in colors ]
    labelLook = fc.TextLook( 8, colour = (0,0,0,192), background_fill_look = fc.SolidColourFillLook( None ) )
    threedFilter = fc.ThreeDFilter(  sigma = 100, kernel_size = (10, 10), offset = (0,0), scale = (0.95, 0.95), surface_size = (100, 100), shadow_colour = (0,0,0,128) )


    pieChart = ObservablePieChart( 100, [1,3,8,5,24,9] )
    pieNode = canvas.createGroup( filter = threedFilter )
    visualizer = PieChartVisualizer( pieChart, pieNode, looks, labelLook )
    
    buttonLook = fc.LinearGradientLook( 'black', (-50,-50), (0,0,255,128), (50,50), (128,128,255,0) )
    shadowFilter = fc.ShadowFilter(  sigma = 3, kernel_size = (8, 8), offset = (3,3), surface_size = (100, 100), shadow_colour = (0,0,255,128) )
    rect = canvas.createRoundedRectangle( (60, 30), 15, look = buttonLook, pos = (200, 0), filter = shadowFilter )
    threedFilter = fc.ThreeDFilter(  sigma = 100, kernel_size = (10, 10), offset = (0,0), scale = (0.95, 0.95), surface_size = (100, 100), shadow_colour = (0,0,0,128) )
    text = canvas.createText( 'Change!', look = labelLook, parent = rect, filter = threedFilter )
    
    def changeModel(event):
        import random
        no_slices = random.randint(1, 8)    
        pieChart.values = [ random.randint( 0, 666 ) for i in range(no_slices) ]
    
    rect.subscribe( changeModel, 'left_down' )
    
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
