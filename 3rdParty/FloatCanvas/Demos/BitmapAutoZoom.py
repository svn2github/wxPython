#!/usr/bin/env python

"""
This is a demo of putting two bitmaps on a Canvas, and auto-zooming them.

This is here as much as a test as anything else, as it found a bug (now fixed) in the bitmap scaling code

Example provided by: nouvellecollection@gmail.com

"""

import wx

#### import local version:
import sys
sys.path.append("..")
from floatcanvas import NavCanvas, FloatCanvas

#from wx.lib.floatcanvas import FloatCanvas

class MyPanel(wx.Panel):
    def __init__(self, parent):
        super(MyPanel, self).__init__(parent)
        self.SetBackgroundColour(wx.WHITE)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.Canvas = FloatCanvas.FloatCanvas(self, BackgroundColor = "LIGHT GREY")
        self.Canvas.MaxScale = 2        

        sizer.Add(self.Canvas, 1, flag=wx.EXPAND)

        bmp1 = wx.BitmapFromImage(wx.Image('bmp1.png', wx.BITMAP_TYPE_PNG))
        bmp2 = wx.BitmapFromImage(wx.Image('bmp2.png', wx.BITMAP_TYPE_PNG))            
        img1 = self.Canvas.AddScaledBitmap(bmp1, (0, 0), Height = bmp1.GetHeight(), Position = 'tl', Quality='normal')
        img2 = self.Canvas.AddScaledBitmap2(bmp2, (100, -100), Height = bmp2.GetHeight(), Position = 'tl', Quality='high')
        
        print img1.Quality
        print img2.Quality

        self.Canvas.ZoomToBB()
        #wx.CallLater(1, self.Canvas.ZoomToBB)

        self.Bind(wx.EVT_SIZE, self.OnSize)

        self.SetSizerAndFit(sizer)

    def OnSize(self, evt):
        wx.CallLater(1, self.Canvas.ZoomToBB)
        evt.Skip()
     
class DemoApp(wx.App):
        def __init__(self, *args, **kwargs):
            wx.App.__init__(self, *args, **kwargs)
            frame = wx.Frame(None)
            MyPanel(frame)
            frame.Show()
            frame.Fit()

app = DemoApp(False)
app.MainLoop()
