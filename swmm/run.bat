:: echo off
:: RUN this script in winpython command prompt. 
:: download epa-swmm binary and install it. Open the examples *inp files using this binary and save them back. (Important to make sure the version compatibility of the library)
:: Download and extract swmm sourcecode to swmm/swmm5/swmm5 directory. 
:: first step both in swmm5.c and swmm5.h #undef WINDOWS after its definition
:: then make sure mkstemp is not used to create temporary files in 
:: char* getTempFileName(char* fname) function (desable WINDOWS macro use
:: Run this script for each python version x architecture combination


:: MAKE SURE to edit version and name in setup.py too!! (Fix this later so that run.bat does not have to specify it!!)

:: rst2html.bat file needs to be copied to the pythonxxx/scripts directory of winpython. New versions seem not to come with this file! Anyway to fix this by having rst2html.bat version in the source?

:: github repo user is asselapathirana 

:: create a release in github and upload relevant EPA-SWMM version. 

set good="false"
if not "%1" == "" (
	set name=%1
	if not "%2"=="" (
		set arch=%2
		if not "%3"=="" (
			set pyversion=%3
			if not  "%4"=="" (
				set version=%4
				set good="true"
			) 
		) 
	)
)


if not %good%=="true" (
	echo "USAGE: %0% <name (case is important check on pypi!)> <arch 64/32> <python_version x.x.x.x> <version x.x.x.x[dev]>
	echo "Example: %0% SWMM5 64 3980 5.2.0"
	goto ERROR
)

:::::::::::::::::::::::::::::::::::::::::::::::::::::::
set swig=C:\_NO_INSTALL\swig\swigwin-4.0.2\swig.exe
set loc=%~dp0
:: set py3=3.9.8.0
:: set py2=2.7.6.4


::2.7.6.4 
:: 3.3.5.0
set pyver=%pyversion:~0,3%
set pv=%pyver:~0,1%
set pyverwhl=%pyver:.=%


	
if %arch% == 64 (
	set arch1=x64
	set arch2=win-amd64
	set arch3=win_amd64
	) else (
	set arch1=x86
	set arch2=win32
	set arch3=win32
	)
echo off
echo VERSION to be build        : %version% 
echo SWIG path                  : %swig% 
echo Location of sources        : %loc% 
echo Name of the package        : %name% 
echo Python version (short)     : %pyver% 
echo Python version (long)      : %pyversion% 
echo Python version (Wheel)     : %pyverwhl%
echo Python family (2,3)        : %pv%
echo Architecture               : %arch% %arch1% %arch2% %arch3%
echo Environment for compiler   : %env%
pause 
:: set DISTUTILS_USE_SDK=1 
:: call %env% /%arch1% /release   || goto ERROR
echo on

cd /d %loc%
call C:\_NO_INSTALL\python\WPy%arch%-%pyversion%\scripts\env.bat || goto ERROR
pip install virtualenv 
echo on
cd %loc%\%name% || goto ERROR
echo on
%swig% -python %name%.i || goto ERROR
cd ..
rd /s /q  build dist env1
pip install wheel
python setup.py    bdist_wheel || goto ERROR
cd /d %loc% || goto ERROR

:: :: test wininst
::rd /s /q   env1
::virtualenv  --clear env1 || goto ERROR
::echo on
::call %loc%\env1\Scripts\activate.bat || goto ERROR
::set OLDPATH=%PATH%
::set PATH=%loc%\env1\Scripts
::echo on
::cd /d %loc% || goto ERROR
::%loc%env1\Scripts\easy_install.exe  %loc%\dist\%name%-%version%.%arch2%-py%pyver%.exe || goto ERROR
::cd /d %loc% || goto ERROR
::echo on
::python -m doctest -f -v README.txt|| goto ERROR
::python tests\test_1.py -v || goto ERROR
::pip install nose 
::python tests\test_multithreading.py || goto ERROR
::set PATH=%OLDPATH%
:: call env1\Scripts\deactivate.bat || goto ERROR
del env1 /f /q
:: test wheel
virtualenv  --clear env1 || goto ERROR
echo on
call %loc%\env1\Scripts\activate.bat || goto ERROR
set OLDPATH=%PATH%
set PATH=%loc%\env1\Scripts
echo on
cd /d %loc% || goto ERROR
%loc%env1\Scripts\pip install  %loc%dist\%name%-%version%-cp%pyverwhl%-none-%arch3%.whl || goto ERROR
cd /d %loc% || goto ERROR
echo on
python -m doctest -v README.txt|| goto ERROR
python tests\test_1.py -v || goto ERROR
pip install nose 
python tests\test_multithreading.py || goto ERROR
set PATH=%OLDPATH%

:: Now deploy
call env1\Scripts\deactivate.bat || goto ERROR
python setup.py --long-description |rst2html  > tmp.html || goto ERROR
python setup.py register || goto ERROR
python setup.py bdist_wininst upload  || goto ERROR
python setup.py bdist_wheel upload || goto ERROR
python setup.py sdist upload|| goto ERROR
goto END
:ERROR
if %errorlevel% neq 0 (
	echo "Problem"
	)
:END
