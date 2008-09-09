''' Default registries for nodes, views and primitive renderers.
    The registries here can create different objects for a specific model
    interface.
    This allows you to register an ILinesRenderer for an ILines model.
    If an object is requested for a model type which is not known (e.g. there's
    only an ILines model registered, but the requested model is ILineLength) the
    registry tries to adapt the ILineLength model to an ILines model and returns
    an object for the adopted model.
    The registries are used for the canvas so you can give a model to the canvas
    and the canvas can consult the registries to create the right node/view/
    primitiveRenderer for the model.
'''

from ..patterns.asSequence import asSequence
from ..patterns.factory import FactoryUsingDict
from ..patterns.adapter import CouldNotAdoptException

class ObjectFromModelRegistry(FactoryUsingDict):
    ''' Base class for a registry. Provides the register methods via
        FactoryUsingDict and provides the getObjectFrom model function which
        looks up the right object for a specific model (if possible).        
    '''
    def __init__(self, adapterRegistry):
        FactoryUsingDict.__init__(self)
        self.adapterRegistry = adapterRegistry
        
    def getObjectFromModel( self, model, **keys ):
        ''' Return the proper object for model, if possible. First tries to get
            an object from any of the interfaces the model implements. If this
            does not work, tries to adopt the model to all known interfaces and
            if this succeeded returns the according object.
            If all fails, raises an exception.
        '''
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
            
        raise ValueError( 'no valid object found for model %s' % model )

class PrimitiveRendererRegistry(ObjectFromModelRegistry):
    getRendererConstructor = ObjectFromModelRegistry.getObjectFromModel

class ViewRegistry(ObjectFromModelRegistry):
    getViewConstructor = ObjectFromModelRegistry.getObjectFromModel

class RenderNodeRegistry(ObjectFromModelRegistry):
    getRenderNodeConstructor = ObjectFromModelRegistry.getObjectFromModel
