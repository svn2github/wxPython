''' This module defines a bunch of commonly used looks '''

from lineLook import LineLook
from fillLooks import SolidColourFillLook, RadialGradientFillLook, LinearGradientFillLook
from fontLook import FontLook
from commonLookBase import CommonLookBase

class SolidColourLook(CommonLookBase):
    ''' Combines a line sub look and a solid colour fill sub look '''
    def __init__(self, line_colour, fill_colour, line_width = 1, line_style = 'solid', line_cap = 'round', line_join = 'round', line_dashes = None, line_stipple = None):
        if line_colour is not None:
            fill_mode = 'fill_and_line'
        else:
            fill_mode = 'fill'            
        
        if fill_colour is None:
            fill_mode = 'line'

        CommonLookBase.__init__( self, fill_look = SolidColourFillLook( fill_colour ), line_look = LineLook( line_colour, line_width, line_style, line_cap, line_join, line_dashes, line_stipple ), fill_mode = fill_mode )


class RadialGradientLook(CommonLookBase):
    ''' Combines a line sub look and a radial gradient fill sub look '''
    def __init__(self, line_colour, origin, colour_origin, center_circle_end, radius, colour_end, line_width = 1, line_style = 'solid', line_cap = 'round', line_join = 'round', line_dashes = None, line_stipple = None):
        if line_colour is not None:
            fill_mode = 'fill_and_line'
        else:
            fill_mode = 'fill'            
        CommonLookBase.__init__( self, fill_look = RadialGradientFillLook( origin, colour_origin, center_circle_end, radius, colour_end ), line_look = LineLook( line_colour, line_width, line_style, line_cap, line_join, line_dashes, line_stipple ), fill_mode = fill_mode )
        
        
class LinearGradientLook(CommonLookBase):
    ''' Combines a line sub look and a linear gradient fill sub look '''
    def __init__(self, line_colour, origin, colour_origin, end, colour_end, line_width = 1, line_style = 'solid', line_cap = 'round', line_join = 'round', line_dashes = None, line_stipple = None):
        if line_colour is not None:
            fill_mode = 'fill_and_line'
        else:
            fill_mode = 'fill'            
        CommonLookBase.__init__( self, fill_look = LinearGradientFillLook( origin, colour_origin, end, colour_end ), line_look = LineLook( line_colour,  line_width, line_style, line_cap, line_join, line_dashes, line_stipple ), fill_mode = fill_mode )


class TextLook(CommonLookBase):
    ''' Defines a text sub look '''
    def __init__(self, size, family = 'default', style = 'normal', weight = 'normal', underlined = False, faceName = '', colour = 'black', background_fill_look = None):
        CommonLookBase.__init__( self, fill_look = background_fill_look, font_look = FontLook( size, family, style, weight, underlined, faceName, colour ), fill_mode = 'fill_and_line' )


class OutlineLook(CommonLookBase):
    ''' Defines a line-only sub look '''
    def __init__(self, line_colour, width = 1, style = 'solid', cap = 'round', join = 'round', dashes = None, stipple = None):
        CommonLookBase.__init__( self, line_look = LineLook( line_colour, width, style, cap, join, dashes, stipple ), fill_mode = 'line' )


class DefaultLook(CommonLookBase):
    pass