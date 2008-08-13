''' inspired by
    http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/86900
'''
from partial import partial

class FactoryUsingMethods(object):
    ''' A factory where you can register a constructor with a name.
        E.g.

        f = FactoryUsingMethods()
        
        f.register( 'createCircle', Circle )
        c = f.createCircle( radius = 7 )
    '''
        
    def register(self, methodName, constructor, *args, **kargs):
        ''' register a constructor '''
        if self.is_registered(methodName):
            raise ValueError( methodName )
        setattr(self, methodName, partial(constructor, *args, **kargs) )
        
    def unregister(self, methodName):
        ''' unregister a constructor '''
        delattr(self, methodName)

    def is_registered(self, methodName):
        return hasattr(self, methodName)


class FactoryUsingDict(object):
    ''' A factory where you can register a constructor with a name.
        E.g.

        f = FactoryUsingDict()
        
        f.register( 'Circle', Circle )
        c = f.create( 'Circle', radius = 7 )
    '''

    def __init__(self):
        self.registered = {}
        
    def register(self, entry_name, constructor, *args, **kargs):
        ''' register a constructor '''
        if self.is_registered(entry_name):
            raise ValueError( 'Duplicate %s' % entry_name )
        self.registered[entry_name] = partial(constructor, *args, **kargs)
        
    def unregister(self, entry_name):
        ''' unregister a constructor '''
        del self.registered[entry_name]

    def create(self, entry_name, *args, **kargs):
        return self.registered[entry_name](*args, **kargs)

    def is_registered(self, entry_name):
        return ( entry_name in self.registered )



# some test code
if __name__ == '__main__':

    class Circle(object):
        def __init__(self, radius):
            self.radius = radius

    def createRectangle(size):
        return size


    def test_factory_methods():
        f = FactoryUsingMethods()
        
        f.register( 'createCircle', Circle )
        c = f.createCircle( radius = 7 )
        print c.radius
        f.unregister( 'createCircle' )

        f.register( 'createRectangle', createRectangle )
        print f.createRectangle( (5,5) )

        try:
            f.createCircle( 7 )
        except:
            pass
        else:
            assert False

        assert f.is_registered( 'createRectangle' )


    def test_factory_dict():
        f = FactoryUsingDict()
        
        f.register( 'Circle', Circle )
        c = f.create( 'Circle', radius = 7 )
        print c.radius
        f.unregister( 'Circle' )

        f.register( 'Rectangle', createRectangle )
        print f.create( 'Rectangle', (5,5) )

        try:
            f.create( 'Circle', 7 )
        except:
            pass
        else:
            assert False

        assert f.is_registered( 'Rectangle' )


    test_factory_methods()
    test_factory_dict()
