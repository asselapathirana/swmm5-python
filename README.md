SWMM5 Python calling interface
(c) Assela Pathirana
Released under GNU GPL v.3

[Source code repository](https://github.com/asselapathirana/swmm5-python)

Release History:
----------------
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
    
 
    
:Example 1: Retrieve simulation properties. 


::

    >>> st.SWMM5_Version()          # Version of underlying SWMM5 engine. 
    '5.1.015'
    >>> st.SWMM5_VERSION            # same thing as an integer 
    51015
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

  >>> 
  
   
   
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

    >>> wq.Subcatch()
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

    >>> wq.Node()
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

    >>> wq.Link()
    ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11']
	
    >>> r=list(wq.Results('LINK','C11', 5)) # TSS out of Link 'C11'. We convert it to a list.
    >>> print ("\n".join( "%5.2f"% (i) for i in  r)) # Lets print the first 10 items.  #doctest:  +ELLIPSIS
     0.00
     0.00
     0.00
     0.00
     0.00
     0.00
     0.00
     5.55
     9.98
    12.72
    ...
    44.95

   
:Example 5: Tracking output files

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
