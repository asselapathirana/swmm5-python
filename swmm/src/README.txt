SWMM5 Python calling interface 
Assela Pathirana

on linux afater making sure gcc, python, matplotlib, numpy is available
sudo python setup.py install 
from the source5-xxx directory.  

to build a distribution, use do.bash

windows: 
<to do> http://docs.python.org/distutils/builtdist.html

try:
1. Install code::blocks ide
2. Run mingwvars.bat (in codeblocks/mingw directory) file at the command prompt. Now gcc should be callable. 
3. pexports c:\Python26\python26.dll
dlltool --dllname c:\Python26\python 26.dll --def python26.def --output-lib libpython26.a
4. Download and install swigwin
5. swig.exe -python swmm5.i 
6. gcc -c *.c -Ic:\python26\include 
gcc -shared *.o -o _swmm5.pyd  -Lc:\Python26 -lpython26
7. If everything works fine then
python.exe setup.py bdist --format=wininst :: AT THE MOMENT THIS DOES NOT BUILD THE PACKAGE PROPERLY
instead
copy _swmm5.pyd and swmm5.py files to <python26>/Lib/site-packages directory. 

To test: run  swmm5_test.py in src directory

