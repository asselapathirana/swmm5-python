%module swmm5
 %include "typemaps.i"
 %include "cstring.i"
 /* read http://www.swig.org/Doc1.3/Arguments.html */
 %apply int *OUTPUT { int *value };
 %apply long *OUTPUT { long *value };
 %apply float *OUTPUT { float *value };
 %apply double *OUTPUT { double *value };
 %cstring_bounded_output(char *value, 1024);
 %{
 /* Includes the header in the wrapper code */
 #include "swmm5_iface.h"
 %}
 
 /* Parse the header file to generate wrappers */
 %include "swmm5_iface.h"
