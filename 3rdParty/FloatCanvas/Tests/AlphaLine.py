#!/usr/bin/env python

"""

An attempt at an AlphaLine class using NavCanvas and GraphicsContext

"""

import numpy as N
import sys, wx
sys.path.append("..")
from floatcanvas import FloatCanvas, NavCanvas
#from math import sin,cos,atan,pi # these are all in numpy!

class AlphaLine(FloatCanvas.Line):
    """

    The AlphaLine class takes a list of N - 2-tuples, or a NX2 NumPy Float array
    of point coordinates.

    It will draw a line.

    """
    def __init__(self,Points,
            LineColor = "Black",
            LineStyle = "Solid",
            LineWidth    = 1,
            InForeground = True,
            StartAlpha = 0,
            EndAlpha = 255,
            BorderColour = "White"):
        FloatCanvas.DrawObject.__init__(self, InForeground)

        self.Points = N.array(Points, N.float).reshape((-1,2))
        self.CalcBoundingBox()

        self.LineColor = LineColor
        self.LineStyle = LineStyle
        self.LineWidth = LineWidth
        self.StartAlpha = StartAlpha
        self.EndAlpha = EndAlpha
        self.BorderColour = BorderColour

    def Perpendicular(self, line, length):
        """Return a point that is perpendicular to 'line'

        Given a line defined as two points [(x1, y1), (x2, y2)] return a point
        that will create a new line that is perpendicular. 'length' gives the 
        vertical distance from (x2, y2)

        """
        # this could be numpy-ified
        x1,y1 = line[0]
        x2,y2 = line[1]
        angle = N.pi

        theta = N.arctan((x2 - x1) / (y2 - y1))
        alpha = 2 * N.pi - (angle + theta)
        l = length * N.cos(alpha)
        dx = l * N.sin(alpha)
        dy = l * N.cos(alpha)

        if dx != abs(dx):
            dx *= -1

        if dy != abs(dy):
            dy *= -1

        x3 = x2 - dx
        y3 = y2 - dy

        return x3, y3

    def _Draw(self, dc , WorldToPixel, ScaleWorldToPixel, HTdc=None):
        bcolour = self.BorderColour

        # you need to translform to pixel coords!
        Points = WorldToPixel(self.Points)
        #Points = self.Points
        GC = wx.GraphicsContext.Create(dc)

        ##FIXME: I sure hope there is a better way to create a color!
        c = wx.Color()
        c.SetFromName(self.LineColor)
	#c = wx.Color(self.LineColor)
        r,g,b = c.Get()

        c1 = wx.Color(r, g, b, self.StartAlpha)
        c2 = wx.Color(r, g, b, self.EndAlpha)

        Path = GC.CreatePath()

        bottomline = Points[1:].copy()

        lastline = Points[-2:]
        firstline = Points[:2]
        firstline = firstline[::-1]
        perplast = self.Perpendicular(lastline, self.LineWidth)
        perpfirst = self.Perpendicular(firstline, self.LineWidth)

        data = Points[:]
        data[:,1] -= self.LineWidth

        while perplast[0] >  data[-1,0]:
            data = data[:-1]

        data = N.resize(data, (len(data) + 1, 2))
	data[-1] = perplast

        data = data[::-1]

        while  perpfirst[0] > data[-1,0]:
            data = data[:-1]

        data = N.resize(data, (len(data) + 1,2))
        data[-1] = perpfirst
        topline = data

        Path.MoveToPoint(perpfirst)

        if bottomline[-1, 0] >= perplast[0]:
            bottomline[-1] = perplast

        for point in bottomline:
            Path.AddLineToPoint(point)

        for point in topline:
            Path.AddLineToPoint(point)

        GC.SetPen(wx.Pen(bcolour))
        GC.DrawPath(Path)

        m = Points[:,0].size - 1

        Brush = \
            GC.CreateLinearGradientBrush(Points[0,0], \
            Points[0,1], Points[m,0], Points[m,1], c1, c2)

        GC.SetBrush(Brush)
        GC.FillPath(Path)

        # Don't know what this does (HTdc?)
	# That's the HIt Test DC -- it draws a version on an
	# off screen bitmap in a unique color for hit testing
        if HTdc and self.HitAble:
            HTdc.SetPen(self.HitPen)
            HTdc.DrawLines(Points)


class MyFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        kwargs['size'] = (700, 300)
        kwargs['pos'] = (50,50)
        wx.Frame.__init__(self, *args, **kwargs)

        NC = NavCanvas.NavCanvas(self ,wx.ID_ANY ,(500,500),
                ProjectionFun = None,
                BackgroundColor = "WHITE"
                )

        self.Canvas = NC.Canvas
        self.DrawLine()
        self.DrawCurve()

        return None

    def DrawLine(self):
        data = ([400,100], [100,50])

        self.Canvas.AddObject(AlphaLine(data,
                LineColor = "Red",
                LineStyle = "Solid",
                LineWidth    = 4,
                InForeground = 1,
                StartAlpha = 255,
                EndAlpha = 0,
                BorderColour = "Black"))

        self.Canvas.Draw()

    def DrawCurve(self):
        time = 2.0*N.pi*N.arange(100)/100.0
        data = 1.0*N.ones((100,2))
        data[:,0] = time * 100 + 20
        data[:,1] = N.sin(time) * 100 + 150

        self.Canvas.AddObject(AlphaLine(data,
                    LineColor = "Blue",
                    LineStyle = "Solid",
                    LineWidth    = 6,
                    InForeground = 1,
                    StartAlpha = 0,
                    EndAlpha = 255,
                    BorderColour = "White"))

        self.Canvas.Draw()

A = wx.App(0)
F = MyFrame(None)
F.Show()
A.MainLoop()
