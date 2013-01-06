#!/usr/bin/env python
"""
setup.py file for SWMM5 pyton library  - Assela Pathirana
"""

from setuptools import setup, Extension
from itertools import product

with open("README.txt","r") as f:
    README=f.read()
 
swmm5_module = Extension('_swmm5',
                           sources=['swmm5/'+x for x in [ 'climate.c', 'controls.c', 'culvert.c', 'datetime.c', 
                                     'dynwave.c', 'error.c', 'findroot.c', 'flowrout.c', 
                                     'forcmain.c', 'gage.c', 'gwater.c', 'hash.c', 'iface.c', 
                                     'infil.c', 'inflow.c', 'input.c', 'inputrpt.c', 'keywords.c', 
                                     'kinwave.c', 'landuse.c', 'lid.c', 'link.c', 'massbal.c', 
                                     'mathexpr.c', 'mempool.c', 'node.c', 'odesolve.c', 'output.c', 
                                     'project.c', 'qualrout.c', 'rain.c', 'rdii.c', 'report.c', 
                                     'routing.c', 'runoff.c', 'shape.c', 'snow.c', 'stats.c', 
                                     'statsrpt.c', 'subcatch.c', 'swmm5.c', 'swmm5_iface.c', 
                                     'swmm5_wrap.c', 'table.c',  'toposort.c', 
                                     'transect.c', 'treatmnt.c', 'xsect.c' ]]
                           )


EXAMPLES=["simple"]
EXTS=["inp", "py"]
EXTS.extend([x.upper() for x in EXTS])
EXAMPLES=list(product(EXAMPLES,EXTS))
package_data=[ "examples/"+x[0]+"/*."+x[1] for x in EXAMPLES]

NAME='SWMM5'
VERSION='0.3.0.0'
SETUPNAME=NAME+"-"+VERSION
LICENSE=u"GNU General Public License version 3"
LONGDISC="""Python interface for the popular urban drainage model EPA-SWMM 5.0 engine. 
SWMM5 is realeased by United States Environmental Protection Agency to public domain. 
This python package is copyrighted by Assela Pathirana and released under %(lc)s. \n\n 
README.txt\n
----------\n
%(rm)s\n
----------\n
""" % {"lc": LICENSE, "rm": README}
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
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Development Status :: 4 - Beta",
        "Natural Language :: English"
        ]
setup (name = NAME,
       version = VERSION,
       author      = "Assela Pathirana",
       author_email = "assela@pathirana.net",
       description = """SWMM5  calls from python""",
       ext_modules = [swmm5_module],
       packages = ["swmm5"],
       package_data={'swmm5': package_data},
       license=LICENSE,
       url=u"http://assela.pathirana.net/SWMM5-Python",
       download_url="http://swmm5-ea.googlecode.com/files/"+SETUPNAME+".zip",
       long_description = LONGDISC, 
       classifiers=CLASSIFY
       )
