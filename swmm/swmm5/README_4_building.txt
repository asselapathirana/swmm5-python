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

make sure wing ide (or any other ide is using this env.)

after each change in c side

env1\Scripts\deactivate.bat
cd swmm5
c:\swig\swigwin-2.0.8\swig.exe -python swmm5.i
cd ..
"c:\Program Files (x86)\CodeBlocks\MinGW\mingwvars.bat"
python setup.py bdist
env1\Scripts\activate.bat
python setup.py install


Testing
-------
nosetests -v --with-doctest  --doctest-fixtures

Deploying Process
----------------
* Do testing before deploying
DO not do the following in a mingw environment:
python setup.py --long-description |rst2html  > tmp.html
(fix any errors, then ..)
python -m doctest README.txt
iterate these two until everyting is fixed. 
then ..
python setup.py register
python setup.py sdist

DO following in mingw enviornment (CodeBlocks\MinGW\mingwvars.bat)
python setup.py bdist_wininst

Now to go cygwin and upload

(last two commands again with "upload --sign")

