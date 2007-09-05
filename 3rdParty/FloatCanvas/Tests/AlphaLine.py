#!/usr/bin/env python

"""

A test to use a GraphicsContext to draw an object with Alpha blending

NOt far yet -- is there a GradientPen???


"""

import numpy as N
from FloatCanvas import Line, PointsObjectMixin

#class Line(PointsObjectMixin, LineOnlyMixin, DrawObject):
class AlphaLine(Line):
    """

    The AlphaLine class takes a list of 2 - 2-tuples, or a 2X2 NumPy Float array
    of point coordinates.

    It will draw a straight line. 
    """
    def __init__(self,Points,
                 LineColor = "Black",
                 LineStyle = "Solid",
                 LineWidth    = 1,
                 InForeground = False):
        DrawObject.__init__(self, InForeground)


        self.Points = N.array(Points,N.float)
        self.CalcBoundingBox()

        self.LineColor = LineColor
        self.LineStyle = LineStyle
        self.LineWidth = LineWidth

        self.SetPen(LineColor,LineStyle,LineWidth)

        self.HitLineWidth = max(LineWidth,self.MinHitLineWidth)


    def _Draw(self, dc , WorldToPixel, ScaleWorldToPixel, HTdc=None):
        Points = WorldToPixel(self.Points)
        dc.SetPen(self.Pen)
        dc.DrawLines(Points)
        if HTdc and self.HitAble:
            HTdc.SetPen(self.HitPen)
            HTdc.DrawLines(Points)
