from events import send, subscribe, unsubscribe

class EventSender(object):
    ''' If an object inherits from this, the object can send messages local to
        itself and observers can subscribe to messages from the object.
        Basically just binds events to a specific object.
        _getMessage can be overridden in derived classes if needed.
    '''
    def _getMessage(self, event_name):
        ''' forms the message name from event_name and id(self) '''
        if event_name is not None:
            return '%d.%s' % ( id(self), event_name )
        else:
            return '%d' % ( id(self), )
    
    def send(self, event_name, **keys):
        return send( self._getMessage( event_name ), **keys )
        
    def subscribe(self, subscriber, event_name ):
        return subscribe( subscriber, self._getMessage( event_name ) )

    def unsubscribe(self, subscriber, event_name):
        return unsubscribe( subscriber, self._getMessage( event_name ) )
