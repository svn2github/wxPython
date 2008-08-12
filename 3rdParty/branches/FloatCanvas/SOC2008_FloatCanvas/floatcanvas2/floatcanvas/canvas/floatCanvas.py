from simpleCanvas import SimpleCanvas
from ..renderers import GCRenderer
from ..nodes.camera import Viewport
from ..events.eventSender import EventSender
import wx

class InputEventSender(EventSender):
    pass


class FloatCanvas(SimpleCanvas):
    def __init__(self, window, double_buffered = True, max_update_delay = 0.05, *args, **keys ):
        renderer = GCRenderer( window = window, double_buffered = double_buffered )
        SimpleCanvas.__init__( self, renderer, max_update_delay, *args, **keys )

        self.window = window
        self.renderer.framebuffer.size = self.window.GetClientSizeTuple()
        self.camera.viewport = Viewport( self.screen_size )
        self.window.Bind( wx.EVT_PAINT, self.OnPaint )
        self.window.Bind( wx.EVT_SIZE, self.OnSize )

    def OnPaint(self, evt):
        self.dirty = True
        evt.Skip()

    def OnSize(self, evt):
        self.renderer.screen_size = self.window.GetClientSizeTuple()
        self.dirty = True
        evt.Skip()
        
    def Bind(self, *args, **keys):
        return self.window.Bind(*args, **keys)
    
    def Unbind(self, *args, **keys):
        return self.window.Unbind( *args, **keys )
    
    def create(self, *args, **keys):
        node = super(FloatCanvas, self).create( *args, **keys )
        return node
    
    
#EVT_FC_ENTER_WINDOW = wx.NewEventType()
#EVT_FC_LEAVE_WINDOW = wx.NewEventType()
#EVT_FC_LEFT_DOWN = wx.NewEventType()
#EVT_FC_LEFT_UP  = wx.NewEventType()
#EVT_FC_LEFT_DCLICK = wx.NewEventType()
#EVT_FC_MIDDLE_DOWN = wx.NewEventType()
#EVT_FC_MIDDLE_UP = wx.NewEventType()
#EVT_FC_MIDDLE_DCLICK = wx.NewEventType()
#EVT_FC_RIGHT_DOWN = wx.NewEventType()
#EVT_FC_RIGHT_UP = wx.NewEventType()
#EVT_FC_RIGHT_DCLICK = wx.NewEventType()
#EVT_FC_MOTION = wx.NewEventType()
#EVT_FC_MOUSEWHEEL = wx.NewEventType()
### these two are for the hit-test stuff, I never make them real Events
### fixme: could I use the PyEventBinder for the Object events too?
#EVT_FC_ENTER_OBJECT = wx.NewEventType()
#EVT_FC_LEAVE_OBJECT = wx.NewEventType()