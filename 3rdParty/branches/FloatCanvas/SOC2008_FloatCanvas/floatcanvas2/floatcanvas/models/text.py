from interfaces import IText
from eventSender import DefaultModelEventSender

class Text(DefaultModelEventSender):
    ''' A text object, obviously holds a string :-) '''
    implements_interfaces = IText

    def __init__( self, text = '' ):
        self.text = text