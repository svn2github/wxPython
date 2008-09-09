class IRenderer(object):
    # line functions
    def DrawLines(self, points, fillStyle = 'oddeven'):
        pass
    
    def StrokeLine(self, x1, y1, x2, y2):
        pass

    def StrokeLines(self, points):
        pass

    # other primitive functions
    def DrawEllipse(self, x, y, w, h):
        pass   

    def DrawRectangle(self, x, y, w, h):
        pass
    
    def DrawRoundedRectangle(self, x, y, w, h, radius):
        pass
   
    def DrawIcon(self, icon, x, y, w, h):
        pass
    
    # text functions
    def DrawText(self, text, x, y):
        pass
        
    def DrawRotatedText(self, text, x, y, angle):
        pass

    def GetPartialTextExtents(self, text):
        pass

    def GetTextExtent(self, text):
        pass

    # factory functions
    def CreatePath(self):
        pass

    def CreateBitmap(self, bmp):
        pass

    def CreatePen(self, colour, width = 1, style = 'solid', stipple_bmp = None, cap = 'round', dashes = None, join = 'round', pen = None):
        pass

    # kind = 'plain', 'linearGradient', 'radialGradient'
    def CreateBrush(self, kind, *args):
        pass

    def CreateFont(self, font, colour = 'black'):
        pass


class IPath(object):
    # path functions
    def Draw(self, fillStyle = 'oddeven'):
        pass    
    
    def Fill(self, fillStyle = 'oddeven'):
        pass

    def Stroke(self):
        pass


class IBitmap(object):
    #bmp = property
    
    def Draw(self, x, y, w, h):
        pass
