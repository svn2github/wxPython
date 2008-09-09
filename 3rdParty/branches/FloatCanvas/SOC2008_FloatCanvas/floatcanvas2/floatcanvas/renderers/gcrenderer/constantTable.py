import wx

class ConstantTable(object):
    ''' Mapping strings to the enums '''
    stringToWx = { 'oddeven' : wx.ODDEVEN_RULE,
                   'winding' : wx.WINDING_RULE,
                 }
    
    def get(cls, string):
        return cls.stringToWx[string]
    
    get = classmethod(get)

    def getEnum(cls, kind, value):
        enum_name = '%s_%s' % (kind.upper(), value.upper())
        return cls.getValue(enum_name)

    getEnum = classmethod(getEnum)


    def getValue(cls, value):
        return getattr(wx, value.upper())

    getValue = classmethod(getValue)
