from events import send, subscribe, unsubscribe

class EventSender(object):
    def _getMessage(self, event_name):
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
