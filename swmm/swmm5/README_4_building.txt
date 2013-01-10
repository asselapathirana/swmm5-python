Building windows binary works only at dos prompt (not in cygwin terminal) at the moment. 
Need to source CodeBlocks\MinGW\mingwvars.bat
( Linker error cannot find -lmsvcr90 is due to failing to do this!)

# any changes to *.i file should be followed by running swig to geterate interface files. 
