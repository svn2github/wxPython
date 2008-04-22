#!/usr/bin/env python

"""
A test of the Editing Mode

It's in a bit of a broken state right now!!!

"""

import wx
## import the installed version
#from wx.lib.floatcanvas import NavCanvas, FloatCanvas

## import the local version
import sys
sys.path.append("..")
from floatcanvas import NavCanvas, FloatCanvas, GUIMode, Resources
from floatcanvas.FloatCanvas import XYObjectMixin, LineOnlyMixin, DrawObject
import numpy as N

class Cross(XYObjectMixin, LineOnlyMixin, DrawObject,):
    def __init__(self,
                       XY,
                       Size = 4,
                       LineColor = "Black",
                       LineStyle = "Solid",
                       LineWidth    = 2,
                       InForeground = False):
        DrawObject.__init__(self, InForeground)

        self.XY = N.array(XY, N.float)
        self.XY.shape = (2,) # Make sure it is a length 2 vector
        self.Size = Size

        self.CalcBoundingBox()

        self.LineColor = LineColor
        self.LineStyle = LineStyle
        self.LineWidth = LineWidth

        self.SetPen(LineColor,LineStyle,LineWidth)
        self.HitLineWidth = max(LineWidth,self.MinHitLineWidth)
    
    def _Draw(self, dc , WorldToPixel, ScaleWorldToPixel, HTdc=None):
        dc.SetPen(self.Pen)
        x, y = WorldToPixel(self.XY)

        size = self.Size
        dc.DrawLine(x, y+size, x, y-size)
        dc.DrawLine(x-size, y, x+size, y)
        if HTdc and self.HitAble:
            HTdc.SetPen(self.HitPen)
            HTdc.DrawLine(x, y+size, x, y-size-1)
            HTdc.DrawLine(x-size-1, y, x+size, y)

class SelectObjectMode(GUIMode.GUIMouse):
    def __init__(self, Canvas=None):
       self._Canvas = Canvas
        
       self.ObjectList = []
        
    def set_Canvas(self, canvas):
        ## gets called when the Canvas is set -- i.e. when the mode is used.
        self._Canvas = canvas
        self.BindAll()
    
    def get_Canvas(self):
        return self._Canvas
    Canvas = property(fget=get_Canvas, fset=set_Canvas)
    
    def Unset(self):
        self.UnBindAll()
    
    def BindAll(self):
        """
        Binds all the objects in self.ObjectList to a handler
        """
        ##fixme -- when do they get unbound???    
        for obj in self.Objects:
            obj.Bind(FloatCanvas.EVT_LEFT_DOWN, self.OnObjectHit)
    def UnBindAll(self):
        """
        Unbinds all the objects in self.ObjectList to a handler
        """
        ##fixme: when does this get called?
        ##     maybe there needs to be a method that gets called when a 
        ##     Mode gets unset.
        for obj in self.Objects:
            obj.UnBindAll()

    def OnObjectHit(obj):
        self.UnBindAll
        self.Canvas.SetMode(EditCircleMode())
        self.Canvas.Mode.SelectObject(obj)


class EditCircleMode(GUIMode.GUIBase):
    def __init__(self, Canvas=None):
        self.Canvas = Canvas
        self.Reset()

    def set_Canvas(self, canvas):
        ## gets called when the Canvas is set -- i.e. when the mode is used.
        self._Canvas = canvas
    
    def get_Canvas(self):
        return self._Canvas
    Canvas = property(fget=get_Canvas, fset=set_Canvas)

    def Reset(self):
        self.Moving = False
        self.StartPoint= None
        self.CenterHandle = None
        self.PrevCircle = None

    def SelectObject(self, Circle):
        self.Circle = Circle
        self.Radius = Circle.WH[0] / 2
        
        self.CenterHandle = self.Canvas.AddBitmap(Resources.getMoveCursorBitmap(),
                                              Circle.Center,
                                              Position='cc',
                                              InForeground=True)

        #cross = Cross(Circle.XY, InForeground=True)
        self.CenterHandle.Bind(FloatCanvas.EVT_FC_LEFT_DOWN, self.OnCenterHit)
        self.Canvas.Draw(True)

    def OnCenterHit(self, object):
        print "In OnCenterHit"
        if not self.Moving:
            self.Moving = True
            self.StartPoint = object.HitCoordsPixel
    
    def DrawOnTop(self, dc):
        if self.Circle is not None:
