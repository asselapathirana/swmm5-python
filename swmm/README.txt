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
3. pexports c:\Python27\python27.dll > python27.def(could be in C:\Windows\SysWOW64 in some cases)
dlltool --dllname c:\Python27\python27.dll --def python27.def --output-lib libpython27.a
4. Download and install swigwin
5. swig.exe -python swmm5.i 
6. gcc -c *.c -Ic:\python27\include 
gcc -shared *.o -o _swmm5.pyd  -Lc:\Python27 -lpython27
(or 
gcc -shared *.o -o _swmm5.pyd  -LC:\Windows\SysWOW64 -lpython27)

7. If everything works fine then
python.exe setup.py bdist --format=wininst :: AT THE MOMENT THIS DOES NOT BUILD THE PACKAGE PROPERLY

( Edit ( create if not existing ) distutils.cfg located at C:\Python27\Lib\distutils\distutils.cfg to be:
[build]
compiler=mingw32

and I also had to patch c:\python27\Lib\distutils\cygwinccompiler.py

#self.set_executables(compiler='gcc -mno-cygwin -O -Wall',
                             #compiler_so='gcc -mno-cygwin -mdll -O -Wall',
                             #compiler_cxx='g++ -mno-cygwin -O -Wall',
                             #linker_exe='gcc -mno-cygwin',
                             #linker_so='%s -mno-cygwin %s %s'
                                        #% (self.linker_dll, shared_option,
                                           #entry_point))
        
        self.set_executables(compiler='gcc  -O -Wall',
                             compiler_so='gcc  -mdll -O -Wall',
                             compiler_cxx='g++  -O -Wall',
                             linker_exe='gcc ',
                             linker_so='%s  %s %s'
                                        % (self.linker_dll, shared_option,
                                           entry_point))     

)

instead
copy _swmm5.pyd and swmm5.py files to <python27>/Lib/site-packages directory. 

To test: run  swmm5_test.py in src directory

