from interfaces import IPolygon, IPolygonList
from eventSender import DefaultModelEventSender
from common import ModelWithPoints
from ..math import numpy

class Polygon(ModelWithPoints, DefaultModelEventSender):
    ''' A polygon model. The polygon is defined by points. '''
    implements_interfaces = IPolygon
    
class PolygonList(DefaultModelEventSender):
    ''' Multiple polygon points in a list '''
    implements_interfaces = IPolygonList
    
    def __init__(self, polygon_list):
        self.polygon_list = polygon_list
        
    def _setPolygonList(self, polygon_list):
        self._polygon_list = [ numpy.array( [ pnt for pnt in polygon] ) for polygon in polygon_list ]
        
    def _getPolygonList(self):
        return self._polygon_list

    polygon_list = property( _getPolygonList, _setPolygonList )
    
    
class PolygonToPolygonListAdapter(object):
    implements_interfaces = IPolygonList
    
    def __init__(self, polygon):
        self.polygon = polygon
        
    def _setPolygonList(self, polygon_list):
        assert len(polygon_list) == 1
        self.polygon.points = numpy.array( polygon_list[0] )
        
    def _getPolygonList(self):
        return [ self.polygon.points ]
       
    polygon_list = property( _getPolygonList, _setPolygonList)
    

from common import registerModelAdapter
registerModelAdapter( IPolygon, IPolygonList, PolygonToPolygonListAdapter )

    