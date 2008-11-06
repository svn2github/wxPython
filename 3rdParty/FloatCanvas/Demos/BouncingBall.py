#!/usr/bin/env python

"""
A test of some simple animation

this is very old-style code: don't imitate it!

"""

import wx
import numpy as np

## import local version:
import sys

ver = 'local'
#ver = 'installed'

if ver == 'installed': ## import the installed version
    from wx.lib.floatcanvas import NavCanvas
    from wx.lib.floatcanvas import FloatCanvas
    print "using installed version:", wx.lib.floatcanvas.__version__
elif ver == 'local':
    ## import a local version
    import sys
    sys.path.append("..")
    from floatcanvas import NavCanvas
    from floatcanvas import FloatCanvas


class Ball(FloatCanvas.Circle):
    def __init__(self, XY, Velocity):
        self.Velocity = np.asarray(Velocity, np.float).reshape((2,))
        FloatCanvas.Circle.__init__(self, XY, Diameter=4, FillColor="red")

class DrawFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)
        
        ## Set up the MenuBar
        
        MenuBar = wx.MenuBar()
        
        file_menu = wx.Menu()
        item = file_menu.Append(wx.ID_ANY, "E&xit","Terminate the program")
        self.Bind(wx.EVT_MENU, self.OnQuit, item)
        MenuBar.Append(file_menu, "&File")
        
       
        self.SetMenuBar(MenuBar)
                
        self.CreateStatusBar()
        self.SetStatusText("")
        
        wx.EVT_CLOSE(self, self.OnCloseWindow)

        # Add a button
        StartButton = wx.Button(self, label="Start")
        StartButton.Bind(wx.EVT_BUTTON, self.OnStart)
        
        # Add the Canvas
        NC = NavCanvas.NavCanvas(self, -1, (500,500),
                                      Debug = False,
                                      BackgroundColor = "BLUE")
        
        self.Canvas = NC.Canvas
        self.Initialize(None)

        # lay it out:
        S = wx.BoxSizer(wx.VERTICAL)
        S.Add(StartButton, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        S.Add(NC, 1, wx.EXPAND)
        self.SetSizer(S)
        
        self.Show(True)
        
    def OnQuit(self,event):
        self.Close(True)
        
    def OnCloseWindow(self, event):
        self.Destroy()
        
    def Initialize(self, event=None):
        Canvas = self.Canvas   
        
        #Add a rectangle to set the domain size
        Canvas.AddRectangle((0, 0), (100, 100), FillColor=None, LineWidth=2, LineColor="Black")

        # add the wall:
        Canvas.AddRectangle( (0,0), (10,50), FillColor='green')

        # add the ball:
        self.Ball = Canvas.AddObject( Ball( (5, 52), (1,1) ) )
        
        wx.CallAfter(Canvas.ZoomToBB)
        
    def OnStart(self, event):
        print "in OnStart"
        self.Ball.SetPoint( (5, 52) )
        self.Ball.SetPoint( (5, 52) )
        self.Ball.Velocity = np.array((1.5, 0.0))
        
        self.timerID = wx.NewId()
        self.timer   = wx.Timer(self,self.timerID)
        wx.EVT_TIMER(self, self.timerID, self.MoveBall)
        self.timer.Start(10)

    def MoveBall(self, event=None):
        dt = .1
        g = 9.806
        m = 1
        Cd = 0.05
        vel = self.Ball.Velocity
        pos = self.Ball.XY

        # check if it's on the wall
        if pos[1] <= 102 and pos[0] <= 10:
            #reverse velocity
            vel[1] = 0
        # check if it's hit the floor
        elif pos[1] <= 2:
            #reverse velocity
            vel[1] *= -1
        else:
            # apply gravity
            vel[1] -= g * dt 
            # apply drag
            vel -= (Cd*vel**2) / m * dt
        # move the ball
        pos += dt * vel 
    
        self.Canvas.Draw(True)
        wx.GetApp().Yield()
    
class DemoApp(wx.App):
    def OnInit(self):
        frame = DrawFrame(None, -1, "Simple Drawing Window",wx.DefaultPosition, (700,700) )

        self.SetTopWindow(frame)

        return True
  
if __name__ == "__main__":

    app = DemoApp(0)
    app.MainLoop()
 
 