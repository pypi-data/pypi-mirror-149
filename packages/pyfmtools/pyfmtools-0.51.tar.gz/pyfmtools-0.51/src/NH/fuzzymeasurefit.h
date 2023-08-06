//#pragma GCC diagnostic ignored "-Wunused-but-set-variable"
//#pragma GCC diagnostic ignored "-Wunused-result"

/********************* Fuzzy measure toolkit ******************************************

FuzzyMeasureFitLP estimates the values of a k-additive fuzzy measure based on
empirical data - the arguments and values of the discrete Choquet integral.
The empirical data, which consists of pairs (x,y), x \in [0,1]^n, y \in [0,1]
are fitted in the least absolute deviation sense, by converting this problem to
a linear programming problem. The result is an array containing the values of
the Mobius transform of the fuzzy measure, ordered according to set cardinalities.

int	FuzzyMeasureFitLP(int n, int m, int K, int Kadd, double *v, double* XYData, int options=0, 
			double* indexlow=NULL, double* indexhigh=NULL , int option1=0, double* orness=NULL);

Input parameters: 
n - the dimension of inputs, m = 2^n - the number of fuzzy measure values
K - the number of empirical data
Kadd - k in k-additive f. measures, 1 < Kadd < n+1. Kdd=n - f.m. is unrestricted
XYData - an array of size K x (n+1), where each row is the pair (x,y), K data altogether
options (default value is 0)
	1 - lower bounds on Shapley values supplied in indexlow
	2 - upper bounds on Shapley values supplied in indexhigh
	3 - lower and upper bounds on Shapley values supplied in indexlow and indexhigh

	4 - lower bounds on all interaction indices supplied in indexlow
	5 - upper bounds on all interaction indices supplied in indexhigh
	6 - lower and upper bounds on all interaction indices supplied inindexlow and indexhigh
all these value will be treated as additional constraints in the LP

indexlow, indexhigh - array of size n (options =1,2,3) or m (options=4,5,6)
containing the lower and upper bounds on the Shapley values or interaction indices

Notes: 1. arrays indexlow and indexhigh are 0-based if they contain Shapley values (i.e., 
the bound on Shapley value of the first input is in indexlow[0], etc.
but when these arrays contain interaction indices, these are 1-based (since there is a 
non-zero value of the interaction index corresponding to empty set). In this case the bounds
are arranged in cardinality order, i.e., the bounds correspond to the sets in this ordering
(for n=3)
emptyset {1} {2} {3} {12} {13} {23} {123}
2. if an exact value of some index or Shapley value is needed, use indexlow[i]=indexhigh[i]=thisvalue
if no value for some index is required, use indexlow[i]=-1, indexhigh[i]=1 
3. Note that Shapley values have range [0,1], whereas interaction indices have range [-1,1]

options1 (default 0) a flag whose bits indicate which additional properties are needed. 
if the first bit is set then the desired interval of orness values specified in array orness will be used.
if the second bit is set, then the f.m. will be forced to be balanced (currently not implemented)
if the third bit is set, then in addition to fitting the data, the order of output values
will be preserved.  I.e., if y_k >= y_j, then the Choquet integral will be foreced to satisfy C(x_k)>=C(x_j)
as well. Note that this constraint may lead to inconsistent set of conditions, in which case the problem
will have no solution (and no output vector returned).

For example options1 = 1+4  means that the first and third bits are set.

orness - array of size 2 which contains the lower and the upper bounds on the orness value. These values
should be from [0,1], and could coincide if an exact orness value is needed. if the bounds are 0 and 1 
respectively they are ignored. Only used if the first bit of options1 is set.


Output
v - the array which contains the values of the fuzzy measure, must be allocated by 
the calling routine and be of the size m. It will contain the values of the Mobius representation
of the fuzzy measure arranged in cardinality order, see above. The output is FM in Moebius representation.

They may be subsequently converted to the binary ordering, and to the standard fuzzy measure
representation, by using the code below:
	FuzzyMeasureFitLP(n,  m,  KData,  Kadd, Mob_Card,  XYData );
// calculate Mobius representation in binary ordering
	for(i=0;i<m;i++)  Mob_bin[card2bit[i]] = Mob_Card[i];
// calculate the standard representation
	Zeta(Mob_bin,fmeasure_std_bin,n,m);
// where Mob_Card,Mob_bin and fmeasure_std_bin are arrays of size m

The return value is 1 if successful, 0 otherwise (LP has no solution, or was not solved).

Also note that calls to FuzzyMeasureFitLP should be made ONLY after calling 
Preparations_FM(n,&m)
see fuzzymeasuretools.h for its description.

Please read the user guide for more information about fuzzy measures.

=======================================================================================================


int	FuzzyMeasureFitLPsymmetric(int n, int m, int K, int Kadd, double *v, double* XYData, int options=0,
double* indexlow=NULL, double* indexhigh=NULL , int option1=0, double* orness=NULL);

int	FuzzyMeasureFitLPsymmetricinterval(int n,  int K, double *v, double* XYData, int options,
double* indexlow, double* indexhigh, int option1, double* orness );

These two methods have the same parameters as  FuzzyMeasureFitLP but ensure the fuzzy measure is symmetric.

FuzzyMeasureFitLPsymmetricinterval function takes the inputs (data set) as intervals rather than exact values.

=======================================================================================================

Function
int	FuzzyMeasureFitLPStandard(int n, unsigned int m, int K, int Kadd, double *v, double* XYData, int options,
double* indexlow, double* indexhigh, int option1, double* orness );

fits k-tolerant fuzzy measure in the standard (not Moebius!) representation. Therefore its output must be converted to
Moebius representation.

Also the output is  in cardinality ordering. It must be converted to the binary ordering using
for (i = 0; i<m; i++)  w[card2bit[i]] = v[i];

and then to Moebius representation with the function Mobius(w, Mob,  n,  m)
if desired.

when K=n, then the fitted measure is unrestricted (no k-tolerance).



The functions 

int	FuzzyMeasureFitLPMIP(int n, unsigned int m, int K, int Kadd, double *v, double* XYData);

int	FuzzyMeasureFitLP_relaxation(int n, unsigned int m, int K, int Kadd, double *v, double* XYData);

fit k-maxitive fuzzy measures. The first one solves the mixed integer program MIP, and due to the rapidly
growing number of binary variables should be used cautiously in small dimension n<6, due to excessive running time.

The second function uses a simple relaxation technique to fit k-maxitive fuzzy measure. It may deliver a slightly suboptimal
solution compared to MIP, but is much faster, and works well to about n<=10. For higher dimensions the FM becomes too complex because
of 2^n parameters to fit.

The parameters are the same as in FuzzyMeasureFitLP, but the options and the desired indices and orness are not yet implemented, hence omitted.


The output is in standard representation and in cardinality ordering. It must be 
converted to the binary ordering using 
for (i = 0; i<m; i++)  		w[card2bit[i]] = v[i];
	
and then to Moebius representation with the function Mobius(w, Mob,  n,  m)
if desired. 






--------------------------------------------------------------------------------------
 *
 *      begin                : June 10 2007
 *		end					 : June 3 2018
 *		version				 : 3.0 
 *		copyright            : (C) 2007-2018 by Gleb Beliakov
 *		email                : gleb@deakin.edu.au
 *
 * 
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the Lesser GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or (at
 * your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 * 
 * You should have received a copy of the GNU Lesser General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
**************************************************************************************/

