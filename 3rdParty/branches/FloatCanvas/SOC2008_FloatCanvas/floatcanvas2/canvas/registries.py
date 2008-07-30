from patterns.asSequence import asSequence
from patterns.factory import FactoryUsingDict
from patterns.adapter import CouldNotAdoptException

class ObjectFromModelRegistry(FactoryUsingDict):
    def __init__(self, adapterRegistry):
        FactoryUsingDict.__init__(self)
        self.adapterRegistry = adapterRegistry
        
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
                adopted_model = self.adapterRegistry.get( model, interface )
            except CouldNotAdoptException:
                pass
            else:
                return self.registered[ interface ], adopted_model

class PrimitiveRendererRegistry(ObjectFromModelRegistry):
    getRendererConstructor = ObjectFromModelRegistry.getObjectFromModel

class ViewRegistry(ObjectFromModelRegistry):
    getViewConstructor = ObjectFromModelRegistry.getObjectFromModel

class RenderNodeRegistry(ObjectFromModelRegistry):
    getRenderNodeConstructor = ObjectFromModelRegistry.getObjectFromModel
