#!/usr/bin/env python

"""
Demo of putting a scaled text box inside a circle...
"""


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

        Point = (0.0,0.0)
        Circle = Canvas.AddCircle(Point,
                                  Diameter=50,
                                  LineWidth=4,
                                  )

        Text = Canvas.AddScaledTextBox("Some text that will need to be wrapped. Here is another sentence.",
                                       Point,
                                       Size=Circle.WH[0]/10.,
                                       #Width = 40,
                                       Width=Circle.WH[0]*1.6,
                                       Position = 'cc',
                                       Color = "Black",
                                       LineStyle = None,
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
    
    
    
    









