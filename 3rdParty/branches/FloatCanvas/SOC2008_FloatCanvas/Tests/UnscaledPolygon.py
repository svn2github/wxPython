
import numpy as N
from FloatCanvas import Polygon, XYObjectMixin

class UnscaledPolygon(XYObjectMixin, Polygon):
    """\
    Draws a polygon which always has the same pixel size.
    """

    def __init__(self,
                 XY,
                 Points,
                 Offset=(0,0)
                 **kw): # All the same keywords as Polygon.
        self.XY = N.array(XY, N.float).reshape( (2,) )

        Polygon.__init__(self, Points, LineColor=Color, FillColor=Color, InForeground=InForeground, **kw)

        self.SetOffset(Offset)

    def SetOffset(self, Offset):
        self.Offset = N.array(Offset, N.float).reshape((2,))# Make sure it is a length 2 vector

    def _Draw(self, dc , WorldToPixel, ScaleWorldToPixel = None, HTdc=None):
        print "Drawing UnscaledPolygon"
        Points = self.Points + self.Offset + WorldToPixel(self.XY)

        dc.SetPen(self.Pen)
        dc.SetBrush(self.Brush)
        dc.DrawPolygon(Points)
        if HTdc and self.HitAble:
            HTdc.SetPen(self.HitPen)
            HTdc.SetBrush(self.HitBrush)
            HTdc.DrawPolygon(Points)

class PolygonArrow(PolygonStatic):
    def __init__(self, XY, *args, **kw):
        kw['LineWidth'] = 1
        PolygonStatic.__init__(self, XY, [(0,0), (-5,-10), (0, -8), (5,-10)], *args, **kw)

class PolygonShip(PolygonStatic):
    def __init__(self, XY, *args, **kw):
        kw['LineWidth'] = 1
        PolygonStatic.__init__(self, XY, [(0,0), (3,0), (0,4), (0,2), (-3,0)], *args, **kw)

