#!/usr/bin/env python

"""

An attempt at an AlphaLine class using NavCanvas and GraphicsContext

"""

import numpy as N
import sys, wx
import math
from math import sin, cos
import time


class MyFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        kwargs['size'] = (1000, 800)
        kwargs['pos'] = (50,50)
        wx.Frame.__init__(self, *args, **kwargs)

        self.Bind( wx.EVT_PAINT, self.OnPaint )

        return None

    def OnPaint(self, evt):
        self.dc = wx.PaintDC(self)
        self.GC = GC = wx.GraphicsContext.Create(self.dc)
        self.GC.SetBrush( wx.BLUE_BRUSH )

        Path = GC.CreatePath()

        vertices = [ (0,0), (100,0), (100,100), (0,100) ]

        Path.MoveToPoint( *vertices[0] )
        for v in vertices[1:]:
            Path.AddLineToPoint(*v)

        angle = 25 * 3.14 / 180
        m = self.GC.CreateMatrix( cos(angle), sin(angle),  -sin(angle), cos(angle),  0, 0 )

        print Path.GetBox()
        self.GC.SetTransform( m )
        print Path.GetBox()

        #Path.Transform( m )
        self.GC.DrawPath( Path )

        #self.Close()

        
    
A = wx.App(0)
F = MyFrame(None, wx.ID_ANY, 'GC Benchmark')
F.Show()
A.MainLoop()
