'''

Module that holds the GUI modes used by FloatCanvas

This approach was inpired by Christian Blouin, who also wrote the initial
version of the code.

'''

import wx
from ..timeMachine import Resources
from ..patterns.partial import partial
import numpy as N


class Cursors(object):
    '''
         Singleton-like class to hold the standard Cursors    
    '''
    
    def __init__(self):
        ''' Build a list with the default cursors, specialize for mac '''
        self.cursors = { 'default' : wx.NullCursor }
        
        if "wxMac" in wx.PlatformInfo: # use 16X16 cursors for wxMac
            self.addCursor( 'Hand', Resources.getHand16Image() )
            self.addCursor( 'GrabHand', Resources.getGrabHand16Image() )
            self.addCursor( 'MagPlus', Resources.getMagPlus16Image(), (6, 6) )
            self.addCursor( 'MagMinus', Resources.getMagMinus16Image(), (6, 6) )        
        else: # use 24X24 cursors for GTK and Windows
            self.addCursor( 'Hand', Resources.getHandImage() )
            self.addCursor( 'GrabHand', Resources.getGrabHandImage() )
            self.addCursor( 'MagPlus', Resources.getMagPlusImage(), (9, 9) )
            self.addCursor( 'MagMinus', Resources.getMagMinusImage(), (9, 9) )        

            
    def addCursor(self, name, img, hotspot = None):
        ''' Adds a cursor to our inventory '''
        if hotspot is not None:
            img.SetOptionInt( wx.IMAGE_OPTION_CUR_HOTSPOT_X, hotspot[0] )
            img.SetOptionInt( wx.IMAGE_OPTION_CUR_HOTSPOT_Y, hotspot[1] )

        self.cursors[ name ] = cursor = wx.CursorFromImage( img )
        return cursor
        
            
    def get(cls, name):
        ''' Retrieve a cursor from the inventory. If there's no instance present
             yet, create one and use it for future requests. This makes for some
             lazy binding, because we can import this module now without having
             to create wx.App object first.
        '''
        if not hasattr(cls, 'instance'):
            cls.instance = Cursors()
            
        return cls.instance.cursors[ name ]
        
    get = classmethod( get )    


class GUIModeBase(object):
    '''
    Basic mouse mode and baseclass for other GUIModes.

    This one can (un-)register to all events and derived classes are free to
    implement any handlers. The default handler tries to find a method on_x
    where x is the name of the event (e.g. 'left_down') and calls it if present.
    This default behaviour allows derived classes to easily implement event
    handlers.
    '''
  
    active = False

    def Deactivate(self):
        '''
        Deactivate this mode, we're likely to switch to a different mode.
        Unregister events.
        '''
        self._unregisterEvents()
        del self.canvas
        self.active = False
    
    def Activate(self, canvas):
        '''
        Activate this mode, register events.
        '''
        assert not self.active
        self.active = True
        self.canvas = canvas
        self._registerEvents()

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
            self.canvas.Bind( wx_evt, partial( self.OnEvent, fc_evt_name ) )

    def _unregisterEvents(self):        
        ''' Unregister all the events we registered to '''
        for fc_evt_name in self.evt_names:
            wx_evt_name = self.fc_to_wx_events.get( fc_evt_name, fc_evt_name )
            wx_evt = getattr( wx, 'EVT_%s' % (wx_evt_name.upper(),) )
            self.canvas.Unbind( wx_evt )

    def OnEvent(self, fc_evt_name, wx_event):
        ''' If any wx event occurs, this one is called. It does some boilerplate
            work like enriching the event with world coordinates and then
            tries to get a handler for it and calls it if present.
        '''
        world_pnt = self.canvas.pointToWorld( wx_event.GetPosition() )

        handler = self._get_handler( fc_evt_name )
        wx_event.coords = world_pnt

        if handler:
            handler( wx_event )
        
        wx_event.Skip()
        
    def _get_handler(self, fc_event):
        ''' by default return a handler named like on_x where x is the name of
            the event (e.g. 'left_down'). This allows derived classes to easily
            implement event handlers.
        '''
        method_name = 'on_%s' % fc_event

        #print method_name
        try:
            handler = getattr(self, method_name)
        except AttributeError:
            pass
        else:
            return handler
    

    def raiseEvent(self, event_name, event):
        ''' can be called by derived classes to perform a hittest and send an
            event to any hit nodes. If no node was hit, the event is sent to the
            background, the canvas node itself.
        '''
        screen_pnt = event.GetPosition()
        world_pnt = self.canvas.pointToWorld( screen_pnt )
        
        nodes = self.canvas.hitTest(screen_pnt, True)
        if not nodes:
            nodes = ( self.canvas, )

        # send the event only to the topmost node for now
        nodes[0].send( event_name, wx_event = event, nodes = nodes, coords = event.coords )
        
        
        
