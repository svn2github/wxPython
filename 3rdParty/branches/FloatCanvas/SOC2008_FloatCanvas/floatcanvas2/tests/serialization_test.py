import sys
import os.path
sys.path.append( os.path.abspath( '..' ) )

import unittest
from floatcanvas.nodes import Node, TextTreeFormatVisitor, FindNodesByNamesVisitor, GetNodesAsFlatListVisitor
from floatcanvas.nodes import NodeWithTransform
from floatcanvas import NodeWithTransform, MercatorTransform, LinearAndArbitraryCompoundTransform, LinearTransform2D
from floatcanvas.canvas.observables import ObservableRectangle, ObservableDefaultRenderableNode
from floatcanvas.serialization import Serializer
import floatcanvas as fc
import wx

class TestNode(unittest.TestCase):
    def setUp(self):
        self.serializer = Serializer()

    def tearDown(self):
        pass
    
    def doSaveLoad(self, input_data):
        s = self.serializer
        data = s.serialize( input_data )
        return s.unserialize(data)

    def testSimpleNode(self):
        node = Node( name = 'simple node' )
        self.doSaveLoad( node )  

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
        
        
    def testRenderableNode(self):
        o = ObservableDefaultRenderableNode( model = None, view = None, transform = LinearTransform2D(), render_to_surface_enabled = False, renderer = None )

        o = self.doSaveLoad( o )

    def testRenderableNodeWithModel(self):        
        model = ObservableRectangle( (10, 10) )
        o = ObservableDefaultRenderableNode( model = model, view = None, transform = LinearTransform2D(), render_to_surface_enabled = False, renderer = None )
    
        o = self.doSaveLoad( o )
        
        
    def testLook(self):
        app = wx.App(0)
        frame = wx.Frame( None, wx.ID_ANY, 'FloatCanvas2 demo', size = (800, 600) )
        frame.Show()
            
        canvas = fc.FloatCanvas( window = frame )

        look = fc.SolidColourLook( line_colour = 'blue', fill_colour = 'red' )
        look.Apply( canvas.renderer )

        look = self.doSaveLoad( look )

    #def testView(self):
    #    app = wx.App(0)
    #    frame = wx.Frame( None, wx.ID_ANY, 'FloatCanvas2 demo', size = (800, 600) )
    #    frame.Show()
    #        
    #    canvas = fc.FloatCanvas( window = frame )
    #
    #    look = fc.SolidColourLook( line_colour = 'blue', fill_colour = 'red' )
    #    r = canvas.create( 'Rectangle', (100, 100), look = look  )
    #
    #    view = self.doSaveLoad( r.view )
    #
    #
    #def testRenderableNodeWithModelAndView(self):
    #    app = wx.App(0)
    #    frame = wx.Frame( None, wx.ID_ANY, 'FloatCanvas2 demo', size = (800, 600) )
    #    frame.Show()
    #        
    #    canvas = fc.FloatCanvas( window = frame )
    #
    #    look = fc.SolidColourLook( line_colour = 'blue', fill_colour = 'red' )
    #    r = canvas.create( 'Rectangle', (100, 100), look = look  )
    #    r.parent = None
    #
    #    r = self.doSaveLoad( r )
        
    #def testCanvas(self):
    #    app = wx.App(0)
    #    frame = wx.Frame( None, wx.ID_ANY, 'FloatCanvas2 demo', size = (800, 600) )
    #    frame.Show()
    #        
    #    canvas = fc.FloatCanvas( window = frame )
    #
    #    look = fc.SolidColourLook( line_colour = 'blue', fill_colour = 'red' )
    #    r = canvas.create( 'Rectangle', (100, 100), look = look  )
    #
    #    c = self.doSaveLoad( c )

if __name__ == '__main__':
    unittest.main()
