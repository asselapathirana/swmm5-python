#!/bin/bash
swig -python   swmm5.i
gcc -c -fPIC *.c -I/usr/include/python2.7
ld -shared *.o -o _swmm5.so
print "now run the following on parent directory"
print """python setup.py build_ext --inplace
python setup.py sdist""""
