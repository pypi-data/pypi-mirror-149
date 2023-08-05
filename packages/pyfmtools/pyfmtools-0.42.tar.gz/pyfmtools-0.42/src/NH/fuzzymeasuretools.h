/********************* Fuzzy measure toolkit ******************************************

This is a set of useful routines for manipulations with fuzzy measures 
(and other set functions). They include binary encoding of a discrete set 
(as  integers (up to 32 elements in a set)), simple set operations: 
intersection, union, inclusion, difference, etc. various representations of 
fuzzy measures (standard, Moebius), orderings of their values, conversions, 
calculations of Shapley, Banzhaf and other interaction indices, orness, entropy, etc.
Calculation of Choquet and Sugeno integrals for a given input x.

--------------------------------------------------------------------------------------
 *
 *      begin                : May 10 2007
 *		end					 : September 3 2020
 *              version                          : 4.0 
 *              copyright            : (C) 2007-2020 by Gleb Beliakov
 *              email                : gleb@deakin.edu.au
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


/*
Notes: The bitwise operations (sets, subsets, element of the set, etc.) are 0-based, ie element 1 corresponds to the 0th element of set A. 

Sparse representation: 1-based , ie pair (1,2) corresponds to the bitwise set A=11b =3

Geberal capacities start with 0 (emptyset) and go to 2^n elements
// in binary ordering the subsets are ordered as
// 0 1 2 12 3 13 23 123 4 14 24 124 34 134 234 1234,...
// (which corresponds to the order 0,1,2,3,... in binary form)
// in cardinality ordering they are ordered as
// 0 1 2 3 4 5 6 12 13 14 15 16 23 24 25 26 34 35 36 45 46 56 123 124,...
// (empty, singletons, pairs,triples, etc.)

2-additive capacities are coded as an array of singletons (starting from 0, hence no empty set) and pairs without repetitions that is pairs (1,2), (1,3)...(2,3), (2,4)...(3,4)...
Always in cardinality ordering

Sparse representation is the structure SparseFM - contains arrays of singletons, nonzero pairs and their indices (1-based) tuples and their cardinalities and indices
Sparse is meaningful for Mobius/interaction or nonmodularity representations


2-additive and sparse methods canbe called without Preparations_FM

*/

#include "generaldefs.h"

#define FM_SPARSE

#define GBtolerance 0.00001

double ElapsedTime();
void   ResetTime();

struct valindex {
        double v;
        int i;
} ;


//#define int_64 unsigned long long
typedef unsigned long long int_64;

typedef unsigned short uint16_t;

//typedef int_64 myint;
//typedef unsigned int myint;

typedef uint16_t myint;
// any of the above, for m<16 use uint_16

typedef unsigned int uint;

// float or double
//typedef float  myfloat;
typedef double  myfloat;

/* Global arrays*/
extern valindex tempxi[100];

LIBDLL_API extern double   *m_factorials;  // keeps factorials  n! up to n
LIBDLL_API extern int      *card;                  // array to keep set cardinalities in binary ordering
LIBDLL_API extern int *cardpos;   // array to store the indices of elements of different cardinalities in the cardinality ordering

LIBDLL_API extern int_64 *bit2card; // arrays to transform from one ordering to another
LIBDLL_API extern int_64 *card2bit;

LIBDLL_API extern int *cardposm;   // array to store the indices of elements of different cardinalities in the cardinality ordering

LIBDLL_API extern int_64 *bit2cardm; // arrays to transform from one ordering to another
LIBDLL_API extern int_64 *card2bitm;

#include<cstdlib>
#include <vector>
using namespace std;


#ifdef FM_SPARSE


/*
template <class T>
class vectorWrapper : public std::vector<T>
{   
public:
  vectorWrapper() {
    this->_M_impl _M_start = this->_M_impl _M_finish = this->_M_impl _M_end_of_storage = NULL;
  }   

  vectorWrapper(T* sourceArray, int arraySize)
  {   
    this->_M_impl _M_start = sourceArray;
    this->_M_impl _M_finish = this->_M_impl _M_end_of_storage = sourceArray + arraySize;
  }   

  ~vectorWrapper() {
    this->_M_impl _M_start = this->_M_impl _M_finish = this->_M_impl _M_end_of_storage = NULL;
  }   

  void wrapArray(T* sourceArray, int arraySize)
  {   
    this->_M_impl _M_start = sourceArray;
    this->_M_impl _M_finish = this->_M_impl _M_end_of_storage = sourceArray + arraySize;
  }   
};*/

