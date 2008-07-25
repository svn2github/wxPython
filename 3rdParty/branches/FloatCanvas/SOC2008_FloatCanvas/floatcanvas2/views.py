# todo: clear this up if/when we decide for an external interface package

def can_render(*args):
    pass

import events
from models import IRectangle, IEllipse, ILine, IPolygon, IPoints, ISpline, IText
from transform import LinearAndArbitraryCompoundTransform, LinearTransform2D
from boundingBox import BoundingBox
import numpy

##class BaseView(object):
##    def __init__(self):
##        events.subscribe( 'modelChanged', object = self, attributeName = name, oldAttributeValue = old_value, newAttributeValue = value )
##
##    def onModelChanged(self):
##        print 'Model changed'



class BaseRenderer(object):
    def __init__(self, renderer, model):
        self.renderer = renderer
        self.model = model
        self._lastNonLinearTransform = None
        self.calcCoords()
        self.create()
    
    def Render(self):
        self.render_object.Draw()
        
    def create(self):
        self.render_object = self.doCreate( self.renderer, self.transformedCoords )
        
    def doCreate(self, coords):
        # override
        raise NotImplementedError()

    def calcCoords(self):
        self.coords = self.doCalcCoords( self.model )
        self.transformCoords()
        
    def transformCoords(self):
        try:
            transform = self._transform
        except AttributeError:
            self.transformedCoords = self.coords
            return
        
        if isinstance(transform, LinearTransform2D):
            self.transformedCoords = self.coords
        elif isinstance(transform, LinearAndArbitraryCompoundTransform):
            # check if the non-linear part is the same. If it is, no need to
            # recreate the shape
            if self._lastNonLinearTransform != transform.transform2:
                self.transformedCoords = transform.transform2( self.coords )
                # need to recreate our object since the coords changed
                self.create()
        else:
            raise ValueError( 'NotImplemented %s %s' % (transform, type(transform)) )

        self.transformedCoords = self.coords

        
    def doCalcCoords(self, model):
        # override
        raise NotImplementedError()
                

    def _setTransform(self, transform):
        self._transform = transform        
        self.transformCoords()    
        self.render_object.transform = self._transform

    def _getTransform(self):
        return self._transform

    transform = property( _getTransform, _setTransform )

    

class DefaultRectangleRenderer(BaseRenderer):
    can_render( IRectangle )
    
    def doCalcCoords(self, model):
        half_size = model.size / 2.0
        return numpy.array( [-half_size, half_size] )
           
    def doCreate(self, renderer, coords):
        x, y = coords[0].tolist()
        w, h = abs(coords[1] - coords[0]).tolist()

        return renderer.CreateRectangle( x, y, w, h )
        
        

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

    def Render(self, renderer):
        self.look.Apply(renderer)
        self.primitive_renderer.Render()
        
    def rebuild(self):
        self.primitive_renderer.calcCoords()
        self.primitive_renderer.create()
        
    def _getTransform(self):
        return self.primitive_renderer.transform
    
    def _setTransform(self, transform):
        self.primitive_renderer.transform = transform
            
    transform = property( _getTransform, _setTransform )