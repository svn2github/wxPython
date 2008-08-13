''' Tests the adapter registry and the adaption mechanism '''

import sys
import os.path
sys.path.append( os.path.abspath( '..' ) )

import unittest
from floatcanvas.patterns.adapter import AdapterRegistry, CouldNotAdoptException

# a few dummy interfaces
class ILine(object):
    # startPoint, endPoint prop
    pass

class ILineLength(object):
    # length prop
    pass

class ILines(object):
    # points
    pass

# some objects
class Whatever(object):
    pass    

class Line(object):
    implements_interfaces = ILine

class LineLength(object):
    implements_interfaces = ILineLength

class Lines(object):
    implements_interfaces = ILines


# some adapters
def LineLengthToLineAdapter(x):
    implements_interfaces = ILine
    return 'LineLengthToLineAdapter'

def LineToLinesAdapter(x):
    implements_interfaces = ILines
    return 'LineToLinesAdapter'
    
def WhateverToLineLengthAdapter(x):
    implements_interfaces = ILineLength
    return 'WhateverToLineLengthAdapter'



class TestNode(unittest.TestCase):
    def setUp(self):
        self.line = Line()
        self.lineLength = LineLength()
        self.lines = Lines()
        self.whatever = Whatever()
        
        globals()['adapterRegistry'] = AdapterRegistry()
        # adapters which peruse interfaces
        adapterRegistry.register( ILineLength, ILine, LineLengthToLineAdapter )
        adapterRegistry.register( ILine, ILines, LineToLinesAdapter )
        # adapter for a concrete type
        adapterRegistry.register( Whatever, ILineLength, WhateverToLineLengthAdapter )

    def testSuperSimple(self):
        self.assert_( adapterRegistry.get( self.line, self.line ) == self.line )
        self.assert_( adapterRegistry.get( self.line, ILine ) == self.line )
        self.assert_( adapterRegistry.get( self.whatever, self.whatever ) == self.whatever )
        self.assert_( adapterRegistry.get( self.whatever, Whatever ) == self.whatever )
        
    def testConcreteObject(self):
        # adapter for a concrete object
        adapterRegistry.register( self.whatever, ILineLength, WhateverToLineLengthAdapter )
        self.assert_( adapterRegistry.get( self.whatever, ILineLength ) == 'WhateverToLineLengthAdapter' )
        self.assertRaises( CouldNotAdoptException, adapterRegistry.get, self.whatever, self.lines )
        self.assert_( adapterRegistry.get( self.whatever, Whatever ) == self.whatever )
        self.assertRaises( CouldNotAdoptException, adapterRegistry.get, Whatever, self.whatever )
        adapterRegistry.unregister( self.whatever, ILineLength )
    
    def testSimple(self):
        self.assert_( adapterRegistry.get( self.line, ILines ) == 'LineToLinesAdapter', adapterRegistry.get( self.line, ILines ) )
        self.assert_( adapterRegistry.get( self.lineLength, ILine ) == 'LineLengthToLineAdapter' )
        self.assert_( adapterRegistry.get( self.whatever, ILineLength ) == 'WhateverToLineLengthAdapter' )
        
        self.assertRaises( CouldNotAdoptException, adapterRegistry.get, self.line, Whatever )
        self.assertRaises( CouldNotAdoptException, adapterRegistry.get, Whatever, self.line )
        self.assertRaises( CouldNotAdoptException, adapterRegistry.get, self.line, self.whatever )
        self.assertRaises( CouldNotAdoptException, adapterRegistry.get, self.whatever, self.line )
        
    def testComplex(self):
        # test ILineLength -> ILine -> ILines chain
        self.assert_( adapterRegistry.get( self.lineLength, ILines ) == 'LineToLinesAdapter' )
        self.assertRaises( CouldNotAdoptException, adapterRegistry.get, self.lineLength, self.lines )
    
    def testComplexer(self):
        # test Whatever -> ILineLength -> ILine -> ILines chain
        self.assertRaises( CouldNotAdoptException, adapterRegistry.get, self.whatever, ILines, max_search_depth = 2 )
        self.assert_( adapterRegistry.get( self.whatever, ILines, max_search_depth = 3 ) == 'LineToLinesAdapter' )
        self.assertRaises( CouldNotAdoptException, adapterRegistry.get, self.whatever, self.lines, max_search_depth = 3 )
        
    def testDuplicate(self):
        self.assertRaises( ValueError, adapterRegistry.register, ILineLength, ILine, 'Duplicate Adapter' )

    def testUnregister(self):
        self.assert_( adapterRegistry.isRegistered( ILineLength, ILine ) )
        adapterRegistry.unregister( ILineLength, ILine )
        self.assert_( not adapterRegistry.isRegistered( ILineLength, ILine ) )

        self.assert_( adapterRegistry.isRegistered( ILine, ILines ) )
        adapterRegistry.unregisterAll()
        self.assert_( not adapterRegistry.isRegistered( ILine, ILines ) )

if __name__ == '__main__':
    unittest.main()
