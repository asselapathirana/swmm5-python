SWMM5 Python calling interface
(c) Assela Pathirana
Released under GNU GPL v.3

Installation:
-------------
Windows: Use the SWMM5-x.y.z.k.win32.exe file downloaded from the respository for click and install. 
Alternatively SWMM5-x.y.z.k.zip can be used to install as 
python setup.py install
Linux: Download SWMM5-x.y.z.k.zip can be used to install as 
python setup.py install

Usage:
------
import swmm5 module
>>> from swmm5 import swmm5 as sw
>>>
run a sample network
>>> ret=sw.RunSwmmDll("./swmm5/examples/simple/swmm5Example.inp","swmm5Example.rpt","swmm5.dat")
>>>
should return 0 if everything is OK (according to to swmm convension)
>>> print ret
0
>>>
Now it is possible to retrive results. 
Open the swmm results file
>>> sw.OpenSwmmOutFile("swmm5.dat")
0
>>>
How many time steps are there?
>>> sw.cvar.SWMM_Nperiods
360
>>>
Let's retrive rainfall in the system. 
Systems rainfall at fifth timestep
>>> ret,x=sw.GetSwmmResult(3,0,1,5)
>>> print '%.2f' % x
7.20
>>>

Acknowlegements:
----------------
David Townshend 
Tim Cera