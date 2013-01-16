Building windows binary works only at dos prompt (not in cygwin terminal) at the moment. 
Need to source CodeBlocks\MinGW\mingwvars.bat
( Linker error cannot find -lmsvcr90 is due to failing to do this!)

# any changes to *.i file should be followed by running swig to geterate interface files. 

Development with virtual environment
------------------------------------
create the virtual environment by virtualenv --no-site-packages env1
Make sure to install nose within that 
env1\Scripts\activate.bat
pip install nose

windows:

make sure to add . to PYTHONPATH in wingide

after each change in c side

env1\Scripts\deactivate.bat
cd swmm5
c:\swig\swigwin-2.0.8\swig.exe -python swmm5.i
cd ..
"c:\Program Files (x86)\CodeBlocks\MinGW\mingwvars.bat"
python setup.py bdist
copy build\lib.win32-2.7\_swmm5.pyd swmm5\.
env1\Scripts\activate.bat


Testing
-------
Try
nosetests -v --with-doctest  --doctest-ext=txt 
IF that fails 
try: 
python -m doctest  README.txt -v
python tests\test_1.py -v 

None of the above (nose of alternative ways) will not run test_multithreading.py. 
To run that
set PYTHONPATH=.
python tests\test_multithreading.py


Deploying Process
----------------
DO NOT do the following in a mingw environment:
* Check for formatting
python setup.py --long-description |rst2html  > tmp.html
(or type README.txt |rst2html  > tmp.html
(fix any errors, then ..)
* Do testing before deploying
nosetests -v --with-doctest  --doctest-ext=txt --doctest-options "+ELLIPSIS,+NORMALIZE_WHITESPACE" --with-coverage
(all tests should pass. Code coverate for swmm5tools should be nearly 100%)
* iterate these two until everyting is fixed. 
then ..
python setup.py register
python setup.py sdist

DO following in mingw enviornment (CodeBlocks\MinGW\mingwvars.bat)
python setup.py bdist_wininst

Now to go cygwin and upload

(last two commands again with "upload --sign")

New SWMM5.0 Version
-------------------
Replace all the files in swmm5/swmm5 directory with new swmm
patch text.h file
-"\n o  Retrieving project data"
+""

