from simpleCanvas import SimpleCanvas
from ..renderers import GCRenderer
from ..nodes.camera import Viewport
import wx

class FloatCanvas(SimpleCanvas):
    ''' A subclass SimpleCanvas which pulls in all the wx-specific parts like
         a gcrenderer, window, binding to wx events etc.
    '''
    def __init__(self, window, double_buffered = True, max_update_delay = 0.05, *args, **keys ):
        renderer = GCRenderer( window = window, double_buffered = double_buffered )
        SimpleCanvas.__init__( self, renderer, max_update_delay, *args, **keys )

        self.window = window
        self.renderer.framebuffer.size = self.window.GetClientSizeTuple()
        self.camera.viewport = Viewport( self.screen_size )
        self.window.Bind( wx.EVT_PAINT, self.OnPaint )
        self.window.Bind( wx.EVT_SIZE, self.OnSize )
        self.window.Bind( wx.EVT_WINDOW_DESTROY, lambda evt: self.destroy() )

    def OnPaint(self, evt):
        ''' redraw ourselves '''
        print "In canvas OnPaint"
        self.dirty = True
        if wx.Platform == '__WXMSW__':
            # Skip() must be called, or Windows doesn't think the window has been painted
            #    resulting in endless recusive paint events. Hoever, if you call Skip() on OS-X,
            #    nothing gets rendered. I"m not sure aobut GTK at this point. 
            #    another option is to create a wx.PaintDC and don't use it, but I figured:
            #    why waste the time on platforms that don't need it?
            evt.Skip()

    def OnSize(self, evt):
        ''' redraw ourselves '''
        self.renderer.screen_size = self.window.GetClientSizeTuple()
        self.dirty = True
        evt.Skip()
        
    def Bind(self, *args, **keys):
        ''' delegate to our window '''
        return self.window.Bind(*args, **keys)
    
    def Unbind(self, *args, **keys):
        ''' delegate to our window '''
        return self.window.Unbind( *args, **keys )