from __future__ import with_statement
# import wxPython
import wx
# import the floatcanvas module
import wx.lib.floatcanvas.floatcanvas2 as fc
from math import radians, floor, ceil
import webbrowser

class RevenueData(object):
    class Country(object):
        def __init__(self, name, coordinates):
            self.name = name
            self.coordinates = coordinates

    class Timepoint(object):
        def __init__(self, name, time):
            self.name = name
            self.time = time
            
    def __init__(self, timePoints, countries):
        self.timePoints = timePoints
        self.timeToTimePoints = {}
        self.countries = countries
        self.countryNameToCountry = {}
        self.table = {}

    def format(self, fieldWidth = 10):        
        header = ''.join( [ tp.name.rjust( fieldWidth ) for tp in self.timePoints ] )
        lines = [ header ]
        for country in self.countries:
            line = country.name.rjust( fieldWidth )
            for timePoint in self.timePoints:
                value = self.table[timePoint][country]
                line += ( '%.1f' % value ).rjust( fieldWidth )
            lines.append( line )
        return '\n'.join( lines )

    def get(self, timeValue, countryName):
        timePoint = self.timeToTimePoints[ timeValue ]
        country = self.countryNameToCountry[ countryName ]
        return self.table[ timePoint ][ country ]

    def getInterpolated(self, time, country):
        time1 = floor( time )
        time2 = ceil( time )
        value1 = self.get( time1, country.name )
        value2 = self.get( time2, country.name )

        t = time - time1
        value = ( 1 - t ) * value1 + t * value2
        return value
        
    @classmethod
    def load( cls, filename ):
        result = RevenueData( [], [] )
        
        with file( filename, 'r' ) as f:
            noTimePoints = int( f.readline() )
            for i in range( noTimePoints ):
                timePointName = f.readline().strip()
                timePoint = cls.Timepoint( timePointName, i )
                result.timePoints.append( timePoint )
                result.timeToTimePoints[ i ] = timePoint

            noCountries = int( f.readline() )
            for i in range( noCountries ):
                name, coordinates = f.readline().strip().split(',', 1)
                coordinates = coordinates.split(',')
                coordinates = ( int(coordinates[0]), int(coordinates[1]) )
                country = cls.Country( name, coordinates )
                result.countries.append( country )
                result.countryNameToCountry[ country.name ] = country

            for c in range( noCountries ):
                for t in range( noTimePoints ):
                    timePoint = result.timePoints[t]
                    country = result.countries[c]
                    value = float( f.readline() )
                    result.table.setdefault( timePoint, {} )[ country ] = value

        return result
            
##
##class BarToRectangleAdapter(object):
##    implements_interfaces = fc.models.interfaces.IRoundedRectangle
##    
##    def __init__(self, bar):
##        self.bar = bar
##
##    def _getSize(self):
##        return ( 10, self.bar.value )
##
##    def _getRadius(self):
##        return 0.05 * self.bar.value
##
##    size = property( _getSize )
##    radius = property( _getRadius )


def getFullPath(filename):
    return '../../../../data/%s' % filename

class RevenueDataVisualizer(object):
    def __init__(self, filename, bitmapFilename, parentNode, animationInterval):
        self.animationInterval = animationInterval
        self.parentNode = parentNode
        self.canvas = parentNode.root
        #self.canvas.adapterRegistry.register( self.RevenueBar, fc.models.interfaces.IRoundedRectangle, BarToRectangleAdapter )
        self.data = RevenueData.load( filename )
        self.mapNode = self.canvas.create( 'Bitmap', wx.Image(bitmapFilename), look = fc.NoLook )
        self.mapNode.position += self.mapNode.boundingBox.Size / 2
        self.logoNode = self.canvas.create( 'Bitmap', wx.Image(getFullPath('wxPython.gif')), look = fc.NoLook )
        self.logoNode.position += ( 350, 350 )
        self.logoNode.scale = 1
        self.logoNode.subscribe( lambda evt: webbrowser.open('http://www.wxpython.org'), 'left_up' )
        self.timer = wx.CallLater( animationInterval * 1000, self.onAnimate )
        self.canvas.Bind( wx.EVT_WINDOW_DESTROY, self.onDestroy )
        self.time = self.data.timePoints[0].time
        self.animationSpeed = 3
    
        self.rebuild()
        
        #print revenueData.format()
        #print revenueData.get( 1, 'Australien' )
        #print revenueData.getInterpolated( 0.4, 'Russland' )
    def onDestroy(self, evt):
        self.timer.Stop()

    def onAnimate(self):
        self.time += self.animationInterval * self.animationSpeed
        if self.time > self.data.timePoints[-1].time:
            self.time = self.data.timePoints[0].time
        self.textNode.model.text = self.data.timePoints[ int( floor( self.time + 0.5 ) ) ].name
        self.setTime( self.time )
        self.timer.Restart( self.animationInterval * 1000 )

    def setTime(self, time):
        for country, barNode, descrNode in self.bars:
            timePoint = self.data.timePoints[ int( floor( self.time + 0.5 ) ) ]
            value = self.data.table[ timePoint ][ country ]
            barNode.model.size = ( 15, self.data.getInterpolated( time, country ) * 2 )
            barNode.pos  = country.coordinates
            barNode.pos -= ( 0, barNode.model.size[1] * 0.5 )
            descrNode.model.text = '%.0f' % value

    def rebuild(self):
        canvas = self.canvas
        #look = fc.LinearGradientLook( ( 0, 0, 0, 128), (0,0), (255,0,0,196), (5, 2), (255, 0, 0, 128) )
        look = fc.RadialGradientLook( (0,0,0,255), (0,0), (255,255,0,128), (0,0), 300, (255,255,0,128) )
        #textBackground = fc.LinearGradientLook( (255,0,0,128), (-50,0), (255,0,0,128), (0,0), 100, (255,255,255,128) )
        textBackground = fc.SolidColourLook( (0,0,0,0), (0,0,0,0) ) #fc.LinearGradientLook( ( 0, 0, 0, 0), (0,0), (196,196,196,128), (50, 100), (128, 128, 128, 128) )
        textLook = fc.TextLook( size = 15, faceName = 'Arial', colour = 'black', background_fill_look = textBackground )
        self.bars = []
        self.headerNode = canvas.createText( 'World revenue map', look = textLook, pos = ( 300, -70 ) )
        self.textNode = canvas.createText( 'Time', look = textLook, pos = ( 300, -30 ) )
        for country in self.data.countries:
            parent = canvas.createGroup()
            node = canvas.create( 'RoundedRectangle', (15, 10), 3, look = look, parent = parent )
            descrNode = canvas.create( 'Text', country.name, look = textLook, parent = parent, pos = country.coordinates )
            descrNode.pos += ( 0, 45 )
            descrNode = canvas.create( 'Text', look = textLook, parent = parent, pos = country.coordinates )
            descrNode.pos += ( 0, 20 )
            self.bars.append( (country, node, descrNode) )


def start(frame):
    ''' this function starts all canvas activities '''
    
    canvas = fc.NavCanvas( frame, backgroundColor = 'white', showStatusBar = True, max_update_delay = 0.03 )

    # create the untransformed bitmap
    RevenueDataVisualizer( getFullPath('revenue_data.txt'), getFullPath('world_map_simple.gif'), canvas, 0.03 )
    canvas.zoomToExtents()
    canvas.camera.zoom *= ( 0.8, 0.8 )

       
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
