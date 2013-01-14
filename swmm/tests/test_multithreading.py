from swmm5.swmm5tools import SWMM5Simulation, SWMM5Error
import unittest
from nose.tools import nottest
from time import sleep


class testSWMM5(unittest.TestCase):
#class testSWMM5(object):
    
    def runSWMM1(self):
        """Runs swmm and obtain some results"""
        ss=SWMM5Simulation("swmm5/examples/simple/swmm5Example.inp")  
        self.assertEquals(ss.Flow_Units(), 'LPS')
        self.assertEquals(ss.entityList(),['SUBCATCH', 'NODE', 'LINK', 'SYS'])
        g=ss.Results('SYS','SYS', 1)
        [g.next() for x in range(8)]
        self.assertAlmostEqual(g.next(),7.600000858306885)
        self.assertAlmostEqual(g.next(),8.000000000000000)    
        ss.getFiles()
        
        return
    def runSWMM2(self):
        """Runs swmm and obtain some results"""
        ss=SWMM5Simulation("swmm5/examples/waterquality/Example5-EXP.inp")       
        self.assertEquals(ss.Flow_Units(), 'CFS')
        self.assertEquals(ss.entityList(),['SUBCATCH', 'NODE', 'LINK', 'SYS'])
        g=ss.Results('SUBCATCH','S3', 6)
        self.assertAlmostEqual(g.next(),0.00)
        self.assertAlmostEqual(g.next(),9.937597274780273)
        self.assertAlmostEqual(g.next(),9.9885835647583)
        self.assertAlmostEqual(g.next(),9.995906829833984)
        ss.getFiles()
        return        
    
    @nottest # nose should not run this test by default!
    def test_if_swmm5_works_properly_in_multiprocessing(self):
        """ the test is not definitive: Passing does not 'prove' the module conforms with this aspect"""
        import multiprocessing
        from sys import stdout
        jobs = []
        global number_of_processes
        for i in range(number_of_processes):
            p = multiprocessing.Process(target=self.runSWMM1)
            jobs.append(p)
            p.start()    
            p = multiprocessing.Process(target=self.runSWMM2)
            jobs.append(p)
            p.start()  
        print "Job List:", jobs
        for i in range(number_of_processes):
            jobs[i].join()
        sleep(5)
        stdout.flush()
        print "Job List:", jobs
        
 
if __name__=="__main__":
    number_of_processes=20
    print "using  number_of_processes: ", number_of_processes
    unittest.main()
    
    