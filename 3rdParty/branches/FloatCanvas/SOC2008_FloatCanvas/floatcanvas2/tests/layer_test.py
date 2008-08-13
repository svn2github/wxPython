''' Tests layer functionality (a group with children rendered to a surface) '''

import sys
import os.path
sys.path.append( os.path.abspath( '..' ) )

import wx
import floatcanvas as fc


def start():
    #  setup very basic window
    app = wx.App(0)
    frame = wx.Frame( None, wx.ID_ANY, 'FloatCanvas2 demo', size = (800, 600) )
    frame.Show()
        
    canvas = fc.FloatCanvas( window = frame, backgroundColor = 'white' )
    #canvas.dirty = False

    parent = canvas.create( 'Group', name = 'group node', pos = (100, 0), render_to_surface = True, surface_size = (800, 100) )
    # create 1000 rectangles
    for i in range(0, 50):
        r = canvas.create( 'Circle', 80, parent = parent, name = 'r%d' % i, pos = (i * 50, 0), look = fc.SolidColourLook( line_colour = 'blue', fill_colour = (255,0,0,128) )  )
        #r._debugDrawBoundingBoxes = True

    # the default cam, looking at 0, 0
    canvas.camera.position = (0, 0)
    canvas.camera.rotation = 0
    canvas.camera.zoom = (0.8, 0.8)
    
    def print_culled_nodes():
        try:
            print 'rendered %d nodes' % ( len(canvas.renderPolicy.renderedNodes), )
            #print r.boundingBox
            #for node in canvas.renderPolicy.renderedNodes:
            #    print node.name
        except AttributeError:
            pass
    
    rotate = True
    if rotate:
        import time
        for i in range(-600, 3000, 5):
            #parent.rotation = i
            canvas.camera.position = (i, 0)
            canvas.Render()
            print_culled_nodes()
            #time.sleep(0.01)
        
    wx.CallLater( 1000, print_culled_nodes )
    
    app.MainLoop()

if __name__ == '__main__':
    #import cProfile
    #cProfile.run('start()', 'profiling_data_cProfile')
    start()
