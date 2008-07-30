def asSequence( arg ):
    try:
        arg.__getitem__
    except AttributeError:
        return (arg,)
    else:
        return arg