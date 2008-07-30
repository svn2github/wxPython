from observable import Observable

class DirtyObservable(Observable):
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

    def _getRecursiveDirty(self):
        if self.dirty:
            return True
        
        for name, value in vars(self).items():
            if hasattr(name, 'dirty'):
                if value.recursiveDirty:
                    return True
        
        return False
    
    def _setRecursiveDirty(self, dirtyValue):
        for name, value in vars(self).items():
            if hasattr(value, 'dirty') and value != self:
                value.recursiveDirty = dirtyValue
                
        self.dirty = dirtyValue

    recursiveDirty = property( _getRecursiveDirty, _setRecursiveDirty )