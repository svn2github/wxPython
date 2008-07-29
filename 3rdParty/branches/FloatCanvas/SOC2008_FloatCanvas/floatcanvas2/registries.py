from patterns.asSequence import asSequence
from patterns.adapter import adapterRegistry

from patterns.factory import FactoryUsingDict

class ObjectFromModelRegistry(FactoryUsingDict):
    def getObjectFromModel( self, model, **keys ):
        for interface in asSequence( model.implements_interfaces ):
            try:
                return self.registered[ interface ], model
            except KeyError:
                pass
            
        # if we get here, there was no direct renderer, let's try an adapter to
        # one of the existing renderers
        for interface, renderer in self.registered.items():
            try:
                adopted_model = adapterRegistry.get( model, interface )
            except ValueError:
                pass
            else:
                return self.registered[ interface ], adopted_model

class PrimitiveRendererRegistry(ObjectFromModelRegistry):
    getRendererConstructor = ObjectFromModelRegistry.getObjectFromModel

class ViewRegistry(ObjectFromModelRegistry):
    getViewConstructor = ObjectFromModelRegistry.getObjectFromModel

class RenderNodeRegistry(ObjectFromModelRegistry):
    getRenderNodeConstructor = ObjectFromModelRegistry.getObjectFromModel
#            
#            
#            
#class PrimitiveRendererRegistry(object):
#    def __init__( self ):
#        self.renderers = []
#        self.interface_to_renderer = {}
#        
#    def register( self, renderer ):
#        self.renderers.append( renderer )
#        if renderer.can_render in self.interface_to_renderer:
#            raise ValueError( 'Multiple interfaces for renderer' )
#        self.interface_to_renderer[ renderer.can_render ] = renderer
#            
#    def unregister( self, renderer ):
#        self.renderers.remove( renderer )
#        del self.interface_to_renderer[ renderer.can_render ]
#        
#    def getRenderer( self, model, **keys ):
#        for interface in asSequence( model.implements_interfaces ):
#            try:
#                renderer = self.interface_to_renderer[ interface ]
#            except KeyError:
#                pass
#            else:
#                return renderer( model = model, **keys )
#            
#        # if we get here, there was no direct renderer, let's try an adapter to
#        # one of the existing renderers
#        for interface, renderer in self.interface_to_renderer.items():
#            try:
#                adopted_model = adapterRegistry.get( model, interface )
#            except ValueError:
#                pass
#            else:
#                return renderer( model = adopted_model, **keys )