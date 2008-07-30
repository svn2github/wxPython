from interfaces import IText
from eventSender import DefaultModelEventSender

class Text(DefaultModelEventSender):
    implements_interfaces = IText

    def __init__( self, text = '' ):
        self.text = text