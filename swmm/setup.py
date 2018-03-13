#!/usr/bin/env python
"""
setup.py file for SWMM5 pyton library  - Assela Pathirana
"""

from distutils.core import  setup, Extension
from itertools import product
from setuptools import setup, Extension, Command
import os
import glob

NAME='SWMM5'
VERSION='5.1.0.102-2'

# in windows use microsoft compilers
if os.name == 'nt':
    compilerargs = []
    linkerargs   = []
else:
    compilerargs = ['-fopenmp','-Wno-deprecated','-O3']
    linkerargs   = ['-fopenmp','-Wno-deprecated','-O3']


with open("README.txt","r") as f:
    README=f.read()
    
ccodefiles=[  'climate.c', 'controls.c', 'culvert.c', 
									 'datetime.c', 'dwflow.c',
                                     'dynwave.c', 'error.c', 'exfil.c','findroot.c', 'flowrout.c', 
                                     'forcmain.c', 'gage.c', 'gwater.c', 'hash.c', 
									 'hotstart.c','iface.c', 
                                     'infil.c', 'inflow.c', 'input.c', 'inputrpt.c', 'keywords.c', 
                                     'kinwave.c', 'landuse.c', 'lid.c', 'lidproc.c',
									 'link.c', 'massbal.c', 
                                     'mathexpr.c', 'mempool.c', 'node.c', 'odesolve.c', 'output.c', 
                                     'project.c', 'qualrout.c', 'rain.c', 'rdii.c', 'report.c', 'roadway.c',
                                     'routing.c', 'runoff.c', 'shape.c', 'snow.c', 'stats.c', 'surfqual.c',
                                     'statsrpt.c', 'subcatch.c', 'swmm5.c', 
                                      'table.c',  'toposort.c', 
                                     'transect.c', 'treatmnt.c', 'xsect.c' , ]

# headers now
#"consts.h", "datetime.h", "enums.h", "error.h", 
#"findroot.h", "funcs.h", "globals.h", "hash.h", 
#"headers.h", "infil.h", "keywords.h", "lid.h", 
#"macros.h", "mathexpr.h", "mempool.h", "objects.h", 
#"odesolve.h", "swmm5.h", "swmm5_iface.h", "text.h"

csources=['swmm5/swmm5/'+x for x in ccodefiles]
csources.extend(['swmm5/swmm5_wrap.c','swmm5/swmm5_interface.c'])
swmm5_module = Extension('_swmm5',
    sources=csources,
    extra_compile_args=compilerargs,
    extra_link_args=linkerargs,
                           )


EXAMPLES=["simple"]
EXTS=["inp", "py"]
EXTS.extend([x.upper() for x in EXTS])
EXAMPLES=list(product(EXAMPLES,EXTS))
package_data=[ "examples/"+x[0]+"/*."+x[1] for x in EXAMPLES]

KEYWORDS=["Hydraulics", "Hydrology", "Urban Drainage", "Sewerage", "Water Engineering", "Numerical Methods","Computer Model","Environmental Science", "Engineering", "Science"]


	

SETUPNAME=NAME+"-"+VERSION
LICENSE="GNU General Public License version 3"
LONGDISC="""%(rm)s""" % {"lc": LICENSE, "rm": README}




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
	"Operating System :: MacOS :: MacOS X",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Development Status :: 5 - Production/Stable",
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
       url="http://assela.pathirana.net/SWMM5-Python",
       #download_url="http://swmm5-ea.googlecode.com/files/"+SETUPNAME+".zip",
       long_description = LONGDISC, 
       classifiers=CLASSIFY,
	   keywords=KEYWORDS
       )
