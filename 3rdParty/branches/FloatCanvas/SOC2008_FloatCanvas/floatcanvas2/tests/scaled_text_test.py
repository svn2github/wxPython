import sys
import os.path
sys.path.append( os.path.abspath( '..' ) )

import wx
import floatcanvas as fc


class NodeScaler(object):
    def __init__(self, node, camera):
        self.node = node
        self.camera = camera
        camera.subscribe( self.update, 'attribChanged' )
        
    def update(self, evt):
        self.node.scale = self.camera.scale
    

def start():
    #  setup very basic window
    app = wx.App(0)
    frame = wx.Frame( None, wx.ID_ANY, 'FloatCanvas2 demo', size = (800, 600) )
    frame.Show()
        
    canvas = fc.NavCanvas( frame, backgroundColor = 'white' )
    
    box = canvas.createRectangle( (200, 100), look = ('black', None)  )
    text = canvas.createText( 'I am scaled', look = fc.TextLook( 14 ), parent = box  )
    
    ns = NodeScaler( box, canvas.camera )
    
    app.MainLoop()

if __name__ == '__main__':
    #import cProfile
    #cProfile.run('start()', 'profiling_data_cProfile')
    start()
