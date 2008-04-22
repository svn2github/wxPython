
wxPython FloatCanvas

The package contains the wxPython FloatCanvas package and a bunch of small
demo applications.

It is designed and tested for wxPython 2.6. 
I"ve had a few problems with wxPython2.8 on OS-X, I haven't tested it yet on
other platforms. Please give it a try ans let me know!

- The floatcanvas directory contains the package with required modules.

- FloatCanvasDemo.py is a demo and test code that has an assortment of
little demos that illustrate how to use most of the functionality of
FloatCanvas. Start it by typing:

python FloatCanvasDemo.py

At the command line in the directory you have it stored in. 

- In the Demos directory, there are a bunch of small, stand alone
applications that test and demonstrate various things. Most are set
up to use this copy of floatcanvas, if started from in the Denos dir.

  - PolyEditor is a very simple app that creates a couple of random
  polygons, and allows you to move their vertexes around with the
  mouse. It does demo how to bind events, and move things about the
  canvas with the mouse.

  - TextBox2.py creates a scalable text box that you can move around and
  change the size of with the mouse.

  - There are a bunch more that are fairly self explanatory

## Installing:

The "install.py" script will install the floatcanvas package into the
wxPython/lib directory, and the FloatCanvasDemo into wxPython demo
directory that is specified at the top of the script. I suggest that you
look at and edit that script before running it. If it's set up
correctly, it should allow you to install this version over the one that
came with wxPython, in order to upgrade it.

If you run the Demo first, from the distro directory, then you'll get a
set of *.pyc files in the floatcanvas module that will get
installed. Otherwise, if you don't have write permissions to the install
directory, then the *.pyc files won't get written.

I think this could be done with distutils, but it isn't trivial to
figure out how.

Any comments, questions, suggestions, and bug fixes are welcome

-Chris

Chris.Barker@noaa.gov
Jan 25, 2007

