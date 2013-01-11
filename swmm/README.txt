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

:New Interface:

One should always use the new interface. The old interface (below) is left only for backward compatibility. The key features of new interface are 
    * More pythonic interface
    * A number of convienience functions
    
 Importing new interface

::

    >>> from swmm5.swmm5tools import SWMM5Simulation
    >>>
    
 
    
:Example 1: Retrive simulation properties. 


::

    >>> with SWMM5Simulation("swmm5/examples/simple/swmm5Example.inp") as st:
    ...     print st.SWMM_Nperiods            # number of reporting periods 
    ...     print st.SWMM_Nsubcatch         # number of subcatchments
    ...     print st.SWMM_Nnodes            # number of drainage system nodes
    ...     print st.SWMM_Nlinks            # number of drainage system links
    ...     print st.SWMM_Npolluts          # number of pollutants tracked
    ...     print "%.2f"%st.SWMM_StartDate  # start date of simulation
    ...     print st.SWMM_ReportStep
    360
    6
    12
    11
    0
    40844.00
    60
    >>>

:Example 2: Prints available entities

   >>> with SWMM5Simulation("swmm5/examples/simple/swmm5Example.inp") as st:
   ...     st.entityList()
   ['NODE', 'SYS', 'LINK', 'SUBCATCH']
   
   >>> with SWMM5Simulation("swmm5/examples/simple/swmm5Example.inp") as st:
   ...     st.Subcatch()
   ...     st.Node()
   ...     st.Link()
   ...     st.Sys()
   ['A2', 'A1', 'A3', 'A4', 'A5', 'E1']
   ['J1', 'J2', 'J3', 'J4', 'J5', 'J6', 'J7', 'J8', 'J9', 'J10', 'J11', 'J12']
   ['T4-1', 'T4-2', 'T4-3', 'T1-1', 'T1-2', 'T2-1', 'T2-2', 'T2-3', 'T3-1', 'T3-2', 'T5']
   []
   
   


:Example 3: Retrive runoff

::

   >>> with SWMM5Simulation("swmm5/examples/simple/swmm5Example.inp") as st:
   ...     pass #print st.Subcatch(0,st.FLOW) # prints the first (index 0) subcatchments, flow 
   >>>
   
:Legacy interface:

import swmm5 module

::

    >>> from swmm5 import swmm5 as sw
    >>>
    
run a sample network

::

    >>> ret=sw.RunSwmmDll("./swmm5/examples/simple/swmm5Example.inp","swmm5Example.rpt","swmm5.dat")
    >>>


should return 0 if everything is OK (according to to swmm convension)

::

    >>> print ret
    0
    >>>

Now it is possible to retrive results. 
Open the swmm results file

::

    >>> sw.OpenSwmmOutFile("swmm5.dat")
    0
    >>>
    
How many time steps are there?

::

    >>> sw.cvar.SWMM_Nperiods
    360
    >>>

Let's retrive rainfall in the system. 
Systems rainfall at fifth timestep
::
    
    >>> ret,x=sw.GetSwmmResult(3,0,1,5)
    >>> print '%.2f' % x
    7.20
    >>>



Acknowlegements
----------------
    * David Townshend 
    * Tim Cera
