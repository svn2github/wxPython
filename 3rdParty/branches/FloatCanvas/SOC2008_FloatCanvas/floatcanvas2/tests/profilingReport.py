''' Displays a report of a previous profile run '''


mode= 'cProfile'

if mode == 'hotshot':
    from hotshot import stats

    s = stats.load("profiling_data_hotshot")

    s.sort_stats("time").print_stats()

elif mode == 'cProfile':
    import pstats
    p = pstats.Stats('profiling_data_cProfile')    
    p.sort_stats('time').print_stats(50)
    print '-' * 80
    p.sort_stats('cumulative').print_stats(50)
##
##    p.sort_stats('cumulative').print_callees('UpdateScene')
