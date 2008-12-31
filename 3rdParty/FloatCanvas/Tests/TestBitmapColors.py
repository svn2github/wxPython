#!/usr/bin/env python
"""

A very simple app for testing what colors go into and out of a wx.Bitmap

"""


import wx

Size = (200, 200)


class DemoApp(wx.App):
    def OnInit(self):
        #frame = TestFrame()
        #frame.Show(True)

        #Start, Stop, Step = (0, 200, 10)
        Start, Stop, Step = (0, 200, 20)
        Depth = 24

        B = wx.EmptyBitmap(Size[0], Size[1], depth=24)
        #B = wx.EmptyBitmap(Size[0], Size[1])
        print "Bitmap depth is:", B.GetDepth()
        #raise Exception("stopping")
        dc = wx.MemoryDC()
        dc.SelectObject(B)

        dc.SetBackground(wx.BLACK_BRUSH)
        dc.Clear()
        del dc

        i = 0
        j = 0
        for r in range(Start, Stop, Step):
            for g in range(Start, Stop, Step):
                for b in range(Start, Stop, Step):
                    i+=1
                    if i >= Size[0]:
                        i = 0
                        j += 1
                    if j >= Size[1]:
                        raise Exception("Too many color tests for bitmap size") 
                    inColor = (r,g,b)
                    print "Drawing:", inColor, "To pixel:", (i,j)

                    dc = wx.MemoryDC(B)
                    dc.SetPen(wx.Pen(wx.Color(*inColor), 4))
                    dc.DrawPoint(i,j)
                    del dc
                    
                    print "Bitmap depth is:", B.GetDepth()
                    pdata = wx.AlphaPixelData(B)
                    pacc = pdata.GetPixels()
                    pacc.MoveTo(pdata, i,j)
                    outColor = pacc.Get()[:3]
                    
                    print "Got", outColor
                    if inColor != outColor:
                        print "Error!!, inColor = %s, outColor = %s at pixel: %s"%(inColor, outColor, (i,j) )

        B.SaveFile("junk.png", wx.BITMAP_TYPE_PNG )
        
        return True

if __name__ == "__main__":
    app = DemoApp(False)
    app.MainLoop()




















