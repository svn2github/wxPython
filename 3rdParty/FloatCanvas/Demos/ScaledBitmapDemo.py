#!/usr/bin/env python

## Set a path to an Image file here:

ImageFile = "./white_tank.jpg" 


import wx

## import the installed version
#from wx.lib.floatcanvas import NavCanvas, FloatCanvas

# import a local version
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
        Canvas.MaxScale=4
        self.Canvas = Canvas

        FloatCanvas.EVT_MOTION(self.Canvas, self.OnMove ) 

        
        # create the image:
        image = wx.Image(ImageFile)
        img = Canvas.AddScaledBitmap( image,
                                      (0,0),
                                      Height=image.GetHeight(),
                                      Position = 'tl',
                                      Quality = 'normal',
                                      )

        img.Bind(FloatCanvas.EVT_FC_LEFT_DOWN, self.OnLeftDown)
        img.Bind(FloatCanvas.EVT_FC_MOTION, self.OnMotion)
        self.Show()
        Canvas.ZoomToBB()

        self.move_count = 0
        
    def OnMove(self, event):
        """
        Updates the status bar with the world coordinates

        """
        self.SetStatusText("%i, %i"%tuple(event.Coords))

    def OnLeftDown(self, obj):
        print "Left Mouse Clicked on ", obj

    def OnMotion(self, obj):
        print "mouse moving on image:", self.move_count
        self.move_count += 1

app = wx.App(False)
F = DrawFrame(None, title="FloatCanvas Demo App", size=(700,700) )
app.MainLoop()
    
    
    
    









