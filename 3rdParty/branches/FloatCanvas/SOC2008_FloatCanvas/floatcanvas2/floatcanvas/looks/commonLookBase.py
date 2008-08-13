class CommonLookBase(object):
    ''' Base for common look. Holds all three possible sub-looks (fill, line,
        font) plus the fill_mode trait which determines how polygons get
        rendered (either 'fill' only, 'line' only or 'fill_and_line').
    '''
    def __init__( self, fill_look = None, line_look = None, font_look = None, fill_mode = 'fill_and_line' ):
        self.fill_look = fill_look
        self.line_look = line_look
        self.font_look = font_look
        self.fill_mode = fill_mode
        
    def Apply(self, renderer):
        ''' Makes this look take effect.
            Todo: make fill_mode a property of the renderer.Draw*() methods, not
                  a global one.
        '''
        renderer.fill_mode = self.fill_mode
        
        if self.fill_look:
            self.fill_look.Apply(renderer)
        if self.line_look:
            self.line_look.Apply(renderer)
        if self.font_look:
            self.font_look.Apply(renderer)