#ifdef R_cpp11
//#include "cpp11.hpp"

//#define m_singletons (*p_singletons)
//#define m_pairs (*p_pairs)
//#define m_tuples (*p_tuples)
//#define m_pair_index (*p_pair_index)
//#define m_tuple_start (*p_tuple_start)
//#define m_tuple_content (*p_tuple_content)




struct SparseFM {
	int n;

	vector<double>  m_singletons;
	vector<double>  m_pairs;
	vector<double>  m_tuples;

	vector<int> m_pair_index;// goes in pairs, hence  m_pair_index[2i],m_pair_index[2i+1] corresponds to m_pairs[i];

	vector<int> m_tuple_start; // pints to cardinality, list of elements, stored  in m_tuple_content
	vector<int> m_tuple_content;  // for any j such that m_tules[j] is the value, m_tuple_content[m_tuple_start[j]] is the cardinality
};	
#else
struct SparseFM {
	int n;

	vector<double>  m_singletons;
	vector<double>  m_pairs;
	vector<double>  m_tuples;

	vector<uint16_t> m_pair_index;// goes in pairs, hence  m_pair_index[2i],m_pair_index[2i+1] corresponds to m_pairs[i];

	vector<int> m_tuple_start; // pints to cardinality, list of elements, stored  in m_tuple_content
	vector<uint16_t> m_tuple_content;  // for any j such that m_tules[j] is the value, m_tuple_content[m_tuple_start[j]] is the cardinality
};	
#endif
#endif

LIBDLL_API int_64 Bit2Card(int_64 c);
LIBDLL_API int_64 Card2Bit(int_64 c);

// this routine should be called first to prepare all the arrays for small FM (up to n=15, may be 24 (sizes are 2^n)), otherwise the arrays become too big
LIBDLL_API void Preparations_FM(int n, int_64 *m);

LIBDLL_API void Preparations_fm_marginal(int n, int_64 *m, int Kinter);

LIBDLL_API void ConvertCard2Bit(double* dest, double* src,  int_64 m);

LIBDLL_API int_64 Bit2card(int_64 id, int n, int kint, int arraysize);

// this routine should be called last to clean all the arrays
LIBDLL_API void Cleanup_FM();


/* useful routines */
extern double   minf(double a, double b); 
double  maxf(double a, double b);
int             sign(int i);   // sign of i
int             IsOdd(int i);  // is i odd ?


LIBDLL_API unsigned int bitweight(int_64 i);

LIBDLL_API unsigned int cardf(int_64 i); // count how many bits in i are set
LIBDLL_API double xlogx(double t);         // x log x (but takes care of x close to 0, using tolerance parameter


/* Set manipulations. A set is represented by an unsigned int (32 bits) */
LIBDLL_API void    RemoveFromSet(int_64* A, int i);  // remove a from set i
LIBDLL_API void    AddToSet(int_64* A, int i);               // add a to set i
LIBDLL_API int             IsInSet(int_64 A, int i);                 // does a belong to set i?
LIBDLL_API int             IsSubset(int_64 A, int_64 B);       // is B subset of A ?
LIBDLL_API int_64  Setunion(int_64 A, int_64 B); // returns the  union of sets A and B
LIBDLL_API int_64  Setintersection(int_64 A, int_64 B); // returns the  intersection of sets i and j
LIBDLL_API int_64  Setdiff(int_64 A, int_64 B);                  // returns set difference  i \ j
LIBDLL_API double min_subset(double* x, int n, int_64 S); // returns minimum of x_i, such that i belongs to set S
LIBDLL_API double max_subset(double* x, int n, int_64 S); // returns maximum of x_i, such that i belongs to set S
LIBDLL_API int_64 UniversalSet(int n);
LIBDLL_API int Removei_th_bitFromSet(int_64* A, int i);

