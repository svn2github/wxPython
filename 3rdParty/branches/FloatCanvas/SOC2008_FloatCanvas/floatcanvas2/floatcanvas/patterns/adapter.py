from asSequence import asSequence

class CouldNotAdoptException(Exception):
    ''' Raised if an object could not be adapted to the desired interface '''
    def __init__(self, msg):
        self.msg = msg
        
    def __str__(self):
        return repr( self.msg )
    

class AdapterRegistry(object):
    ''' Registry for adapters. Users can register adapters here by using the
        register function.
        Later the get method can be used to adapt an object to a desired
        interface.
    '''
    def __init__(self):
        self.adapters = {}
        
    def register(self, from_interface, to_interface, adapter):
        ''' Registers an adapter which can adapt an object with from_interface
            so it provides to_interface.
            Right now there can be only one adapter for a pair of from-to
            interfaces. If you try to insert a duplicate one, a ValueError is
            thrown.
        '''
        if from_interface not in self.adapters:
            self.adapters[from_interface] = {}
        if self.isRegistered( from_interface, to_interface ):
            raise ValueError( 'Duplicate adapter (current: %s, new: %s) from %s to %s not supported (yet)' % (self.adapters[from_interface][to_interface], adapter, from_interface, to_interface) )
        self.adapters[from_interface][to_interface] = adapter
        
    def unregister(self, from_interface, to_interface):
        ''' unregister a previously registered adapter '''
        del self.adapters[from_interface][to_interface]
        
    def unregisterAll(self):
        ''' unregisters all adapters '''
        self.adapters = {}
        
    def isRegistered(self, from_interface, to_interface):
        ''' queries whether there's an adapter to adapt from_interface to
            to_interface.
        '''
        try:
            self.adapters[from_interface][to_interface]
        except KeyError:
            return False
        else:
            return True
        
    def get(self, from_obj, to_interface, max_search_depth = 2):
        ''' Tries to adapt from_obj to to_interface. If this is not possible a
            CouldNotAdoptException is raised.
            max_search_depth specifies how deep to search the adaption tree.
            This is useful if you have two adapters where the first does A->B
            and the second B->C. Now if you call get(A(), C) then this method
            first adapts A to B and then the adopted B to C. This requires
            searching for an intermediate adapter and that's where
            max_search_depth comes into play. It limits the number of
            intermediate adapters searched. This is mainly used to save time,
            because right now the search is performed brute-force.
            So if you have 3 adapters doing A->B->C->D, then you'd need to
            set max_search_depth at least to 3.
            For more speed consideration, see the doc for _doGetInterfaceChain.
        '''
        interfaceChain = self._doGetInterfaceChain( self._getImplementedInterfaces( from_obj ), to_interface, max_search_depth, 0 )
        
        to_obj = from_obj
        for from_interface, to_interface in zip(interfaceChain, interfaceChain[1:]):
            adapter = self.adapters[from_interface][to_interface]
            to_obj = adapter(to_obj)
            
        return to_obj
    
    def _getImplementedInterfaces(obj):
        ''' Internal method. Returns the interfaces that obj implements.
            First it implements its own interface, then it implements the
            interface of its type (todo: maybe should extend this so this
            returns each of its base classes if obj is a class).
            Finally it implements any interfaces specified by the objects'
            implements_interfaces attribute.
        '''
        implemented_interfaces = [ obj, type(obj) ]
        try:
            implemented_interfaces += asSequence( obj.implements_interfaces )
        except AttributeError:
            pass
        return implemented_interfaces
            
    _getImplementedInterfaces = staticmethod(_getImplementedInterfaces)
        
    def _doGetInterfaceChain(self, from_interfaces, to_interface, max_search_depth, current_depth):
        ''' Internal method. Performs all the work for the get function.
            Searches the adapter tree for an adapter chain to adapt
            one of from_interfaces to to_interface.
            Rather slow, especially for deep searches. As deep searches will
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