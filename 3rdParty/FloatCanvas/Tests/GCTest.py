#/usr/bin/env python

"""
A simmple test for GraphicsContext

"""
import wx


class MyFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        
    def OnPaint(self, evt):
        print "In OnPaint"
        
        DC = wx.PaintDC(self)
        self.Draw(DC)
    
    def Draw(self, DC):
        print "In Draw"
        DC.SetBackground(wx.Brush("White"))
        DC.Clear()
        
        GC = wx.GraphicsContext.Create(DC)
        
        Pen = GC.CreatePen(wx.Pen("Black", 4))
        
        GC.SetPen(Pen)
        GC.DrawLines([(0,0),(100,100),(300,100)])
        GC.SetPen(wx.TRANSPARENT_PEN)
        c1 = wx.Color(255, 0, 0, 255)
        c2 = wx.Color(255, 0, 0, 0)
        Brush = GC.CreateLinearGradientBrush(20, 150, 300, 150, c1, c2)
        GC.SetBrush(Brush)
        GC.DrawRectangle(20, 150, 200, 1)
        
A = wx.App(0)
F = MyFrame(None)
F.Show()
A.MainLoop()


        
        
        