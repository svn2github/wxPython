from interfaces import ICubicSpline, IQuadraticSpline
from eventSender import DefaultModelEventSender
from common import ModelWithPoints

class CubicSpline(ModelWithPoints, DefaultModelEventSender):
    implements_interfaces = ICubicSpline
    
class QuadraticSpline(ModelWithPoints, DefaultModelEventSender):
    implements_interfaces = IQuadraticSpline
