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

    def Clear(self):
        self.dc.Clear()

# some double buffer info: http://wiki.wxpython.org/index.cgi/DoubleBufferedDrawing
# also see wxAutoBufferedPaintDC (not mentioned in the wiki)
class NativeDoubleBuffer(DoubleBuffer):
    def _recreate(self):
        w, h = self.window.GetClientSizeTuple()
        self._doubleBufferBitmap = wx.EmptyBitmap(w, h)
        self.dc = wx.BufferedDC( self.client_dc, self._doubleBufferBitmap, wx.BUFFER_VIRTUAL_AREA  )

        
class MemoryDoubleBuffer(DoubleBuffer):
    def __init__(self, window):
        self.dc = self.memory_dc = wx.MemoryDC()
        DoubleBuffer.__init__( self, window )

    def _recreate(self):
        w, h = self.size = self.window.GetClientSizeTuple()
        self._doubleBufferBitmap = wx.EmptyBitmap(w, h)
        self.dc.SelectObject(self._doubleBufferBitmap)
        
    def Present(self):
        self.client_dc.Blit(0, 0, self.size[0], self.size[1], self.memory_dc, 0, 0)        
