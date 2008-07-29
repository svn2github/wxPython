from patterns.observer.recursiveAttributeObservable import RecursiveAttributeObservable, RecursiveListItemObservable


def makeObservable( klass, attribs, msg, prefix = 'Observable', observer_type = RecursiveAttributeObservable ):    
    name = '%s%s' % (prefix, klass.__name__)
    new_observable_klass = type( name, (observer_type, klass), {} )
    def __init__(self, *args, **keys):
        observer_type.__init__(self)
        klass.__init__(self, *args, **keys)
    new_observable_klass.__init__ = __init__
    new_observable_klass.observer_attribs = attribs
    new_observable_klass.notify_msg = msg
    #globals()[name] = new_observable_klass
    return new_observable_klass
        

# create the observable versions of all classes here
from transform import ArbitraryTransform, CompoundTransform, LinearAndArbitraryCompoundTransform, LinearTransform, LinearTransform2D, MercatorTransform

from node import Node
from transformNode import NodeWithTransform, NodeWithBounds
from renderableNode import RenderableNode, DefaultRenderableNode
from camera import Camera

from models import Rectangle, Circle, Ellipse
from views import DefaultRectangleRenderer, DefaultView
from look import SolidColourLook, RadialGradientLook, LinearGradientLook, OutlineLook

info = \
{
    ArbitraryTransform      : ('func',),
    CompoundTransform       : ('transform1', 'transform2'),
    LinearAndArbitraryCompoundTransform      : ('transform1', 'transform2'),
    LinearTransform         : ('position', 'pos', 'translation', 'scale'),
    LinearTransform2D       : ('position', 'pos', 'translation', 'scale', 'rotation'),
    MercatorTransform       : ('longitudeCenter',),
        
    Node                    : ('_parent', '_children'),
    NodeWithTransform       : ('transform', '_parent', '_children'),
    NodeWithBounds          : ('transform', '_parent', '_children'),
    RenderableNode          : ('transform', '_parent', '_children'),
    DefaultRenderableNode   : ('transform', '_parent', '_children', 'model', 'view'),
    Camera                  : ('transform', '_parent', '_children'),
        
    Rectangle               : ('size',),
    Circle                  : ('radius',),
    Ellipse                 : ('size',),
        
    DefaultRectangleRenderer: ('model', 'transform'),
    DefaultView             : ('look', 'transform'),
        
    SolidColourLook         : ('line_colour', 'fill_kind', 'args'),
    RadialGradientLook      : ('line_colour', 'fill_kind', 'args'),
    LinearGradientLook      : ('line_colour', 'fill_kind', 'args'),
    OutlineLook             : ('line_colour', 'fill_kind', 'args'),
    
}

class ObservableChildren(RecursiveListItemObservable):
    notify_msg = 'attribChanged'

def createObservableClass(klass, attribs, prefix = 'Observable'):        
    observer_class = makeObservable( klass, attribs, 'attribChanged', prefix )
    globals()[observer_class.__name__] = observer_class
    
    if issubclass( observer_class, Node ):
        org_init = observer_class.__init__
        def __init__(self, *args, **keys):
            org_init(self, *args, **keys)
            self._children = ObservableChildren( self._children )
        observer_class.__init__ = __init__

for klass, attribs in info.items():
    createObservableClass( klass, attribs )
    


##def notifyDecorator(func):
##    def decorated(self, *args, **keys):
##        result = func(self, *args, **keys)
##        #print func, self.name
##        if not self.dirty:
##            self.dirty = True
##            send( '%s.%d' % ( self.msg, id(self), ) )
##        return result
##    return decorated


#class NotifyNodeMixin(SimpleObservable):
#    ''' Sends out "nodeChanged" messages. To optimize, we can switch over to the
#        notifyDecorator for the addChild etc. functions.
#    '''
#    
#    msg = 'nodeChanged'
#    observer_attribs = [ '_children', '_parent' ]
#   
    # uncomment for optimized version:
    #
    #BaseClass = Node    
    #
    #def __getParent( self ):
    #    return self.__parent
    #
    #def __setParent( self, parent ):
    #    self.__parent = parent
    #
    #__init__ = notifyDecorator( __init__ )
    #_parent = property( __getParent, notifyDecorator( __setParent ) )
    #
    #addChild = notifyDecorator( BaseClass.addChild )
    #addChildren = notifyDecorator( BaseClass.addChildren )
    #removeChild = notifyDecorator( BaseClass.removeChild )
    #removeChildAt = notifyDecorator( BaseClass.removeChildAt )
    #removeChildren = notifyDecorator( BaseClass.removeChildren )
    #removeAllChildren = notifyDecorator( BaseClass.removeAllChildren )



#orgInit = ObservableNodeWithTransform.__init__
#
#def ObservableNodeWithTransform__init__(*args, **keys):
#    if 'transform' in keys:
#        assert isinstance( transform, Observable), (transform, type(transform) )
#    else:
#        keys['transform'] = None
#    orgInit(*args, **keys)
#
#ObservableNodeWithTransform.__init__ = ObservableNodeWithTransform__init__


