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
    #from wx.lib.floatcanvas.floatcanvas2.floatcanvas.canvas.renderPolicies import DefaultRenderPolicy
    #canvas = fc.NavCanvas( frame, backgroundColor = 'white', renderPolicy = DefaultRenderPolicy() )
    canvas = fc.NavCanvas( frame, backgroundColor = 'white' )
    
    f = file('lion.svg', 'r')
    importer = SimpleSVGImporter( f.read(), canvas )
    canvas.zoomToExtents()
    

# not a good example how to write a parser, but I don't want this to grow into
# a project of its own for now
import xml.parsers.expat

class SimpleSVGImporter(object):
    def __init__(self, content, canvas):
        self.content = content
        self.canvas = canvas
        
        p = xml.parsers.expat.ParserCreate()
        
        p.StartElementHandler = self.start_element
        p.EndElementHandler = self.end_element
        p.CharacterDataHandler = self.char_data
        
        self.elements = []
        self.fc_nodes = []
        p.Parse( content, 1 )

    def start_element(self, name, attrs):
        #print 'Start element:', name, attrs
        self.elements.append( [name, attrs] )

        handler = getattr(self, 'handle_%s' % name)
        handler( *(attrs, None) )

    def end_element(self, name):
        #print 'End element:', name
        pass

    def char_data(self, data):
        pass
        #print 'Character data:', repr(data)
        
       
    def handle_svg(self, attrs, data):
        pass
    
    def handle_g(self, attrs, data):
        node = self.canvas.createCircle( 0, look = self.parseLook( attrs ), where = 'front' )
        self.fc_nodes.append( node )

    def parseLook(self, attrs):
        props = { 'line_colour' : None, 'fill_colour' : None }

        try:                
            style = attrs['style']
        except KeyError:
            pass
        else:            
            style_parts = style.split(';')
            
            for part in style_parts:
                if not part:
                    continue
                name, value = part.split( ':' )
                name = name.strip()
                value = value.strip()
                if name == 'fill':
                    props[ 'line_colour' ] = self.parseColour( value )
                elif name == 'fill-opacity':
                    pass
                elif name == 'stroke':
                    props[ 'fill_colour' ] = self.parseColour( value )
                elif name == 'stroke-width':
                    props[ 'line_width' ] = float(value)
                    print props['line_width']
                else:
                    raise Exception( 'Unknown style property %s : %s' % ( name, value ) )
    
        try:                
            fill = attrs['fill']
        except KeyError:
            pass
        else:
            props[ 'fill_colour' ] = self.parseColour( fill )

        if (props['line_colour'] is None) and (props['fill_colour'] is None):
            return fc.NoLook
        if (props['line_colour'] is not None) and (props['fill_colour'] is not None):
            return fc.SolidColourLook( **props )
        
        if props[ 'fill_colour' ] is not None:
            return fc.SolidColourFillLook( props['fill_colour'] )
        if props[ 'line_colour' ] is not None:
            return fc.OutlineLook( props['line_colour'], props['line_width'] )
        
        raise Exception('internal error')
        
    def parseColour(self, string):
        if string[0] == '#':
            string = string[1:]
            return ( int( string[0:2], 16 ), int( string[2:4], 16 ), int( string[4:6], 16 ), 255 )
        elif string.lower().startswith( 'rgb(' ):
            stripped = string.replace('rgb(', '').replace(')', '')
            return tuple( c for c in stripped.split( ',' ) )
        elif string.lower().strip() == 'none':
            return None
            
        raise Exception('Colour is neither hex nor rgb %s' % string)

    def handle_path(self, attrs, data):
        parent = self.fc_nodes[-1]
        
    def handle_polygon(self, attrs, data):
        parent = self.fc_nodes[-1]
        points = []
        for p in attrs['points'].strip().split(' '):
            x, y = p.strip().split(',')
            points.append( (float(x), float(y)) )
        self.canvas.createPolygon( points, parent = parent, look = self.parseLook( attrs ), where = 'front' )

    
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
