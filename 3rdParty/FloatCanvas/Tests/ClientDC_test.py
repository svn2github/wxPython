#!/usr/bin/env python

"""
A simple test for drawing multiple times to a ClientDC from inside an event

"""
import wx
import random
import time

NumToDraw = 1000

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)
        
        # put a "Animate" button in
        B = wx.Button(self, label="Run")
        B.Bind(wx.EVT_BUTTON, self.OnRun)
        #B.Bind(wx.EVT_BUTTON, self.OnRun2)
        
        # A Panel to do the animation on
        self.DrawPanel = wx.Panel(self)
        self.DrawPanel.SetBackgroundColour(wx.RED)

        S = wx.BoxSizer(wx.VERTICAL)
        S.Add(B, 0, wx.ALIGN_CENTER|wx.ALL, 10)
        S.Add(self.DrawPanel, 1, wx.EXPAND)
        
        self.SetSizer(S)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        
    def OnPaint(self, evt):
        print "Ini OnPaint"
        pass

    def OnRun2(self, evt):
        print "Drawing"
        dc = wx.ClientDC(self.DrawPanel)
        dc.Clear()
        del dc
        w = 30
        h = 20
        pw, ph = self.DrawPanel.Size
        start = time.clock()
        for i in xrange(NumToDraw):
            print "drawing %i"%i
            dc = wx.ClientDC(self.DrawPanel)
            dc.SetPen(wx.TRANSPARENT_PEN)
            dc.SetBrush(wx.BLUE_BRUSH)
            dc.SetTextForeground(wx.Colour(255,255,255))
            dc.SetTextBackground(wx.Colour(255,0,0))
            x = random.randint(0, pw)
            y = random.randint(0, ph)
            dc.DrawRectangle(x, y, w, h)
            dc.DrawText(`i`, x+4, y+2)
            del dc
            self.DrawPanel.Update()
            # something to create a delay
            #for x in range(1000):
            #    z = x**10
        print "It took %f seconds to draw"%(time.clock() - start)

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
        start = time.clock()

        for i in xrange(NumToDraw):
            x = random.randint(0, pw)
            y = random.randint(0, ph)
            dc.DrawRectangle(x, y, w, h)
            dc.DrawText(`i`, x+4, y+2)
            self.DrawPanel.Update()
            # something to create a delay
            #for x in range(1000):
            #    z = x**10
        print "It took %f seconds to draw"%(time.clock() - start)


A = wx.App(0)
F = MyFrame(None, size=(600,600))
F.Show()
A.MainLoop()


        
        
        