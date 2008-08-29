base_path = 'FloatCanvasDemo'

# we could place those into the code files, but I'd like to avoid that to not
# clutter the code
# the better solution is to add demo_info.py files to each demo folder which
# define the variables like icon and name
icon_mapping = [ ('FloatCanvasDemo', 'kpaint'),
                 ('FloatCanvasDemo/01-Tutorial', 'edu_miscellaneous'),
                 ('FloatCanvasDemo/01-Tutorial/01-Basics', 'kaddressbook'),
                 ('FloatCanvasDemo/01-Tutorial/04-Miscellaneous', 'kaddressbook'),
                 ('FloatCanvasDemo/02-Demos', 'fsview'),
               ]
       

class Entry(object):
    def __init__(self, name, display_name, icon, code_filename, text_filename):
        self.name = name
        self.display_name = display_name
        self.icon = icon
        self.code_filename = code_filename
        self.text_filename = text_filename


entries = []

import glob
def add_entry( path ):
    info_file = os.path.join( path, 'info.py' )
    info_code = compile( file(info_file).read(), info_file, 'exec' )
    globals = {}
    exec info_code in globals, globals
    name = globals['name']

    ugly_name = os.path.basename(path)
    ugly_name = ugly_name[ ugly_name.find( '-' ) + 1: ]

    html_file = os.path.join( path, '%s.html' % ugly_name )
    py_file = os.path.join( path, '%s.py' % ugly_name )

    
    if not os.path.exists( html_file ):
        print( 'Warning, skipping, no document found in %s' % html_file )
        return
    
    if not os.path.exists( py_file ):
        py_file = None    
    
    icon = globals.get('icon', None)
    
    for mapping in reversed( icon_mapping ):
        path_name, icon_name = mapping
        if path.replace(os.sep, '/').startswith( path_name ):
            icon = icon_name
            break

    entry = Entry( path.replace(os.sep, '/'), name, icon, py_file, html_file )
    entries.append( entry )


import os
for root, dirs, files in os.walk( base_path ):
    dirs.sort()     # os.walk allows to change dirs inplace
    if '.svn' in root:
        continue
    add_entry( root )    
    #for dir in sorted(dirs):
    #    add_entry( os.path.join( root, dir ) )