#ifndef NULL
#define NULL 0
#endif

LIBDLL_API double max_subset_complement(double* x, int n, int_64 S);


LIBDLL_API int	FuzzyMeasureFitLP(int n, int_64 m, int K, int Kadd, double *v, double* XYData, int options ,
			double* indexlow, double* indexhigh , int option1, double* orness);

LIBDLL_API int	FuzzyMeasureFitLPsymmetric(int n,  int K, double *v, double* XYData, int options,
			double* indexlow, double* indexhigh, int option1, double* orness );

LIBDLL_API int	FuzzyMeasureFitLPsymmetricinterval(int n,  int K, double *v, double* XYData, int options,
			double* indexlow, double* indexhigh, int option1, double* orness );
			
LIBDLL_API int	FuzzyMeasureFitLPStandard(int n, int_64 m, int K, int Kadd, double *v, double* XYData, int options,
			double* indexlow, double* indexhigh, int option1, double* orness );
			
LIBDLL_API int	FuzzyMeasureFitLPMIP(int n, int_64 m, int K, int Kadd, double *v, double* XYData);

LIBDLL_API int	FuzzyMeasureFitLP_relaxation(int n, int_64 m, int K, int Kadd, double *v, double* XYData);

LIBDLL_API int	FuzzyMeasureFitLPKinteractive(int n, int_64 m, int K, int Kadd, double *v, double* XYData, int options,
	double* indexlow, double* indexhigh, int option1, double* orness, double KConst);

LIBDLL_API int	FuzzyMeasureFitLPKinteractiveMaxChains(int n, int_64 m, int K, int Kadd, double *v, double* XYData, int options,
	double* indexlow, double* indexhigh, int option1, double* orness, double KConst);

LIBDLL_API int	FuzzyMeasureFitLPKinteractiveMarginal(int n, int_64 m, int K, int Kadd, double *v, double* XYData, int options,
	double* indexlow, double* indexhigh, int option1, double* orness, double KConst);

LIBDLL_API int	FuzzyMeasureFitLPKinteractiveMarginalMaxChain(int n, int_64 m, int K, int Kadd, double *v, double* XYData, int options,
	double* indexlow, double* indexhigh, int option1, double* orness, double KConst);

LIBDLL_API int	FuzzyMeasureFitLPKinteractiveAutoK(int n, int_64 m, int K, int Kadd, double *v, double* XYData, int options,
	double* indexlow, double* indexhigh, int option1, double* orness, double* KConst, int maxiter);

LIBDLL_API int testmap(int n, int m);
