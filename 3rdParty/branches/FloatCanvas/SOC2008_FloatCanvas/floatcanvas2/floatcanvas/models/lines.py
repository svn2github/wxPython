from interfaces import ILine, ILineLength, ILines, ILinesList, ILineSegments, ILineSegmentsSeparate
from eventSender import DefaultModelEventSender
from common import ModelWithPoints
from ..math import numpy

class Line(DefaultModelEventSender):
    ''' A line model. Has startPoint and endPoint. '''
    implements_interfaces = ILine

    def __init__( self, startPoint, endPoint ):
        self.startPoint = startPoint
        self.endPoint = endPoint

    def _setStartPoint(self, value):
        self._startPoint = numpy.array( value )
        
    def _getStartPoint(self):
        return self._startPoint
    
    def _setEndPoint(self, value):
        self._endPoint = numpy.array( value )
        
    def _getEndPoint(self):
        return self._endPoint

    startPoint = property( _getStartPoint, _setStartPoint )
    endPoint = property( _getEndPoint, _setEndPoint )
    
    
class LineLength(DefaultModelEventSender):
    ''' A line model. Has only a length attribute, line is assumed to be
        centered around the origin.
    '''
    implements_interfaces = ILineLength

    def __init__( self, length ):
        self.length = length
        
        
class Lines(ModelWithPoints, DefaultModelEventSender):
    ''' Lines model. It's a collection of points where one point is connected
        to the next one. The lines are not automatically closed between last and
        first point.
    '''
    implements_interfaces = ILines

    
class LinesList(DefaultModelEventSender):
    ''' A model which is a list of lines. '''
    implements_interfaces = ILinesList

    def __init__(self, lines_list):
        self.lines_list = lines_list
        
    def _setLinesList(self, lines_list):
        self._lines_list = [ numpy.array( [ pnt for pnt in lines] ) for lines in lines_list ]
        
    def _getLinesList(self):
        return self._lines_list

    lines_list = property( _getLinesList, _setLinesList )

    
class LineSegments( ModelWithPoints, DefaultModelEventSender):
    ''' A model for line segments. Two points are considered to be a line.
        E.g. points[0] and points[1] form the first line, points[2] and
        points[3] form the 2nd line and so on.
    '''
    implements_interfaces = ILineSegments


class LineSegmentsSeparate( DefaultModelEventSender):
    ''' A model for line segments. Starting points are stored in startPoints,
        end points in endPoints. So the first line goes from startPoints[0] to
        endPoints[0], the second one from startPoints[1] to endPoints[1] and so
        on.
    '''
    implements_interfaces = ILineSegmentsSeparate

    def __init__(self, startPoints, endPoints):
        self.startPoints = startPoints
        self.endPoints = endPoints
        
    def _setStartPoints(self, points):
        self._startPoints = numpy.array( [ numpy.array( pnt ) for pnt in points ] )
        
    def _getStartPoints(self):
        return self._startPoints
    
    def _setEndPoints(self, points):
        self._endPoints = numpy.array( [ numpy.array( pnt ) for pnt in points ] )
        
    def _getEndPoints(self):
        return self._endPoints
    
    startPoints = property( _getStartPoints, _setStartPoints)
    endPoints = property( _getEndPoints, _setEndPoints)




# ------ adapters -------

# only the ILines and ILineSegmentsSeparate renderers are present by default
# so all other models are adapted to them

class LineLengthToLineAdapter(object):
    implements_interfaces = ILine
    
    def __init__(self, lineWithLength):
        self.lineWithLength = lineWithLength
        
    def _getStartPoint(self):
        return numpy.array( ( -self.lineWithLength.length / 2.0 , 0 ) )
    
    def _getEndPoint(self):
        return numpy.array( ( +self.lineWithLength.length / 2.0 , 0 ) )
        
    startPoint = property( _getStartPoint )
    endPoint = property( _getEndPoint )


class LineSegmentsToLineSegmentsSeparateAdapter(object):
    implements_interfaces = ILineSegmentsSeparate
    
    def __init__(self, lineSegments):
        self.lineSegments = lineSegments
        
    def _setStartPoints(self, points):
        self.lineSegments.points[::2] = numpy.array( [ numpy.array( pnt ) for pnt in points ] )
        
    def _getStartPoints(self):
        return self.lineSegments.points[::2]
    
    def _setEndPoints(self, points):
        self.lineSegments.points[1::2] = numpy.array( [ numpy.array( pnt ) for pnt in points ] )
        
    def _getEndPoints(self):
        return self.lineSegments.points[1::2]
    
    startPoints = property( _getStartPoints, _setStartPoints)
    endPoints = property( _getEndPoints, _setEndPoints)
    
    
class LineToLineSegmentsSeparateAdapter(object):
    implements_interfaces = ILineSegmentsSeparate
    
    def __init__(self, line):
        self.line = line
        
    def _setStartPoints(self, points):
        assert len(points) == 1
        self.line.startPoint = numpy.array( points[0] )
        
    def _getStartPoints(self):
        return [ self.line.startPoint ]
    
    def _setEndPoints(self, points):
        assert len(points) == 1
        self.line.endPoint = numpy.array( points[0] )
        
    def _getEndPoints(self):
        return [ self.line.endPoint ]
    
    startPoints = property( _getStartPoints, _setStartPoints)
    endPoints = property( _getEndPoints, _setEndPoints)


class LinesToLinesListAdapter(object):
    implements_interfaces = ILinesList
    
    def __init__(self, lines):
        self.lines = lines
        
    def _setLinesList(self, lines_list):
        assert len(lines_list) == 1
        self.lines.points = numpy.array( lines_list[0] )
        
    def _getLinesList(self):
        return [ self.lines.points ]
       
    lines_list = property( _getLinesList, _setLinesList)
    

from common import registerModelAdapter
registerModelAdapter( ILineLength, ILine, LineLengthToLineAdapter )
registerModelAdapter( ILineSegments, ILineSegmentsSeparate, LineSegmentsToLineSegmentsSeparateAdapter )
registerModelAdapter( ILine, ILineSegmentsSeparate, LineToLineSegmentsSeparateAdapter )
registerModelAdapter( ILines, ILinesList, LinesToLinesListAdapter )

    