#!/usr/bin/env python

"""
Demo of using EVT_ENTER etc to get multi-hit functionality
"""

import wx

## import the installed version
#from wx.lib.floatcanvas import NavCanvas, FloatCanvas

## import a local version
import sys
sys.path.append("../")
from floatcanvas import NavCanvas, FloatCanvas

FC = FloatCanvas


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

        FC.EVT_MOTION(self.Canvas, self.OnMove ) 

        # create a few test rectangles:

        self.rects = []
        x = 0
        for i in range(2):
            x += 50
            y = 0
            for j in range(4):
                y += 20
                rect = Canvas.AddRectangle((x, y), (40,10), FillColor="Red")
                rect.rectid = (i,j)
                rect.Bind(FC.EVT_FC_LEFT_DOWN, self.OnDown)
                rect.Bind(FC.EVT_FC_ENTER_OBJECT, self.OnEnter)

        # bind the events to the Canvas
        FC.EVT_LEFT_UP(Canvas, self.OnUp)
        self.Show()
        Canvas.ZoomToBB()

        self.InSelectMode = False

    def OnEnter(self, obj):
      if self.InSelectMode:
        print "selected: %s"%(obj.rectid,)

    def OnDown(self, obj):
      self.InSelectMode = True

    def OnUp(self, evt):
      self.InSelectMode = False
      print "mouse up"


    def OnMove(self, event):
        """
        Updates the status bar with the world coordinates

        """
        self.SetStatusText("%.2f, %.2f"%tuple(event.Coords))

app = wx.App(False)
F = DrawFrame(None, title="FloatCanvas Demo App", size=(700,700) )
app.MainLoop()
    
    
    
    









