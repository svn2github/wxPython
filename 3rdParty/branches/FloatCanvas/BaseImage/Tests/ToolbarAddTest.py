"""

And test adding tools to a toolbar after the fact.

"""

import wx
#---------------------------------------------------------------------------

class TestCanvas(wx.Panel):

    def __init__(self,
                   parent,
                   id = wx.ID_ANY,
                   size = wx.DefaultSize,
                   **kwargs): # The rest just get passed into FloatCanvas
        wx.Panel.__init__(self, parent, id, size=size)

        self.BuildToolbar()
        ## Create the vertical sizer for the toolbar and Panel
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self.ToolBar, 0, wx.ALL | wx.ALIGN_LEFT | wx.GROW, 4)

        self.Panel = wx.Panel(self)
        box.Add(self.Panel, 1, wx.GROW)

        self.SetSizerAndFit(box)

        return None

    def BuildToolbar(self):
        tb = wx.ToolBar(self)
        self.ToolBar = tb

        self.Buttons = []
        for l in ("But1", "But2", "But3"):
            But = wx.Button(tb, label=l)
            tb.AddControl(But)
            But.Bind(wx.EVT_BUTTON, self.OnBut)
            self.Buttons.append(But)

        tb.Realize()
        ## fixme: remove this when the bug is fixed!
        wx.CallAfter(self.HideShowHack) # this required on wxPython 2.8.1 onm OS-X

        return tb

    def HideShowHack(self):
        ##fixme: remove this when the bug is fixed!
        """
        Hack to hide and show button on toolbar to get around OS-X bug on
        wxPython2.8 on OS-X
        """
        for b in self.Buttons:
            b.Hide()
            b.Show()

    def OnBut(self, Event):
        print "%s clicked"%(Event.GetEventObject().GetLabel())

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)
        
        P = TestCanvas(self)
        
        # Add some buttons to the Toolbar
        tb = P.ToolBar

        ClearButton = wx.Button(tb, wx.ID_ANY, "Clear")
        tb.AddControl(ClearButton)
        ClearButton.Bind(wx.EVT_BUTTON, self.Clear)

        tb.Realize()

    def Clear(self, evt):
        print "Clear button clicked"

if __name__ == "__main__":
    a = wx.App(False)
    f = MyFrame(None)
    f.Show()
    a.MainLoop()