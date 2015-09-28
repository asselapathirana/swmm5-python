SWMM5 Python calling interface 
Assela Pathirana

on linux afater making sure gcc, python, matplotlib, numpy is available
sudo python setup.py install 
from the source5-xxx directory.  

to build a distribution, use do.bash

windows: 

1. Install code::blocks ide
2. Run mingwvars.bat (in codeblocks/mingw directory) file at the command prompt. Now gcc should be callable. 
3. pexports c:\Python27\python27.dll > python27.def(could be in C:\Windows\SysWOW64 in some cases)
dlltool --dllname c:\Python27\python27.dll --def python27.def --output-lib libpython27.a
* copy libpython27.a to c:\python27\libs (this is needed for setup.py below to run)
4. Download and install swigwin
5. swig.exe -python swmm5.i 
# this part is not necessary
# 6. gcc -c *.c -Ic:\python27\include 
#gcc -shared *.o -o _swmm5.pyd  -Lc:\Python27 -lpython27
#or 
#gcc -shared *.o -o _swmm5.pyd  -LC:\Windows\SysWOW64 -lpython27)

add any extra files (e.g. swmm5_test.py, swmm5example.inp) to script directive
scripts= ['swmm5Example.inp', 'swmm5_test.py'] # these will be installed into the SCRIPTS directory. 
#7. If everything works fine then
7. Then run 
python.exe setup.py bdist --format=wininst 

( Edit ( create if not existing ) distutils.cfg located at C:\Python27\Lib\distutils\distutils.cfg to be:
[build]
compiler=mingw32

and I also had to patch c:\python27\Lib\distutils\cygwinccompiler.py
(remove depricated -mno-cygwin option)
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



