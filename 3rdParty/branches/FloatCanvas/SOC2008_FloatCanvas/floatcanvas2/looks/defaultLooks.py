from compositeLook import CompositeLook
from outlineLook import OutlineLook
from fillLooks import SolidColourFillLook, RadialGradientFillLook, LinearGradientFillLook
from fontLook import FontLook

class SolidColourLook(CompositeLook):
    def __init__(self, line_colour, fill_colour):
        looks = [ OutlineLook( line_colour ), SolidColourFillLook( fill_colour ) ]
        CompositeLook.__init__( self, looks )       

class RadialGradientLook(CompositeLook):
    def __init__(self, line_colour, origin, colour_origin, center_circle_end, radius, colour_end):
        looks = [ OutlineLook( line_colour ), RadialGradientFillLook( origin, colour_origin, center_circle_end, radius, colour_end ) ]
        CompositeLook.__init__( self, looks )       
        
class LinearGradientLook(CompositeLook):
    def __init__(self, line_colour, origin, colour_origin, end, colour_end):
        looks = [ OutlineLook( line_colour ), LinearGradientFillLook( origin, colour_origin, end, colour_end ) ]
        CompositeLook.__init__( self, looks )       

class TextLook(CompositeLook):
    def __init__(self, size, family = 'default', style = 'normal', weight = 'normal', underlined = False, faceName = '', colour = 'black', background_fill_look = None):
        looks = [ FontLook( size, family, style, weight, underlined, faceName, colour ), background_fill_look ]
        CompositeLook.__init__( self, looks )     
