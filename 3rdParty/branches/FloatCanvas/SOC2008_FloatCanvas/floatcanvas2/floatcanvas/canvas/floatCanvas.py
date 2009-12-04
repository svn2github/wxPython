from simpleCanvas import SimpleCanvas
from ..renderers import GCRenderer
from ..nodes.camera import Viewport
from ..patterns.partial import partial
from ..math import numpy
import wx

class FloatCanvas(SimpleCanvas):
    ''' A subclass SimpleCanvas which pulls in all the wx-specific parts like
         a gcrenderer, window, binding to wx events etc.
    '''
    def __init__(self, window, double_buffered = True, max_update_delay = 0.05, *args, **keys ):
        renderer = GCRenderer( window = window, double_buffered = double_buffered )
        SimpleCanvas.__init__( self, renderer, max_update_delay, *args, **keys )

        self.window = window
        self.window.Bind( wx.EVT_PAINT, self.OnPaint )
        self.window.Bind( wx.EVT_SIZE, self.OnSize )
        self.window.Bind( wx.EVT_WINDOW_DESTROY, lambda evt: self.destroy() )
        self.window.SendSizeEvent()

        self._registerEvents()

    def OnPaint(self, evt):
        ''' redraw ourselves '''
        #print "In canvas OnPaint"
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
        oldSize = self.renderer.screen_size
        self.renderer.screen_size = self.window.GetClientSizeTuple()
        self.camera.viewport.size = self.screen_size
        self.dirty = True
        self.sendEvent( 'onSize', SizeEvent(oldSize, self.screen_size) )
        evt.Skip()

    def Bind(self, *args, **keys):
        ''' delegate to our window '''
        return self.window.Bind(*args, **keys)
    
    def Unbind(self, *args, **keys):
        ''' delegate to our window '''
        return self.wi

    # -- input events
    evt_names = [ '%s_%s' % (btn_name, btn_kind) for btn_name in [ 'left', 'middle', 'right' ] for btn_kind in [ 'down', 'up', 'dclick' ] ]
    evt_names += [ 'move', 'wheel', 'key_down', 'key_up' ]

    fc_to_wx_events = { 'move'     : 'MOTION',
                        'wheel'    : 'MOUSEWHEEL',
                      }
    
    def _registerEvents(self):
        ''' Register to all wx events we're interested in '''
        for fc_evt_name in self.evt_names:
            wx_evt_name = self.fc_to_wx_events.get( fc_evt_name, fc_evt_name )
            wx_evt = getattr( wx, 'EVT_%s' % (wx_evt_name.upper(),) )
            self.window.Bind( wx_evt, partial( self.OnEvent, fc_evt_name ) )

    def _unregisterEvents(self):        
        ''' Unregister all the events we registered to '''
        for fc_evt_name in self.evt_names:
            wx_evt_name = self.fc_to_wx_events.get( fc_evt_name, fc_evt_name )
            wx_evt = getattr( wx, 'EVT_%s' % (wx_evt_name.upper(),) )
            self.window.Unbind( wx_evt )

    def OnEvent(self, fc_evt_name, wx_event):
        ''' If any wx event occurs, this one is called. It does some boilerplate
            work like enriching the event with world coordinates and then
            tries to get a handler for it and calls it if present.
        '''

        screen_pnt = wx_event.GetPosition()
        world_pnt = self.pointToWorld( screen_pnt )
        
        nodes = self.hitTest(screen_pnt, True)
        nodes.reverse()
        if not nodes:
            nodes = ( self, )
        node = nodes[0]
        localCoord = node.transform.inverse( [world_pnt] )[0]

        # send the global event
        self.sendEvent( 'raw_input.%s' % fc_evt_name, InputEvent( fc_evt_name, wx_event, nodes, node, world_pnt, screen_pnt, localCoord ) )
       
        wx_event.Skip()


class SizeEvent(object):
    def __init__( self, oldSize, newSize ):
        self.oldSize = numpy.asarray( oldSize, 'float' )
        self.newSize = numpy.asarray( newSize, 'float' )

class InputEvent(object):
    class Coords(object):
        def __init__(self, world, screen, local):
            self.world = world
            self.screen = screen
            self.local = local

    def __init__(self, type, wx_event, nodes, node, worldCoord, screenCoord, localCoord):
        self.type = type
        self.wx_event = wx_event
        self.nodes = nodes
        self.node = node
        self.coords = self.Coords(worldCoord, screenCoord, localCoord)

    def __getattr__(self, name):
        ''' try to return the attribute of the wx event if it couldn't be found in ourselves '''
        try:
            return getattr( self.wx_event, name )
        except AttributeError:
            return object.__getattr__(self, name )
