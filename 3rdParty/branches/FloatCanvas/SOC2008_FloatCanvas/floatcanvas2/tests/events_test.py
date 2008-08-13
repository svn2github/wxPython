''' Tests the events subpackage '''

import sys
import os.path
sys.path.append( os.path.abspath( '..' ) )

import unittest
from floatcanvas import events
from floatcanvas import EventSender

class CallChecker(object):
    def __init__(self, **expected_vars):
        self.expected_vars = expected_vars
        
    def __call__(self, evt):
        self.evt = evt
        
    def verify(self, test):
        test.assert_( self.evt.vars == self.expected_vars )
        for name, value in self.expected_vars.iteritems():
            test.assert_( getattr( self.evt, name ) == value )
        del self.evt

    def verifyNotCalled(self, test):
        test.failIf( hasattr( self, 'evt' ) )
        
    @events.expandEventKeywords
    def receiveKeywords(self, **keys):
        #import gc
        #print 'X', keys
        #for x in gc.get_referrers( self ):
        #    print x
        self.keys = keys
        
    def verifyKeywords(self, test):
        test.assert_( self.keys == self.expected_vars )
        

class TestNode(unittest.TestCase):
    def testAll(self):
        events.send( 'testEvent', value1 = 1 )
        
        callChecker = CallChecker( value1 = 1 )
        events.subscribe( callChecker, 'testEvent',  )
        events.send( 'testEvent', value1 = 1 )
        callChecker.verify(self)        

        events.unsubscribe( callChecker, 'testEvent' )
        callChecker.verifyNotCalled(self)     

        events.subscribe( callChecker.receiveKeywords, 'testEvent' )
        events.send( 'testEvent', value1 = 1 )
        callChecker.verifyKeywords(self)        

        # test weak referencing works
        #del callChecker
        #import gc
        #gc.collect()
        #events.send( 'testEvent', value2 = 3 )
        
    def testEventSender(self):
        e = EventSender()
        
        e.send( 'testEvent', value1 = 1 )
        
        callChecker = CallChecker( value1 = 1 )
        e.subscribe( callChecker, 'testEvent',  )
        e.send( 'testEvent', value1 = 1 )
        callChecker.verify(self)        

        e.unsubscribe( callChecker, 'testEvent' )
        callChecker.verifyNotCalled(self)     

        e.subscribe( callChecker.receiveKeywords, 'testEvent' )
        e.send( 'testEvent', value1 = 1 )
        callChecker.verifyKeywords(self)        
        
    
if __name__ == '__main__':
    unittest.main()
