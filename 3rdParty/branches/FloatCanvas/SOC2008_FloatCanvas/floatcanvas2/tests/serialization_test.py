import sys
import os.path
sys.path.append( os.path.abspath( '..' ) )

import unittest
from floatcanvas.nodes import Node, TextTreeFormatVisitor, FindNodesByNamesVisitor, GetNodesAsFlatListVisitor
from floatcanvas.nodes import NodeWithTransform
from floatcanvas import NodeWithTransform, MercatorTransform, LinearAndArbitraryCompoundTransform, LinearTransform2D
from floatcanvas.canvas.observables import ObservableRectangle, ObservableDefaultRenderableNode
from floatcanvas.serialization import Serializer, defaultSerializers
import floatcanvas as fc
import wx

class TestNode(unittest.TestCase):
    def setUp(self):
        self.serializer = Serializer()
        defaultSerializers.registerDefaultSerializers( self.serializer.nodeSerializerRegistry )

    def tearDown(self):
        pass
    
    def doSaveLoad(self, input_data):
        s = self.serializer
        data = s.serializeNode( input_data )
        return s.unserializeNode(data)

    def testSimpleNode(self):
        node = Node( name = 'simple node' )
        node2 = self.doSaveLoad( node )
        self.assert_( node2.name == 'simple node' )        

    def testNodeWithChildren(self):
        children = [ Node( name = 'child %d' % i ) for i in range(0,5) ]
        parentNode = Node( name = 'parent' )
        
        parentNode.addChildren( children )
        
        root = self.doSaveLoad( parentNode )        
        self.assert_( root.children[4].parent is root )
        self.assert_( root.children[4].root is root )

        
    def testNodeWithTransform(self):
        child = NodeWithTransform( LinearTransform2D(), name = 'child' )
        parent = NodeWithTransform( LinearTransform2D(), name = 'parent' )
        child.parent = parent

        parent.position = (5,5)
       
        mercatorNode = NodeWithTransform( parent = child, transform = MercatorTransform(10) )
        mercatorNode.localTransform.longitudeCenter = 0
        
        root = self.doSaveLoad( parent )

        child = root.children[0]

        self.assert_( child.position.tolist() == [0,0], child.position )
        self.assert_( child.worldTransform.position.tolist() == [5,5], child.position )
        
        mercatorNode = child.children[0]
        self.assert_( isinstance(mercatorNode.localTransform, MercatorTransform), mercatorNode.localTransform )
        self.assert_( isinstance(mercatorNode.worldTransform, LinearAndArbitraryCompoundTransform), mercatorNode.worldTransform )        
        self.assert_( mercatorNode.worldPosition.tolist() == [5,5], mercatorNode.worldPosition )


    #def testRenderableNode(self):
    #    o = ObservableDefaultRenderableNode( model = None, view = None, transform = LinearTransform2D(), render_to_surface = False, surface_size = (0,0), renderer = None )
    #
    #    o = self.doSaveLoad( o )
    #
    #def testRenderableNodeWithModel(self):        
    #    model = ObservableRectangle( (10, 10) )
    #    o = ObservableDefaultRenderableNode( model = model, view = None, transform = LinearTransform2D(), render_to_surface = False, surface_size = (0,0), renderer = None )
    #
    #    o = self.doSaveLoad( o )


    def testRenderableNodeWithModelAndView(self):
        app = wx.App(0)
        frame = wx.Frame( None, wx.ID_ANY, 'FloatCanvas2 demo', size = (800, 600) )
        frame.Show()
            
        canvas = fc.FloatCanvas( window = frame )

        look = fc.SolidColourLook( line_colour = 'blue', fill_colour = 'red' )
        r = canvas.create( 'Rectangle', (100, 100), look = look  )

        self.serializer.canvas = canvas
        canvas2 = self.doSaveLoad( canvas )
        self.assert_( canvas is canvas2 )
        canvas.serializeToFile( 'test.fcsf' )


    def testLots(self):
        app = wx.App(0)
        frame = wx.Frame( None, wx.ID_ANY, 'FloatCanvas2 demo', size = (800, 600) )
        frame.Show()
            
        canvas = fc.FloatCanvas( window = frame )

        look = fc.SolidColourLook( line_colour = 'blue', fill_colour = 'red' )
        for i in range(0, 100):
            r = canvas.create( 'Rectangle', (100, 100), pos = (i * 50, 0), look = look  )

        canvas.serializeToFile( 'test_lots.fcsf' )
        
    def testLoadLots(self):
        app = wx.App(0)
        frame = wx.Frame( None, wx.ID_ANY, 'FloatCanvas2 demo', size = (800, 600) )
        frame.Show()
            
        canvas = fc.FloatCanvas( window = frame )

        def log(msg):
            print msg

        wx.CallLater( 2000, canvas.unserializeFromFile, 'test_lots.fcsf' )
        wx.CallLater( 2000, log, 'Unserialized' )
        wx.CallLater( 4000, frame.Close )
        app.MainLoop()
        
        
if __name__ == '__main__':
    unittest.main()