class GUIModeMouse(GUIModeBase):
    '''
    Mouse mode just raises any event it receives.
    '''

    def Activate(self, canvas):
        canvas.window.Cursor = Cursors.get('default')
        return super( GUIModeMouse, self ).Activate( canvas )

    def _get_handler(self, fc_event):
        ''' We just raise the event we got to the appropriate node '''
        return partial( self.raiseEvent, fc_event )


from ..math import numpy

class GUIModeMove(GUIModeBase):
    ''' Move mode allows the user to drag the canvas around by using a hand-like
        tool. It also allows zooming with the scroll wheel.
    '''
    def __init__(self, canvas=None):
        GUIModeBase.__init__(self, canvas)
        self.startMove = None

    def Activate(self, canvas):
        canvas.window.Cursor = Cursors.get('Hand')
        return super( GUIModeMove, self ).Activate( canvas )

    def on_left_down(self, event):
        ''' Record where on the canvas the button went down and capture mouse
        '''
        self.canvas.window.Cursor = Cursors.get('GrabHand')
        self.canvas.window.CaptureMouse()
        self.startMove = event.GetPosition()
        self.startCamPos = self.canvas.camera.position.copy()
 
    def on_left_up(self, event):
        ''' Release mouse and restore cursor '''
        self.canvas.window.Cursor = Cursors.get('Hand')
        self.canvas.window.ReleaseMouse()
        self.startMove = None

    def on_move(self, event):
        ''' If the user is dragging the mouse, move the camera of the canvas '''
        wx_event = event
        if wx_event.Dragging() and wx_event.LeftIsDown() and not self.startMove is None:
            transform = self.canvas.camera.transform
            transform.translation = (0,0)
            self.canvas.camera.position = self.startCamPos - transform( [event.GetPosition() - self.startMove] )[0]

    def on_wheel(self, event):
        ''' By default, zoom in/out by a 0.1 factor per Wheel event.
            todo: make this configurable.
        '''
        if event.GetWheelRotation() < 0:
            self.canvas.zoom( 0.9 )
        else:
            self.canvas.zoom( 1.1 )


from ..math import boundingBox

