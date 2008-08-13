def asSequence( arg ):
    ''' little helper function which is useful if you have a function which
        takes a sequence as an argument. E.g.:
        
        def func(colours):
            for colour in colours:
                print colour
        
        However, quite often the user might want to pass a list with a single
        element. He'd have to keep in mind to write func( ['blue'] ).
        With asSequence you can write func in the following way:

        def func(colours):
            for colour in asSequence(colours):
                print colour
            
        This allows the user to call func( 'blue' ) without having to keep the
        list/sequence in mind.
        If the argument is already a sequence it just returns the sequence.
    '''
    try:
        arg.__getitem__
    except AttributeError:
        return (arg,)
    else:
        return arg