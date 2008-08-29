# only svg export for now
# with the help of svg's foreign objects one could export custom data into the
# svg. this could be useful for a later import.
# http://www.w3.org/TR/SVG11/extend.html
# This way a pie-chart cam be exported with the % instead of (or in addition to)
#  the individual lines that make up the pie.

import cPickle as pickle
from ...patterns.factory import FactoryUsingDict

from ...views import RemoveNonLinearTransformFromCoords
from ...canvas.registries import ObjectFromModelRegistry


class ViewModelCreatorRegistry(ObjectFromModelRegistry):
    getViewModelCreatorConstructor = ObjectFromModelRegistry.getObjectFromModel
    
    
class ElementCreatorRegistry(ObjectFromModelRegistry):
    getElementCreatorConstructor = ObjectFromModelRegistry.getObjectFromModel



class SVGExporter(object):
    def __init__(self, adapter_registry):
        self.nodeSerializerRegistry = FactoryUsingDict()
        self.viewModelCreatorRegistry = ViewModelCreatorRegistry( adapter_registry )
        self.elementCreatorRegistry = ElementCreatorRegistry( adapter_registry )
    
    def getSerializer(self, node):
        return self.nodeSerializerRegistry.create( type(node) )
    
    def serializeNode(self, node):
        nodeSerializer = self.getSerializer( node )
        return nodeSerializer.serialize( node, self )
    
    def serialize(self, rootNode, camera, serializeChildren = True):
        self.camera = camera
        return self.serializeNode( rootNode )

    def save(self, filename, rootNode, camera, serializeChildren = True):
        data = self.serialize( rootNode, camera, serializeChildren )
        f = file( filename, 'wb' )
        f.write( data )
        f.close()



        
    def convertModelToSVGElement(self, model, transform):
        viewModelCreatorConstructor, model = self.viewModelCreatorRegistry.getViewModelCreatorConstructor( model )
        viewModelCreator, model = viewModelCreatorConstructor(model, look = None)
        
        def getCoords():
            return viewModelCreator.getCoords( model )
        
        transformer = RemoveNonLinearTransformFromCoords( getCoords )
        transformer.transform = transform
                
        viewModel = viewModelCreator.getViewModel( model, transformer.transformedCoords )
        linearTransform = transformer.linearTransform
        
        handler, xxx = self.elementCreatorRegistry.getElementCreatorConstructor( viewModelCreator )
        element = handler( viewModel )
        element.attributes['transform'] = linearTransform
        
        return element