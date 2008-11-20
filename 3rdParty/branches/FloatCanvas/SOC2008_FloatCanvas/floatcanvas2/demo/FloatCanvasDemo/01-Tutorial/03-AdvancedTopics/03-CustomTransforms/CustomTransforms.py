''' Source code for the FloatCanvas tutorial

    Part 5 - A simple example
'''

# import wxPython
import wx
# import the floatcanvas module
import wx.lib.floatcanvas.floatcanvas2 as fc

numpy = fc.math.numpy

class SwirlTransform(object):    
    ''' Implements a swirl (vortex-like) transform
        see http://www.cs.kent.ac.uk/projects/pivotal/cgraphics.html "Swirling Patterns"
        --> formulate: swirl (r, theta) = (r, r + theta)
    '''
    def __init__(self, center, strength):
        self.center = center
        self.strength = strength
    
    def __call__(self, coords):
        ''' coords is a sequence of points.
            this function can be implemented more efficiently with numpy, but it serves only as a demonstration for now
        '''
        # loop through all coordinates (slow)
        transformedCoords = []
        for coord in coords:
            # step 1: convert cartesian to polar
            #          --> r = sqrt(x^2+y^2) where x and y are the distance to the center
            #          --> theta = atan2( y, x )
            dist = coord - self.center
            r = fc.math.vector.length(dist)
            theta = numpy.arctan2( dist[1], dist[0] )
            # step 2: apply effect
            #          --> swirl (r, theta) = (r, r + theta)
            swirledTheta = r * self.strength + theta 
            # step 3: convert back to cartesian
            #          --> x = r * cos(theta), y = r * sin(theta)    + center
            transformedCoord = ( r * numpy.cos(swirledTheta) + self.center[0], r * numpy.sin(swirledTheta) + self.center[1] )
            # step 5: add the transformed coordinate to our result
            transformedCoords.append( transformedCoord )
            
        # step 6: beginning of efficient implementation with numpy, not yet ready
        # coords = fc.math.numpy.asarray(coords)        
        # dist = coords - [self.center] * len(coords)

        return transformedCoords
    

def createRectangleGrid(name, canvas, totalSize, noRectangles, look, transform = None):
    ''' simple helper, creates a grid of small rectangles with a label'''
    grid = canvas.createGroup(transform = transform, name = 'grid %s' % name)

    # create the grid
    rectangleSize = ( totalSize[0] / noRectangles[0], totalSize[1] / noRectangles[1] )
    for y in range(noRectangles[1]):
        for x in range(noRectangles[0]):
            canvas.createLine( (0,0), (0, rectangleSize[1]), pos = (x * rectangleSize[0], y * rectangleSize[1]), name = '%s %d %d' % (name, x, y), look = look, parent = grid )
            canvas.createLine( (0,0), (rectangleSize[0], 0), pos = (x * rectangleSize[0], y * rectangleSize[1]), name = '%s %d %d' % (name, x, y), look = look, parent = grid )

    # close the ends
    for y in range(noRectangles[1]):
        canvas.createLine( (0,0), (0, rectangleSize[1]), pos = (noRectangles[0] * rectangleSize[0], y * rectangleSize[1]), name = '%s %d %d' % (name, x, y), look = look, parent = grid )
    for x in range(noRectangles[0]):
        canvas.createLine( (0,0), (rectangleSize[0], 0), pos = (x * rectangleSize[0], noRectangles[1] * rectangleSize[1]), name = '%s %d %d' % (name, x, y), look = look, parent = grid )

    canvas.createText( name, pos = (totalSize[0] / 2, totalSize[1] + 20), name = 'label %s' % name, parent = grid, look = fc.TextLook( size = 14, colour = 'black' ) )

    return grid

def start(frame):
    ''' this function starts all canvas activities '''
        
    # Let's create a canvas, in this case a NavCanvas
    canvas = fc.NavCanvas( frame, backgroundColor = 'white' )

    # create our custom transform
    transform = SwirlTransform( (100,100), 0.003 )

    # now create two grids, one untransformed and one with our swirl transform applied
    totalSize = (200, 200)
    noRectangles = (10, 10)

    grid1 = createRectangleGrid( 'Untransformed', canvas, totalSize, noRectangles, ('black', None) )
    grid2 = createRectangleGrid( 'Custom swirl transform', canvas, totalSize, noRectangles, ('red', None ), transform )
    grid2.position = ( totalSize[0] * 1.5, 0 )

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
