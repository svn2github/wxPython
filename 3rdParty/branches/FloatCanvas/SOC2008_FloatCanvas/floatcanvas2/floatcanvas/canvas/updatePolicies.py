''' Analogous to render policy a update policy controls when and how the canvas
    is updated.
'''

import wx
class DefaultUpdatePolicy(object):
    ''' A simple update policy. It is notified when the canvas needs to be
        updated (repainted) and then performs the updates at specified
        intervals.
        This allows lots of changes to pile up and then render them from time
        to time. This way the canvas is not redrawn for each change
        individually.
    '''
    def __init__(self, canvas, interval):
        ''' interval in seconds '''
        self.canvas = canvas
        self.interval = interval
        self.dirty = False
        self.timer = wx.CallLater( self.interval * 1000, self.onIntervalOver )
        
    def stop(self):
        self.timer.Stop()
        
    def onDirty(self):
        self.dirty = True
            
    def onIntervalOver(self):
        self.Render()
        self.timer.Restart( self.interval * 1000 )
        
    def Render(self):
        if self.dirty:
            #print 'RENDER'
            self.canvas.Render()
            self.dirty = False
