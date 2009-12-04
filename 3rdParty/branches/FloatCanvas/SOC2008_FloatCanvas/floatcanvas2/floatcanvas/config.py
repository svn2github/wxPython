# hack
import patterns

class Config(object):
    speedMode = False

    def enableSpeedMode(self):
        del patterns.observer.recursiveAttributeObservable.RecursiveAttributeObservable.__setattr__
        del patterns.observer.recursiveAttributeObservable.RecursiveAttributeObservable._forwardDirty
        del patterns.observer.dirtyObservable.DirtyObservable.dirty
        patterns.observer.dirtyObservable.DirtyObservable.dirty = False
        self.speedMode = True
        
config = Config()