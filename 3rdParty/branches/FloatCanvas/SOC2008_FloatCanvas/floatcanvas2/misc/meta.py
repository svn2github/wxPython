import new

class EventTypeTemplate(type):
    def __init__(cls, name, bases, dikt):
        super(EventTypeTemplate, cls).__init__(name, bases, dikt)

        def __init__(self, **keys):
            self.__dict__.update(**keys)
            
        cls.__init__ = __init__
       

ModelEvent = EventTypeTemplate( 'ModelEvent', (), {} )
modelEventInstance = ModelEvent( a = 1, b = 2, c = 3, y = 4)
print modelEventInstance.c
