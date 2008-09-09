from rendererSpecificLook import RendererSpecificLook

class FontLook(RendererSpecificLook):
    ''' The sub-look controlling the look of a rendered font '''
    class RendererSpecificFontLook(object):
        def __init__(self, renderer, size, family, style, weight, underlined, faceName, colour):
            self.font = renderer.CreateFont( size, family, style, weight, underlined, faceName, colour )

        def Apply(self):
            self.font.Activate()

    def __init__(self, size, family = 'default', style = 'normal', weight = 'normal', underlined = False, faceName = '', colour = 'black'):
        RendererSpecificLook.__init__(self)
        self.size = size
        self.family = family
        self.style = style
        self.weight = weight
        self.underlined = underlined
        self.faceName = faceName
        self.colour = colour
        
    def createLook(self, renderer):
        return self.RendererSpecificFontLook( renderer, self.size, self.family, self.style, self.weight, self.underlined, self.faceName, self.colour )
