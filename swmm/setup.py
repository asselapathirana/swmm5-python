#!/usr/bin/env python
"""
setup.py file for SWMM5 pyton library  - Assela Pathirana
"""

from distutils.core import  setup, Extension
from itertools import product
#from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import os

NAME='SWMM5'
VERSION='5.2.0.post6'

# in windows use microsoft compilers
if os.name == 'nt':
    compilerargs = ['-D/DLL=1']
    linkerargs   = []
    class custom_build_ext(build_ext):
        pass
else:
    compilerargs = ['-fPIC', '-D SOL=1', '-fopenmp','-Wno-deprecated','-O3','-Wno-error','-Wno-error=format-security' ]
    linkerargs   = ['-fopenmp','-Wno-deprecated','-O3','-Wno-error']

    class custom_build_ext(build_ext):
        def build_extensions(self):
            # Override the compiler executables. Importantly, this
            # removes the "default" compiler flags that would
            # otherwise get passed on to to the compiler, i.e.,
            # distutils.sysconfig.get_var("CFLAGS").
            self.compiler.set_executable("compiler_so", "g++")
            self.compiler.set_executable("compiler_cxx", "g++")
            self.compiler.set_executable("linker_so", "g++")
            build_ext.build_extensions(self)


with open("README.txt","r") as f:
    README=f.read()
src_path="swmm5/swmm5"
allsrc=[os.path.join(src_path, ff) for ff in os.listdir(src_path) if os.path.isfile(os.path.join(src_path, ff))]
csources = [file for file in allsrc if file[-2:].lower()==".c"]
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
	   keywords=KEYWORDS,
       #options={'build_ext':{'inplace':True}}, 
       cmdclass={"build_ext": custom_build_ext}
       )
