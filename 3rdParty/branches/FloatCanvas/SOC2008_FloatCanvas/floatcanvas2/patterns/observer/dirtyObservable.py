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
