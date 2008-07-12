import sys
import os.path
sys.path.append( os.path.abspath( '../..' ) )

import unittest
import numpy
from floatcanvas2.transformNode import NodeWithTransform
from floatcanvas2.transform import MercatorTransform, LinearAndArbitraryCompoundTransform

class TestNode(unittest.TestCase):    
    def testAttribs(self):
        node = NodeWithTransform()
        node.localTransform
        node.worldTransform

        parent = NodeWithTransform()
        node.parent = parent
        node.localTransform
        node.worldTransform

        parent.position = (5,5)

        self.assert_( node.position.tolist() == [0,0], node.position )
        self.assert_( node.worldTransform.position.tolist() == [5,5], node.position )
        
        mercatorNode = NodeWithTransform( parent = node, transform = MercatorTransform(10) )
        node.localTransform.longitudeCenter = 0
        self.assert_( isinstance(mercatorNode.localTransform, MercatorTransform), mercatorNode.localTransform )
        self.assert_( isinstance(mercatorNode.worldTransform, LinearAndArbitraryCompoundTransform), mercatorNode.worldTransform )        
        self.assert_( mercatorNode.worldPosition.tolist() == [5,5], mercatorNode.worldPosition )

if __name__ == '__main__':
    unittest.main()
