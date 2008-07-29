from asSequence import asSequence

class AdapterRegistry(object):
    def __init__(self):
        self.adapters = {}
        
    def register(self, from_interface, to_interface, adapter):
        self.adapters[ (from_interface, to_interface) ] = adapter
        
    def get(self, from_obj, to_interface):
        # let's see whether from_obj already implements the desired interface
        if to_interface in asSequence( from_obj.implements_interfaces ):
            return from_obj

        # let's see whether there's a specialized adapter from type(from_obj)
        # objects
        try:
            adapter = self.adapters[ (type(from_obj), to_interface) ]
        except KeyError:
            pass
        else:
            return adapter( from_obj )

        # check whether from_obj implements any interface which can be adopted
        # to the target interface
        for from_interface in asSequence( from_obj.implements_interfaces ):
            try:
                adapter = self.adapters[ (from_interface, to_interface) ]
            except KeyError:
                pass
            else:
                return adapter( from_obj )
            
        # all attempts failed...
        raise ValueError( 'Could not adapt %s to %s' % (from_obj, to_interface) )
        
        
adapterRegistry = AdapterRegistry()