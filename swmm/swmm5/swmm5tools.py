import swmm5
from collections import OrderedDict
from tempfile import mkstemp
from os.path import basename, dirname
from  os import close, remove


def checkError(ret):
    if ret > 1: # not 0, or minus
        raise SWMM5Error(ret)    

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
    
FILEOPENED=False

class SWMM5Simulation(object):
    """Handles the communication with underlying C routines to run swmm5 and read simulation results."""
    
    class _SWMM5Results_file_open(object):
        
        
        def __init__(self,outFile):
            global FILEOPENED
            self.outFile=outFile
            
        def __enter__(self):
            global FILEOPENED
            if (not FILEOPENED):
                checkError(swmm5.OpenSwmmOutFile(self.outFile))
                FILEOPENED=True
                self.CLOSE=True
            else:
                self.CLOSE=False
            return self
        
        def __exit__(self, type, value, traceback):
            global FILEOPENED
            try:
                if(self.CLOSE):
                    swmm5.CloseSwmmOutFile()
                    FILEOPENED=False
            except:
                pass
            
    
    def __init__(self, inpFile, rptFile=None, outFile=None, clean=True):
        #dc=dict.__init__(self)
        self._clean=clean
        bn=basename(inpFile)
        dn=dirname(inpFile)
        if not rptFile: 
            h,rptFile=mkstemp(prefix=bn[0:-4], suffix=".rpt")
            close(h)
        if not outFile: 
            h,outFile=mkstemp(prefix=bn[0:-4], suffix=".dat")
            close(h)
        self.inpFile=inpFile
        self.rptFile=rptFile
        self.outFile=outFile
        self.SWMM5run()
        self._setvariables()

    def __addvar(self,val):
        self._variables.append(val)
        
    def __del__(self):
        if (self._clean):
            self.clean()

    def clean(self):
        """Delete all the files created by swmm run"""
        remove(self.rptFile)
        remove(self.outFile)
        #print "cleaning up."

            
        
        
    def SWMM5_Version(self):
        v=str(self.SWMM5_VERSION)
        return v[0]+"."+v[1]+"."+v[2:]
    
    def _setvariables(self):
        with self._SWMM5Results_file_open(self.outFile):
            UNITS=["mg/l","ug/l","counts/l"]
            swmm5.InitGetIDName()
            self._ids=OrderedDict()
            d={swmm5.GetIDName():x for x in range(swmm5.cvar.SWMM_Nsubcatch)}
            self._ids["SUBCATCH"  ]=[0,OrderedDict(sorted(d.items(), key=lambda t: t[1]))]
            d={swmm5.GetIDName():x for x in range(swmm5.cvar.SWMM_Nnodes)}
            self._ids["NODE"      ]=[1,OrderedDict(sorted(d.items(), key=lambda t: t[1]))]
            d={swmm5.GetIDName():x for x in range(swmm5.cvar.SWMM_Nlinks)}
            self._ids["LINK"      ]=[2,OrderedDict(sorted(d.items(), key=lambda t: t[1]))]
            self._ids["SYS"       ]=[3,OrderedDict({"SYS":0})]
            self._pollutants       =[swmm5.GetIDName() for x in range(swmm5.cvar.SWMM_Npolluts)]
            self._pollunits        =[UNITS[swmm5.GetInt()] for x in range(swmm5.cvar.SWMM_Npolluts)]
       
            # now build a list of available outputs for each entity. 
        su=[        
        "Rainfall (in/hr or mm/hr)",
        "Snow depth (in or mm)",
        "Evaporation + infiltration losses (in/hr or mm/hr)",
        "Runoff rate (flow units)",
        "Groundwater outflow rate (flow units)",
        "Groundwater water table elevation (ft or m)"]
        su.extend(["Runoff concentration of %s (%s)" % x for x in zip(self._pollutants, self._pollunits)])
        no=[
        "Depth of water above invert (ft or m)",
        "Hydraulic head (ft or m)",
        "Volume of stored + ponded water (ft3 or m3)",
        "Lateral inflow (flow units)",
        "Total inflow (lateral + upstream) (flow units)",
        "Flow lost to flooding (flow units)"]
        no.extend(["Concentration of %s (%s)" % x for x in zip(self._pollutants, self._pollunits)])
        li=[
        "Flow rate (flow units)",
        "Flow depth (ft or m)",
        "Flow velocity (ft/s or m/s)",
        "Froude number",
        "Capacity (fraction of conduit filled)"]
        li.extend(["Concentration of %s (%s)" % x for x in zip(self._pollutants, self._pollunits)])
        sy=[
        "Air temperature (deg. F or deg. C)",
        "Rainfall (in/hr or mm/hr)",
        "Snow depth (in or mm)",
        "Evaporation + infiltration loss rate (in/hr or mm/hr)",
        "Runoff flow (flow units)",
        "Dry weather inflow (flow units)",
        "Groundwater inflow (flow units)",
        "RDII inflow (flow units)",
        "User supplied direct inflow (flow units)",
        "Total lateral inflow (sum of variables 4 to 8) (flow units)",
        "Flow lost to flooding (flow units)",
        "Flow leaving through outfalls (flow units)",
        "Volume of stored water (ft3 or m3)",
        "Evaporation rate (in/day or mm/day)"]     
      
        self._variables=OrderedDict()
        self._variables["SUBCATCH"  ]=su
        self._variables["NODE"      ]=no
        self._variables["LINK"      ]=li
        self._variables["SYS"       ]=sy

       

    def SWMM5run(self):
        checkError(swmm5.RunSwmmDll(self.inpFile,self.rptFile,self.outFile))

       
      
    
    def __getattribute__(self, name): 
        try:
            return object.__getattribute__(self, name)
        except:
            pass
        with self._SWMM5Results_file_open(self.outFile):
            if(hasattr(swmm5.cvar,name)): # search c library. 
                return getattr(swmm5.cvar,name)
        raise AttributeError("The attribute %s not found with this class or underlying c interface" % name)

        # Default behaviour
        return object.__getattribute__(self, name)   
        
    def entityList(self):
        return self._ids.keys()
    
    def varList(self,entity):
        return self._variables[entity]
        
    def Subcatch(self):
        return self._ids["SUBCATCH"][1].keys()
    def Node(self):
        return self._ids["NODE"][1].keys()
    def Link(self):
        return self._ids["LINK"][1].keys()
    def Sys(self):
        return self._ids["SYS"][1].keys()
    def Pollutants(self,index=0):
        return self._pollutants
    def getFiles(self):
        return [self.inpFile, self.rptFile, self.outFile]
    
    def Results(self,entity,id,variable):
       with self._SWMM5Results_file_open(self.outFile):
            # [swmm5.GetSwmmResult(self._ids[entity][0],self._ids[entity][1][id],variable,i)[1] for i in range(self.SWMM_Nperiods)]
            for i in range(self.SWMM_Nperiods):
                yield swmm5.GetSwmmResult(self._ids[entity][0],self._ids[entity][1][id],variable,i)[1] 
            #return swmm5.GetSwmmResult(1,0,4,0)
    def Flow_Units(self):
        return ["CFS", "GPM", "MGD" , "CMS", "LPS", "LPD" ][self.SWMM_FlowUnits]
    
    
if __name__=="__main__":
    ss=SWMM5Simulation("swmm5/examples/simple/swmm5Example.inp")
    print ss.SWMM_Nperiods
    print list(ss.Results('NODE','J1', 4))
    print ss.SWMM5_Version()
    
    