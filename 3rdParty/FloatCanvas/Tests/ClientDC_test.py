#!/usr/bin/env python

"""
A simple test for drawing multiple times to a ClientDC from inside an event

"""
import wx
import random

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)
        
        # put a "Animate" button in
        B = wx.Button(self, label="Run")
        B.Bind(wx.EVT_BUTTON, self.OnRun)
        
        # A Panel to do the animation on
        self.DrawPanel = wx.Panel(self)
        self.DrawPanel.SetBackgroundColour(wx.RED)

        S = wx.BoxSizer(wx.VERTICAL)
        S.Add(B, 0, wx.ALIGN_CENTER|wx.ALL, 10)
        S.Add(self.DrawPanel, 1, wx.EXPAND)
        
        self.SetSizer(S)
        #self.Bind(wx.EVT_PAINT, self.OnPaint)
        
    def OnRun(self, evt):
        print "Drawing"
        dc = wx.ClientDC(self.DrawPanel)
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.SetBrush(wx.BLUE_BRUSH)
        dc.SetTextForeground(wx.Colour(255,255,255))
        dc.SetTextBackground(wx.Colour(255,0,0))
        
        dc.Clear()
        w = 30
        h = 20
        pw, ph = self.DrawPanel.Size
        for i in xrange(1000):
            x = random.randint(0, pw)
            y = random.randint(0, ph)
            dc.DrawRectangle(x, y, w, h)
            dc.DrawText(`i`, x+4, y+2)
            # something to create a delay
            for x in range(1000):
                z = x**10
        
    
#    def Draw(self, DC):
#        print "In Draw"
#        DC.SetBackground(wx.Brush("White"))
#        DC.Clear()
#        
#        GC = wx.GraphicsContext.Create(DC)
#        
#        Pen = GC.CreatePen(wx.Pen("Black", 4))
#        
#        GC.SetPen(Pen)
#        GC.DrawLines([(0,0),(100,100),(300,100)])
#        GC.SetPen(wx.TRANSPARENT_PEN)
#        c1 = wx.Color(255, 0, 0, 255)
#        c2 = wx.Color(255, 0, 0, 0)
#        Brush = GC.CreateLinearGradientBrush(20, 150, 300, 150, c1, c2)
#        GC.SetBrush(Brush)
#        GC.DrawRectangle(20, 150, 200, 1)
#        
#        Path = GC.CreatePath()
#        Path.MoveToPoint(0,0)
#        Path.AddLineToPoint(500,300)
#        Path.AddLineToPoint(500,298)
#        Path.AddLineToPoint(0,-2)
#        
#        GC.SetPen(wx.Pen("Blue", 3))
#        #GC.SetBrush(wx.Brush("Red"))
#        #GC.DrawPath(Path)
#        Brush = GC.CreateLinearGradientBrush(-2, -2, 500, 300, c1, c2)
#        GC.SetBrush(Brush)
#        GC.FillPath(Path)
#        
A = wx.App(0)
F = MyFrame(None, size=(600,600))
F.Show()
A.MainLoop()


        
        
        