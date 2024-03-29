SWMM5 Python calling interface
(c) Assela Pathirana
Released under GNU GPL v.3

[Source code repository](https://github.com/asselapathirana/swmm5-python)

Release History:
----------------
version 5.2.1
Newer version of swmm (5.2.1)
Support for python 3.10 added.
Still linux version does not work.  (removing custom_build_ext gets to  build, but causes buffer overflow)

version 5.2.0.post6
(fixed upstream bugs in swmm code https://www.openswmm.org/Topic/31733/undeclared-problems-when-compiling-swmm5-2-on-linux)
However, linux version still not working (Core dumping. For linux, I suggest to use 5.1.015 for the moment!)
version 5.2.000 released in 2022

version 5.1.015 released in 2021

version 1.0.0.1 first production (non-beta) release. 

version 1.1.0.1 version with new SWMM 5.1 version (instead of SWMM 5.0)



Installation:
-------------
:Windows: 

As of version 1.0.0.1 SWMM5 is verified to work with Python 3 as well. 

Now (as of version 1.0.0.1) the package is provided as python Wheel too. This means for windows the following command should install SWMM5


::

    pip install SWMM5
    
Alternatively, use the SWMM5-x.y.z.k.win32.exe file downloaded from the repository for click and install. 

If you have your own C compilers, then  SWMM5-x.y.z.k.zip can be used to install as 

::

    python setup.py install
    
:Linux: 

Download SWMM5-x.y.z.k.zip can be used to install as 

::

    python setup.py install

Or, just with, 
::

    pip install SWMM5

Usage:
------

:New Interface:

One should always use the new interface. The old interface (below) is left only for backward compatibility. The key features of new interface are 
    * More pythonic interface
    * A number of convenience functions
    
 Import new interface and run SWMM

::

    >>> from swmm5.swmm5tools import SWMM5Simulation
    >>> st=SWMM5Simulation("swmm5/examples/simple/swmm5Example.inp")
    
 
    
:Example 1: Retrive simulation properties. 


::

    >>> st.SWMM5_Version()          # Version of underlying SWMM5 engine. 
    '5.2.001'
    >>> st.SWMM5_VERSION            # same thing as an integer 
    52001
    >>> st.Flow_Units()           # Flow units. 
    'LPS'
    >>> st.SWMM_FlowUnits         # returns flow units as an index.  0 = CFS, 1 = GPM, 2 = MGD, 3 = CMS, 4 = LPS, and 5 = LPD  
    4
    >>> st.SWMM_Nperiods          # number of reporting periods 
    360
    >>> st.SWMM_Nsubcatch         # number of subcatchments
    6
    >>> st.SWMM_Nnodes            # number of drainage system nodes
    12
    >>> st.SWMM_Nlinks            # number of drainage system links
    11
    >>> st.SWMM_Npolluts          # number of pollutants tracked
    0
    >>> print ("%.2f"%st.SWMM_StartDate)  # start date of simulation
    40844.00
    >>> st.SWMM_ReportStep
    60
    >>>

:Example 2: Prints available entities

::

   >>> st.entityList()
   ['SUBCATCH', 'NODE', 'LINK', 'SYS']
   >>> st.Subcatch() # Deprecated
   ['A2', 'A1', 'A3', 'A4', 'A5', 'E1']
   >>> st.entityList(within='SUBCATCH') # use these new since version 5.2
   ['A2', 'A1', 'A3', 'A4', 'A5', 'E1']
   >>> st.Node() # Deprecated
   ['J1', 'J2', 'J3', 'J4', 'J5', 'J6', 'J7', 'J8', 'J9', 'J10', 'J11', 'J12']
   >>> st.entityList(within='NODE') # use these new since version 5.2
   ['J1', 'J2', 'J3', 'J4', 'J5', 'J6', 'J7', 'J8', 'J9', 'J10', 'J11', 'J12']
   >>> st.Link() # Deprecated
   ['T4-1', 'T4-2', 'T4-3', 'T1-1', 'T1-2', 'T2-1', 'T2-2', 'T2-3', 'T3-1', 'T3-2', 'T5']
   >>> st.entityList(within='LINK')
   ['T4-1', 'T4-2', 'T4-3', 'T1-1', 'T1-2', 'T2-1', 'T2-2', 'T2-3', 'T3-1', 'T3-2', 'T5']
   >>> st.Sys() # Deprecated
   ['SYS']
   >>> st.entityList(within='SYS') # use these new since version 5.2
   ['SYS']
   >>> st.Pollutants() # no pollutants in this file. 
   []
   >>> wq=SWMM5Simulation("swmm5/examples/waterquality/Example5-EXP5.1.inp")
   >>> wq.SWMM_Npolluts
   1
   >>> wq.Pollutants() # TSS in this case.  
   ['TSS']
   >>> lst=st.varList("SUBCATCH")
   >>> print ("\n".join( "%4i %s"% (i,v) for i,v in  enumerate(lst))) # print in a column with index.
      0 Rainfall (in/hr or mm/hr)
      1 Snow depth (in or mm)
      2 Evaporation loss (in/hr or mm/hr)
      3 Infiltration loss (in/hr or mm/hr)
      4 Runoff rate (flow units)
      5 Groundwater outflow rate (flow units)
      6 Groundwater water table elevation (ft or m)
      7 Soil Moisture (volumetric fraction, less or equal tosoil porosity)



   >>> lst=wq.varList("SUBCATCH") # for the network that has pollutants. 
   >>> print ("\n".join( "%4i %s"% (i,v) for i,v in  enumerate(lst))) # print in a column with index.
      0 Rainfall (in/hr or mm/hr)
      1 Snow depth (in or mm)
      2 Evaporation loss (in/hr or mm/hr)
      3 Infiltration loss (in/hr or mm/hr)
      4 Runoff rate (flow units)
      5 Groundwater outflow rate (flow units)
      6 Groundwater water table elevation (ft or m)
      7 Soil Moisture (volumetric fraction, less or equal tosoil porosity)
      8 Runoff concentration of TSS (mg/l)
      
   >>> lst=wq.varList("NODE")
   >>> print ("\n".join( "%4i %s"% (i,v) for i,v in  enumerate(lst))) # print in a column with index.
      0 Depth of water above invert (ft or m)
      1 Hydraulic head (ft or m)
      2 Volume of stored + ponded water (ft3 or m3)
      3 Lateral inflow (flow units)
      4 Total inflow (lateral + upstream) (flow units)
      5 Flow lost to flooding (flow units)
      6 Concentration of TSS (mg/l)
   >>> lst=wq.varList("LINK")
   >>> print ("\n".join( "%4i %s"% (i,v) for i,v in  enumerate(lst))) # print in a column with index.
      0 Flow rate (flow units)
      1 Flow depth (ft or m)
      2 Flow velocity (ft/s or m/s)
      3 Froude number
      4 Capacity (fraction of conduit filled)
      5 Concentration of TSS (mg/l)
   >>> lst=wq.varList("SYS")
   >>> print ("\n".join( "%4i %s"% (i,v) for i,v in  enumerate(lst))) # print in a column with index.
      0 Air temperature (deg. F or deg. C)
      1 Rainfall (in/hr or mm/hr)
      2 Snow depth (in or mm)
      3 Evaporation + infiltration loss rate (in/hr or mm/hr)
      4 Runoff flow (flow units)
      5 Dry weather inflow (flow units)
      6 Groundwater inflow (flow units)
      7 RDII inflow (flow units)
      8 User supplied direct inflow (flow units)
      9 Total lateral inflow (sum of variables 4 to 8) (flow units)
     10 Flow lost to flooding (flow units)
     11 Flow leaving through outfalls (flow units)
     12 Volume of stored water (ft3 or m3)
     13 Evaporation rate (in/day or mm/day)
     14 Potential evaporation rate (PET) in/day or mm/day)
  
   
   
:Example 3: Results

::

    >>> r=list(st.Results('NODE','J1', 4)) # total inflow into node "J1". The Results function returns a generator. We convert it to a list.
    >>> print ("\n".join( "%5.2f"% (i) for i in  r[0:10])) # Lets print the first 10 items.  
     0.00
     0.00
     0.00
     3.21
    12.02
    25.68
    43.48
    61.88
    78.69
    100.23
    >>> r=st.Results('SYS','SYS', 1)  #1 Rainfall (in/hr or mm/hr). This time we use the generator directly. 
    >>> print ("\n".join(["%5.2f"% (i) for i in  r]))  #doctest: +ELLIPSIS
     0.00
     0.00
     7.20
     7.20
     7.20
     7.60
     7.60
     7.60
     8.00
     ...
     0.00
     

:Example 4: Pollutant Concentration

::

    >>> wq.entityList(within='SUBCATCH')
    ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7']
	
    >>> r=list(wq.Results('SUBCATCH','S3', 8)) # TSS out of catchment 'S3'. We convert it to a list.
    >>> print ("\n".join( "%5.2f"% (i) for i in  r[0:10])) # Lets print the first 10 items.  #doctest.NORMALIZE_WHITESPACE
     0.00
     0.00
     0.00
     0.00
     0.00
    13.45
    14.11
    14.71
    15.24
    15.70

	
::

    >>> wq.entityList(within='NODE')
    ['J1', 'J2', 'J3', 'J4', 'J5', 'J6', 'J7', 'J8', 'J9', 'J10', 'J11', 'O1']
	
    >>> r=list(wq.Results('NODE','J3', 6)) # TSS out of Node 'J3'. We convert it to a list.
    >>> print ("\n".join( "%5.2f"% (i) for i in  r[0:10])) # Lets print the first 10 items.  
     0.00
     0.00
     0.00
     0.00
     0.00
    10.73
    13.97
    14.58
    15.14
    15.64

    >>> wq.entityList(within='LINK')
    ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11']
	
    >>> r=list(wq.Results('LINK','C11', 5)) # TSS out of Link 'C11'. We convert it to a list.
    >>> print ("\n".join( "%5.2f"% (i) for i in  r)) #   #doctest:  +ELLIPSIS
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
     0.00
     0.00
     6.50
    12.81
    16.77
    19.81
    22.73
    ...
     0.00

:Example 5: Get all results once (inefficient, but easy)

::

    >>> simtemp=SWMM5Simulation("swmm5/examples/simple/swmm5Example.inp")
    >>> ar=simtemp.allResults()
    >>> len(ar)
    4
    >>> list(ar.keys())
    ['SUBCATCH', 'NODE', 'LINK', 'SYS']
    >>> len(ar['NODE'])
    12
    >>> list(ar['NODE'].keys())
    ['J1', 'J2', 'J3', 'J4', 'J5', 'J6', 'J7', 'J8', 'J9', 'J10', 'J11', 'J12']
    >>> list(ar['NODE']['J1'].keys())[5]
    'Flow lost to flooding (flow units)'
    >>> max(list(ar['NODE']['J1']['Flow lost to flooding (flow units)'])) # doctest: +ELLIPSIS
    4267.9...
    >>> # or we can use the index for shorthand
    >>> max(list(list(ar['NODE']['J10'].values())[5]))  # doctest: +ELLIPSIS
    2252.7...


:Example 6: Tracking output files

::

    >>> simtemp=SWMM5Simulation("swmm5/examples/simple/swmm5Example.inp")
    >>> f=simtemp.getFiles()
    >>> f #doctest: +ELLIPSIS
    ['swmm5/examples/simple/swmm5Example.inp', '...swmm5Example....rpt', '...swmm5Example....dat']
    >>> from os.path import isfile
    >>> [isfile(x) for x in f] # do they exist in the operating system. 
    [True, True, True]
    >>> simtemp.clean()
    >>> [isfile(x) for x in f] # do they exist in the operating system. 
    [True, False, False]
    
Thread Safety
-------------
Calling SWMM5Simulation with input file as only argument (SWMM5Simulation will 
choose the report and binary output file names) and subsequent use of the object 
to retreive results is threadsafe to the degree I could verify. 

There is a test ``test_multithreading.py`` in the test directory, which can be run to test this to some degree. It should be run as ``python test_multithreading.py``. 


   
Legacy interface 
----------------

:Note: This is provided only for backward compatibility. Always use the new interface (above). 

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

    >>> print (ret)
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
    >>> print ('%.2f' % x)
    7.20
    >>>



Acknowlegements
----------------
    * David Townshend 
    * Tim Cera
