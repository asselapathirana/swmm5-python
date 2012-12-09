#!/usr/bin/env python

"""
setup.py file for SWMM5 pyton library  - Assela Pathirana
"""

from setuptools import setup, Extension

 
swmm5_module = Extension('_swmm5',
                           sources=[ 'climate.c', 'controls.c', 'culvert.c', 'datetime.c', 'dynwave.c', 'error.c', 'findroot.c', 'flowrout.c', 'forcmain.c', 'gage.c', 'gwater.c', 'hash.c', 'iface.c', 'infil.c', 'inflow.c', 'input.c', 'inputrpt.c', 'keywords.c', 'kinwave.c', 'landuse.c', 'lid.c', 'link.c', 'massbal.c', 'mathexpr.c', 'mempool.c', 'node.c', 'odesolve.c', 'output.c', 'project.c', 'qualrout.c', 'rain.c', 'rdii.c', 'report.c', 'routing.c', 'runoff.c', 'shape.c', 'snow.c', 'stats.c', 'statsrpt.c', 'subcatch.c', 'swmm5.c', 'swmm5_iface.c', 'swmm5_wrap.c', 'table.c',  'toposort.c', 'transect.c', 'treatmnt.c', 'xsect.c' ]
                           )

setup (name = 'SWMM5',
       version = '0.1',
       author      = "Assela Pathirana",
       author_email = "assela@pathirana.net",
       url         = "assela.pathirana.net",
       description = """SWMM5  calls from python""",
       ext_modules = [swmm5_module],
       py_modules = ["swmm5"],
	   scripts= ['swmm5Example.inp', 'swmm5_test.py']
       )
