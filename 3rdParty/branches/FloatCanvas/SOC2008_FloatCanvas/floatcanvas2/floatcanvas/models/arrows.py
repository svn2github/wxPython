from interfaces import IArrow, IAngleArrow
from lines import Line
from eventSender import DefaultModelEventSender
from ..math import numpy

class Arrow(Line):
    ''' Arrow model. Has startPoint and endPoint and a headSize which is a
        2-element tuple (x-size = head size along arrow direction, y-size =
        "broadness" of arrow head).
    '''
    implements_interfaces = IArrow

    def __init__( self, startPoint, endPoint, headSize ):
        Line.__init__( self, startPoint, endPoint )
        self.headSize = headSize

    def _setHeadSize(self, headSize):
        self._headSize = numpy.array( headSize )
        
    def _getHeadSize(self):
        return self._headSize
    
    headSize = property( _getHeadSize, _setHeadSize )
    

class AngleArrow(DefaultModelEventSender):
    ''' Arrow model. Is specified with startPoint, length and angle and
        headSize. For the meaning of the headSize parameter, see Arrow.
    '''
    implements_interfaces = IAngleArrow

    def __init__( self, startPoint, length, angle, headSize ):
        self.startPoint = startPoint
        self.length = length
        self.angle = angle
        self.headSize = headSize

    def _setStartPoint(self, value):
        self._startPoint = numpy.array( value )
        
    def _getStartPoint(self):
        return self._startPoint
    
    startPoint = property( _getStartPoint, _setStartPoint )

    def _setHeadSize(self, headSize):
        self._headSize = numpy.array( headSize )
        
    def _getHeadSize(self):
        return self._headSize
    
    headSize = property( _getHeadSize, _setHeadSize )


class AngleArrowToArrowAdapter(object):
    ''' Adapts AngleArrows to Arrows '''
    implements_interfaces = IAngleArrow
    
    def __init__(self, angleArrow):
        self.angleArrow = angleArrow

    # let's implement them read-only properties just because for the fun of it
    startPoint = property( lambda self: self.angleArrow.startPoint )
    headSize = property( lambda self: self.angleArrow.headSize )

    def _getEndPoint(self):
        endPoint = self.startPoint + numpy.array( [ numpy.cos(self.angleArrow.angle), numpy.sin(self.angleArrow.angle) ] ) * self.angleArrow.length
        return endPoint

    endPoint = property( _getEndPoint )

from common import registerModelAdapter
registerModelAdapter( IAngleArrow, IArrow, AngleArrowToArrowAdapter )