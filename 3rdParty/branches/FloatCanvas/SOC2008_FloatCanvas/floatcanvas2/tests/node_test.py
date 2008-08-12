import sys
import os.path
sys.path.append( os.path.abspath( '..' ) )

import unittest
from floatcanvas.nodes import Node, TextTreeFormatVisitor, FindNodesByNamesVisitor, GetNodesAsFlatListVisitor, EnumerateNodesVisitor

class TestNode(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testConstructor(self):
        children = [ Node() for i in range(0,5) ]
        parentNode = Node()

        self.assert_( parentNode.parent == None )
        self.assert_( parentNode.children == [] )

        node = Node( name = 'Some Node', parent = parentNode, children = children )

        self.assert_( node.name == 'Some Node' )
        self.assert_( node.parent == parentNode )
        self.assert_( node.children == children )

        self.assert_( parentNode.parent == None )
        self.assert_( parentNode.children == [ node ] )
        
    def testAddRemoveChildren(self):
        # test the add/remove functions
        children = [ Node() for i in range(0,5) ]
        parentNode = Node()
        
        parentNode.addChildren( children, where = 'front' )
        self.assert_( parentNode.children == children )
        
        child = Node()
        parentNode.addChild( child, where = 'back' )
        self.assert_( parentNode.children == children + [ child ] )
        self.assert_( child.parent == parentNode )
        
        parentNode.removeChild( child )
        self.assert_( parentNode.children == children )
        self.assert_( child.parent == None )
        
        parentNode.removeAllChildren()
        self.assert_( parentNode.children == [] )
        
        # test some bogus operations    
        self.assertRaises( ValueError, parentNode.removeChild, child )
        self.assertRaises( ValueError, parentNode.removeChildren, children )
        #self.assertRaises( IndexError, parentNode.addChild, child, where = 666 )
        self.assertRaises( IndexError, parentNode.addChild, child, where = 'qwertz' )
        #self.assertRaises( IndexError, parentNode.addChildren, children, where = 666 )
        self.assertRaises( IndexError, parentNode.addChildren, children, where = 'qwertz' )

        # test re-parenting of child        
        parent1 = Node()
        parent2 = Node()
        child2 = Node()
        
        parent1.addChild( child2 )
        self.assert_( parent1.children == [ child2 ] )
        self.assert_( child2.parent == parent1 )

        parent2.addChild( child2 )
        self.assert_( parent2.children == [ child2 ] )
        self.assert_( parent1.children == [] )
        self.assert_( child2.parent == parent2 )

        child2.parent = None
        self.assert_( parent2.children == [] )
        self.assert_( child2.parent == None )

        child2.parent = parent1
        self.assert_( parent1.children == [ child2 ] )
        self.assert_( child2.parent == parent1 )
        
        child2.parent = child2.parent
        self.assert_( parent1.children == [ child2 ] )
        self.assert_( child2.parent == parent1 )


    def testGetRoot(self):
        single = Node()
        level1 = Node( parent = single )
        level2 = Node( parent = level1 )
        level3 = Node( parent = level2 )
        
        self.assert_( single.root == single )
        self.assert_( level1.root == single )
        self.assert_( level2.root == single )
        self.assert_( level3.root == single )

    
class TestNodeVisitors(unittest.TestCase):
    def setUp(self):
        rootNode = Node( name = 'root node' )
        rootNode2 = Node( name = 'root node2' )
        level1 = Node( parent = rootNode, name = 'level 1 - node 1' )
        level2Node1 = Node( parent = level1, name = 'level 2 - node 1' )
        level2Node2 = Node( parent = level1, name = 'level 2 - node 2' )
        level3Node1 = Node( parent = level2Node1, name = 'level 3 - node 1' )
        level3Node2 = Node( parent = level2Node2, name = 'level 3 - node 2' )
        level3Node3 = Node( parent = level2Node1, name = 'level 3 - node 3' )
        
        self.__dict__.update( locals() )

    def testTextTreeFormatVisitor(self):
        ttfv = TextTreeFormatVisitor( sys.stdout, indentString = ' -> ' )
        ttfv.visit( [ self.rootNode, self.rootNode2 ] )
    
    def testFindNodesByNameVisitor(self):
        fnbnv = FindNodesByNamesVisitor( [ 'level 1 - node 1', 'level 3 - node 2' ] )
        fnbnv.visit( [self.rootNode, self.rootNode2] )            
        self.assert_( fnbnv.nodes == [self.level1, self.level3Node2] )
                
    def testGetNodesAsFlatListVisitor(self):
        gnaflv = GetNodesAsFlatListVisitor()        
        gnaflv.visit( [self.rootNode, self.rootNode2] )
        
        nodes = [ self.rootNode,
                  self.level1,
                  self.level2Node1, self.level3Node1, self.level3Node3,
                  self.level2Node2, self.level3Node2,
                  self.rootNode2
                ]
                 
        self.assert_( gnaflv.nodes == nodes, gnaflv.nodes )
        
        
    def testNodeEnumerationVisitor(self):
        env = EnumerateNodesVisitor()        
        env.visit( [self.rootNode, self.rootNode2] )
        
        self.assert_( env.getPosition( self.rootNode ) == 0 )
        self.assert_( env.getPosition( self.level2Node2 ) == 5 )
        self.assert_( env.getPosition( self.level3Node3 ) == 4 )
        self.assert_( env.getPosition( self.level3Node2 ) == 6 )
        self.assert_( env.getPosition( self.rootNode2 ) == 7)
        
        self.assert_( env.getNode( 0 ) == self.rootNode )
        self.assert_( env.getNode( 5 ) == self.level2Node2 )
        self.assert_( env.getNode( 4 ) == self.level3Node3 )
        self.assert_( env.getNode( 6 ) == self.level3Node2 )
        self.assert_( env.getNode( 7 ) == self.rootNode2 )
    
if __name__ == '__main__':
    unittest.main()
