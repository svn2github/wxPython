#!/usr/bin/env python

"""
This demo shows how to use a ScaledBitmap2 (which is like a scaled bitmap,
but uses memory more efficiently for large images and high zoom levels.)

This also demonstrates how to auto-rescale the image when the Window is re-sized

"""

## Set a path to an Image file here:
ImageFile = "white_tank.jpg" 


import wx
import random
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
        Canvas = NavCanvas.NavCanvas(self,
                                     ProjectionFun = None,
                                     BackgroundColor = "DARK SLATE BLUE",
                                     ).Canvas
        Canvas.MaxScale=20 # sets the maximum zoom level
        self.Canvas = Canvas

        FloatCanvas.EVT_MOTION(self.Canvas, self.OnMove ) 

        
        # create the image:
        image = wx.Image(ImageFile)
        self.width, self.height = image.GetSize()
        img = FloatCanvas.ScaledBitmap2( image,
                                        (0,0),
                                        Height=image.GetHeight(),
                                        Position = 'tl',
                                        )
        Canvas.AddObject(img)
        
        self.Canvas.Bind(wx.EVT_SIZE, self.OnSize)

        self.Show()
        Canvas.ZoomToBB(margin_adjust=1.0)
    
    def OnSize(self, event):
        """
        re-zooms the canvas to fit the window

        """
        self.Canvas.ZoomToBB(margin_adjust=1.0)
        event.Skip()

    def OnMove(self, event):
        """
        Updates the status bar with the world coordinates

        """
        self.SetStatusText("%i, %i"%tuple(event.Coords))


app = wx.App(False)
F = DrawFrame(None, title="FloatCanvas Demo App", size=(700,700) )
app.MainLoop()
    
    
    
    









