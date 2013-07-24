#!/usr/bin/env python
"""

This is a demo, showing how to work with a "tree" structure

It demonstrates moving objects around, etc, etc.

"""

import wx

ver = 'installed'

from wx.lib.floatcanvas import NavCanvas, Resources
from wx.lib.floatcanvas import FloatCanvas as FC
from wx.lib.floatcanvas.Utilities import BBox
print "using installed version:", wx.lib.floatcanvas.__version__

import numpy as np

## here we create some new mixins:
## fixme: These really belong in floatcanvas package -- but I kind of want to clean it up some first

class MovingObjectMixin:
    """
    Methods required for a Moving object
    
    """
    def GetOutlinePoints(self):
        """
        Returns a set of points with which to draw the outline when moving the 
        object.
        
        Points are a NX2 array of (x,y) points in World coordinates.
        
        
        """
        BB = self.BoundingBox
        OutlinePoints = np.array( ( (BB[0,0], BB[0,1]),
                                   (BB[0,0], BB[1,1]),
                                   (BB[1,0], BB[1,1]),
                                   (BB[1,0], BB[0,1]),
                                 )
                               )

        return OutlinePoints

class ConnectorObjectMixin:
    """
    Mixin class for DrawObjects that can be connected with lines
    
    Note that this version only works for Objects that have an "XY" attribute:
      that is, one that is derived from XHObjectMixinp.
    
    """
    
    def GetConnectPoint(self):
        return self.XY
        
class MovingBitmap(FC.ScaledBitmap, MovingObjectMixin, ConnectorObjectMixin):
    """
    ScaledBitmap Object that can be moved
    """
    ## All we need to do is is inherit from:
    ##  ScaledBitmap, MovingObjectMixin and ConnectorObjectMixin
    pass
    
class MovingCircle(FC.Circle, MovingObjectMixin, ConnectorObjectMixin):
    """
    ScaledBitmap Object that can be moved
    """
    ## All we need to do is is inherit from:
    ##  Circle MovingObjectMixin and ConnectorObjectMixin
    pass


class MovingGroup(FC.Group, MovingObjectMixin, ConnectorObjectMixin):
    
    def GetConnectPoint(self):
        return self.BoundingBox.Center
        


class NodeObject(FC.Group, MovingObjectMixin, ConnectorObjectMixin):
    """
    A version of the moving group for nodes -- an ellipse with text on it.
    """
    def __init__(self,
                 Label,
                 XY,
                 Diameter,
                 TextColor= "Black", 
                 LineColor = "Black",
                 LineStyle = "Solid",
                 LineWidth    = 1,
                 FillColor    = None,
                 FillStyle    = "Solid",
                 InForeground = False,
                 IsVisible = True):
        self.XY = np.asarray(XY, np.float).reshape(2,)

        Label = FC.ScaledText(Label,
                        self.XY,
                        Size = Diameter / 2.0,
                        Color = TextColor,
                        Position = 'cc',
                        )
        self.Circle = FC.Circle( self.XY,
                                 Diameter,
                                 FillColor = FillColor,
                                 LineStyle = None,
                                 )
        FC.Group.__init__(self, [self.Circle, Label], InForeground, IsVisible)

    def GetConnectPoint(self):
        return self.XY
        
class ConnectorLine(FC.LineOnlyMixin, FC.DrawObject,):
    """

    A Line that connects two objects -- it uses the objects to get its coordinates
    The objects must have a GetConnectPoint() method.

    """
    ##fixme: this should be added to the Main FloatCanvas Objects some day.
    def __init__(self,
                 Object1,
                 Object2,
                 LineColor = "Black",
                 LineStyle = "Solid",
                 LineWidth    = 1,
                 InForeground = False):
        FC.DrawObject.__init__(self, InForeground)

        self.Object1 =  Object1       
        self.Object2 =  Object2       
        self.LineColor = LineColor
        self.LineStyle = LineStyle
        self.LineWidth = LineWidth

        self.CalcBoundingBox()
        self.SetPen(LineColor,LineStyle,LineWidth)

        self.HitLineWidth = max(LineWidth,self.MinHitLineWidth)

    def CalcBoundingBox(self):
        self.BoundingBox = BBox.fromPoints((self.Object1.GetConnectPoint(),
                                            self.Object2.GetConnectPoint()) )
        if self._Canvas:
            self._Canvas.BoundingBoxDirty = True


    def _Draw(self, dc , WorldToPixel, ScaleWorldToPixel, HTdc=None):
        Points = np.array( (self.Object1.GetConnectPoint(),
                           self.Object2.GetConnectPoint()) )
        Points = WorldToPixel(Points)
        dc.SetPen(self.Pen)
        dc.DrawLines(Points)
        if HTdc and self.HitAble:
            HTdc.SetPen(self.HitPen)
            HTdc.DrawLines(Points)
    
    

### Tree Utilities (from Tim Hochberg on the wxPython list)


class Node(object):
    def __init__(self, rows, level, spot):
        if level < 6:
            self.left = Node(rows, level+1,spot*2+0)
            self.right = Node(rows, level+1,spot*2+1)
            self.x = (self.left.x + self.right.x) / 2
        else:
            self.x = spot * 10
        rows[level].append( self )



class DrawFrame(wx.Frame):

    """
    A simple frame used for the Demo

    """

    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)

        self.CreateStatusBar()            
        # Add the Canvas
        Canvas = NavCanvas.NavCanvas(self,-1,(500,500),
                                          ProjectionFun = None,
                                          Debug = 0,
                                          BackgroundColor = "White",
                                          ).Canvas
        
        self.Canvas = Canvas


        self.AddTree()    
        
        self.Show(True)
        self.Canvas.ZoomToBB()

        return None

    def AddTree(self):
        rows = [[],[],[],[],[],[],[]]
        tree = Node(rows, 0, 0 )
        base_diameter = 50.0

        y = 0
        Nodes = []
        for no, row in enumerate(rows):
            Nodes.append([])
            d = base_diameter/(no+1)
            y = y - (1.5*d)
            for ball in row:
                obj = NodeObject('X',
                                 (ball.x, y),
                                 d,
                                 FillColor = "Yellow",
                                 )
                Nodes[-1].append(obj)
        for no, row in enumerate(Nodes[1:]):
            for i in range(0,len(row)/2):
                Connector = ConnectorLine(row[2*i],   Nodes[no][i], LineWidth=2, LineColor="Red")
                self.Canvas.AddObject(Connector)
                Connector = ConnectorLine(row[2*i+1], Nodes[no][i], LineWidth=2, LineColor="Red")
                self.Canvas.AddObject(Connector)
        #Add the nodes to the canvas (on top of the connectors):
        for row in Nodes:
            for node in row:
                self.Canvas.AddObject(node)
app = wx.App(False)
DrawFrame(None,
          title="FloatCanvas Tree Demo App",
          size=(700,700) )
app.MainLoop()
