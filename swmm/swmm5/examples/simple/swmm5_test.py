
import time
import sys
__author__="Assela Pathirana"
__date__ ="$Apr 09, 2011 12:59:16 PM$"

def err(e):
    if(e>0):
        print e, "Error!" #sw.ENgeterror(e,25)


if __name__ == "__main__":

    from swmm5 import swmm5 as sw
    outfile="swmm5Example.bin"
    ret=sw.RunSwmmDll("swmm5Example.inp","swmm5Example.rpt",outfile)
    err(ret)
    err(sw.OpenSwmmOutFile(outfile))
    results=[]
    t=0.0
    for i in range(sw.cvar.SWMM_Nperiods):
        ret,x=sw.GetSwmmResult(3,0,1,i)
        ret,y=sw.GetSwmmResult(3,0,4,i)
        ret,z=sw.GetSwmmResult(3,0,11,i)
        t+=sw.cvar.SWMM_ReportStep
        results.append([t,x,y,z])
    
    print "\n\nIf you saw no errors until now, swmm5 part OK!"
    print "If you see any erors after this point, it is probably because your matplotlib is broken!"
    print "It has nothing to do with swmm5. You can use it now"
    print "---------------------------------------------------------"
    
    import matplotlib
    matplotlib.use('Qt4Agg')
    import matplotlib.pyplot as plt
    from numpy import array
    trans=array(results).T
    plt.fill_between(trans[0],0,trans[1],label="Ranfall(in)")
    ax=plt.gca()
    #plt.legend(loc=1)
    print ax.get_ylim()
    ax.set_ylim(480,0) 
    ax.set_ylabel("Rainfall (mm)")
    ax.set_xlabel("Time (s)")
    plt2=plt.twinx()
    plt2.plot(trans[0],trans[2]/1000.,label="Runoff()")
    plt2.plot(trans[0],trans[3]/1000.,label="Outflow()")
    ax2=plt.gca();
    ax2.set_ylim(0,250)
    ax2.set_xlim(0,15000)
    ax2.set_ylabel(r"Q (m$^3$/s)")
    plt.legend(loc=4)
    plt.show() 