LIBDLL_API  int_64 choose(int i, int n);




LIBDLL_API int_64 remove1bit(int_64 a, int i);
// counting fom 0


LIBDLL_API int_64 RemoveHighestBit(int_64 a, int K);

LIBDLL_API inline int HasBitsAboveK(int_64 a, int K) { // K counting from 1
	return(a >= (int_64)1 << K);
}

LIBDLL_API inline int TopElement(int_64 a) {
	// return true is a= 11111...
	return (bitweight(a + 1) == 1);
}



#include "fmrandom.h"






LIBDLL_API void ExpandKinteractive2Bit(double* dest, double* src, int n, int_64 m, int kint, int arraysize);
LIBDLL_API void ExpandKinteractive2Bit_m(double* dest, double* src, int n, int_64 m, int kint, int arraysize, double* VVC);
// converts compact k-interactive representation to full length binary ordering. The second call required working memory of size m.

LIBDLL_API unsigned int ShowValue(int_64 s); // shows the elements of a subset as a decimal string (up to 10 elements)

LIBDLL_API double Choquet(double*x, double* v, int n, int_64 m);
/* Calculates the value of a descrete Choquet integral of x, wrt fuzzy measure v. 
   Parameters: x array[n] ,v array[m], n, m=2^n 
   This proceduce requires sorting the array of pairs (v[i],i) in non-decreasing order
   (perfored by standard STL sort function, and RemoveFromSet() function, to remove
   an indicated bit from a set (in its binary representation). 
*/

LIBDLL_API double ChoquetKinter(double*x, double* v, int n, int_64 m, int kint);
/* As above, but for kinteractive f.m. using compact representation of v  (in cardinality ordering! */

LIBDLL_API double ChoquetMob(double*x, double* Mob, int n, int_64 m);
/* This is an alternative calculation of the Choquet integral from the Moebius transform v. 
   It is not as efficient as Choquet(). Provided for testing purposes.
*/

LIBDLL_API double Sugeno(double*x, double* v, int n, int_64 m);
/* Calculates the value of a descrete Sugeno integral of x, wrt fuzzy measure v 
Parameters: x array[n] ,v array[m], n, m=2^n 
This proceduce requires sorting the array of pairs (v[i],i) in non-decreasing order
(perfored by standard STL sort function, and RemoveFromSet() function, to remove
an indicated bit from a set (in its binary representation)
Also requires maxf and minf functions.
*/

LIBDLL_API double OWA(double*x, double* v, int n );
/* Calculates the value of OWA */

LIBDLL_API double WAM(double*x, double* v, int n );
/* Calculates the value of WAM */

LIBDLL_API void ConstructLambdaMeasure(double *singletons, double *lambda, double *v, int n, int_64 m);
/* Given the values of the fuzzy measure at singletons, finds the appropriate
lambda, and constructs the rest of the fuzzy measure. Returns lambda and v at the output
*/

/* ---------------Operations on fuzzy measures -------------------------*/

LIBDLL_API double Orness(double* Mob, int n, int_64 m); // calculates orness value of a fuzzy measure

LIBDLL_API double Entropy(double* v, int n, int_64 m);// calculates Entropy of a fuzzy measure

LIBDLL_API double OrnessOWA(double* w, int n); // calculates orness value of a fuzzy measure

LIBDLL_API void Mobius(double* v, double* Mob, int n, int_64 m); // calculates Moebius representation of v
/* the output array w should have the same size 2^n=m as v */

LIBDLL_API void Zeta(double* Mob, double* v, int n, int_64 m);// calculates inverse Moebius transform

LIBDLL_API void Shapley(double* v, double* x, int n, int_64 m); // calculates the array x of Shapley values
LIBDLL_API void Banzhaf(double* v, double* x, int n, int_64 m);// calculates the array x of Banzhaf indices

LIBDLL_API void ShapleyMob(double* Mob, double* w, int n, int_64 m);
LIBDLL_API void BanzhafMob(double* Mob, double* w, int n, int_64 m);

