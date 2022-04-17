/* %module swmm5 */
 %module(package="swmm5", moduleimport="import $module") swmm5 
/* ABOVE fix was needed when swig upgraded to verson 4. thanks: https://github.com/swig/swig/issues/1486 */
 %include "typemaps.i"
 %include "cstring.i"
 /* read http://www.swig.org/Doc1.3/Arguments.html */
 %apply int *OUTPUT { int *value };
 %apply long *OUTPUT { long *value };
 %apply float *OUTPUT { float *value };
 %apply double *OUTPUT { double *value };
 %cstring_bounded_output(char *value, 129);
 %{
 /* Includes the header in the wrapper code */
 #include "swmm5_interface.h"
 #include "swmm5/error.h"
 %} 
 
 /* Parse the header file to generate wrappers */
 %include "swmm5_interface.h"
 %include "swmm5/error.h"
