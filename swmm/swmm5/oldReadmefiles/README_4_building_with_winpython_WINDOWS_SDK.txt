NOTE NOTE NOTE: 
Water quality is not working properly as of 5.1. Instead of values, the results are bunch of zeros!
For the moment, waterquality tests are disabled. Once fixed do the following
1. On README.txt 
Extracting of pollutants do not work properly in this version. Expect a fix later. 
 

    >>> r=list(wq.Results('SUBCATCH','S3', 6)) # TSS out of catchment 'S3'. We convert it to a list.
    >>> print ("\n".join( "%5.2f"% (i) for i in  r[0:10])) # Lets print the first 10 items.  
     0.00
     0.00
     0.00
     0.00
     0.00
     0.00
     0.00
     0.00
     0.00
     0.00

Above water quality TSS values are wrong!!

2. On test_multithreading.py uncomment:
    def runSWMM2(self):
        """Runs swmm and obtain some results"""
#        ss=SWMM5Simulation("swmm5/examples/waterquality/Example5-EXP.inp")       
#        self.assertEquals(ss.Flow_Units(), 'CFS')
#        self.assertEquals(ss.entityList(),['SUBCATCH', 'NODE', 'LINK', 'SYS'])
#        g=ss.Results('SUBCATCH','S3', 6)
#        self.assertAlmostEqual(next(g),0.00)
#        self.assertAlmostEqual(next(g),9.937597274780273)
#        self.assertAlmostEqual(next(g),9.9885835647583)
#        self.assertAlmostEqual(next(g),9.995906829833984)
#        ss.getFiles()
#        return 

#######################
1. Download and extract winpython (both 64 bit and 32 bit version are needed for full building of 2.7 set.)
2. Download and install Windows SDK ("Windows SDK (.NET 3.5 SP1)" for python 2.6, 27.7 and 3.1, And Windows SDK (.NET 4) for python 3.3)
 As of 9/Sept/2014 : the link was http://www.microsoft.com/en-us/download/details.aspx?id=3138
(Download winsdk_web.exe and use it to download and install. No need to install documentation and samples.)
3. Install swig (c:\swig\swigwin-3.0.2\)


Open a command shell of SDK (all compilers, libraries are ready with relevant environmental variables!)
For v7, Use the start menu shortcut start>All Programs>Microsoft Windows SDK v7> cmd shell 
(target was C:\Windows\System32\cmd.exe /E:ON /V:ON /T:0E /K "C:\Program Files\Microsoft SDKs\Windows\v7.0\Bin\SetEnv.cmd")

Now just run the command 
run.bat 
with the required three arguments. 
For each SDK (7.0 and 7.1 this has to be done two times, one each for 32bit and 64bit)
So all four versions ( (py 3.3/2.7)x(64bit/32bit) ) will be built and uploaded. 

Now
1. Setup proper compiling environment by: 
set DISTUTILS_USE_SDK=1
setenv /x64 /release    
Or if building 32 bit
setenv /x86 /release 
(command prompt becomes green)
set name=SWMM5
set version=1.1.0.1dev

2. run <winpython directory>\scripts\env.bat (D:\WinPython-64bit-2.7.6.4\scripts\env.bat)  to set pythyon env on top of it. 


Go to <swmm5-python>\swmm level  (e:\learn\swmm5-python\swmm)


Now ...


cd swmm5
c:\swig\swigwin-3.0.2\swig.exe -python swmm5.i
cd .. #now we are at <swmm5-python>\swmm level
python setup.py bdist
copy build\lib.win-amd64-2.7\_swmm5.pyd swmm5\.



Testing
-------
create the virtual environment by 
virtualenv --no-site-packages env1
Make sure to install nose within that 
env1\Scripts\activate.bat
pip install nose

env1\Scripts\activate.bat
set PYTHONPATH=.;%PYTHONPATH%
(in swmm5-python\swmm\swmm5 directory...)
nosetests -v --with-doctest  --doctest-ext=txt  
IF that fails 
try: 
python -m doctest  README.txt -v
python tests\test_1.py -v 

None of the above (nose of alternative ways) will not run test_multithreading.py. 
To run that
set PYTHONPATH=.
python tests\test_multithreading.py

Finally make sure to 
env1\Scripts\deactivate.bat


Deploying Process
----------------

* Check for formatting
python setup.py --long-description |rst2html  > tmp.html
(or type README.txt |rst2html  > tmp.html
(fix any errors, then ..)
* Do testing before deploying
pip install coverage
(in swmm5-python\swmm\swmm5 directory...)
nosetests -v --with-doctest  --doctest-ext=txt --doctest-options "+ELLIPSIS,+NORMALIZE_WHITESPACE" --with-coverage 
(all tests should pass. Code coverate for swmm5tools should be nearly 100%)
* iterate these two until everyting is fixed. 
then ..

python setup.py register (may be asked for the password for pypi : more than sixteen letters 
python setup.py sdist
python setup.py bdist_wininst
python setup.py sdist upload
python setup.py bdist_wininst upload


New SWMM5.0 Version
-------------------
Overwrite the files in swmm5/swmm5 directory with new swmm
patch text.h file
-"\n o  Retrieving project data"
+""
In dynwave.c omp.h include has to be removed (Windows SDK does not come with omp)
If the new version of swmm5 brings new *.c files, setup.py has to be updated.

