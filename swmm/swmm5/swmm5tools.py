import swmm5


class SWMM5Error(Exception):
    
    """ swmm5 call (c function) has returned an error (convention : non zero value)"""
    
    def __init__(self,value):
        self.value=value
        try:
            self.msg=swmm5.error_getMsg(value)
        except:
            self.msg=u"Unknown swmm error."
    def __str__(self):
        return repr(self.value)+": "+self.msg
    

class SWMM5Simulation(object):
    """Handles the communication with underlying C routines to run swmm5 and read simulation results."""
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        try:
            swmm5.CloseSwmmOutFile()
        except:
            pass
    
    def __init__(self, inpFile, rptFile=None, outFile=None):
        #dc=dict.__init__(self)
        if not rptFile: rptFile=inpFile[0:-3]+"rpt"
        if not outFile: outFile=inpFile[0:-3]+"dat"
        self.inpFile=inpFile
        self.rptFile=rptFile
        self.outFile=outFile
        self.initialize_swmm()
        self._setvariables()

    def __addvar(self,val):
        self._variables.append(val)
    
    def _setvariables(self):
        swmm5.InitGetIDName()
        self._ids={
                        "SUBCATCH":[0,[swmm5.GetIDName() for x in range(swmm5.cvar.SWMM_Nsubcatch)]],
                        "NODE":[1,[swmm5.GetIDName() for x in range(swmm5.cvar.SWMM_Nnodes)]],
                        "LINK":[2,[swmm5.GetIDName() for x in range(swmm5.cvar.SWMM_Nlinks)]],
                        "SYS":[3,[]]}
        
        #self._variables["SUBCATCH"][1].append(["rainfall (in/hr or mm/hr)"],[]])

        """
        0 for rainfall (in/hr or mm/hr)
        1 for snow depth (in or mm)
        2 for evaporation + infiltration losses (in/hr or mm/hr)
        3 for runoff rate (flow units)
        4 for groundwater outflow rate (flow units)
        5 for groundwater water table elevation (ft or m)
        6 for runoff concentration of first pollutant
        ...  
        
        5 + N for runoff concentration of N-th pollutant.  
        
         
       Number of node variables (currently 6 + number of pollutants)  
        
       Code number of each node variable:  
        
         
        0 for depth of water above invert (ft or m)
        1 for hydraulic head (ft or m)
        2 for volume of stored + ponded water (ft3 or m3)
        3 for lateral inflow (flow units)
        4 for total inflow (lateral + upstream) (flow units)
        5 for flow lost to flooding (flow units)
        6 for concentration of first pollutant
        ...  
        
        5 + N for concentration of N-th pollutant.  
        
         
       Number of link variables (currently 5 + number of pollutants)  
        
       Code number of each link variable:  
        
         
        0 for flow rate (flow units)
        1 for flow depth (ft or m)
        2 for flow velocity (ft/s or m/s)
        3 for Froude number
        4 for capacity (fraction of conduit filled)
        5 for concentration of first pollutant
        ...  
        
        4 + N for concentration of N-th pollutant.  
        
         
       Number of system-wide variables (currently 14)  
        
       Code number of each system-wide variable:  
        
         
        0 for air temperature (deg. F or deg. C)
        1 for rainfall (in/hr or mm/hr)
        2 for snow depth (in or mm)
        3 for evaporation + infiltration loss rate (in/hr or mm/hr)
        4 for runoff flow (flow units)
        5 for dry weather inflow (flow units)
        6 for groundwater inflow (flow units)
        7 for RDII inflow (flow units)
        8 for user supplied direct inflow (flow units)
        9 for total lateral inflow (sum of variables 4 to 8) (flow units)
        10 for flow lost to flooding (flow units)
        11 for flow leaving through outfalls (flow units)
        12 for volume of stored water (ft3 or m3)
        13 for evaporation rate (in/day or mm/day)   
        """

    def initialize_swmm(self):
        self.checkError(swmm5.RunSwmmDll(self.inpFile,self.rptFile,self.outFile))
        self.checkError(swmm5.OpenSwmmOutFile(self.outFile))
       
    def checkError(self,ret):
        if ret: # not 0
            raise SWMM5Error(ret)          
    
    def __getattribute__(self, name):
        if(hasattr(swmm5.cvar,name)): # search c library. 
            return getattr(swmm5.cvar,name)
        else:
            # Default behaviour
            return object.__getattribute__(self, name)   
        
    def entityList(self):
        return self._ids.keys()
        
    def Subcatch(self,index=0):
        return self._ids["SUBCATCH"][1]
    def Node(self,index=0):
        return self._ids["NODE"][1]
    def Link(self,index=0):
        return self._ids["LINK"][1]
    def Sys(self,index=0):
        return self._ids["SYS"][1] 
    
    
     

    
if __name__=="__main__":
    with SWMM5Simulation("swmm5/examples/simple/swmm5Example.inp") as st:
        print st.SWMM_Nperiods
    
    