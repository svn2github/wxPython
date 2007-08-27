import wx

## import a local version of FloatCanvas


from floatcanvas import FloatCanvas
from floatcanvas.Utilities import BBox

import numpy as N

XYObjectMixin = FloatCanvas.XYObjectMixin
LineOnlyMixin = FloatCanvas.LineOnlyMixin
DrawObject = FloatCanvas.DrawObject

class PieChart(XYObjectMixin, LineOnlyMixin, DrawObject):
    """
    This is DrawObject for a pie chart
    
    You can pass in a bunch of values, and it will draw a pie chart for
    you, and it will make the chart, scaling the size of each "slice" to
    match your values.
    
    The parameters are:
    
     XY : The (x,y) coords of the center of the chart
     Diameter : The diamter of the chart in worls coords, unless you set
                "Scaled" to False, in which case it's in pixel coords.
     Values : sequence of values you want to make the chart of.
     FillColors=None : sequence of colors you want the slices. If
                       None, it will choose (no guarantee youll like them!)
     FillStyles=None : Fill style you want ("Solid", "Hash", etc)
     LineColor = None : Color of lines separating the slices
     LineStyle = "Solid" : style of lines separating the slices
     LineWidth    = 1 : With of lines separating the slices
     Scaled = True : Do you want the pie to scale when zooming? or stay the same size in pixels?
     InForeground = False: Should it be on the foreground?             
    

    """
    
    
    ##fixme: this should be a longer and better designed set.
    DefaultColorList = ["Red", "Green", "Blue", "Purple", "Yellow", "Cyan"]

    def __init__(self,
                 XY,
                 Diameter,
                 Values,
                 FillColors=None,
                 FillStyles=None,
                 LineColor = None,
                 LineStyle = "Solid",
                 LineWidth    = 1,
                 Scaled = True,
                 InForeground = False):               
        DrawObject.__init__(self, InForeground)

        self.XY = N.asarray(XY, N.float).reshape( (2,) )
        self.Diameter = Diameter
        self.Values = N.asarray(Values, dtype=N.float).reshape((-1,1))
        if FillColors is None:
            FillColors = self.DefaultColorList[:len(Values)]
        if FillStyles is None:
            FillStyles = ['Solid'] * len(FillColors)
        self.FillColors = FillColors
        self.FillStyles = FillStyles
        self.LineColor = LineColor
        self.LineStyle = LineStyle

        self.Scaled = Scaled
        self.InForeground = InForeground
        
        self.SetPen(LineColor, LineStyle, LineWidth)
        self.SetBrushes()
        self.CalculatePoints()

    def SetFillColors(self, FillColors):
        self.FillColors = FillColors
        self.SetBrushes()

    def SetFillStyles(self, FillStyles):
        self.FillStyles = FillStyles
        self.SetBrushed()

    def SetValues(self, Values):
        Values = N.asarray(Values, dtype=N.float).reshape((-1,1))
        self.Values = Values
        self.CalculatePoints()

    def CalculatePoints(self):
        # add the zero point to start
        Values = N.vstack( ( (0,), self.Values) )
        Diameter = self.Diameter

        Fractions = Values/Values.sum()
        Angles = 2*N.pi * Fractions
        Angles = N.cumsum(Angles, axis=0)
        Angles[-1,0] = 0 # this should be a full circle, and we want to avoid rounding error.
        CirclePoints = N.hstack( (N.cos(Angles)*Diameter, N.sin(Angles)*Diameter) )
        if self.Scaled:
            CirclePoints += self.XY
        else:
            CirclePoints = CirclePoints * (1, -1) #(in pixel coords, y is down)
        self.Points = CirclePoints
        
        self.CalcBoundingBox()
        

    def SetBrushes(self):
        self.Brushes = []
        for FillColor, FillStyle in zip(self.FillColors, self.FillStyles):
            if FillColor is None or FillStyle is None:
                self.Brush = wx.TRANSPARENT_BRUSH
            else:
                self.Brushes.append(self.BrushList.setdefault( (FillColor, FillStyle),
                                                               wx.Brush( FillColor, self.FillStyleList[FillStyle] )
                                                              )
                                    )
    def CalcBoundingBox(self):
        if self.Scaled:
            self.BoundingBox = BBox.asBBox( ((self.XY-self.Diameter),(self.XY+self.Diameter)) )
        else:
            self.BoundingBox = BBox.asBBox((self.XY, self.XY))
        if self._Canvas:
            self._Canvas.BoundingBoxDirty = True

    def _Draw(self, dc , WorldToPixel, ScaleWorldToPixel, HTdc=None):
        CenterXY = WorldToPixel(self.XY)
        if self.Scaled:
            CirclePoints = WorldToPixel(self.Points)
        else:
            CirclePoints = self.Points + CenterXY
        dc.SetPen(self.Pen)
        for i, brush in enumerate(self.Brushes):
            dc.SetBrush( brush )
            dc.DrawArcPoint(CirclePoints[i], CirclePoints[i+1], CenterXY)
        if HTdc and self.HitAble:
            if self.Scaled:
                radius = (ScaleWorldToPixel(self.Diameter)/2)[0]# just the x-coord
            else:
                radius = self.Diameter/2
            HTdc.SetPen(self.HitPen)
            HTdc.SetBrush(self.HitBrush)
            HTdc.DrawCirclePoint(CenterXY, radius)
