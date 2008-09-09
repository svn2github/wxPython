''' Provides an implementation for partial function application which is similar
    to currying.
    Python 2.5 provides already a module for this, so in this case we just
    use it. If the module is not present we provide a custom implementation.
'''

try:
    import functools
except ImportError:
    # for python < 2.5
    # taken from python's functools.partial manual/docstring
    def partial(func, *args, **keywords):
        def newfunc(*fargs, **fkeywords):
            newkeywords = keywords.copy()
            newkeywords.update(fkeywords)
            return func(*(args + fargs), **newkeywords)
        newfunc.func = func
        newfunc.args = args
        newfunc.keywords = keywords
        return newfunc

else:
    partial = functools.partial