LIBDLL_API void InteractionMob(double* Mob, double* w, int_64 m); // calculates all 2^n interaction indices (returned in w)
LIBDLL_API void InteractionBMob(double* Mob, double* w, int_64 m); // calculates all 2^n Banzhaf interaction indices (returned in w)

LIBDLL_API void NonadditivityIndex(double* v, double* w, int n, int_64 m); // calculates  all 2^n nonadditivity indices (returned in w)
LIBDLL_API void NonadditivityIndexMob(double* Mob, double* w, int n, int_64 m); // calculates  all 2^n nonadditivity indices (returned in w) using Mobius transform


LIBDLL_API void NonmodularityIndex(double* v, double* w, int n, int_64 m);
// calculates  all 2^n nonmodularity indices (returned in w)

LIBDLL_API void NonmodularityIndexMob(double* Mob, double* w, int n, int_64 m);
// calculates  all 2^n nonmodularity indices (returned in w) using Mobius transform

LIBDLL_API void NonmodularityIndexMobkadditive(double* Mob, double* w, int n, int k, int_64 m);
// calculates  all 2^n nonmodularity indices (returned in w) using Mobius transform of 
//a k-additive FM in cardinality ordering (of length 2^n=m)

LIBDLL_API void NonmodularityIndexKinteractive(double* v, double* w, int n, int kint,int_64 m, int length );
// the same for k-interactive FM. Requires the length = arraysize of the k-interactive FM. Can be optimised by not calculating many zeros, todo.

LIBDLL_API void BipartitionShapleyIndex(double* v, double* w, int n, int_64 m); // calculates  all 2^n bipartition Shapley indices (returned in w)
LIBDLL_API void BipartitionBanzhafIndex(double* v, double* w, int n, int_64 m); // calculates  all 2^n bipartition Banzhaf indices (returned in w)

LIBDLL_API void dualm(double* v, double* w, int n, int_64 m); // calculates the dual fuzzy measure, returns it in w
LIBDLL_API void dualMob(myfloat* src, myfloat* dest, int_64 m);  // same using Mobius

// Various queries about a fuzzy measure. All performed with a given tolerance. 
LIBDLL_API int IsMeasureAdditive(double* v, int n, int_64 m);
LIBDLL_API int IsMeasureBalanced(double* v, int_64 m);
LIBDLL_API int IsMeasureSelfdual(double* v, int_64 m);
LIBDLL_API int IsMeasureSubadditive(double* v, int_64 m);
LIBDLL_API int IsMeasureSubmodular(double* v, int_64 m);
LIBDLL_API int IsMeasureSuperadditive(double* v, int_64 m);
LIBDLL_API int IsMeasureSupermodular(double* v, int_64 m);
LIBDLL_API int IsMeasureSymmetric(double* v, int n, int_64 m);
LIBDLL_API int IsMeasureKMaxitive(double* v, int n, int_64 m);




LIBDLL_API void dualMobKadd( myfloat* src, myfloat* dest, int m, int length, int k);

LIBDLL_API void Shapley2addMob(double* v, double* x, int n);
// calculates the array x of Shapley values for 2 additive fm in compact representation (cardinality based)
LIBDLL_API void Banzhaf2addMob(double* v, double* x, int n);
// calculates the array x of Banzhaf indices for 2 additive fm in compact representation (cardinality based)

LIBDLL_API double Choquet2add(double*x, double* Mob, int n);
// calculates the Choquet integal of x  for 2 additive fm in compact Mobius representation (cardinality based)

LIBDLL_API void random_coefficients(int n, vector<myfloat> & c);

#ifdef FM_SPARSE

/*
Sparse representation of k-additive capacities. Thre representation is in the form of singletons, pairs and tuples with nonzero values, stored and indexed in the respective 
arrays (see above in this file)

 Prepares an empty structure, given the list of cardinalities of the nonzero tuples (cardinality, tuple composition) like this 2 pairs 4-tuple and a triple:  (2,1,2,  2, 3,1,   4, 1,2,3,4,  3,3,2,1...)

 It is used to allocate storage and later populate these values
*/
LIBDLL_API void Prepare_FM_sparse0(int n, int tupsize,  int* tuples, struct SparseFM* cap);
LIBDLL_API void Prepare_FM_sparse(int n, int tupsize, double *tups, int* tuples, struct SparseFM* cap);
LIBDLL_API void Free_FM_sparse(struct SparseFM* cap);

