import wx

class SingleBuffer(object):
    def __init__(self, window):
        self.window = window
        self.client_dc = self.dc = wx.ClientDC( self.window )
    
    def Present(self):
        pass

    def Clear(self):
        self.dc.Clear()


class DoubleBuffer(object):
    def __init__(self, window):
        self.window = window
        self.window.Bind( wx.EVT_SIZE, self.OnSize )
        self.client_dc = wx.ClientDC( self.window )
        self._recreate()
    
    def OnSize(self, event):
        self._recreate()
        event.Skip()
        
    def _recreate(self):
        raise NotImplementedError()
    
    def Present(self):
        pass


# some double buffer info: http://wiki.wxpython.org/index.cgi/DoubleBufferedDrawing
# also see wxAutoBufferedPaintDC (not mentioned in the wiki)
class NativeDoubleBuffer(DoubleBuffer):
    def _recreate(self):
        w, h = self.window.GetClientSizeTuple()
        self._doubleBufferBitmap = wx.EmptyBitmap(w, h)
        self.dc = wx.BufferedDC( self.client_dc, self._doubleBufferBitmap, wx.BUFFER_VIRTUAL_AREA  )

    def Clear(self):
        self.dc.Clear()
        
        
class MemoryDoubleBuffer(DoubleBuffer):
    def __init__(self, window, render_surface):
        self.render_surface = render_surface
        self.render_surface.Activate()
        DoubleBuffer.__init__( self, window )

    def _recreate(self):
        self.render_surface.size = self.window.GetClientSizeTuple()
        
    def Clear(self, background_color):
        self.render_surface.Clear( background_color )

    def Present(self):
        assert self.render_surface.active
        self.client_dc.Blit(0, 0, self.render_surface.size[0], self.render_surface.size[1], self.render_surface.dc, 0, 0)
        
           
    def _setSize(self, size):
        self.render_surface.size = size
        
    def _getSize(self):
        return self.render_surface.size
        
    size = property( _getSize, _setSize )
    