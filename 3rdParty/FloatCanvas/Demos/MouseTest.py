#!/usr/bin/env python

"""
Small demo of catching Mouse events using just FloatCanvas, rather than
NavCanvas

"""

import wx

try:
    # See if there is a local copy
    import sys
    sys.path.append("../")
    from floatcanvas import NavCanvas, FloatCanvas, GUIMode
except ImportError:
    from wx.lib.floatcanvas import NavCanvas, FloatCanvas

class TestFrame(wx.Frame):
    
    def __init__(self, *args, **kwargs):

        wx.Frame.__init__(self, *args, **kwargs)
        self.canvas =FloatCanvas.FloatCanvas(self, BackgroundColor = "DARK SLATE BLUE")
        
        # Layout
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        MainSizer.Add(self.canvas, 4, wx.EXPAND)
        
        self.SetSizer(MainSizer)
        
        self.canvas.Bind(FloatCanvas.EVT_LEFT_DOWN, self.OnLeftDown)

        self.canvas.AddRectangle((10,10), (100, 20), FillColor="red")
        
        self.canvas.SetMode(GUIMode.GUIMouse(self.canvas))
        #self.canvas.SetMode(GUIMode.GUIZoomIn(self.canvas))
        
        wx.CallAfter(self.canvas.ZoomToBB)
                        

    def OnLeftDown(self, event):
        print 'Left Button clicked at:', event.Coords

class App1(wx.App):

    def OnInit(self):
        frame = TestFrame(None, title="Mouse Event Tester")
        frame.Show(True)
        self.SetTopWindow(frame)
        return True
    
app = App1(0)

app.MainLoop()

