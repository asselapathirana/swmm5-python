:: echo off
set arch=64bit
:::name and version variables are used by setup.py. They are very important. 
set name=SWMM5
set version=1.0.0.1dev

set good="false"
if not "%1" == "" (
	set name=%1
	if not "%2"=="" (
		set arch=%2
		if not  "%3"=="" (
			set version=%3
			set good="true"
		) 
	) 
)

if not %good%=="true" (
	echo "USAGE: %0% <name (case is important check on pypi!)> <arch 64bit/32bit> <version x.x.x.x[dev]>
	goto ERROR
)

:::::::::::::::::::::::::::::::::::::::::::::::::::::::
set swig=c:\swig\swigwin-3.0.5\swig.exe
set loc=%~dp0
set py3=3.3.5.0
set py2=2.7.6.4

if defined sdkdir (
	set sdkv=%SdkDir:~40,4%
	)
if defined sdksetupdir (
	set sdkv=%SdkSetupDir:~40,4%
	)

if defined sdkdir (
	if defined sdksetupdir (
		echo "Problem: environment is mixed between SDK 7.0 and 7.1"
		goto ERROR
	)
)

if %sdkv%==v7.0 (
	set pyversion=%py2%
)
if %sdkv%==v7.1 (
	set pyversion=%py3%
)

::2.7.6.4 
:: 3.3.5.0
set pyver=%pyversion:~0,3%
set pv=%pyver:~0,1%
set pyverwhl=%pyver:.=%



if %pv%==2 (
	set env="C:\Program Files\Microsoft SDKs\Windows\v7.0\Bin\SetEnv.cmd"
	)
if %pv%==3 (
    set env="C:\Program Files\Microsoft SDKs\Windows\v7.1\Bin\SetEnv.cmd"
	)

if %pv%=="" (
	echo "Unknown python version" %pv%
	goto ERROR
	)
	
	
if %arch% == 64bit (
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
echo SDK version                : %sdkv%
pause 
set DISTUTILS_USE_SDK=1 
call %env% /%arch1% /release   || goto ERROR
echo on

cd /d %loc%
call D:\WinPython-%arch%-%pyversion%\scripts\env.bat || goto ERROR
pip install virtualenv 
echo on
cd %loc%\%name% || goto ERROR
echo on
%swig% -python %name%.i || goto ERROR
cd ..
rd /s /q  build dist env1
pip install wheel
python setup.py   bdist_wininst bdist_wheel || goto ERROR
cd /d %loc% || goto ERROR

:: test wininst
rd /s /q   env1
virtualenv --no-site-packages --clear env1 || goto ERROR
echo on
call %loc%\env1\Scripts\activate.bat || goto ERROR
set OLDPATH=%PATH%
set PATH=%loc%\env1\Scripts
echo on
cd /d %loc% || goto ERROR
%loc%env1\Scripts\easy_install.exe  %loc%\dist\%name%-%version%.%arch2%-py%pyver%.exe || goto ERROR
cd /d %loc% || goto ERROR
echo on
python -m doctest -f -v README.txt|| goto ERROR
python tests\test_1.py -v || goto ERROR
pip install nose 
python tests\test_multithreading.py || goto ERROR
set PATH=%OLDPATH%
:: test wheel

del env1 /f /q
virtualenv --no-site-packages --clear env1 || goto ERROR
echo on
call %loc%\env1\Scripts\activate.bat || goto ERROR
set OLDPATH=%PATH%
set PATH=%loc%\env1\Scripts
echo on
cd /d %loc% || goto ERROR
%loc%env1\Scripts\pip install  %loc%\dist\%name%-%version%-cp%pyverwhl%-none-%arch3%.whl || goto ERROR
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
