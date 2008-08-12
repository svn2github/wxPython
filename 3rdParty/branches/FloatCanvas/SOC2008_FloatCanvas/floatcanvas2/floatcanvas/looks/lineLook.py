from rendererSpecificLook import RendererSpecificLook

class LineLook(RendererSpecificLook):
    class RendererSpecificLineLook(object):
        def __init__(self, renderer, line_colour, width = 1, style = 'solid', cap = 'round', join = 'round', dashes = None, stipple = None ):
            self.renderer = renderer
            self.pen = renderer.CreatePen(line_colour, width, style, cap, join, dashes, stipple)

        def Apply(self):
            self.pen.Activate()
            
    def __init__(self, line_colour, width = 1, style = 'solid', cap = 'round', join = 'round', dashes = None, stipple = None):
        RendererSpecificLook.__init__(self)
        self.line_colour = line_colour
        self.width = width
        self.style = style
        self.cap = cap
        self.join = join
        self.dashes = dashes
        self.stipple = stipple

    def createLook(self, renderer):
        return self.RendererSpecificLineLook( renderer, self.line_colour, self.width, self.style, self.cap, self.join, self.dashes, self.stipple )
