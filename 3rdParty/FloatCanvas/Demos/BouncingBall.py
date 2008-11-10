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
    def __init__(self, XY, Velocity, Radius=2.0):
        self.Velocity = np.asarray(Velocity, np.float).reshape((2,))
        self.Radius = Radius
        FloatCanvas.Circle.__init__(self, XY, Diameter=Radius*2, FillColor="red", InForeground=False)

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

        # Add the  buttons
        ResetButton = wx.Button(self, label="Reset")
        ResetButton.Bind(wx.EVT_BUTTON, self.OnReset)

        StartButton = wx.Button(self, label="Start")
        StartButton.Bind(wx.EVT_BUTTON, self.OnStart)
       
        StopButton = wx.Button(self, label="Stop")
        StopButton.Bind(wx.EVT_BUTTON, self.OnStop)

        butSizer = wx.BoxSizer(wx.HORIZONTAL)
        butSizer.Add(StartButton, 0, wx.RIGHT, 5 )
        butSizer.Add(ResetButton, 0, wx.RIGHT, 5)
        butSizer.Add(StopButton, 0, )
        # Add the Canvas
        NC = NavCanvas.NavCanvas(self, -1, (500,500),
                                      Debug = False,
                                      BackgroundColor = "BLUE")
        
        self.Canvas = NC.Canvas
        self.Initialize(None)

        # lay it out:
        S = wx.BoxSizer(wx.VERTICAL)
        S.Add(butSizer, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        S.Add(NC, 1, wx.EXPAND)
        self.SetSizer(S)

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.MoveBall, self.timer)

        self.Show(True)
        
    def OnQuit(self,event):
        self.Close(True)
        
    def OnCloseWindow(self, event):
        self.Destroy()
        
    def Initialize(self, event=None):
        Canvas = self.Canvas   
        
        #Add a rectangle to set the domain
        Canvas.AddRectangle((0, 0), (100, 100), FillColor=None, LineWidth=2, LineColor="Black")

        # add the wall:
        Canvas.AddRectangle( (0,0), (10,50), FillColor='green')

        # add the ball:
        self.Ball = Ball( (5, 52), (2, 0) ) 
        Canvas.AddObject( self.Ball )
        
        wx.CallAfter(Canvas.ZoomToBB)
        
    def OnReset(self, event):
        self.Ball.SetPoint( (5, 52) )
        self.Ball.Velocity = np.array((1.5, 0.0))
        self.Canvas.Draw(True)
        
    def OnStart(self, event):
        self.timer.Start(20)

    def OnStop(self, event):
        self.timer.Stop()

    def MoveBall(self, event=None):
        dt = .1
        g = 9.806
        m = 1
        Cd = 0.05
        ball = self.Ball
        vel = ball.Velocity
        pos = ball.XY

        # check if it's on the wall
        if pos[1] <= 102 and pos[0] <= 10:
            #reverse velocity
            vel[1] = 0
        # check if it's hit the floor
        elif pos[1] <= ball.Radius:
            #reverse velocity
            vel[1] *= -1.0
        else:
            # apply gravity
            vel[1] -= g * dt 
            # apply drag
            vel -= (Cd*vel**2) / m * dt
        # move the ball
        pos += dt * vel 
        if pos[1] < ball.Radius:
            # push to the surface:
            pos[1] = ball.Radius    

        #print "The ball is at:", pos, "with vel:", vel
        self.Ball.SetPoint( pos ) 
        
        self.Canvas.Draw(True)
        #wx.GetApp().Yield(onlyIfNeeded=True)
        
class DemoApp(wx.App):
    def OnInit(self):
        frame = DrawFrame(None, -1, "Simple Drawing Window",wx.DefaultPosition, (700,700) )

        self.SetTopWindow(frame)

        return True
  
if __name__ == "__main__":

    app = DemoApp(0)
    app.MainLoop()
 
 