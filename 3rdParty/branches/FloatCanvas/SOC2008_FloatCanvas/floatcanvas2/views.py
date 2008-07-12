# todo: clear this up if/when we decide for an external interface package

def can_render(*args):
    pass

import events
from models import IRectangle, IEllipse, ILine, IPolygon, IPoints, ISpline, IText
from transform import LinearAndArbitraryCompoundTransform, LinearTransform2D
import numpy

##class BaseView(object):
##    def __init__(self):
##        events.subscribe( 'modelChanged', object = self, attributeName = name, oldAttributeValue = old_value, newAttributeValue = value )
##
##    def onModelChanged(self):
##        print 'Model changed'

def setTransform(renderer, transform, coords):
    if isinstance(transform, LinearTransform2D):
        twoxthree_transform = transform.matrix[:-1, ...]
        renderer.SetTransform( twoxthree_transform )
        return coords
    elif isinstance(transform, LinearAndArbitraryCompoundTransform):
        twoxthree_transform = transform.matrix[:-1, ...]
        renderer.SetTransform( twoxthree_transform )
        return transform.transform2(coords)
    else:
        raise ValueError( 'NotImplemented %s %s' % (transform, type(transform)) )
        
    

class DefaultRectangleRenderer(object):
    can_render( IRectangle )
    
    def Render(self, renderer, model, transform):
        half_size = model.size / 2.0
        coords = numpy.array( [-half_size, half_size] )
        coords = setTransform( renderer, transform, coords  )
        x, y = coords[0].tolist()
        w, h = (coords[1] - coords[0]).tolist()
        renderer.DrawRectangle( x, y, w, h )

# adopt circle to ellipse

class DefaultEllipseRenderer(object):
    can_render( IEllipse )
    def Render(self, renderer, model):
        renderer.DrawRectangle( model.size )

class DefaultLineRenderer(object):
    can_render( ILine )
    
    def Render(self, renderer, model):
        renderer.DrawRectangle( model.size )

class DefaultPolygonRenderer(object):
    can_render( IPolygon )
    
    def Render(self, renderer, model):
        renderer.DrawRectangle( model.size )

class DefaultPointsRenderer(object):
    can_render( IPoints )
    
    def Render(self, renderer, model):
        renderer.DrawRectangle( model.size )

class DefaultSplineRenderer(object):
    can_render( ISpline )
    
    def Render(self, renderer, model):
        renderer.DrawRectangle( model.size )

class DefaultTextRenderer(object):
    can_render( IText )

    def Render(self, renderer, model):
        renderer.DrawRectangle( model.size )



class DefaultView(object):
    def __init__(self, look, primitive_renderer):
        self.look = look
        self.primitive_renderer = primitive_renderer

    def Render(self, renderer, model, transform):
        self.look.Apply(renderer)
        self.primitive_renderer.Render( renderer, model, transform )
            
