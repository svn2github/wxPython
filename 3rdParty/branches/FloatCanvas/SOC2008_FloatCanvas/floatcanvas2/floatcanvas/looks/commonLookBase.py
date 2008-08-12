class CommonLookBase(object):
    def __init__( self, fill_look = None, line_look = None, font_look = None, fill_mode = 'fill_and_line' ):
        self.fill_look = fill_look
        self.line_look = line_look
        self.font_look = font_look
        self.fill_mode = fill_mode
        
    def Apply(self, renderer):
        renderer.fill_mode = self.fill_mode
        
        if self.fill_look:
            self.fill_look.Apply(renderer)
        if self.line_look:
            self.line_look.Apply(renderer)
        if self.font_look:
            self.font_look.Apply(renderer)
