class DefaultUpdatePolicy(object):
    def __init__(self, canvas, interval):
        self.canvas = canvas
        self.interval = interval * 1000
        self.dirty = False
        import wx
        self.timer = wx.CallLater( self.interval , self.onIntervalOver )
        
    def onDirty(self):
        self.dirty = True
            
    def onIntervalOver(self):
        self.Render()
        self.timer.Restart( self.interval )
        
    def Render(self):
        if self.dirty:
            print 'RENDER'
            self.canvas.Render()
            self.dirty = False