class GUIModeZoomIn(GUIModeBase):
    ''' Zoom in mode allows the user to zoom in on parts of the canvas. He can
        either left_click which centers the view at the clicked position and
        zooms a bit in. The user can also drag a 'rubberband box' to select an
        area he wants to view. Or he can right click to zoom out. Or scroll to
        zoom.
    '''
    def Activate(self, canvas):
        canvas.window.Cursor = Cursors.get( 'MagPlus' )
        return super( GUIModeZoomIn, self ).Activate( canvas )

    def on_left_down(self, event):
        self.startBox = event.GetPosition()
        self.prevBox = None
        self.canvas.window.CaptureMouse()

    def on_left_up(self, event):
        ''' zoom in either by using a rubberband box or at the specific point.
            todo: make minimum cursor movement (5,5) and default zoom factor
                   (1.5) configurable
        '''
        if event.LeftUp() and not self.startBox is None:
            box = boundingBox.fromPoints( ( self.startBox, event.GetPosition() ) )
            # if mouse has moved less that five pixels, don't use the box.
            if ( box.Size > (5,5) ).all():
                start = self.canvas.pointToWorld( box.min )
                end = self.canvas.pointToWorld( box.max )
                bb = boundingBox.fromPoints( (start, end) )
                self.canvas.zoomToExtents( bb, padding_percent = 0 )
            else:
                center = self.canvas.pointToWorld( self.startBox )
                self.canvas.zoom( 1.5, center )
            self.prevBox = None
            self.startBox = None
            self.canvas.window.ReleaseMouse()

    def on_move(self, event):
        ''' Take care of drawing the rubberband box '''
        if event.Dragging() and event.LeftIsDown() and not (self.startBox is None):
            dc = wx.ClientDC( self.canvas.window )
            dc.BeginDrawing()
            dc.SetPen( wx.Pen('WHITE', 2, wx.SHORT_DASH) )
            dc.SetBrush( wx.TRANSPARENT_BRUSH )
            dc.SetLogicalFunction( wx.XOR )
            if not self.prevBox is None:
                dc.DrawRectanglePointSize( self.prevBox.min, self.prevBox.Size )
            thisBox = boundingBox.fromPoints( ( self.startBox, event.GetPosition() ) )
            dc.DrawRectanglePointSize( thisBox.min, thisBox.Size )
            dc.EndDrawing()
            
            self.prevBox = thisBox
            
    #def UpdateScreen(self):
    #    """
    #    Update gets called if the screen has been repainted in the middle of a zoom in
    #    so the Rubber Band Box can get updated
    #    """
    #    if self.PrevRBBox is not None:
    #        dc = wx.ClientDC(self.Canvas)
    #        dc.SetPen(wx.Pen('WHITE', 2, wx.SHORT_DASH))
    #        dc.SetBrush(wx.TRANSPARENT_BRUSH)
    #        dc.SetLogicalFunction(wx.XOR)
    #        dc.DrawRectanglePointSize(*self.PrevRBBox)

    def on_right_down(self, event):
        ''' zoom out.
            todo: make default zoom factor (1.5) configurable
        '''
        self.canvas.zoom( 1 / 1.5, event.coords, centerCoords = 'world' )

    def on_wheel(self, event):
        ''' By default, zoom in/out by a 0.1 factor per Wheel event.
            todo: make this configurable.
        '''
        if event.GetWheelRotation() < 0:
            self.canvas.zoom( 0.9 )
        else:
            self.canvas.zoom( 1.1 )
            

class GUIModeZoomOut(GUIModeBase):
    ''' Zoom out mode allows the user to zoom out off parts of the canvas. He
        can either left_click which centers the view at the clicked position and
        zooms a bit out. Or he can right click to zoom in. Or scroll to zoom.
    '''
    def Activate(self, canvas):
        canvas.window.Cursor = Cursors.get( 'MagMinus' )
        return super( GUIModeZoomOut, self ).Activate( canvas )

    def on_left_down(self, event):
        ''' zoom out.
            todo: make default zoom factor (1.5) configurable
        '''
        self.canvas.zoom( 1 / 1.5, event.coords, centerCoords = 'world' )

    def on_right_down(self, event):
        ''' zoom in.
            todo: make default zoom factor (1.5) configurable
        '''
        self.canvas.zoom( 1.5, event.coords, centerCoords = 'world' )

    def on_wheel(self, event):
        ''' By default, zoom in/out by a 0.1 factor per Wheel event.
            todo: make this configurable.
        '''
        if event.GetWheelRotation() < 0:
            self.canvas.zoom( 0.9 )
        else:
            self.canvas.zoom( 1.1 )
