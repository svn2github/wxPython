#!/usr/bin/env python

"""
A small demo to show how to make a new GUIMode that allows panning the
image with the right mouse button.

"""

import wx
app = wx.App(False)

import numpy as N

## import the installed version
#from wx.lib.floatcanvas import NavCanvas, FloatCanvas

## import a local version
import sys
sys.path.append("..")
from floatcanvas import NavCanvas, FloatCanvas

## A new GUI Mode:
from floatcanvas.GUIMode import GUIMove

class GUIRightMove(GUIMove):
    ## rename these methods from GUIMMove
    OnRightDown = GUIMove.OnLeftDown
    def OnLeftDown(self, event):
        ## you'll probably want to do something else with this.
        pass
    
    OnRightUp = GUIMove.OnLeftUp
    def OnLeftUp(self, event):
        ## you'll probably want to do something else with this.
        pass

    def OnMove(self, event):
        # Allways raise the Move event.
        self.Canvas._RaiseMouseEvent(event,FloatCanvas.EVT_FC_MOTION)
        if event.Dragging() and event.RightIsDown() and not self.StartMove is None:
            self.MoveImage(event)


class DrawFrame(wx.Frame):

    """
    A frame used for the FloatCanvas Demo

    """

    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)

        self.CreateStatusBar()

        # Add the Canvas
        Canvas = NavCanvas.NavCanvas(self,-1,
                                     size = (500,500),
                                     ProjectionFun = None,
                                     Debug = 0,
                                     BackgroundColor = "DARK SLATE BLUE",
                                     ).Canvas
        
        self.Canvas = Canvas

        FloatCanvas.EVT_MOTION(self.Canvas, self.OnMove ) 

        Point = (45,40)
        Box = Canvas.AddScaledTextBox("A Two Line\nString",
                                      Point,
                                      2,
                                      Color = "Black",
                                      BackgroundColor = None,
                                      LineColor = "Red",
                                      LineStyle = "Solid",
                                      LineWidth = 1,
                                      Width = None,
                                      PadSize = 5,
                                      Family = wx.ROMAN,
                                      Style = wx.NORMAL,
                                      Weight = wx.NORMAL,
                                      Underlined = False,
                                      Position = 'br',
                                      Alignment = "left",
                                      InForeground = False)

        Box.Bind(FloatCanvas.EVT_FC_LEFT_DOWN, self.Binding)
        self.Show()
        Canvas.ZoomToBB()
        self.GUIRightMove = GUIRightMove(Canvas)
        Canvas.SetMode(self.GUIRightMove)

    def OnMove(self, event):
        """
        Updates the status bar with the world coordinates

        """
        self.SetStatusText("%.2f, %.2f"%tuple(event.Coords))

    def Binding(self, event):
        print "Writing a png file:"
        self.Canvas.SaveAsImage("junk.png")
        print "Writing a jpeg file:"
        self.Canvas.SaveAsImage("junk.jpg",wx.BITMAP_TYPE_JPEG)


F = DrawFrame(None, title="FloatCanvas Demo App", size=(700,700) )
app.MainLoop()








