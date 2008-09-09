def remove_spaces(s):
    result = ''
    cap = False
    for c in s:
        if c == ' ':
            cap = True
        else:
            x = c if not cap else c.upper()
            result += x
            cap=False
    return result

##print remove_spaces( '01 - A little Test' )
            

import os
for root, dirs, files in os.walk( '.' ):
    f = open( root + '/info.py', 'w' )
    name = ''.join( os.path.basename(root).split('- ')[1:] )
    f.write( "name = '%s'\nicon = None" % name )
    f.close()
         
    for file in files:
        path = os.path.join( root, file )
        path2 = os.path.join( root, remove_spaces(file) )
        os.rename( path, path2 )

for root, dirs, files in os.walk( '.', False ):
    base = os.path.basename( root )
    path2 = os.path.join( os.path.dirname(root), remove_spaces(base) )
    os.rename( root, path2 )
        
