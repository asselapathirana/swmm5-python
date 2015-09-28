from swmm5.swmm5tools import SWMM5Simulation, SWMM5Error
import unittest
from nose.tools import nottest
from time import sleep


class testSWMM5(unittest.TestCase):
#class testSWMM5(object):

    #class testSWMM5(object):
    # since python 3.4 testcase is not picklable without 
    #doing the following (offender is _outcome)
    # http://stackoverflow.com/questions/25646382/python-3-4-multiprocessing-does-not-work-with-unittest
    def __getstate__(self):
        self_dict = self.__dict__.copy()
        try:
            del self_dict['_outcome']
        except KeyError:
            print("This python version does not provide key '_outcome' - harmless, ignoring...")
        
        return self_dict

    def __setstate(self, state):
            self.__dict__.update(self_dict) 
    
    def runSWMM1(self):
        """Runs swmm and obtain some results"""
        ss=SWMM5Simulation("swmm5/examples/simple/swmm5Example.inp")  
        self.assertEquals(ss.Flow_Units(), 'LPS')
        self.assertEquals(ss.entityList(),['SUBCATCH', 'NODE', 'LINK', 'SYS'])
        g=ss.Results('SYS','SYS', 1)
        [next(g) for x in range(7)]
        self.assertAlmostEqual(next(g),7.600000858306885)
        self.assertAlmostEqual(next(g),8.000000000000000)    
        ss.getFiles()
        
        return
    def runSWMM2(self):
        """Runs swmm and obtain some results"""

        ss=SWMM5Simulation("swmm5/examples/waterquality/Example5-EXP.inp")       
        self.assertEquals(ss.Flow_Units(), 'CFS')
        self.assertEquals(ss.entityList(),['SUBCATCH', 'NODE', 'LINK', 'SYS'])
        g=ss.Results('SUBCATCH','S3', 8)
        self.assertAlmostEqual(next(g),0.00)
        self.assertAlmostEqual(next(g),0.00)
        self.assertAlmostEqual(next(g),0.00)
        self.assertAlmostEqual(next(g),0.00)
        self.assertAlmostEqual(next(g),0.00)
        self.assertAlmostEqual(next(g),13.44666862487793)
        self.assertAlmostEqual(next(g),14.10814380645752)
        self.assertAlmostEqual(next(g),14.707027435302734)
        self.assertAlmostEqual(next(g),15.237997055053711)
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
        print("Job List:", jobs)
        for i in range(number_of_processes):
            jobs[i].join()
        sleep(5)
        stdout.flush()
        print("Job List:", jobs)
        
 
if __name__=="__main__":
    number_of_processes=20
    print("using  number_of_processes: ", number_of_processes)
    unittest.main()
    
    