/*  Returns the cardinality of the tuple numbered i in the list of tuples */
LIBDLL_API int TupleCardinalitySparse(int i, struct SparseFM* cap);

LIBDLL_API int  GetNumTuples(struct SparseFM* cap);
LIBDLL_API int  GetSizeArrayTuples(struct SparseFM* cap);


/* checks if element i (1-based!!!) belongs to the tuple indexed A (whose cardinality can be 1,2, other (automatically determined) */
LIBDLL_API int             IsInSetSparse(int A, int card, int i, struct SparseFM* cap);

/* checks if tuple B is a subset of A */
LIBDLL_API int             IsSubsetSparse(int A, int cardA, int B, int cardB, struct SparseFM* cap);

/* calculates minimum (maximum) of (x_i) with the indices belonging to tuple indexed as S (its cardinality cardS can be 1,2, other( put 3, will be determined automatically)
note that x is 0-based, tuples are 1-based */
LIBDLL_API double min_subsetSparse(double* x, int n, int S, int cardS, struct SparseFM* cap);
LIBDLL_API double max_subsetSparse(double* x, int n, int S, int cardS, struct SparseFM* cap);

/* calculates the Choquet integral in Mobius representation */
LIBDLL_API double ChoquetMobSparse(double*x, int n, struct SparseFM* cap);

/* Shapley and Banzhaf values vector of a capacity */
LIBDLL_API void ShapleyMobSparse(double* v, int n, struct SparseFM* cap);
LIBDLL_API void BanzhafMobSparse(double* v, int n, struct SparseFM* cap);

LIBDLL_API void NonmodularityIndexMobSparse(double* w, int n, int_64 m, struct SparseFM* cap);
// calculates  all 2^n nonmodularity indices (returned in w) using Mobius transform of 
//a k-additive FM in cardinality ordering (of length 2^n=m), using sparse representation

/* populates 2-additive sparse capacity with nonzero values using the singletons and two arrays of indices (of size numpairs) . Indices need to be 1-based. Singletons 0-based */
LIBDLL_API void PopulateFM2Add_Sparse(double* singletons, int numpairs, double* pairs, int* indicesp1, int* indicesp2, struct SparseFM* cap);

/* for populating capacities. Add pair (v_ij) to the structure. indices are 1-based */
LIBDLL_API void AddPairSparse(int i, int j, double* v, struct SparseFM* cap);
/* for populating capacities, adds a tuple of size tupsize whose 1-based indices are in tuple */
LIBDLL_API void AddTupleSparse(int tupsize, int* tuple, double* v, struct SparseFM* cap);

/* Given 2-additive capacity singletons=pairs in one array v , selects nonzero pairs */
LIBDLL_API void PopulateFM2Add_Sparse_from2add(int n, double * v, struct SparseFM* cap);

/* from sparse to full representaiotn of 2-additive capacity (singletons and paits, augmented with 0 ) Vector v has to be allocated, size is n+ n(n-1)/2 */
LIBDLL_API void Expand2AddFull(double* v, struct SparseFM* cap);

/* from sparse to full capacity (vector v, size 2^n has to be preallocated) */
LIBDLL_API void ExpandSparseFull(double* v, struct SparseFM* cap);

LIBDLL_API void ExportSparseSingletons(int n, double *v, struct SparseFM* cap);
LIBDLL_API int ExportSparsePairs(int* pairs, double *v, struct SparseFM* cap);
LIBDLL_API int ExportSparseTuples(int* tuples, double *v, struct SparseFM* cap);


/* random generation of  sparse supermodular capacities */
LIBDLL_API int generate_fm_2additive_convex_sparse(int n, struct SparseFM* cap);

/* this is actually a total monotone, Belief measure */
LIBDLL_API int generate_fm_kadditive_convex_sparse(int n, int k, int nonzero, struct SparseFM* cap);



#endif
