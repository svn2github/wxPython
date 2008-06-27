from renderer import IRenderer, IPath, IBitmap
import wx

class ConstantTable(object):
    stringToWx = { 'oddeven' : wx.ODDEVEN_RULE,
                   'winding' : wx.WINDING_RULE
                 }
    
    def get(cls, string):
        return cls.stringToWx[string]

    get = classmethod(get)


class GCRenderer(object):
    # implements(IRenderer)

    def __init__(self, window = None, dc = None, native_window = None, native_dc = None, wx_renderer = None):
        if window or dc:
            func = 'CreateContext'
        elif native_window:
            func = 'CreateContextFromNativeWindow'
        elif native_dc:
            func = 'CreateContextFromNativeContext'
        else:
            raise ValueError('You have to supply exactly one of the window, dc, native_context or native_dc arguments!')

        if wx_renderer is None:
            renderer = wx.GraphicsRenderer.GetDefaultRenderer()
            
        self.renderer = renderer
        self.GC = getattr(self.renderer, func)( window or dc or native_dinow or native_dc )

    # line functions
    def DrawLines(self, points, fillStyle = 'oddeven'):
        return self.GC.DrawLines(points, ConstantTable.get(fillStyle) )

    # factory functions
    def CreatePath(self):
        return GCPath(self)

    def CreateBitmap(self, bmp):
        return GCBitmap(self, bmp)

    def CreatePen(self, colour, **keys ):
        return GCPen(self, colour, **keys)

    # kind = 'plain', 'linearGradient', 'radialGradient'
    def CreateBrush(self, kind, *args, **keys):
        return GCBrush(self, kind, *args, **keys)

    def CreateFont(self, *args, **keys):
        return GCFont(self, *args, **keys)

    # maps all the other functions
    def __getattr__(self, name):
        return getattr(self.GC, name)


class GCPath(object):
    # implements(IPath)
    
    def __init__(self, renderer):
        self.renderer = renderer
        self.GC = GC = renderer.GC
        self.path = GC.CreatePath()

    def Draw(self, fillStyle = 'oddeven'):
        return self.GC.DrawPath(path, ConstantTable.get(fillStyle) )
    
    def Fill(self, fillStyle = 'oddeven'):
        return self.GC.DrawPath(self.path, ConstantTable.get(fillStyle) )    

    def Stroke(self):
        return self.GC.StrokePath(self.path)

    # maps all the other functions
    def __getattr__(self, name):
        return getattr(self.path, name)


class GCFont(object):
    def __init__(self, renderer, colour, *args, **keys):
        self.renderer = renderer
        self.GC = GC = renderer.GC
        self.font = GC.CreateFont( wx.Font(*args, **keys), colour)

    def Activate(self):
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

        self.brush = brush

    def Activate(self):
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
