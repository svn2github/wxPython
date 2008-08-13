from rendererSpecificLook import RendererSpecificLook

class FillLook(RendererSpecificLook):
    ''' Baseclass of a sub-look specifying how to fill an object '''
    class RendererSpecificFillLook(object):
        def __init__(self, renderer, fill_kind, *args):
            self.brush = renderer.CreateBrush(fill_kind, *args)

        def Apply(self):
            self.brush.Activate()
            
    def __init__(self, fill_kind, *args):
        RendererSpecificLook.__init__(self)
        self.fill_kind = fill_kind
        self.args = args

    def createLook(self, renderer):
        return self.RendererSpecificFillLook( renderer, self.fill_kind, *self.args )


class SolidColourFillLook(FillLook):
    ''' Fill an object with a solid/flat colour '''
    def __init__(self, colour):
        FillLook.__init__( self, 'plain', colour )


class RadialGradientFillLook(FillLook):
    ''' Fill an object with a radial gradient '''
    def __init__(self, origin, colour_origin, center_circle_end, radius, colour_end):
        FillLook.__init__( self, 'radialGradient', origin[0], origin[1], center_circle_end[0], center_circle_end[1], radius, colour_origin, colour_end )


class LinearGradientFillLook(FillLook):
    ''' Fill an object with a linear gradient '''
    def __init__(self, origin, colour_origin, end, colour_end):
        FillLook.__init__( self, 'linearGradient', origin[0], origin[1], end[0], end[1], colour_origin, colour_end )
