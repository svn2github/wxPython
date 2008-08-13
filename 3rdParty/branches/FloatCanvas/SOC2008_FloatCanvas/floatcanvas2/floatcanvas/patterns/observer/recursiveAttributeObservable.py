from dirtyObservable import DirtyObservable
    
class RecursiveAttributeObservable(DirtyObservable):
    ''' Very simple observable. If an attribute is set which is in the
        observer_attribs list, then it marks itself dirty. When an attribute is
        set it also checks whether it can subscribe for any attribChanged events
        and marks itself dirty if one of its attributes is dirty. This works
        fine as long as there are no cycles :-)
    
        This can be optimized by using the notify decorator at the appropriate
        places. This class probably generates lots of redundant calls and is
        inefficient in many situations.        
    '''
    
    def __setattr__(self, name, value):
        if name in self.observer_attribs:
            try:
                getattr(self, name).unsubscribe( self._forwardDirty, self.notify_msg )
            except:
                pass

        object.__setattr__( self, name, value )
        

        if name in self.observer_attribs:
            try:
                getattr(self, name).subscribe( self._forwardDirty, self.notify_msg )
            except:
                pass

            self.dirty = True
            
    def _forwardDirty(self, *args, **keys):
        self.dirty = True


from listObserver import list_observer
class RecursiveListItemObservable(DirtyObservable, list_observer):
    ''' The list version of RecursiveAttributeObservable. '''
    def __init__(self, initialvalue = []):
        DirtyObservable.__init__(self)
        list_observer.__init__(self, [], self)
        if initialvalue:
            self.extend( initialvalue )
        
    def _forwardDirty(self, *args, **keys):
        self.dirty = True

    #def list_create(self, key):
    #    # what's this good for?! Is list_observer flawed and has a copy'n'psate
    #    #  error from dict_observer? Not so likely...
    #    pass
    
    def list_set(self, self2, key, oldvalue):
        self._unsubscribeItem( oldvalue )
        self._subscribeItem( self[key] )
        self.dirty = True
        
    def list_del(self, self2, key, oldvalue):
        self._unsubscribeItem( oldvalue )
        self.dirty = True
        
    def list_append(self, self2):
        self._subscribeItem( self[-1] )
        self.dirty = True

    def list_pop(self, self2, oldvalue):
        self._unsubscribeItem( oldvalue )
        self.dirty = True

    def list_extend(self, self2, newvalue):
        for item in newvalue:
            self._subscribeItem( item )
        self.dirty = True

    def list_insert(self, self2, key, value):
        self._subscribeItem( value )
        self.dirty = True

    def list_remove(self, self2, key, oldvalue):
        self._unsubscribeItem( oldvalue )
        self.dirty = True


    def _subscribeItem(self, item):
        item.subscribe( self._forwardDirty, self.notify_msg )
        
    def _unsubscribeItem(self, item):
        item.unsubscribe( self._forwardDirty, self.notify_msg )
        
        
    def notImplemented(*args):
        raise NotImplementedError()

    list_setslice = list_delslice = list_create = notImplemented
    
    def doNothing(*args):
        pass

    list_reverse = list_sort = doNothing
    