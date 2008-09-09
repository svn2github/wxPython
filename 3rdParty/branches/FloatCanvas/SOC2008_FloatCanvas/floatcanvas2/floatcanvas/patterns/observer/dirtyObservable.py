from observable import Observable

class DirtyObservable(Observable):
    ''' An observable which has an attribute dirty and which notifies any
        observers when dirty changes to True. Important: it does not notify
        the observers every time dirty is set to True. Only when it switches
        from False to True.
    '''
    def __init__(self):
        self._dirty = False
    
    def _setDirty(self, value):
        # no change
        if self._dirty == value:
            return 
        
        self._dirty = value
        if self._dirty:
            self._notifyDirty()
            
    def _getDirty(self):
        return self._dirty
    
    dirty = property( _getDirty, _setDirty )

    def _notifyDirty(self):
        self.send( self.notify_msg )

    def subscribe(self, *args, **keys):
        Observable.subscribe( self, *args, **keys )
        if self.dirty:
            self._notifyDirty()
    #
    #def _getRecursiveDirty(self):
    #    if self.dirty:
    #        return True
    #    
    #    for name, value in vars(self).items():
    #        if hasattr(name, 'dirty'):
    #            if value.recursiveDirty:
    #                return True
    #    
    #    return False
    #
    #def _setRecursiveDirty(self, dirtyValue):
    #    for name in self.observer_attribs:
    #        value = getattr(self, name)
    #        try:
    #            value.recursiveDirty = dirtyValue
    #        except AttributeError:
    #            pass
    #        #value.dirty = False
    #        pass
    #            
    #    self.dirty = dirtyValue
    #
    #recursiveDirty = property( _getRecursiveDirty, _setRecursiveDirty )