#            dc.SetPen(wx.Pen('WHITE', 2, wx.SHORT_DASH))
            dc.SetPen(wx.Pen('WHITE', 2))
            dc.SetBrush(wx.TRANSPARENT_BRUSH)
            #dc.SetLogicalFunction(wx.XOR)
            dc.DrawCirclePoint( *self.Circle )
            dc.SetPen(wx.Pen('BLACK', 2, wx.SHORT_DASH))
            dc.DrawCirclePoint( *self.Circle )

    def OnLeftDown(self, event):
        print "In EditCircleMode.OnLeftDown()"
        EventType = FloatCanvas.EVT_FC_LEFT_DOWN
        if not self.Canvas.HitTest(event, EventType):
            self.Canvas._RaiseMouseEvent(event, EventType)

    def OnMove(self, event):
        """
        Moves the Circle
        """
        # always raise the move event
        self.Canvas._RaiseMouseEvent(event,FloatCanvas.EVT_FC_MOTION)

        if self.Moving:
            dxy = event.GetPosition() - self.StartPoint
            xy = self.Circle.Center
            xyp  = self.Canvas.WorldToPixel(xy) + dxy
            Radius = self.Canvas.ScaleWorldToPixel((self.Radius, self.Radius),)[0]

            # draw the ghost Circle
            dc = wx.ClientDC(self.Canvas)
            dc.SetPen(wx.Pen('WHITE', 2, wx.SHORT_DASH))
            dc.SetBrush(wx.TRANSPARENT_BRUSH)
            dc.SetLogicalFunction(wx.XOR)
            if self.PrevCircle is not None:
                dc.DrawCirclePoint(*self.PrevCircle)
            self.PrevCircle = ( xyp, Radius )
            dc.DrawCirclePoint( *self.PrevCircle )


    def OnLeftUp(self, event):
        if self.StartPoint is not None:
            dxy = event.GetPosition() - self.StartPoint
            dxyw = self.Canvas.ScalePixelToWorld(dxy)
            self.Circle.Move(dxyw)
            self.CenterHandle.Move(dxyw)
            self.StartPoint = None
            self.PrevCircle = None
            self.Canvas.Draw(Force=True)


class CreateCircleMode(GUIMode.GUIBase):
    def __init__(self, Properties, ObjectList=None):
        GUIMode.GUIBase.__init__(self)

        if ObjectList is None:
            self.ObjectList = []
        else:
            self.ObjectList = ObjectList

        self.Properties = Properties
        self.Circle = None
        self.OldCircle = None

    def OnLeftDown(self, event):
        # start a new circle
        self.Circle = [N.array(event.GetPosition(), N.float), 0]
        self.OldCircle = None # just to make sure
        self.Canvas.CaptureMouse()

    def OnMove(self, event):
        # always raise the move event
        self.Canvas._RaiseMouseEvent(event,FloatCanvas.EVT_FC_MOTION)
        if event.Dragging() and event.LeftIsDown() and self.Circle is not None:
            Point = N.array(event.GetPosition(), N.float)
            distance = Point-self.Circle[0]
            self.Circle[1] = N.hypot(distance[0], distance[1])
            dc = wx.ClientDC(self.Canvas)
            dc.SetPen(wx.Pen('WHITE', 2, wx.SHORT_DASH))
            dc.SetBrush(wx.TRANSPARENT_BRUSH)
            dc.SetLogicalFunction(wx.INVERT)
            if self.OldCircle is not None:
                dc.DrawCirclePoint( *self.OldCircle )
            dc.DrawCirclePoint( *self.Circle )
            self.OldCircle = self.Circle[:]# need to make a copy

    def OnLeftUp(self, event):
        if self.Circle is not None:
            Point = N.array(event.GetPosition(), N.float)
            distance = Point-self.Circle[0]
            Radius = N.hypot(distance[0], distance[1])
            Center = self.Canvas.PixelToWorld(self.Circle[0])
            Diameter = 2 * self.Canvas.ScalePixelToWorld((Radius, Radius))[0]
            if Diameter > 0:
                self.ObjectList.append(self.Canvas.AddCircle(Center,
                                                         Diameter,
                                                         **self.Properties),
                                       )
            self.Circle = None
            self.OldCircle = None
            self.Canvas.Draw()

from Icons import CircleIcon, CircleEditIcon

