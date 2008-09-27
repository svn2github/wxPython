''' Shows various way how to create nodes on the canvas '''

import sys
import os.path
sys.path.append( os.path.abspath( '..' ) )

import wx
import floatcanvas as fc

class TestFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)
        self.canvas = canvas = fc.FloatCanvas(window=self)

        r1 = canvas.create( 'Rectangle',
                            (100, 200),
                            look = fc.SolidColourLook( line_colour = 'blue', fill_colour = 'red' )
                            )
        semiTransparentGradientLook = fc.RadialGradientLook( 'blue',
                                                             (0,0),
                                                             (255,0,0,64),
                                                             (0,0),
                                                             200,
                                                             (0,0,255,128)
                                                             )
        r2 = canvas.createRectangle( (200, 100),
                                     position = (100, 100),
                                     look = semiTransparentGradientLook
                                      )
        r3 = canvas.create( 'Rectangle',
                            (20, 20),
                            look = ( 'red', 'black' ),
                            name = 'Rectangle 3',
                            where = 'front' )
        linearGradientLook = fc.LinearGradientLook( 'green',
                                                    (-100,-100),
                                                    (255, 255, 0, 64),
                                                    (100,100),
                                                    (0,255,0,128)
                                                    )
        r5 = canvas.create( 'Rectangle',
                            (150, 150),
                            look = linearGradientLook,
                            position = (200, 200),
                            rotation = 45,
                            scale = (2, 1),
                            parent = r2,
                            name = 'Child',
                            where = 'front' )
        #mr = canvas.createPoints( [(70, 70)],
        #                          transform = 'MercatorTransform',
        #                          look = semiTransparentGradientLook,
        #                          name = 'mercator' )
        #mr.scale = (1, 100)

        # the default cam, looking at 500, 500
        canvas.camera.position = (0, 0)
        canvas.camera.zoom = (1.0, 1.0)

        wx.CallAfter(self.RunSequence)

    def RunSequence(self):
        import time
        canvas = self.canvas
        #for i in range(200):
        for i in range(10):
            print "interation: %i"%i
        for i in (0):
            canvas.camera.position = (0, 0)
            canvas.camera.rotation = i
            zoom = 1 + abs(i - 50) / 50.0
            canvas.camera.zoom = ( zoom, zoom )
            canvas.Render()
            wx.GetApp().Yield()
            #time.sleep(0.01)

def start():
    #  setup very basic window
    app = wx.App(0)
    
    frame = TestFrame(None,
                      title='FloatCanvas2 demo',
                      size=(800, 600)
                      )
    frame.Show()        
    app.MainLoop()

if __name__ == '__main__':
    start()
