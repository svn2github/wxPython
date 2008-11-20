# We'll use the wx.lib.pubsub module for event sending now, other possibilities
# include pydispatcher or louie

# note: The main reason for using pubsub is to minimize the number of external
#       dependencies of fc.

from wx.lib.pubsub import Publisher

def _getId(obj):
    try:
        return hash(obj)
    except TypeError:
        return id(obj)

class fcEventManager(object):
    ''' Simple wrapper around pubsub to allow for easy exchange against other
        event libraries. Could probably need a rewrite. I am not sure the
        EventTypeTemplate and **keys methods are the best way to do this.
        Maybe just wrap send, subscribe, ... directly.
    '''

    class EventTypeTemplate(type):
        ''' Meta-class to create a specific event-type'''
        def __init__(cls, name, bases, dikt):
            type.__init__(cls, name, bases, dikt)

            def __init__(self, **keys):
                self.__dict__.update(**keys)
                self.vars = keys
            
            cls.__init__ = __init__
        
    def __init__(self):
        self.publisher = Publisher()
        self.event_types = {}
        self._wrapper_funcs = {}
        
    def send(self, event_name, **keys):
        try:
            evt_type = self.event_types[ event_name ]
        except KeyError:
            evt_type = self.event_types[ event_name ] = self.EventTypeTemplate( event_name, (), {} )
                
        event_instance = evt_type( **keys )
        return self.publisher.sendMessage( event_name, event_instance )
        
    def sendEvent(self, event_name, event):
        return self.publisher.sendMessage( event_name, event )

    def subscribe(self, subscriber, event_name ):
        def wrap( msg ):
            return subscriber( msg.data )
        
        # we need to add this into a dictionary, because we have to keep a
        # reference to the wrap function. publisher uses weakrefs.
        self._wrapper_funcs.setdefault( _getId(subscriber), {} )[event_name] = wrap
        return self.publisher.subscribe( wrap, event_name )

    def unsubscribe(self, subscriber, event_name = None):
        try:
            self._wrapper_funcs[_getId(subscriber)]
        except KeyError:        # isn't subscribed here, ignore it
            return
        
        if event_name is None:
            func = self._wrapper_funcs[_getId(subscriber)].values()[0]
        else:
            func = self._wrapper_funcs[_getId(subscriber)][event_name]

        result = self.publisher.unsubscribe( func, event_name )
        
        if event_name is None:
            del self._wrapper_funcs[ _getId(subscriber) ]
        else:
            del self._wrapper_funcs[ _getId(subscriber) ][event_name]            
            
        return result


def expandEventKeywords(func):
    ''' Decorator to turn an event handler taking a single key argument into
        a function taking keywords instead, e.g. instead of
    
        def myFunc(evt):
            x = evt.arg1
            y = evt.arg2
            ...
            
        you can use
    
        @expandEventKeywords
        def myFunc( x, y, ... ):
            # use x and y here directly
            pass
    '''
    def expand(*args):
        evt = args[-1]
        return func( *args[0:-1], **evt.vars )
            
    return expand

defaultFcEventManager = fcEventManager()

send = defaultFcEventManager.send
sendEvent = defaultFcEventManager.sendEvent
subscribe = defaultFcEventManager.subscribe
unsubscribe = defaultFcEventManager.unsubscribe
