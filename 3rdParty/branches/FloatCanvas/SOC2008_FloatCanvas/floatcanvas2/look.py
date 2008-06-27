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
        def __init__(self, renderer, line_colour, fill_colour):
            self.pen = renderer.CreatePen(line_colour)
            self.brush = renderer.CreateBrush(fill_colour)

        def Apply(self):
            self.pen.Activate()
            self.brush.Activate()
            
    def __init__(self, line_colour, fill_colour):
        self.line_colour = line_colour
        self.fill_colour = fill_colour

        self.look_cacher = entries
        
    def Apply(self, renderer):
        try:
            renderer_specific_look = self.look_cacher.get( renderer )
        except KeyError:
            renderer_specific_look = self.RendererSpecificLook( renderer )
            self.look_cacher.add( self.RendererSpecificLook )

        renderer_specific_look.Apply()
        
