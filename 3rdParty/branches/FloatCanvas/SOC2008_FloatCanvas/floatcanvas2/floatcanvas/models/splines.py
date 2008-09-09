from interfaces import ICubicSpline, IQuadraticSpline
from eventSender import DefaultModelEventSender
from common import ModelWithPoints

class CubicSpline(ModelWithPoints, DefaultModelEventSender):
    ''' A cubic bezier spline defined by four points. '''
    implements_interfaces = ICubicSpline
    
class QuadraticSpline(ModelWithPoints, DefaultModelEventSender):
    ''' A quadratic bezier spline defined by three points. '''
    implements_interfaces = IQuadraticSpline
