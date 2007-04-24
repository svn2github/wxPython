#!/usr/bin/env python


import wx

## import the installed version
#from wx.lib.floatcanvas import NavCanvas, FloatCanvas

## import a local version
import sys
sys.path.append("..")
from floatcanvas import NavCanvas, FloatCanvas

import ArcObject
FloatCanvas.ArcPoint = ArcObject.ArcPoint

import numpy as N

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
                                     Debug = 0,
                                     BackgroundColor = "DARK SLATE BLUE",
                                     ).Canvas
      
        self.Canvas = Canvas
        
        Point = N.array((0,0))
        StartXY = (5,0)
        EndXY = (0,4)
        CenterXY = (0, 0)
        
        Arc = FloatCanvas.ArcPoint(StartXY,
                                   EndXY,
                                   CenterXY,
                                   LineColor = "Black",
                                   LineStyle = "Solid",
                                   LineWidth    = 3,
                                   FillColor    = "Red",
                                   FillStyle    = "Solid",
                                   InForeground = False)              

        Canvas.AddObject(Arc)

        FloatCanvas.EVT_MOTION(self.Canvas, self.OnMove ) 

        
        self.Show()
        Canvas.ZoomToBB()

    def OnMove(self, event):
        """
        Updates the status bar with the world coordinates
        """
        self.SetStatusText("%.2g, %.2g"%tuple(event.Coords))


app = wx.App(False)
F = DrawFrame(None, title="FloatCanvas Demo App", size=(700,700) )
app.MainLoop()
    
    
    
    
