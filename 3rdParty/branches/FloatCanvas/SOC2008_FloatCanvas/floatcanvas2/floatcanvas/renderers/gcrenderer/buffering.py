''' Different kinds of framebuffers '''

import wx

class SingleBuffer(object):
    ''' Single buffering, render directy to screen '''
    def __init__(self, window):
        self.window = window
    
    def BeginRendering(self):
        self.client_dc = self.dc = wx.ClientDC( self.window )
        self.gc = wx.GraphicsRenderer.GetDefaultRenderer().CreateContext( self.client_dc )

    def EndRendering(self):
        del self.gc
        del self.client_dc
        del self.dc
                
    def Present(self):
        self.window.Update()
    
    def Clear(self, background_color):
        self.dc.SetBackground( wx.Brush(background_color) )
        self.dc.Clear()
    
    def _setSize(self, size):
        self.window.SetClientSize( size )
        
    def _getSize(self):
        return self.window.GetClientSizeTuple()
        
    size = property( _getSize, _setSize )

#class DoubleBuffer(object):
#    ''' Double buffering base class, provides a client_dc to draw to screen '''
#    def __init__(self, window):
#        self.window = window
#        self.window.Bind( wx.EVT_SIZE, self.OnSize )
#        self._recreate()
#    
#    def OnSize(self, event):
#        self._recreate()
#        event.Skip()
#        
#    def _recreate(self):
#        raise NotImplementedError()
#    
#    def BeginRendering(self):
#        self.client_dc = self.dc = wx.ClientDC( self.window )
#        self.gc = wx.GraphicsRenderer.GetDefaultRenderer().CreateContext( self.client_dc )
#
#    def EndRendering(self):
#        del self.gc
#        del self.client_dc
#        del self.dc
#
#    def Present(self):
#        self.window.Update()
#
#    def _setSize(self, size):
#        self.window.SetClientSize( size )
#        
#    def _getSize(self):
#        return self.window.GetClientSizeTuple()
#        
#    size = property( _getSize, _setSize )

# some double buffer info: http://wiki.wxpython.org/index.cgi/DoubleBufferedDrawing
# also see wxAutoBufferedPaintDC (not mentioned in the wiki)
#class NativeDoubleBuffer(DoubleBuffer):
#    ''' A buffer using the native double buffering of the platform '''
#    def _recreate(self):
#        w, h = self.window.GetClientSizeTuple()
#        self._doubleBufferBitmap = wx.EmptyBitmap(w, h)
#        self.dc = wx.BufferedDC( self.client_dc, self._doubleBufferBitmap, wx.BUFFER_VIRTUAL_AREA  )
#
#    def Clear(self):
#        self.dc.Clear()
#        
        
class MemoryDoubleBuffer(object):
    ''' A double buffer which has an offscreen surface (bitmap) which is
        rendered to. After drawing the surface is blitted to the screen all at
        once to reduce flickering as much as possible.
    '''
    def __init__(self, window, render_surface):
        self.window = window
        self.render_surface = render_surface
        self.render_surface.Activate()

        self.window.Bind( wx.EVT_SIZE, self.OnSize )
        self._recreate()
    
    def OnSize(self, event):
        self._recreate()
        event.Skip()

    def _recreate(self):
        self.render_surface.size = self.window.GetClientSizeTuple()
        
    def Clear(self, background_color):
        self.render_surface.Clear( background_color )

    def BeginRendering(self):
        self.render_surface.BeginRendering()

    def EndRendering(self):
        self.render_surface.EndRendering()

    def Present(self):
        print "in MemoryDoubleBuffer.Present",
        assert self.render_surface.active
        client_dc = wx.ClientDC( self.window )
        
        try:
            self.count += 1
        except AttributeError:
            self.count = 0
        print "render called for the %ith time"%self.count
        #print 'saving the bitmap to : "Junk%i.png"'%self.count
        #self.render_surface.bitmap.SaveFile("Junk%i.png"%self.count, wx.BITMAP_TYPE_PNG)
        
        #print "Drawing the bitmap to the ClientDC"
        #client_dc.Blit(0, 0, self.render_surface.size[0], self.render_surface.size[1], self.render_surface.dc, 0, 0)
        client_dc.DrawBitmap(self.render_surface.bitmap, 0, 0, True)
        #del client_dc
        #print "calling Refresh and Update"
        #self.window.Refresh(False)
        #self.window.Update()
           
    def _setSize(self, size):
        self.render_surface.size = size
        
    def _getSize(self):
        return self.render_surface.size
        
    size = property( _getSize, _setSize )
    