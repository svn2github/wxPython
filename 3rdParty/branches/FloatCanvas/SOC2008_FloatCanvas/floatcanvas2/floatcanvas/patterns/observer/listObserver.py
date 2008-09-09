'''
taken from http://code.activestate.com/recipes/306864/

Implement an observer pattern for lists and dictionaries.

A subclasses for dicts and lists are defined which send information
about changes to an observer.

The observer is sent enough information about the change so that the
observer can undo the change, if desired.
'''

class list_observer(list):
    """
    Send all changes to an observer.
    """
    
    def __init__ (self,value,observer):
        list.__init__(self,value)
        self.set_observer(observer)
    
    def set_observer (self,observer):
        """
        All changes to this list will trigger calls to observer methods.
        """
        self.observer = observer 
    
    def __setitem__ (self,key,value):
        """
        Intercept the l[key]=value operations.
        Also covers slice assignment.
        """
        try:
            oldvalue = self.__getitem__(key)
        except KeyError:
            list.__setitem__(self, key, value)
            self.observer.list_create(self, key)
        else:
            list.__setitem__(self, key, value)
            self.observer.list_set(self, key, oldvalue)
    
    def __delitem__ (self,key):
        oldvalue = list.__getitem__(self, key)
        list.__delitem__(self, key)
        self.observer.list_del(self, key, oldvalue)
    
    def __setslice__ (self, i, j, sequence):
        oldvalue = list.__getslice__(self, i, j)
        self.observer.list_setslice(self, i, j, sequence, oldvalue)
        list.__setslice__(self, i, j, sequence)
    
    def __delslice__ (self, i, j):
        oldvalue = list.__getitem__(self, slice(i, j))
        list.__delslice__(self, i, j)
        self.observer.list_delslice(self, i, oldvalue)
    
    def append (self,value):
        list.append(self,value)
        self.observer.list_append(self)
    
    def pop (self):
        oldvalue = list.pop(self)
        self.observer.list_pop(self,oldvalue)
    
    def extend (self, newvalue):
        list.extend(self, newvalue)
        self.observer.list_extend(self, newvalue)
    
    def insert (self, i, element):
        list.insert(self, i, element)
        self.observer.list_insert(self, i, element)
    
    def remove (self, element):
        index = list.index(self, element)
        list.remove(self, element)
        self.observer.list_remove(self, index, element)
    
    def reverse (self):
        list.reverse(self)
        self.observer.list_reverse(self)
    
    def sort (self,cmpfunc=None):
        oldlist = self[:]
        list.sort(self,cmpfunc)
        self.observer.list_sort(self, oldlist)


if __name__ == '__main__':
    class printargs(object):
        """
        If a call to a method is made, this class prints the name of the method
        and all arguments.
        """
        def p(self, *args):
            print self.attr, args
        def __getattr__(self, attr):
            self.attr = attr
            return self.p
    
    # minimal demonstration of the observer pattern.
    observer = printargs()
    l = list_observer([1, 2, 3], observer)
    l.append(1)
