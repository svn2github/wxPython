#!/usr/bin/env python

"""

A test of the Editing Mode

"""

import wx
app = wx.PySimpleApp()
## import the installed version
#from wx.lib.floatcanvas import NavCanvas, FloatCanvas

## import the local version
import sys
sys.path.append("..")
from floatcanvas import NavCanvas, FloatCanvas, GUIMode

import numpy as N

class CreateCircleMode(GUIMode.GUIBase):
    def __init__(self, parent, Properties):
        GUIMode.GUIBase.__init__(self, parent)
        self.Properties = Properties
        self.Center = None
        self.PrevCircle = None
        
    def OnLeftDown(self, event):
        # start a new circle
        self.Center = N.array(event.GetPosition(), N.float)
        print "mouse clicked at:", self.Center

    def OnMove(self, event):
        # always raise the move event
        self.parent._RaiseMouseEvent(event,FloatCanvas.EVT_FC_MOTION)
        if event.Dragging() and event.LeftIsDown() and not (self.Center is None):
            Point = N.array(event.GetPosition(), N.float)
            distance = Point-self.Center
            Radius = N.hypot(distance[0], distance[1])
            print "Radius is:", Radius
            dc = wx.ClientDC(self.parent)
            dc.SetPen(wx.Pen('WHITE', 2, wx.SHORT_DASH))
            dc.SetBrush(wx.TRANSPARENT_BRUSH)
            dc.SetLogicalFunction(wx.XOR)
            if self.PrevCircle is not None:
                dc.DrawCirclePoint(*self.PrevCircle)
            self.PrevCircle = ( self.Center, Radius )
            dc.DrawCirclePoint( *self.PrevCircle )
    def OnLeftUp(self, event):
        if self.Center is not None:
            Point = N.array(event.GetPosition(), N.float)
            distance = Point-self.Center
            Radius = N.hypot(distance[0], distance[1])
            Center = self.parent.PixelToWorld(self.Center)
            Diameter = 2 * self.parent.ScalePixelToWorld((Radius, Radius))[0]
            self.parent.AddCircle(Center,
                                  Diameter,
                                  **self.Properties)
            
            self.Center = None
            self.PrevCircle = None
            self.parent.Draw()
            
            
class DrawFrame(wx.Frame):

    """
    A frame used for the FloatCanvas Demo

    """

    def __init__(self,parent, id,title,position,size):
        wx.Frame.__init__(self,parent, id,title,position, size)

        # Add the Canvas
        self.CreateStatusBar()            
        Canvas = NavCanvas.NavCanvas(self,-1,(500,500),
                                          ProjectionFun = None,
                                          Debug = 0,
                                          BackgroundColor = "DARK SLATE BLUE",
                                          ).Canvas
        
        self.Canvas = Canvas
        FloatCanvas.EVT_MOTION(self.Canvas, self.OnMove ) 
        
        Point = (45,40)
        Circle =  Canvas.AddCircle(Point, 10,
                                   FillColor = "Black",
                                   LineColor = "Red",
                                   )
        self.Show(True)
        self.Canvas.ZoomToBB()
        Properties = {"FillColor":"Red",
                      "LineColor":"Purple",
                      "LineWidth":3,
                      }
        self.Canvas.SetMode(CreateCircleMode(self.Canvas, Properties) )
        return None
    
    def OnMove(self, event):
        """
        Updates the status bar with the world coordinates
        """
        self.SetStatusText("%.2f, %.2f"%tuple(event.Coords))


DrawFrame(None, -1, "FloatCanvas Demo App", wx.DefaultPosition, (700,700) )
app.MainLoop()



