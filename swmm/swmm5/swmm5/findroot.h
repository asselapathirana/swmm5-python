<<<<<<< HEAD
//-----------------------------------------------------------------------------
//   findroot.h
//
//   Header file for root finding method contained in findroot.c
//
//   Last modified on 11/19/13.
//-----------------------------------------------------------------------------
int findroot_Newton(double x1, double x2, double* rts, double xacc,
                    void (*func) (double x, double* f, double* df, void* p),
					void* p);
double findroot_Ridder(double x1, double x2, double xacc,
	                   double (*func)(double, void* p), void* p);
=======
//-----------------------------------------------------------------------------
//   findroot.h
//
//   Header file for root finding method contained in findroot.c
//-----------------------------------------------------------------------------
int findroot_Newton(double x1, double x2, double* rts, double xacc,
                    void (*func) (double x, double* f, double* df) );
double findroot_Ridder(double x1, double x2, double xacc, double (*func)(double));
>>>>>>> 69bcb3e905257c4a370e55f483acbc4df825991b
