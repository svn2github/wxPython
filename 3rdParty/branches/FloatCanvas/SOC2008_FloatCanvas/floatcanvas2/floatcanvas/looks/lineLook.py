from rendererSpecificLook import RendererSpecificLook

class LineLook(RendererSpecificLook):
    ''' The sub-look controlling the rendering of the outline of an object '''
    class RendererSpecificLineLook(object):
        def __init__(self, renderer, line_colour, width = 1, style = 'solid', cap = 'round', join = 'round', dashes = None, stipple = None ):
            self.renderer = renderer
            self.pen = renderer.CreatePen(line_colour, width, style, cap, join, dashes, stipple)

        def Apply(self):
            self.pen.Activate()
            
    def __init__(self, line_colour, width = 1, style = 'solid', cap = 'round', join = 'round', dashes = None, stipple = None):
        # Call SetCap if you need to specify how the ends of thick lines should
        # look: round (the default) specifies rounded ends,
        #       projecting specifies a square projection on either end
        #       butt specifies that the ends should be square and should
        #         not project.
        # join styles: round, bevel and miter

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
