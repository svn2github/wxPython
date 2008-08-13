''' Different kinds of framebuffers '''

import wx

class SingleBuffer(object):
    ''' Single buffering, render directy to screen '''
    def __init__(self, window):
        self.window = window
        self.client_dc = self.dc = wx.ClientDC( self.window )
    
    def Present(self):
        pass

    def Clear(self):
        self.dc.Clear()
    
    def _setSize(self, size):
        self.window.SetClientSize( size )
        
    def _getSize(self):
        return self.window.GetClientSizeTuple()
        
    size = property( _getSize, _setSize )

class DoubleBuffer(object):
    ''' Double buffering base class, provides a client_dc to draw to screen '''
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

    def _setSize(self, size):
        self.window.SetClientSize( size )
        
    def _getSize(self):
        return self.window.GetClientSizeTuple()
        
    size = property( _getSize, _setSize )

# some double buffer info: http://wiki.wxpython.org/index.cgi/DoubleBufferedDrawing
# also see wxAutoBufferedPaintDC (not mentioned in the wiki)
class NativeDoubleBuffer(DoubleBuffer):
    ''' A buffer using the native double buffering of the platform '''
    def _recreate(self):
        w, h = self.window.GetClientSizeTuple()
        self._doubleBufferBitmap = wx.EmptyBitmap(w, h)
        self.dc = wx.BufferedDC( self.client_dc, self._doubleBufferBitmap, wx.BUFFER_VIRTUAL_AREA  )

    def Clear(self):
        self.dc.Clear()
        
        
class MemoryDoubleBuffer(DoubleBuffer):
    ''' A double buffer which has an offscreen surface (bitmap) which is
        rendered to. After drawing the surface is blitted to the screen all at
        once to reduce flickering as much as possible.
    '''
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
    