import wx
from constantTable import ConstantTable

class GCPath(object):
    # implements(IPath)
    
    def __init__(self, renderer):
        self.renderer = renderer
        self.GC = GC = renderer.GC
        self.path = GC.CreatePath()

    def Draw(self, fillStyle = 'oddeven'):
        return self.GC.DrawPath(self.path, ConstantTable.get(fillStyle) )
    
    def Fill(self, fillStyle = 'oddeven'):
        return self.GC.DrawPath(self.path, ConstantTable.get(fillStyle) )    

    def Stroke(self):
        return self.GC.StrokePath(self.path)

    # maps all the other functions
    def __getattr__(self, name):
        return getattr(self.path, name)


class GCFont(object):
    def __init__(self, renderer, size, family, style, weight, underlined, faceName, colour):
        self.renderer = renderer
        self.GC = GC = renderer.GC
        family = ConstantTable.getEnum( 'fontfamily', family)
        style = ConstantTable.getEnum( 'fontstyle', style)
        weight = ConstantTable.getEnum( 'fontweight', weight)
        font = wx.Font( size, family, style, weight, underlined, faceName )
        self.font = GC.CreateFont( font, colour )

    def Activate(self):
        if self.renderer.active_font == self:
            return
        self.renderer.active_font = self
        self.GC.SetFont(self.font)


class GCBrush(object):
    def __init__(self, renderer, kind, *args, **keys):
        self.renderer = renderer
        self.GC = GC = renderer.GC
        self.kind = kind
        if kind == 'plain':
            brush = GC.CreateBrush( wx.Brush( *args, **keys ) )
        elif kind == 'linearGradient':
            brush = GC.CreateLinearGradientBrush( *args, **keys )
        elif kind == 'radialGradient':
            brush = GC.CreateRadialGradientBrush( *args, **keys )
        elif kind is None:
            brush = GC.CreateBrush( wx.NullBrush )
        else:
            raise ValueError('Wrong kind for brush %s' % kind)

        self.brush = brush

    def Activate(self):
        if self.renderer.active_brush == self:
            return
        self.renderer.active_brush = self
        self.GC.SetBrush(self.brush)

class GCPen(object):
    def __init__(self, renderer, colour, **keys):
        # keys: width = 1, style = 'solid', stipple_bmp = None, cap = 'round', dashes = None, join = 'round', pen = None        

        self.renderer = renderer
        self.GC = GC = renderer.GC
        
        if 'pen' in keys:
            pen = keys['pen']
            del keys['pen']
        else:
            pen = wx.Pen(colour)
            
        for name, value in keys.iteritems():
            getattr( pen, 'Set%s' % (name.capitalize(),))( value )

        self.pen = GC.CreatePen( pen )

    def Activate(self):
        if self.renderer.active_pen == self:
            return
        self.renderer.active_pen = self
        self.GC.SetPen(self.pen)
                

class GCBitmap(object):
    # implements (IBitmap)

    def __init__(self, renderer, bmp):
        self.renderer = renderer
        self.GC = renderer.GC
        #self.bitmap = renderer.CreateBitmap()
        self.bmp = bmp

    def Draw(self, x, y, w, h):
        self.GC.DrawBitmap(self.bmp, x, y, w, h)
