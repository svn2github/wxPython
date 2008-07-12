class Look(object):
    pass

class Cacher(object):
    def __init__(self):
        self.entries = {}

    def add(self, key, value):
        self.entries[key] = value

    def get(self, key):
        return self.entries[key]
    
    
class DefaultLook(Look):
    class RendererSpecificLook(object):
        def __init__(self, renderer, line_colour, fill_kind, *args):
            self.pen = renderer.CreatePen(line_colour)
            self.brush = renderer.CreateBrush(fill_kind, *args)

        def Apply(self):
            self.pen.Activate()
            self.brush.Activate()
            
    def __init__(self, line_colour, fill_kind, *args):
        self.line_colour = line_colour
        self.fill_kind = fill_kind
        self.args = args

        self.look_cacher = Cacher()
        
    def Apply(self, renderer):
        try:
            renderer_specific_look = self.look_cacher.get( renderer )
        except KeyError:
            renderer_specific_look = self.RendererSpecificLook( renderer, self.line_colour, self.fill_kind, *self.args )
            self.look_cacher.add( renderer, renderer_specific_look )

        renderer_specific_look.Apply()
        

class SolidColourLook(DefaultLook):
    def __init__(self, line_colour, fill_colour):
        DefaultLook.__init__( self, line_colour, 'plain', fill_colour )

class OutlineLook(DefaultLook):
    def __init__(self, line_colour):
        DefaultLook.__init__( self, line_colour, None )

class RadialGradientLook(DefaultLook):
    def __init__(self, line_colour, origin, colour_origin, center_circle_end, radius, colour_end):
        DefaultLook.__init__( self, line_colour, 'radialGradient', origin[0], origin[1], center_circle_end[0], center_circle_end[1], radius, colour_origin, colour_end )

class LinearGradientLook(DefaultLook):
    def __init__(self, line_colour, origin, colour_origin, end, colour_end):
        DefaultLook.__init__( self, line_colour, 'linearGradient', origin[0], origin[1], end[0], end[1], colour_origin, colour_end )


class NoLook(Look):    
    def Apply(renderer):
        pass
    Apply = staticmethod(Apply)