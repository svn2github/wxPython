#!/usr/bin/env python
"""

Module that holds the GUI modes used by FloatCanvas

Note that this can only be imported after a wx.App() has been created.

This approach was inpired by Christian Blouin, who also wrote the initial
version of the code.

"""

import wx
from ..timeMachine import Resources
from ..patterns.partial import partial
import numpy as N

import wx


class Cursors(object):
    """
    Class to hold the standard Cursors
    
    """
    
    def __init__(self):
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
        if hotspot is not None:
            img.SetOptionInt( wx.IMAGE_OPTION_CUR_HOTSPOT_X, hotspot[0] )
            img.SetOptionInt( wx.IMAGE_OPTION_CUR_HOTSPOT_Y, hotspot[1] )

        self.cursors[ name ] = cursor = wx.CursorFromImage( img )
        return cursor
        
            
    def get(cls, name):
        if not hasattr(cls, 'instance'):
            cls.instance = Cursors()
            
        return cls.instance.cursors[ name ]
        
    get = classmethod( get )    


class GUIModeBase(object):
    """
    Basic Mouse mode and baseclass for other GUImode.

    This one does nothing with any event

    """
  
    active = False

    def Deactivate(self):
        """
        this method gets called by FloatCanvas when a new mode is being set
        on the Canvas
        """
        self._unregisterEvents()
        del self.canvas
        self.active = False
    
    def Activate(self, canvas):
        """
        this method gets called by FloatCanvas when a new mode is being set
        on the Canvas
        """
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
        for fc_evt_name in self.evt_names:
            wx_evt_name = self.fc_to_wx_events.get( fc_evt_name, fc_evt_name )
            wx_evt = getattr( wx, 'EVT_%s' % (wx_evt_name.upper(),) )
            self.canvas.Bind( wx_evt, partial( self.OnEvent, fc_evt_name ) )

    def _unregisterEvents(self):        
        for fc_evt_name in self.evt_names:
            wx_evt_name = self.fc_to_wx_events.get( fc_evt_name, fc_evt_name )
            wx_evt = getattr( wx, 'EVT_%s' % (wx_evt_name.upper(),) )
            self.canvas.Unbind( wx_evt )

    def OnEvent(self, fc_evt_name, wx_event):
        world_pnt = self.canvas.pointToWorld( wx_event.GetPosition() )

        handler = self._get_handler( fc_evt_name )
        wx_event.coords = world_pnt

        if handler:
            handler( wx_event )
        
        wx_event.Skip()
        
    def _get_handler(self, fc_event):
        method_name = 'on_%s' % fc_event

        #print method_name
        try:
            handler = getattr(self, method_name)
        except AttributeError:
            pass
        else:
            return handler
    
    def UpdateScreen(self):
        """
        Update gets called if the screen has been repainted in the middle of a zoom in
        so the Rubber Band Box can get updated. Other GUIModes may require something similar
        """
        pass

    def raiseEvent(self, event_name, event):
        screen_pnt = event.GetPosition()
        world_pnt = self.canvas.pointToWorld( screen_pnt )
        
        nodes = self.canvas.hitTest(screen_pnt, True)
        if not nodes:
            nodes = ( self.canvas, )

        # send the event only to the topmost node for now
        nodes[0].send( event_name, wx_event = event, nodes = nodes, coords = event.coords )
        
        
        
class GUIModeMouse(GUIModeBase):
    """

    Mouse mode checks for a hit test, and if nothing is hit,
    raises a FloatCanvas mouse event for each event.

    """

    def Activate(self, canvas):
        canvas.window.Cursor = Cursors.get('default')
        return super( GUIModeMouse, self ).Activate( canvas )

    def _get_handler(self, fc_event):
        return partial( self.raiseEvent, fc_event )


from ..math import numpy

class GUIModeMove(GUIModeBase):
    def __init__(self, canvas=None):
        GUIModeBase.__init__(self, canvas)
        self.startMove = None

    def Activate(self, canvas):
        canvas.window.Cursor = Cursors.get('Hand')
        return super( GUIModeMove, self ).Activate( canvas )

    def on_left_down(self, event):
        self.canvas.window.Cursor = Cursors.get('GrabHand')
        self.canvas.window.CaptureMouse()
        self.startMove = event.GetPosition()
        self.startCamPos = self.canvas.camera.position.copy()
 
    def on_left_up(self, event):
        self.canvas.window.Cursor = Cursors.get('Hand')
        self.canvas.window.ReleaseMouse()
        self.startMove = None

    def on_move(self, event):
        wx_event = event
        if wx_event.Dragging() and wx_event.LeftIsDown() and not self.startMove is None:
            transform = self.canvas.camera.transform
            transform.translation = (0,0)
            self.canvas.camera.position = self.startCamPos - transform( [event.GetPosition() - self.startMove] )[0]

    def on_wheel(self, event):
        """
           By default, zoom in/out by a 0.1 factor per Wheel event.
        """
        if event.GetWheelRotation() < 0:
            self.canvas.zoom( 0.9 )
        else:
            self.canvas.zoom( 1.1 )


from ..math import boundingBox

class GUIModeZoomIn(GUIModeBase):

    def Activate(self, canvas):
        canvas.window.Cursor = Cursors.get( 'MagPlus' )
        return super( GUIModeZoomIn, self ).Activate( canvas )

    def on_left_down(self, event):
        self.startBox = event.GetPosition()
        self.prevBox = None
        self.canvas.window.CaptureMouse()

    def on_left_up(self, event):
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
            
    def UpdateScreen(self):
        """
        Update gets called if the screen has been repainted in the middle of a zoom in
        so the Rubber Band Box can get updated
        """
        if self.PrevRBBox is not None:
            dc = wx.ClientDC(self.Canvas)
            dc.SetPen(wx.Pen('WHITE', 2, wx.SHORT_DASH))
            dc.SetBrush(wx.TRANSPARENT_BRUSH)
            dc.SetLogicalFunction(wx.XOR)
            dc.DrawRectanglePointSize(*self.PrevRBBox)

    def on_right_down(self, event):
        self.canvas.zoom( 1 / 1.5, event.coords, centerCoords = 'world' )

    def on_wheel(self, event):
        if event.GetWheelRotation() < 0:
            self.canvas.zoom( 0.9 )
        else:
            self.canvas.zoom( 1.1 )
            

class GUIModeZoomOut(GUIModeBase):
    def Activate(self, canvas):
        canvas.window.Cursor = Cursors.get( 'MagMinus' )
        return super( GUIModeZoomOut, self ).Activate( canvas )

    def on_left_down(self, event):
        self.canvas.zoom( 1 / 1.5, event.coords, centerCoords = 'world' )

    def on_right_down(self, event):
        self.canvas.zoom( 1.5, event.coords, centerCoords = 'world' )

    def on_wheel(self, event):
        if event.GetWheelRotation() < 0:
            self.canvas.zoom( 0.9 )
        else:
            self.canvas.zoom( 1.1 )
