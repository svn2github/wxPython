from asSequence import asSequence

class CouldNotAdoptException(Exception):
    def __init__(self, msg):
        self.msg = msg
        
    def __str__(self):
        return repr( self.msg )
    

class AdapterRegistry(object):
    def __init__(self):
        self.adapters = {}
        
    def register(self, from_interface, to_interface, adapter):
        if from_interface not in self.adapters:
            self.adapters[from_interface] = {}
        if self.isRegistered( from_interface, to_interface ):
            raise ValueError( 'Duplicate adapter (current: %s, new: %s) from %s to %s not supported (yet)' % (self.adapters[from_interface][to_interface], adapter, from_interface, to_interface) )
        self.adapters[from_interface][to_interface] = adapter
        
    def unregister(self, from_interface, to_interface):
        del self.adapters[from_interface][to_interface]
        
    def unregisterAll(self):
        self.adapters = {}
        
    def isRegistered(self, from_interface, to_interface):
        try:
            self.adapters[from_interface][to_interface]
        except KeyError:
            return False
        else:
            return True
        
    def get(self, from_obj, to_interface, max_search_depth = 2):
        interfaceChain = self._doGetInterfaceChain( self._getImplementedInterfaces( from_obj ), to_interface, max_search_depth, 0 )
        
        to_obj = from_obj
        for from_interface, to_interface in zip(interfaceChain, interfaceChain[1:]):
            adapter = self.adapters[from_interface][to_interface]
            to_obj = adapter(to_obj)
            
        return to_obj
    
    def _getImplementedInterfaces(obj):
        implemented_interfaces = [ obj, type(obj) ]
        try:
            implemented_interfaces += asSequence( obj.implements_interfaces )
        except AttributeError:
            pass
        return implemented_interfaces
            
    _getImplementedInterfaces = staticmethod(_getImplementedInterfaces)
        
    def _doGetInterfaceChain(self, from_interfaces, to_interface, max_search_depth, current_depth):
        ''' Rather slow, especially for deep searches. As deep searches will
            occur very seldom (who wanted to adapt an adapter of an adapter of
            something?!) this is ok. If somebody was really interested in
            optimising this, using a suitable path finding algorithm like
            like Dijkstra's is likely to give good results.
        '''
        
        # let's see whether from_obj already implements the desired interface
        if to_interface in from_interfaces:
            return (to_interface,)

        # check whether from_obj implements any interface which can be adopted
        # to the target interface
        for from_interface in from_interfaces:
            try:
                possible_intermediate_interfaces = self.adapters[ from_interface ]
            except KeyError:
                pass
            else:
                if (current_depth + 1) > max_search_depth:
                    raise CouldNotAdoptException( 'Could not find adapters from %s to %s (maxSearchDepth %d)' % (from_interfaces, to_interface, max_search_depth) )
                
                try:
                    return (from_interface,) + self._doGetInterfaceChain( possible_intermediate_interfaces, to_interface, max_search_depth, current_depth + 1 )
                except CouldNotAdoptException:
                    pass
        
        raise CouldNotAdoptException( 'Could not find adapters from %s to %s (maxSearchDepth %d)' % (from_interfaces, to_interface, max_search_depth) )
    
        
#adapterRegistry = AdapterRegistry()