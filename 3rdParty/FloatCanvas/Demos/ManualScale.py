#!/usr/bin/env python
"""
A demo showing how to se the scale manually

In this case to have an exact 1:1 relationship with teh pixels in a AddScaledBitmap
"""


import wx

import sys

ver = 'local'
#ver = 'installed'

if ver == 'installed': ## import the installed version
    from wx.lib.floatcanvas import FloatCanvas
    print "using installed version:", wx.lib.floatcanvas.__version__
elif ver == 'local':
    ## import a local version
    import sys
    sys.path.append("..")
    from floatcanvas import FloatCanvas


import numpy as np

class TestFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)
        self.canvas =FloatCanvas.FloatCanvas(self, BackgroundColor = "DARK SLATE BLUE")
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        MainSizer.Add(self.canvas, 4, wx.EXPAND)
        self.SetSizer(MainSizer)
        img = wx.Image('mypng(309x34).png')   
        A = self.canvas.AddScaledBitmap(img, (0,0), Height=img.GetHeight(), Position = 'tl')
        A.Bind(FloatCanvas.EVT_FC_MOTION, self.OnMotion)
        
        self.canvas.Scale = 1.0
        self.canvas.ViewPortCenter  = (154, -17)

    def OnMotion(self, event):
        x, y = event.HitCoords[0] - event.BoundingBox[0,0], event.BoundingBox[1,1] - event.HitCoords[1]
        print self.canvas.Scale, x, y

app = wx.App(0)
frame = TestFrame(None, title="Image hitcoords", size=(350,200))
frame.Show(True)
app.MainLoop()

