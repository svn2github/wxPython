''' tests some screenshot functions
    @todo increase test coverage
'''

import sys
import os.path
sys.path.append( os.path.abspath( '..' ) )

import wx
import floatcanvas as fc


class MyFrame(wx.Frame):
  def __init__(self,p):
        wx.Frame.__init__(self,p, -1, )
        panel = wx.Panel(self, -1)
        self.SetBackgroundColour('WHITE')

        canvas = fc.NavCanvas(self)
        # try to take an empty screen shot
        image_background = canvas.getScreenshot('raw', False)
        print len(image_background)

        image_background = canvas.getScreenshot('jpg', False)
        print len(image_background)

        image_background = canvas.getScreenshot('jpg')
        print len(image_background)

        image_background = canvas.getScreenshot('raw')
        print len(image_background)

if __name__ == '__main__':
   app = wx.App(False)
   frame = MyFrame(None)
   frame.Show(True)
   app.MainLoop()
