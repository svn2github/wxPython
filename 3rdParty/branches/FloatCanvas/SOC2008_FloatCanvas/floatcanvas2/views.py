# todo: clear this up if/when we decide for an external interface package

def can_render(*args):
    pass

import events
from models import IRectangle, IEllipse, ILine, IPolygon, IPoints, ISpline, IText

##class BaseView(object):
##    def __init__(self):
##        events.subscribe( 'modelChanged', object = self, attributeName = name, oldAttributeValue = old_value, newAttributeValue = value )
##
##    def onModelChanged(self):
##        print 'Model changed'

class DefaultRectangleRenderer(object):
    can_render( IRectangle )
    
    def Render(self, renderer, model):
        renderer.DrawRectangle( model.size )

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

    def Render(self, renderer, model):
        self.look.Apply()
        self.primitive_renderer.Render( renderer, model )
            