class EditCanvas(NavCanvas.NavCanvas):
    ##fixme: could this be a mixin instead?
    def BuildToolbar(self):
        """
        over-rideing the native one -- so I can add some tools.
        """
        
        self.Properties = {"FillColor":"Red",
                           "LineColor":"Purple",
                           "LineWidth":3,
                           }
        self.ObjectList = []
        
        tb = wx.ToolBar(self)
        self.ToolBar = tb
        tb.SetToolBitmapSize((24,24))
        Modes = self.Modes
        Modes.append(("Add Circles",
                      CreateCircleMode(self.Properties, self.ObjectList),
                      CircleIcon.getBitmap(),
                     )
                    )
        Modes.append(("Edit Circles",
                      EditCircleMode(),
                      CircleEditIcon.getBitmap(),
                     )
                    )
        self.AddToolbarModeButtons(tb, Modes)
        self.AddToolbarZoomButton(tb)
        tb.Realize()

class DrawFrame(wx.Frame):
    """
    A frame used for the FloatCanvas Demo

    """
    def __init__(self, parent, id, title, position, size):
        wx.Frame.__init__(self,parent, id,title,position, size)

        # Add the Canvas
        self.CreateStatusBar()            
        self.NC = EditCanvas(self,
                             BackgroundColor = "DARK SLATE BLUE",
                             )
        
        self.Canvas = Canvas = self.NC.Canvas
        
        self.ObjectList = self.NC.ObjectList
        
        tb = self.NC.ToolBar
        tb.AddSeparator()

        EditCircleButton = wx.Button(tb, wx.ID_ANY, "Edit")
        tb.AddControl(EditCircleButton)
        EditCircleButton.Bind(wx.EVT_BUTTON, self.SetCircleEdit)

        ClearButton = wx.Button(tb, wx.ID_ANY, "Clear")
        tb.AddControl(ClearButton)
        ClearButton.Bind(wx.EVT_BUTTON, self.Clear)

        #AddButton = wx.Button(tb, wx.ID_ANY, "Add Circles")
        #tb.AddControl(AddButton)
        #AddButton.Bind(wx.EVT_BUTTON, self.SetAddCircles)
        #self.AddButton = AddButton
        
#        self.AddCircleTool = tb.AddRadioTool(wx.ID_ANY,
#                                             bitmap=Resources.getMoveCursorBitmap(),
#                                             shortHelp = "Add Circle")
#        self.Bind(wx.EVT_TOOL, self.SetAddCircleMode, self.AddCircleTool)#
#
#        self.EditCircleTool = tb.AddRadioTool(wx.ID_ANY,
#                                             bitmap=Resources.getMoveRLCursorBitmap(),
#                                             shortHelp = "Edit Circle")
        #self.Bind(wx.EVT_TOOL, lambda evt : NC.SetMode(Mode=self.NC.MouseMode), self.EditCircleTool)
        #self.Bind(wx.EVT_TOOL, self.SetEditMode, self.EditCircleTool)
        
        tb.Realize()

        FloatCanvas.EVT_MOTION(self.Canvas, self.OnMove ) 
        
        Point = (45,40)
        Circle =  Canvas.AddCircle(Point, 10,
                                   FillColor = "cyan",
                                   LineColor = "Red",
                                   LineWidth = 2,
                                   )

        cross = Cross(Point)

        self.Canvas.AddObject(cross)
        self.Show(True)
        self.Canvas.ZoomToBB()

        self.ObjectList.append(Circle)
        return None
    
    def OnMove(self, event):
        """
        Updates the status bar with the world coordinates
        """
        self.SetStatusText("%.2f, %.2f"%tuple(event.Coords))

    def Clear(self, event=None):
        self.ObjectList = []
        self.Canvas.ClearAll()
        self.Canvas.Draw()

    def SetAddCircleMode(self, event=None):
        self.Canvas.SetMode(self.CreateCircleMode)
        print "UnBinding all Objects"
        self.Canvas.UnBindAll()

    def SetEditMode(self, event=None):
        print "Setting Mode to Mouse Mode"
        self.Canvas.SetMode(self.NC.GUIMouse)
        self.BindAll()
    
    def BindAll(self):
        for obj in self.ObjectList:
            print "Binding:", obj
            obj.Bind(FloatCanvas.EVT_FC_LEFT_DOWN, self.SetCircleEdit)

    def SetCircleEdit(self, obj=None):
        print "In SetCircle Edit"
        Mode = EditCircleMode(self.Canvas)
        #if obj is None:
        obj = self.ObjectList[0]
        Mode.SelectObject(obj)
        self.Canvas.SetMode(Mode)

if __name__ == "__main__":
    app = wx.PySimpleApp()
    DrawFrame(None, -1, "FloatCanvas Demo App", wx.DefaultPosition, (700,700) )
    app.MainLoop()



