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


class EditCircleMode(GUIMode.GUIBase):
    def __init__(self, Canvas=None):
        self.Canvas = Canvas
        self.Reset()

    def Reset(self):
        self.Moving = False
        self.StartPoint= None
        self.CenterHandle = None
        self.PrevCircle = None

    def SelectObject(self, Circle):
        self.Radius = Circle.WH[0] / 2
        self.CenterHandle = self.Canvas.AddBitmap(Resources.getMoveCursorBitmap(),
                                              Point,
                                              Position='cc',
                                              nForeground=True)

        #cross = Cross(Circle.XY, InForeground=True)
        self.CenterHandle.Bind(FloatCanvas.EVT_LEFT_DOWN, self.OnCenterHit)

    def OnCenterHit(self, object):
        if not self.Moving:
            self.Moving = True
            self.StartPoint = object.HitCoordsPixel
    
    def DrawOnTop(self, dc):
        if self.Circle is not None:
            dc.SetPen(wx.Pen('WHITE', 2, wx.SHORT_DASH))
            dc.SetBrush(wx.TRANSPARENT_BRUSH)
            dc.SetLogicalFunction(wx.XOR)
            dc.DrawCirclePoint( *self.Circle )

    def OnMove(self, event):
        """
        Moves the Circle
        """
        # always raise the move event
        self.Canvas._RaiseMouseEvent(event,FloatCanvas.EVT_FC_MOTION)

        if self.Moving:
            dxy = event.GetPosition() - self.StartPoint
            xy = self.Circle.XY
            xyp  = self.Canvas.WorldToPixel(xy) + dxy
            Radius = self.Canvas.ScaleWorldToPixel((self.Radius, self.Radius),)[0]

            # draw the ghost Circle
            dc = wx.ClientDC(self.Canvas)
            dc.SetPen(wx.Pen('WHITE', 2, wx.SHORT_DASH))
            dc.SetBrush(wx.TRANSPARENT_BRUSH)
            dc.SetLogicalFunction(wx.XOR)
            if self.PrevCircle is not None:
                dc.DrawCirclePoint(*self.PrevCircle)
            self.PrevCircle = ( self.Center, Radius )
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
    def __init__(self, Canvas, Properties, ObjectList=None):
        GUIMode.GUIBase.__init__(self, Canvas)

        if ObjectList is None:
            self.ObjectList = []
        else:
            self.ObjectList = ObjectList

        self.Properties = Properties
        self.Circle = None

    def DrawOnTop(self, dc):
        if self.Circle is not None:
            dc.SetPen(wx.Pen('WHITE', 2, wx.SHORT_DASH))
            dc.SetBrush(wx.TRANSPARENT_BRUSH)
            dc.SetLogicalFunction(wx.INVERT)
            dc.DrawCirclePoint( *self.Circle )

    def OnLeftDown(self, event):
        # start a new circle
        self.Circle = [N.array(event.GetPosition(), N.float), 0]
        self.Canvas.CaptureMouse()

    def OnMove(self, event):
        # always raise the move event
        self.canvas._RaiseMouseEvent(event,FloatCanvas.EVT_FC_MOTION)
        if event.Dragging() and event.LeftIsDown() and self.Circle is not None:
            Point = N.array(event.GetPosition(), N.float)
            distance = Point-self.Circle[0]
            self.Circle[1] = N.hypot(distance[0], distance[1])
            self.Canvas.Refresh()

    def OnLeftUp(self, event):
        if self.Circle is not None:
            Point = N.array(event.GetPosition(), N.float)
            distance = Point-self.Circle[0]
            Radius = N.hypot(distance[0], distance[1])
            Center = self.canvas.PixelToWorld(self.Circle[0])
            Diameter = 2 * self.canvas.ScalePixelToWorld((Radius, Radius))[0]
            if Diameter > 0:
                self.ObjectList.append(self.Canvas.AddCircle(Center,
                                                         Diameter,
                                                         **self.Properties),
                                       )
            self.Circle = None
            self.Canvas.Draw()


class DrawFrame(wx.Frame):
    """
    A frame used for the FloatCanvas Demo

    """
    def __init__(self, parent, id, title, position, size):
        wx.Frame.__init__(self,parent, id,title,position, size)


        # Add the Canvas
        self.CreateStatusBar()            
        self.NC = NavCanvas.NavCanvas(self,#-1,(500,500),
                                  ProjectionFun = None,
                                  Debug = 0,
                                  BackgroundColor = "DARK SLATE BLUE",
                                  )
        
        self.Canvas = Canvas = self.NC.Canvas
        
        self.Properties = {"FillColor":"Red",
                      "LineColor":"Purple",
                      "LineWidth":3,
                      }
        self.ObjectList = []
        self.CreateCircleMode = CreateCircleMode(self.Canvas, self.Properties, self.ObjectList)

        # Add some buttons to the Toolbar
        tb = self.NC.ToolBar
        tb.AddSeparator()

        ClearButton = wx.Button(tb, wx.ID_ANY, "Clear")
        tb.AddControl(ClearButton)
        ClearButton.Bind(wx.EVT_BUTTON, self.Clear)

        #AddButton = wx.Button(tb, wx.ID_ANY, "Add Circles")
        #tb.AddControl(AddButton)
        #AddButton.Bind(wx.EVT_BUTTON, self.SetAddCircles)
        #self.AddButton = AddButton
        
        self.AddCircleTool = tb.AddRadioTool(wx.ID_ANY,
                                             bitmap=Resources.getMoveCursorBitmap(),
                                             shortHelp = "Add Circle")
        self.Bind(wx.EVT_TOOL, self.SetAddCircleMode, self.AddCircleTool)

        self.EditCircleTool = tb.AddRadioTool(wx.ID_ANY,
                                             bitmap=Resources.getMoveRLCursorBitmap(),
                                             shortHelp = "Edit Circle")
        #self.Bind(wx.EVT_TOOL, lambda evt : NC.SetMode(Mode=self.NC.MouseMode), self.EditCircleTool)
        self.Bind(wx.EVT_TOOL, self.SetEditMode, self.EditCircleTool)

        
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

    def SetCircleEdit(self, obj):
        print "In SetCircle Edit"
        Mode = EditCircleMode(self.Canvas)
        Mode.SelectObject(obj)
        self.Canvas.SetMode(Mode)

if __name__ == "__main__":
    app = wx.PySimpleApp()
    DrawFrame(None, -1, "FloatCanvas Demo App", wx.DefaultPosition, (700,700) )
    app.MainLoop()



