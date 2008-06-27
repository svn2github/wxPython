import sys
import os.path
sys.path.append( os.path.abspath( '../..' ) )

import unittest
import numpy
from floatcanvas2.transformNode import NodeWithTransform

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

        self.assert_( node.position.tolist() == [5,5] )
        

if __name__ == '__main__':
    unittest.main()
