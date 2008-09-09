''' Checks the model event sender whether it sends the appropriate
    'modelChanged' events.
    todo: make more elaborate
'''

import sys
import os.path
sys.path.append( os.path.abspath( '..' ) )

import unittest
from floatcanvas import events
from floatcanvas.models import Rectangle

from events_test import CallChecker

class TestModels(unittest.TestCase):
    def testEvents(self):
        r = Rectangle( size = (1, 3) )
        
        # see if the model changes an event when its data changes
        cc = CallChecker( object = r, attributeName = 'size', oldAttributeValue = (1, 3), newAttributeValue = (7, 9) )
        events.subscribe( 'modelChanged', cc )
        r.size = (7, 9)
        
    
if __name__ == '__main__':
    unittest.main()
