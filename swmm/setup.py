#!/usr/bin/env python
"""
setup.py file for SWMM5 pyton library  - Assela Pathirana
"""
<<<<<<< HEAD
NAME="SWMM5"
VERSION="5.1.0.10"

from distutils.core import  setup, Extension
from itertools import product
from setuptools import setup, Extension, Command
import os,sys

=======

from distutils.core import  setup, Extension
from itertools import product
>>>>>>> 69bcb3e905257c4a370e55f483acbc4df825991b

with open("README.txt","r") as f:
    README=f.read()
    
<<<<<<< HEAD
csources=['swmm5/swmm5/'+x for x in [ 'climate.c', 'controls.c', 'culvert.c', 
									 'datetime.c', 'dwflow.c',
                                     'dynwave.c', 'error.c', 'exfil.c','findroot.c', 'flowrout.c', 
                                     'forcmain.c', 'gage.c', 'gwater.c', 'hash.c', 
									 'hotstart.c','iface.c', 
                                     'infil.c', 'inflow.c', 'input.c', 'inputrpt.c', 'keywords.c', 
                                     'kinwave.c', 'landuse.c', 'lid.c', 'lidproc.c',
									 'link.c', 'massbal.c', 
=======
csources=['swmm5/swmm5/'+x for x in [ 'climate.c', 'controls.c', 'culvert.c', 'datetime.c', 
                                     'dynwave.c', 'error.c', 'findroot.c', 'flowrout.c', 
                                     'forcmain.c', 'gage.c', 'gwater.c', 'hash.c', 'iface.c', 
                                     'infil.c', 'inflow.c', 'input.c', 'inputrpt.c', 'keywords.c', 
                                     'kinwave.c', 'landuse.c', 'lid.c', 'link.c', 'massbal.c', 
>>>>>>> 69bcb3e905257c4a370e55f483acbc4df825991b
                                     'mathexpr.c', 'mempool.c', 'node.c', 'odesolve.c', 'output.c', 
                                     'project.c', 'qualrout.c', 'rain.c', 'rdii.c', 'report.c', 
                                     'routing.c', 'runoff.c', 'shape.c', 'snow.c', 'stats.c', 
                                     'statsrpt.c', 'subcatch.c', 'swmm5.c', 
                                      'table.c',  'toposort.c', 
                                     'transect.c', 'treatmnt.c', 'xsect.c' , 
                                     # headers now
                                     #"consts.h", "datetime.h", "enums.h", "error.h", 
                                     #"findroot.h", "funcs.h", "globals.h", "hash.h", 
                                     #"headers.h", "infil.h", "keywords.h", "lid.h", 
                                     #"macros.h", "mathexpr.h", "mempool.h", "objects.h", 
                                     #"odesolve.h", "swmm5.h", "swmm5_iface.h", "text.h"
                                     ]]
csources.extend(['swmm5/swmm5_wrap.c','swmm5/swmm5_interface.c'])
swmm5_module = Extension('_swmm5',
<<<<<<< HEAD
                           sources=csources,
						     #extra_compile_args=['/openmp'],
                             #extra_link_args=['/openmp']
=======
                           sources=csources
>>>>>>> 69bcb3e905257c4a370e55f483acbc4df825991b
                           )


EXAMPLES=["simple"]
EXTS=["inp", "py"]
EXTS.extend([x.upper() for x in EXTS])
EXAMPLES=list(product(EXAMPLES,EXTS))
package_data=[ "examples/"+x[0]+"/*."+x[1] for x in EXAMPLES]
<<<<<<< HEAD
print(package_data)




if ((not NAME) or (not VERSION)):
	print ("environment variables 'name' and 'version' are not set.")
	print ("Please set them e.g. name=SWMM5, version=1.1.0.1 (x.y.z.k)")
	print (" .. and rerun.")
	print ("Exiting ...")
	sys.exit()


KEYWORDS=["Hydraulics", "Hydrology", "Urban Drainage", "Sewerage", "Water Engineering", "Numerical Methods","Computer Model","Environmental Science", "Engineering", "Science"]


	

SETUPNAME=NAME+"-"+VERSION
LICENSE="GNU General Public License version 3"
LONGDISC="""%(rm)s""" % {"lc": LICENSE, "rm": README}




=======
print package_data
NAME='SWMM5'
VERSION='0.4.1.0dev'
SETUPNAME=NAME+"-"+VERSION
LICENSE=u"GNU General Public License version 3"
LONGDISC="""%(rm)s""" % {"lc": LICENSE, "rm": README}
>>>>>>> 69bcb3e905257c4a370e55f483acbc4df825991b
CLASSIFY=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Environment :: Other Environment",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
<<<<<<< HEAD
	"Operating System :: MacOS :: MacOS X",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Development Status :: 5 - Production/Stable",
=======
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Development Status :: 4 - Beta",
>>>>>>> 69bcb3e905257c4a370e55f483acbc4df825991b
        "Natural Language :: English"
        ]
setup (name = NAME,
       version = VERSION,
       author      = "Assela Pathirana",
       author_email = "assela@pathirana.net",
       description = """SWMM5  calls from python""",       
       packages = ["swmm5"],
       package_data={'': package_data},
       ext_modules = [swmm5_module],
       license=LICENSE,
<<<<<<< HEAD
       url="http://assela.pathirana.net/SWMM5-Python",
       #download_url="http://swmm5-ea.googlecode.com/files/"+SETUPNAME+".zip",
       long_description = LONGDISC, 
       classifiers=CLASSIFY,
	   keywords=KEYWORDS
=======
       url=u"http://assela.pathirana.net/SWMM5-Python",
       #download_url="http://swmm5-ea.googlecode.com/files/"+SETUPNAME+".zip",
       long_description = LONGDISC, 
       classifiers=CLASSIFY
>>>>>>> 69bcb3e905257c4a370e55f483acbc4df825991b
       )
