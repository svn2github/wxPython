from .. import events

class DefaultModelEventSender(object):
    def __setattr__(self, name, value):
        old_value = getattr(self, name, '<undefined>')
        object.__setattr__(self, name, value)
        events.send( 'modelChanged', object = self, attributeName = name, oldAttributeValue = old_value, newAttributeValue = value )
        