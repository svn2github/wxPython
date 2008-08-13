''' Test the canvas.observables module '''

import sys
import os.path
sys.path.append( os.path.abspath( '..' ) )

import unittest
from floatcanvas.canvas.observables import makeObservable, ObservableDefaultRenderableNode, ObservableRectangle, ObservableLinearTransform2D, ObservableMercatorTransform, ObservableLinearAndArbitraryCompoundTransform
from floatcanvas.patterns.observer.observable import Observable
from floatcanvas.patterns.observer.recursiveAttributeObservable import RecursiveListItemObservable
from floatcanvas.events import subscribe
from floatcanvas.math import LinearAndArbitraryCompoundTransform, LinearTransform2D, MercatorTransform

class EventCatcher(object):
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.args = None
        self.keys = None
        self.wasCalled = False
        
    def checkCalled(self, testcase, reset = True):
        testcase.assert_( self.wasCalled )
        if reset:
            self.reset()
        
    def checkNotCalled(self, testcase):
        testcase.assert_( not self.wasCalled )

    def __call__(self, *args, **keys):
        self.args = args
        self.keys = keys
        self.wasCalled = True
        
        
class Test(object):
    def __init__(self):
        self.x = 5

ObservableTest = makeObservable( Test, ['x'], 'attribChanged' )
#ObservableLinearAndArbitraryCompoundTransform = makeObservable( LinearAndArbitraryCompoundTransform, ['transform1', 'transform2'], 'changeEvt' )
#ObservableLinearTransform2D = makeObservable( LinearTransform2D, ['translation', 'position', 'pos', 'scale', 'rotation'], 'changeEvt' )
#ObservableMercatorTransform = makeObservable( MercatorTransform, ['longitudeCenter'], 'changeEvt' )

class TestNode(unittest.TestCase):
    def setUp(self):
        self.eventCatcher = EventCatcher()
        
    def testObservable(self):
        eventCatcher = self.eventCatcher

        eventCatcher.checkNotCalled( self )
        o = Observable()
        eventCatcher.checkNotCalled( self )
        o.subscribe( eventCatcher, 'xxx' )
        o.send( 'testEvt', m = 1 )
        eventCatcher.checkNotCalled( self )
        o.unsubscribe( eventCatcher, 'xxx' )
        o.subscribe( eventCatcher, 'testEvt' )
        eventCatcher.checkNotCalled( self )
        o.send( 'testEvt', m = 1)
        eventCatcher.checkCalled( self )
        
        
    def testRecursiveAttributeObservable(self):
        eventCatcher = self.eventCatcher
        
        eventCatcher.checkNotCalled( self )
        o = ObservableTest()
        eventCatcher.checkNotCalled( self )

        o.subscribe( eventCatcher, 'attribChanged' )
        eventCatcher.checkCalled( self )
        o.dirty = False
        
        o.y = 5
        eventCatcher.checkNotCalled( self )
        
        o.x = 7
        eventCatcher.checkCalled( self )
        o.dirty = False
        
        o.x = ObservableTest()
        eventCatcher.checkCalled( self )
        o.dirty = False
        o.x.dirty = False
        
        o.x.y = 11
        eventCatcher.checkNotCalled( self )
        o.x.x = 13
        eventCatcher.checkCalled( self )
        o.dirty = False
        
        
    def testTransforms(self):
        eventCatcher = self.eventCatcher
        
        eventCatcher.checkNotCalled( self )

        tl = ObservableLinearTransform2D()
        tm = ObservableMercatorTransform()
        tc = ObservableLinearAndArbitraryCompoundTransform(tl, tm)

        tc.subscribe( eventCatcher, 'attribChanged' )
        eventCatcher.checkCalled( self )
        tc.dirty = tl.dirty = tm.dirty = False

        eventCatcher.checkNotCalled( self )
        
        tl.pos = (3,3)
        eventCatcher.checkCalled( self )
        tc.dirty = tl.dirty = tm.dirty = False

        tm.longitudeCenter = 1        
        eventCatcher.checkCalled( self )
        tc.dirty = tl.dirty = tm.dirty = False
        
        tc( [ [0,0] ] )
        self.assert_( type(tl * tl) == type(tl) )
        
    def testObservableDefaultRenderableNode(self):
        o = ObservableDefaultRenderableNode( model = None, view = None, transform = ObservableLinearTransform2D(), render_to_surface_enabled = False, surface_size = None, renderer = None )
        self.assert_( o.dirty )
        o.dirty = False
        self.assert_( not o.dirty )

        o.model = ObservableRectangle( (10, 10) )
        self.assert_( o.dirty )
        o.dirty = False
        o.model.dirty = False
        
        o.model.size = (20, 20)
        self.assert_( o.model.dirty )
        self.assert_( o.dirty )
        o.dirty = False
        o.model.dirty = False
        
        self.assert_( not o.transform.dirty )
        self.assert_( not o.dirty )
        o.transform.position = (666, 666)
        self.assert_( o.transform.dirty )
        self.assert_( o.dirty )
        o.transform = False
        o.dirty = False

        o2 = ObservableDefaultRenderableNode( model = None, view = None, transform = ObservableLinearTransform2D(), render_to_surface_enabled = False, surface_size = None, renderer = None )
        o2.dirty = False
        o.addChild( o2 )
        self.assert_( o2.dirty )
        self.assert_( o.dirty )
        
        
    def testRecursiveListItemObservable(self):
        eventCatcher = self.eventCatcher
        
        eventCatcher.checkNotCalled( self )
        o = RecursiveListItemObservable()
        o.notify_msg = 'attribChanged'
        o2 = RecursiveListItemObservable()
        o2.notify_msg = 'attribChanged'
        o3 = ObservableTest()
        o3.dirty = False
        eventCatcher.checkNotCalled( self )

        o.subscribe( eventCatcher, 'attribChanged' )
        eventCatcher.checkNotCalled( self )

        o.append( o2 )
        eventCatcher.checkCalled( self )
        o.dirty = False        
        
        o2.insert( 0, o3 )
        eventCatcher.checkCalled( self )
        o.dirty = False        
        o2.dirty = False        

        o3.x = 9
        eventCatcher.checkCalled( self )
        o.dirty = False        

        eventCatcher.checkNotCalled( self )
    #def testNode(self):
    #    eventCatcher = self.eventCatcher
    #    
    #    eventCatcher.checkNotCalled( self )
    #    node = ObservableNode( name = 'node 1' )
    #    node2 = ObservableNode( name = 'node 2' )
    #    eventCatcher.checkCalled( self )
    #    
    #    node.dirty = False
    #    node2.dirty = False
    #    
    #    eventCatcher.checkNotCalled( self )
    #    node2.parent = node
    #    eventCatcher.checkCalled( self )
    #    node2.parent = None
    #    
    #    eventCatcher.reset()
    #    node.dirty = False
    #    node2.dirty = False
    #    
    #    node.addChild( node2 )
    #    eventCatcher.checkCalled( self )
    #    
    #def testDefaultRenderableNode(self):
    #    eventCatcher = self.eventCatcher
    #
    #    eventCatcher.checkNotCalled( self )
    #    
    #    node = ObservableDefaultRenderableNode( None, None )
    #    eventCatcher.checkCalled( self )
    #    node.dirty = False
    #    
    #    node.view = None
    #    eventCatcher.checkCalled( self )
    #    node.dirty = False
    #
    #    node.model = None        
    #    eventCatcher.checkCalled( self )
    #    node.dirty = False
    #    
    #    node.transform.position = (50, 50)
    #    eventCatcher.checkCalled( self )

if __name__ == '__main__':
    unittest.main()
