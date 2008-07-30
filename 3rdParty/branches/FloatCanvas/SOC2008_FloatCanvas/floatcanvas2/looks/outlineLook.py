from rendererSpecificLook import RendererSpecificLook

class OutlineLook(RendererSpecificLook):
    class RendererSpecificOutlineLook(object):
        def __init__(self, renderer, line_colour):
            self.pen = renderer.CreatePen(line_colour)

        def Apply(self):
            self.pen.Activate()
            
    def __init__(self, line_colour):
        RendererSpecificLook.__init__(self)
        self.line_colour = line_colour

    def createLook(self, renderer):
        return self.RendererSpecificOutlineLook( renderer, self.line_colour )
