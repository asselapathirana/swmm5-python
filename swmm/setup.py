#!/usr/bin/env python
"""
setup.py file for SWMM5 pyton library  - Assela Pathirana
"""

from distutils.core import  setup, Extension
from itertools import product
#from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import os
import pathlib

NAME='SWMM5'
VERSION='5.2.1'

# in windows use microsoft compilers
if os.name == 'nt':
    compilerargs = ['-D/DLL=1']
    linkerargs   = []
    class custom_build_ext(build_ext):
        pass
else:

    class CMakeExtension(Extension):
        def __init__(self, name):
            # don't invoke the original build_ext for this special extension
            super().__init__(name, sources=[])

    compilerargs = ['-fPIC', '-D SOL=1', '-fopenmp','-Wno-deprecated','-O3','-Wno-error','-Wno-error=format-security' ]
    linkerargs   = ['-fopenmp','-Wno-deprecated','-O3','-Wno-error']

    class custom_build_ext(build_ext):
        cwd = pathlib.Path().absolute()
        # these dirs will be created in build_py, so if you don't have
        # any python sources to bundle, the dirs will be missing
        build_temp = pathlib.Path(self.build_temp)
        build_temp.mkdir(parents=True, exist_ok=True)
        extdir = pathlib.Path(self.get_ext_fullpath(ext.name))
        extdir.mkdir(parents=True, exist_ok=True)
        # example of cmake args
        config = 'Debug' if self.debug else 'Release'
        cmake_args = [
            '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + str(extdir.parent.absolute()),
            '-DCMAKE_BUILD_TYPE=' + config
        ]

        # example of build args
        build_args = [
            '--config', config,
            '--', '-j4'
        ]

        os.chdir(str(build_temp))
        self.spawn(['cmake', str(cwd)] + cmake_args)
        if not self.dry_run:
            self.spawn(['cmake', '--build', '.'] + build_args)
        # Troubleshooting: if fail on line above then delete all possible 
        # temporary CMake files including "CMakeCache.txt" in top level dir.
        os.chdir(str(cwd))


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
