import wx

class ConstantTable(object):
    stringToWx = { 'oddeven' : wx.ODDEVEN_RULE,
                   'winding' : wx.WINDING_RULE,
                 }
    
    def get(cls, string):
        return cls.stringToWx[string]
    
    get = classmethod(get)

    def getEnum(cls, kind, value):
        enum_name = '%s_%s' % (kind.upper(), value.upper())
        return getattr(wx, enum_name)

    getEnum = classmethod(getEnum)
