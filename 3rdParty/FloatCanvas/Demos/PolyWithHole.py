#!/usr/bin/env python

import wx

## import the installed version
#from wx.lib.floatcanvas import NavCanvas, FloatCanvas

## import a local version
import sys
sys.path.append("../")
from floatcanvas import NavCanvas, FloatCanvas


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

        Points = (( 0,30),
                  ( 0, 0),
                  (30, 0),
                  (30,30),
                  ( 0,30),
                  (10,20),
                  (10,10),
                  (20,10),
                  (20,20),
                  (10,20),
                  )

        Poly = Canvas.AddPolygon(Points,
                                 FillColor = "blue",
                                 LineColor = None,
                                 )

        self.Show()
        Canvas.ZoomToBB()


    def OnMove(self, event):
        """
        Updates the status bar with the world coordinates

        """
        self.SetStatusText("%.2f, %.2f"%tuple(event.Coords))

app = wx.App(False)
F = DrawFrame(None, title="FloatCanvas Demo App", size=(700,700) )
app.MainLoop()
    
    
    
    









