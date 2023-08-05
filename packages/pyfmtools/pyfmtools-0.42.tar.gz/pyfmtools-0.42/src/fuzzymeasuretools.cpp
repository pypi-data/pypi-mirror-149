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
 *              version                          : 3.0
 *              copyright            : (C) 2007-2020 by Gleb Beliakov
 *              email                : gleb@deakin.edu.au
 *
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


// todo Mobius from kinteractive 

#include <iostream>
#include <fstream>
#include <cmath>
#include <algorithm>
#include <ctime>
#include<random>
#include <numeric>

#define MEMCHK
// GB: this makes extra checks for sparse structures, not to go out of bounds, but at the cost of some losses in speed
// comment out if certain not to go out of bounds and speed is an issue

clock_t clockS, clockF;
double TotalTime;
void   ResetTime() { TotalTime = 0; clockS = clock(); }

double ElapsedTime()
{
	clockF = clock();
	double duration = (double)(clockF - clockS) / CLOCKS_PER_SEC;
	TotalTime += duration;
	clockS = clockF;
	return TotalTime;
}



//#include <R.h>
#include "fuzzymeasuretools.h"

/* ===========================Auxiliary functions block ================================================*/

struct Less_than {
	int operator()(const valindex& a, const valindex& b) { return a.v < b.v; }
};
struct Greater_than {
	int operator()(const valindex& a, const valindex& b) { return a.v > b.v; }
};
using namespace std;

  Less_than less_than;              /* declare a comparison function object, to */
  Greater_than  greater_than ;      /*  pass to sort and search algorithms */

 valindex tempxi[100];
 LIBDLL_API double         *m_factorials;  // keeps factorials  n! up to n
 LIBDLL_API int            *card;                  // array to keep set cardinalities in binary ordering
 LIBDLL_API int            *cardpos;   // array to store the indices of elements of different cardinalities in the cardinality ordering

 LIBDLL_API  int_64 *bit2card;        // arrays to transform from one ordering to another
 LIBDLL_API  int_64 *card2bit;


 // marginal representation
 LIBDLL_API int            *cardposm;   // array to store the indices of elements of different cardinalities in the cardinality ordering
 LIBDLL_API int_64 *bit2cardm;        // arrays to transform from one ordering to another
 LIBDLL_API int_64 *card2bitm;

int sign(int i) {if(i<0) return -1; else return 1;}
int signd(double i) {if(i<0) return -1; else return 1;}

typedef double ( *USER_FUNCTION)(double );
double bisection(double a, double b, USER_FUNCTION f, int nmax)
{
        double u,v,c,w;
        int i;
        u=f(a); v=f(b);
        if(signd(u)==signd(v)) { return -10e10;} // no solution
        i=nmax;
        while(i>0) {
                i--;
                c=(a+b)/2.0;
                w=f(c);
                if( (b-a) < 1.0e-10 ) break;
                if(signd(u)==signd(w)) {
                        u=w; a=c;
                } else {
                        v=w;b=c;
                }
        }
        return (a+b)/2.0;
}


 int_64 choose(int i, int n)
{
	if (i == 1) return n;
	if (i == 2) return (int_64)(n*(n - 1)) / 2;
	if (i == 3) return (int_64)(n*(n - 1)*(n - 2)) / 6;
	if (i == 4) return (int_64)(n*(n - 1)*(n - 2)*(n-3)) / 24;
	if (i == 5) return (int_64)(n*(n - 1)*(n - 2)*(n - 3)*(n-4)) / 120;

	return (int_64)(m_factorials[n] / m_factorials[i] / m_factorials[n - i]);
}

double ChooseInverse(int n, int a, int b) { return m_factorials[b] * m_factorials[n - a - b] / m_factorials[n - a]; }

double minf(double a, double b) {if (a<b) return a; else return b;}
double maxf(double a, double b) {if (a>b) return a; else return b;}

int IsOdd(int i) {return ((i & 0x1)?1:0); }
unsigned int cardf(int_64 A) // count how many bits in i are set
{
        int s=0;
        int_64 t=A;
                while(t>0) {
                        if(t & 0x1) s++;
                        t=(t>>1);
                }
        return s;
}

//int __builtin_popcount (unsigned int x);
#ifdef __GNUC__
unsigned int bitweight(int_64 i) {
	return __builtin_popcountl(i);
}

#elif _MSC_VER
#  include <intrin.h>

#ifdef  _WIN64
#  define __builtin_popcountl  __popcnt64  //_mm_popcnt_u64
 unsigned int bitweight(int_64 i) {
	return (uint) __builtin_popcountl(i);
}
#else
#  define __builtin_popcountl  __popcnt  //_mm_popcnt_u64
inline unsigned int bitweight(int_64 i) {
	return __builtin_popcountl((uint32_t)(i >> 32)) + __builtin_popcountl((uint32_t)i);
}
#endif

#else 
//#ifndef CHAR_BIT
//#define CHAR_BIT 8
//#endif	

uint bitweight(int_64 v) {
	v = v - ((v >> 1) & (int_64)~(int_64)0 / 3);                           // temp
	v = (v & (int_64)~(int_64)0 / 15 * 3) + ((v >> 2) & (int_64)~(int_64)0 / 15 * 3);      // temp
	v = (v + (v >> 4)) & (int_64)~(int_64)0 / 255 * 15;                      // temp
	unsigned int c = (int_64)(v * ((int_64)~(int_64)0 / 255)) >> (sizeof(int_64) - 1) * 8 ; // count  CHAR_BIT
	return (unsigned int)c;
}
//#endif
/*
unsigned int bitweight(unsigned int i)
{
	 i = i - ((i >> 1) & 0x55555555);
	 i = (i & 0x33333333) + ((i >> 2) & 0x33333333);
	 return (((i + (i >> 4)) & 0x0F0F0F0F) * 0x01010101) >> 24;
}*/
#endif

int_64 UnivSetTable[20] = { 0, 1, 3, 7, 15, 31, 63, 127, 255,511,1023,2047,4095,8191,16383,32767,65535,131071,262143 };
//int_64 UnivSetTable[7] = { 0, 1, 3, 7, 15, 31, 63};


double xlogx(double t) { if(t<GBtolerance) return 0; else return t*log(t);} 

void RemoveFromSet(int_64* A, int i) { *A &= (~(int_64(1) << i)); }
void AddToSet(int_64* A, int i) { *A |= (int_64(1) << i); }
int  IsInSet(int_64 A, int i) { return int((A >> i) & 0x1); }  // 0-based i
int  IsSubset(int_64 A, int_64 B) { return ((A & B) == B); } //
int_64 Setunion(int_64 A, int_64 B) { return (A | B); }
int_64 Setintersection(int_64 A, int_64 B) { return (A & B); }
int_64 Setdiff(int_64 A, int_64 B) { return (A & ~(A & B)); }

int Removei_th_bitFromSet(int_64* A, int i) { int_64 B = (*A) & (~(int_64(1) << i)); 
                          if (B == *A) return 1; else *A = B; return 0; 
}

int_64 UniversalSet(int n) {
	int_64 A = UnivSetTable[min(n, 19)];
	while (n > 19)  {AddToSet(&A, --n);}
	return A;
}

// Additions to version 4
int_64 remove1bit(int_64 a, int i)
// counting fom 0
{
	int_64 b = 1;
	b = b << i;
	b = ~b;
	b = a & b;
	return b;
}

int_64 RemoveHighestBit(int_64 a, int K) {
	for (int k = K-1; k >= 0; k--)
		if (IsInSet(a, k)) { RemoveFromSet(&a, k); return a; }
	return 0;
}



inline int Cardinality(int_64 A) { return bitweight(A); }


unsigned int     ShowValue(int_64 s) {
                int i,k;
                k=0;
                
                for(i=0;i<9;i++) {
                        if(IsInSet(s,i)) {
                                k *= 10;
                                k += (i+1);
                        }
                }
				for (i = 9; i<10; i++) {
					if (IsInSet(s, i)) {
						k *= 10;
						//k += (i + 1);
					}
				}
                return k;
}

// returns the position of the value id in the copact array of kinterctive f.m.: up to kint as bit2card otherwise a small array after card[id] at the end, from the position arraysize

int_64 Bit2card(int_64 id, int n, int kint, int arraysize) {  // used for k-interactive FM

	if (card[id] <= kint) return bit2card[id];
	return arraysize + (card[id] - kint) - 1;
}

int_64 Bit2Card(int_64 c) { return bit2card[c]; }
int_64 Card2Bit(int_64 c) { return card2bit[c]; }

double min_subset(double* x, int n, int_64 S)
{ // returns min x_i when i \in S, or 0 if S is empty
	int i;
	double r = 10e10;
	for (i = 0;i < n;i++)
		if (IsInSet(S, i)) r = minf(r, x[i]);
	if (r > 1) r = 0;
	return r;
}

double max_subset(double* x, int n, int_64 S)
{ // returns max x_i when i \in S, or 0 if S is empty
	int i;
	double r = -10e10;
	for (i = 0;i < n;i++) {
		if (IsInSet(S, i)) r = maxf(r, x[i]);
	}
	if (r < 0) r = 0;
	return r;
}


void ConvertCard2Bit(double* dest, double* src, int_64 m)
{
	for (int_64 i = 0; i < m; i++)
		dest[card2bit[i]] = src[i];
}



// this is a recursive procedure which helps build all subsets of a given cardinality, and 
// set up conversion arrays
void recursive_card(int_64* k, unsigned int level, unsigned int maxlevel,
	unsigned int start, unsigned int finish,
	int_64* b2c, int_64* c2b, int_64 *s, int n)
{
	unsigned int i1;
	for (i1 = start; i1 <= finish; i1++) {
		AddToSet(s, i1);
		if (level == maxlevel) {
			b2c[*s] = *k;
			c2b[*k] = (*s);
			(*k)++;
		}
		else {
			recursive_card(k, level + 1, maxlevel, i1 + 1, finish + 1, b2c, c2b, s, n);
		}
		RemoveFromSet(s, i1);
	}
}


void main_card(int_64* k, unsigned int level, int_64* b2c, int_64* c2b, int n)
{
	// we recursively construct all subsets of cardinality "level"
	int_64 s = 0;
	recursive_card(k, 1, level, 0, n - level, b2c, c2b, &s, n);
}



// this is a recursive procedure which helps build all subsets of a given cardinality, and 
// set up conversion arrays
void recursive_card_marginal(int_64* k, unsigned int level, unsigned int maxlevel,
	unsigned int start, unsigned int finish,
	int_64* b2c, int_64* c2b, int_64 *s, int n)
{
	unsigned int i1;
	for (i1 = start; i1 <= finish; i1++) {
		AddToSet(s, i1);
		if (level == maxlevel) {
			b2c[*s] = *k;
			c2b[*k] = (*s);
			for (unsigned int r = 1; r < level; r++)
			{
				c2b[++(*k)] = (*s);
			}
			(*k)++;
		}
		else {
			recursive_card_marginal(k, level + 1, maxlevel, i1 + 1, finish + 1, b2c, c2b, s, n);
		}
		RemoveFromSet(s, i1);
	}
}


void main_card_marginal(int_64* k, unsigned int level, int_64* b2c, int_64* c2b, int n, int Kinter)
{
	// we recursively construct all subsets of cardinality "level"
	int_64 s = 0;
	recursive_card_marginal(k, 1, level, 0, n - level, b2c, c2b, &s, Kinter);
}



/* ===========================End Auxiliary functions block ================================================*/

/* ===========================The significant functions block ================================================*/

double Choquet(double*x, double* v, int n, int_64 m)
/* Calculates the value of a discrete Choquet integral of x, wrt fuzzy measure v 
Parameters: x array[n] ,v array[m], n, m=2^n 
This proceduce requires sorting the array of pairs (v[i],i) in non-decreasing order
(perfored by standard STL sort function, and RemoveFromSet() function, to remove
an indicated bit from a set (in its binary representation) */
{       double s=0;
        int i;
        for(i=0;i<n;i++) { (tempxi[i]).v=x[i]; (tempxi[i]).i=i;}
        sort(&(tempxi[0]),&(tempxi[n]),less_than); // sorted in increasing order

        int_64 id = m-1; // full set N (11111... in binary)

        s=tempxi[0].v*v[id];
        RemoveFromSet(&id, tempxi[0].i);
        for(i=1;i<n;i++) {
                s+=(tempxi[i].v - tempxi[i-1].v)* v[id];
                RemoveFromSet(&id, tempxi[i].i);
        }
        return s;
}



double ChoquetKinter(double*x, double* v, int n, int_64 m, int kint)
/* As above, but for kinteractive f.m. using compact representation of v  (in cardinality ordering! ) */
{
	double s = 0;
	int i;
	for (i = 0;i < n;i++) { (tempxi[i]).v = x[i]; (tempxi[i]).i = i; }
	sort(&(tempxi[0]), &(tempxi[n]), less_than); // sorted in increasing order

	int_64 id = m - 1; // full set N (11111... in binary)

	int arraysize = cardpos[kint];

	s = tempxi[0].v*v[Bit2card(id, n, kint, arraysize)];
	RemoveFromSet(&id, tempxi[0].i);
	for (i = 1;i < n;i++) {
		s += (tempxi[i].v - tempxi[i - 1].v)* v[Bit2card(id, n, kint, arraysize)];
		RemoveFromSet(&id, tempxi[i].i);
	}
	return s;

}

double ChoquetMob(double*x, double* Mob, int n, int_64 m)
/* This is an alternative calculation of the Choquet integral from the Moebius transform. 
   It is not as efficient as Choquet(). Provided for testing purposes. 
*/
{
    double s=0;
    int_64 A;
    for(A=1; A < m; A++)
        s += Mob[A] * min_subset( x, n, A);
    return s;
}



double Sugeno(double*x, double* v, int n, int_64 m)
/* Calculates the value of a discrete Sugeno integral of x, wrt fuzzy measure v 
   Parameters: x array[n] ,v array[m], n, m=2^n 
   This proceduce requires sorting the array of pairs (v[i],i) in non-decreasing order
   (perfored by standard STL sort function, and RemoveFromSet() function, to remove
   an indicated bit from a set (in its binary representation)
   Also requires maxf and minf functions. 
*/
{
    double s=0;
    int i;
    for(i=0;i<n;i++) { (tempxi[i]).v=x[i]; (tempxi[i]).i=i;}
    sort(&(tempxi[0]),&(tempxi[n]),less_than); // sorted in decreasing order

    int_64 id = m-1; // full set N (11111... in binary)

    s=0;
    for(i=0;i<n;i++) {
        s =maxf(s, minf(tempxi[i].v , v[id]));
        RemoveFromSet(&id, tempxi[i].i);
    }
    return s;
}


double OWA(double*x, double* v, int n )
/* Calculates the value of an OWA 
Parameters: x array[n] ,v array[n], n, 
This proceduce requires sorting the array of pairs (v[i],i) in non-decreasing order
 */
{       double s=0;
        int i;
        for(i=0;i<n;i++) { (tempxi[i]).v=x[i]; (tempxi[i]).i=i;}
        sort(&(tempxi[0]),&(tempxi[n]),less_than); // sorted in increasing order

        for(i=0;i<n;i++) {
                s+=  tempxi[n-i-1].v * v[i];
        }
        return s;
}
double WAM(double*x, double* v, int n )
/* Calculates the value of a WAM 
Parameters: x array[n] ,v array[n], n, 
 */
{       double s=0;
        int i;
        for(i=0;i<n;i++) {
                s+=  x[i] * v[i];
        }
        return s;
}


double auxarray[100];
int auxN;
double auxfun(double lam)
{
        int i;
        double s=1;
        for(i=0;i<auxN;i++) s*= (1 + lam* auxarray[i]);
        s -= (lam+1);
        return s;
}
void ConstructLambdaMeasure(double *singletons, double *lambda, double *v, int n, int_64 m)
/* Given the values of the fuzzy measure at singletons, finds the appropriate
lambda, and constructs the rest of the fuzzy measure. Returns lambda and v at the output
*/
{
        double tol=1.0e-8;
        int i;
        auxN=n;
	 double cond=0;
        double a,b,c;             
		int_64 j;
        double s;
   
	for(i=0;i<n;i++) {cond +=singletons[i]; auxarray[i]=singletons[i];}
        
	 if(fabs(cond-1)<tol) // additive
	{
		*lambda=0;
		c=0;
		goto E1;
	}

  
        a=-1+tol;
        b=0-tol;
        c=bisection(a,b,auxfun,10000);
        if(c<-1) { //means we have to use another interval
                a=tol;
            b=10000;
                c=bisection(a,b,auxfun,100000);
        }
        // so lambda is c now
	 tol *=tol;
	
	if(fabs(c)<tol) goto E1;

        v[0]=0;
        for(j=1;j<m;j++) {
                s=1;
                for(i=0;i<n;i++) if(IsInSet(j, i)) 
                        s *= (1+ c* auxarray[i]);
                s = (s-1)/c;
                v[j]=s;
        }
        *lambda=c;
	return;

// special calse lambda=0

E1:
	*lambda=0;
        v[0]=0;
        for(j=1;j<m;j++) {
                s=0;
                for(i=0;i<n;i++) if(IsInSet(j, i)) 
                        s += auxarray[i];
                
                v[j]=s;
        }

	        
}

double Orness(double* Mob, int n, int_64 m)
{
		int_64 i;
        double s;
        s=0;
        for(i=1;i<m;i++) { 
                s += Mob[i] * (n-card[i])/(card[i]+1.);
        }
        return s/(n-1);
}

double OrnessOWA(double* w,  int n)
{
        int i;
        double s;
        s=0;
        for(i=1;i<=n;i++) { 
                s += w[i-1] * (n-i+0.0)/(n-1.);
        }
        return s;
}

double Entropy(double* v, int n, int_64 m)
{
        int i;
		int_64 id, tempid;
        double s=0;
        double nfac=m_factorials[n];
        for(i=0;i<n;i++) {
                tempid=0;       AddToSet(&tempid,i);
                for(id=0;id<m;id++) if(!IsInSet(id,i)) { 
                        s += -xlogx(v[ Setunion(id,tempid) ] - v[id]) * m_factorials[n-card[id]-1]*m_factorials[card[id]]/nfac;
                }
        }
        return s;
}

void Mobius(double* v, double* Mob, int n, int_64 m)
{
	int_64 i;
	int_64 id;
        double s;
        for(i=0;i<m;i++) {
                s=0;
                for(id=0;id <= i;id++) if(IsSubset(i,id)) {
                        s += v[id] * (IsOdd( card[Setdiff(i,id) ]) ? -1:1); ;
                }
                Mob[i]=s;
        }
}
void Zeta(double* Mob, double* v, int n, int_64 m)
//inverse Moebius transform
{
		int_64 i;
		int_64 id;
        double s;
        for(i=0;i<m;i++) {
                s=0;
                for(id=0;id <= i;id++) if(IsSubset(i,id)) {
                        s += Mob[id] ;
                }
                v[i]=s;
        }
}


void Shapley(double* v, double* x, int n, int_64 m)
{
		int j;
		int_64 i;
		int_64 id;

        for(j=0;j<n;j++) {
                id=0; AddToSet(&id, j); 
                x[j]=0;
                for(i=0;i<m;i++) 
                        if(!IsInSet(i,j)) {
                                x[j] += (m_factorials[n-card[i]-1]*m_factorials[card[i]])/m_factorials[n] *
                                        ( v[ Setunion(i,id) ] - v[i]);
                        }
        }
}

void Banzhaf(double* v, double* x, int n, int_64 m)
{
		int j;
		int_64 i;
		int_64 id;

        for(j=0;j<n;j++) {
                id=0; AddToSet(&id, j); 
                x[j]=0;
                for(i=0;i<m;i++) 
                        if(!IsInSet(i,j)) {
                                x[j] +=  (v[ Setunion(i,id) ] - v[i]);
                        }
                x[j] /= (1<<(n-1));
        }
}

void ShapleyMob(double* Mob, double* w, int n, int_64 m)
// only the Shapley values, Mob in binary ordering
{
	int_64 j;
	int i;
	int_64 id;
	for (i = 0;i < n;i++) {
		w[i] = 0;
		j = 1;
		for (id = i;id < m;id++) // supersets only
			if (IsInSet(id, (int) i))
				w[i] += Mob[id] / (card[id] - j + 1);
	}
}
void BanzhafMob(double* Mob, double* w, int n, int_64 m)
// only the Banzhaf values, Mob in binary ordering
{
	int_64 j;
	int i;
	int_64 id;
	for (i = 0;i < n;i++) {
		w[i] = 0;
		j = 1;
		for (id = i;id < m;id++) // supersets only
			if (IsInSet(id, (int)i))
				w[i] += Mob[id] / (1 << (card[id] - j));
	}
}
/* Shapley interaction index */
void InteractionMob(double* Mob, double* w, int_64 m)
{
	int_64 j, i;
	int_64 id;
        for(i=0;i<m;i++) {
                w[i]=0;
                j=card[i];
                for(id=i;id<m;id++) // supersets only
                        if(IsSubset(id,i))
                                w[i]+=Mob[id]/( card[id]- j +1);
        }
}

/* Banzhaf interaction index */
void InteractionBMob(double* Mob, double* w, int_64 m)
{
	int_64 j, i;
	int_64 id;
        for(i=0;i<m;i++) {
                w[i]=0;
                j=card[i];
                for(id=i;id<m;id++) // supersets only
                        if(IsSubset(id,i))
                                w[i]+=Mob[id]/ (1<<( card[id]- j ));
        }
}



void NonadditivityIndex(double* v, double* w, int n, int_64 m) // calculates  all 2^n nonadditivity indices (returned in w)
{
	int_64 j, i;
	double r;
	int_64 id;
	w[0] = 0;
	for (i = 1; i<m; i++) {
		w[i] = 0;
		j = card[i];

		if (j == 1){ w[i] = v[i]; }
		else{

			r = (j>1) ? 1. / ((int(1) << (j - 1)) - 1.) : 1;
			for (id = 1; id < i; id++) // subsets only
			if (IsSubset(i, id))
				w[i] += v[id];
			w[i] *= r;
			w[i] = v[i] - w[i];
		}
	}
}


void NonadditivityIndexMob(double* Mob, double* w, int n, int_64 m) // calculates  all 2^n nonadditivity indices (returned in w) using Mobius transform
{
	unsigned int j; int_64 i;
	double r;
	int_64 id;
	w[0] = 0;
	for (i = 1; i<m; i++) {
		w[i] = 0;
		j = card[i];
		
		for (id = 0; id<i; id++) // subsets only
		if (IsSubset(i, id))
		{
			r = (j>1) ? (  (int(1) << (j - 1)) - (int(1) << (j-card[id]))  ) / ((int(1) << (j - 1)) - 1.)  : 1;
			w[i] += Mob[id]*r;
		}
		w[i] += Mob[i] ;
	}
}



void NonmodularityIndex(double* v, double* w, int n, int_64 m) // calculates  all 2^n nonmodularity indices (returned in w)
{
	int_64 j, i;
	int k;
	double r;
	int_64 id;
	w[0] = 0;
	for (i = 1; i < m; i++) {
		w[i] = 0;
		j = card[i];

		if (j == 1) { w[i] = v[i]; }
		else {
			r = 0;
			for(k=0;k<n;k++)
				if (IsInSet(i, k)) {
					id = 0;
					AddToSet(&id, k);
					r += v[id];
					id = i;
					RemoveFromSet(&id, k);
					r += v[id];
				}
			w[i] = v[i] - r/j  + v[0];
		}
	}
}



void NonmodularityIndexMob(double* Mob, double* w, int n, int_64 m) // calculates  all 2^n nonmodularity indices (returned in w) using Mobius transform
{
	unsigned int j; int_64 i;
	double r;
	int_64 id;
	w[0] = 0;
	for (i = 1; i < m; i++) {
		w[i] = 0;
		j = card[i];
		if (j == 1) w[i] = Mob[i];
		else {
			r = 0;
			for (id = 1; id < i; id++) // subsets only
				if (IsSubset(i, id) && card[id]>=2)
				{
					r += Mob[id] * card[id];
				}
			r /= j;
			w[i] = Mob[i]+r;
		}
	}
}

void NonmodularityIndexMobkadditive(double* Mob, double* w, int n, int k, int_64 m) // calculates  all 2^n nonmodularity indices (returned in w) using Mobius transform of 
//a k-additive FM in cardinality ordering (of length 2^n=m)
{
	 int_64 i;
	int_64 id;
	w[0] = 0;
	int_64 length = fm_arraysize_kadd(n, k);
	for (i = 1; i < (int_64) n; i++) w[i] = Mob[i];
	for (int_64 i = length; i < m; i++) w[i] = 0;

	for (int_64 i = (int_64) n; i < length; i++) {
		int_64 A = card2bit[i];
		w[i] = Mob[i];

		for (id = i + 1;id < m;id++)  // over all supersets
			if (IsSubset(card2bit[id], A)) w[id] += Mob[i] * card[A] / card[card2bit[id]];
	}
}








void CalculateDeltaHat(double* v, double* w, int_64 A, int_64 B, int_64 m)
{
	unsigned int j;
	int_64 id;

	*w = 0;	j = card[A];
	if (j == 0) return;
	if (j == 1) { *w = v[Setunion(A, B)] - v[B];  return; }

	for (id = 1; id < A; id++)
	if (IsSubset(A, id)){
		*w += v[ Setunion(B, id) ];
	}

	*w *= 1. / ( (int(1)<<(j-1)) -1.);
	id = Setunion(A, B);
	*w = v[id] + v[B] - *w;
}


void BipartitionShapleyIndex(double* v, double* w, int n, int_64 m) // calculates  all 2^n bipartition Shapley indices (returned in w)
{
	unsigned int j,k;
	int_64 A, B;
	double r,d,ch;
	w[0] = 0;
	for (A = 1; A < m; A++) {
		w[A] = 0;
		j = card[A];
		r = 1. / (n - j + 1.);
		for (B = 0; B < m; B++)
		if (Setintersection(A, B) == 0){
			CalculateDeltaHat(v, &d, A, B, m);
			k = card[B];
			ch = ChooseInverse(n, j, k);
			w[A] += r* ch* d;
		}
	}
}
void BipartitionBanzhafIndex(double* v, double* w, int n, int_64 m) // calculates  all 2^n bipartition Shapley indices (returned in w)
{
	unsigned int j;
	int_64 A, B;
	double r, d;
	w[0] = 0;
	for (A = 1; A < m; A++) {
		w[A] = 0;
		j = card[A];
		r = 1. / (int(1)<<(n-j));
		for (B = 0; B < m; B++)
		if (Setintersection(A, B) == 0){
			CalculateDeltaHat(v, &d, A, B, m);
			w[A] += r* d;
		}
	}
}


void dualm(double* v, double* w, int n, int_64 m)
{
        int_64 i;
        for(i=0;i<m;i++)
        {
                w[ (~i) & (m-1) ] = 1-v[i];
        }
}

void dualMob(myfloat* src, myfloat* dest,  int_64 m)
// m size of src , k-
{ //dual of capacity in Mobius in compact representation, 
	// assumes fm has been initialised

	int mone = 1;
	dest[0] = 0;

	for (int_64 i = 1; i < m; i++) {
		int_64 A = i;
		mone = 1;
		if (IsOdd(Cardinality(A) + 1)) mone = -1;

		dest[i] = src[i];// itself
		for (int_64 j = i + 1; j < m;j++) {
			int_64 B = j;
			if (IsSubset(B, A)) dest[i] += src[j];
		}
		dest[i] *= mone;

	}

}


int IsMeasureAdditive(double* v, int n, int_64 m)
{       
	int j;
	int_64 i;
        double s;
        for(i=3;i<m;i++) {
                if(card[i]>1) {
                        s=0;
                        for(j=0;j<n;j++)
                         if(IsInSet(i,j)) s+=v[(int_64) 1<<j ];
                        if(fabs(s-v[i])>GBtolerance) return 0;
                }
        }
        return 1;
}

int IsMeasureKMaxitive(double* v, int n, int_64 m)
{
	int j;
	int_64 i;
	double s;
	int K = 1;
	for (i = 1; i<m; i++) {
		if (card[i]>1) {
			s = 0;
			for (j = 0; j<n; j++)
			if (IsInSet(i, j)) s = maxf(v[Setdiff(i,(int_64)1<<j)], s);
			if (fabs(s - v[i])>GBtolerance) K=max(K,card[i]); // fails for cardinality K
		}
	}
	return K;
}

int IsMeasureBalanced(double* v, int_64 m)
{
	int_64 i, j;
        for(i=0;i<m;i++) {
                for(j=i;j<m;j++) {
                        if((card[i]<card[j]) && (v[i]>v[j])) return 0;
                        if((card[i]>card[j]) && (v[i]<v[j])) return 0;
                }
        }
        return 1;
}


int IsMeasureSelfdual(double* v, int_64 m)
{       
	int_64 i;
        for(i=0;i<m;i++)
        {
                if(fabs(v[ (~i) & (m-1) ] + v[i]-1) > GBtolerance) return 0;
        }
        return 1;
}


int IsMeasureSubadditive(double* v, int_64 m)
{
	int_64 i, j;
        for(i=0;i<m;i++) {
                for(j=i+1;j<m;j++) if(Setintersection(i,j)==0) {
                        if(v[i]+v[j] - v[Setunion(i,j)] < -GBtolerance) return 0;
                }
        }
        return 1;
}


int IsMeasureSubmodular(double* v, int_64 m)
{
	int_64 i, j;
        for(i=0;i<m;i++) {
                for(j=i+1;j<m;j++) if(Setintersection(i,j)==0) {
                        if(v[i]+v[j] - v[Setunion(i,j)]- v[Setintersection(i,j)] < -GBtolerance) return 0;
                }
        }
        return 1;

}


int IsMeasureSuperadditive(double* v, int_64 m)
{
	int_64 i, j;
        for(i=0;i<m;i++) {
                for(j=i+1;j<m;j++) if(Setintersection(i,j)==0) {
                        if(v[i]+v[j] - v[Setunion(i,j)] > GBtolerance) return 0;
                }
        }
        return 1;
}


int IsMeasureSupermodular(double* v, int_64 m)
{
	int_64 i, j;
        for(i=0;i<m;i++) {
                for(j=i+1;j<m;j++) {
                        if(v[i]+v[j] - v[Setunion(i,j)] - v[Setintersection(i,j)] > GBtolerance) return 0;
                }
        }
        return 1;
}


int IsMeasureSymmetric(double* v, int n, int_64 m)
{
	int_64 i, j;
        double *w=new double[n+1];
        for(i=0;i<(unsigned int)n+1;i++) w[i]=-1;

        for(i=0;i<m;i++) {
                j=card[i];
                if(w[j]<0) w[j]=v[i]; else
                        if(fabs(w[j]-v[i])>GBtolerance) {delete[] w; return 0; }
        }
        delete[] w;
        return 1;
}






void Preparations_FM(int n, int_64 *m)
{
        int i;
        int_64 j;
        *m= (int_64)1<<(n);

    // calculate the array containing factorials of i! (faster than calculating them every time)
    m_factorials=new double[n+1];
        m_factorials[0]=1;
        for(i=1;i<=n;i++) m_factorials[i] = m_factorials[i-1]*i;

    // this array will contains cardinailities of subsets (coded as binaries), i.e. the number of bits in i.
        card=new int[(int) *m];
        cardpos=new int[n+1];
        card[0]=0;
        for(j=1;j<*m;j++) card[j] = cardf(j);

// these two arrays are used to pass from binary to cardinality ordering
// they are precomputed 
// in binary ordering the subsets are ordered as
// 0 1 2 12 3 13 23 123 4 14 24 124 34 134 234 1234,...
// (which corresponds to the order 0,1,2,3,... in binary form)
// in cardinality ordering they are ordered as
// 0 1 2 3 4 5 6 12 13 14 15 16 23 24 25 26 34 35 36 45 46 56 123 124,...
// (empty, singletons, pairs,triples, etc.)
// for a given subset s in cardinality ordering, to find its binary code use  card2bit[s]
// and vice versa
// cardpos[i] is the index at which subsets with cardinality i+1 start in the cardinality ordering
// i.e. cardpos[0]..cardpos[1]-1 - singletons, cardpos[1]..cardpos[2]-1 - pairs, etc.

		bit2card = new int_64[*m];
		card2bit = new int_64[*m];

		int_64 k; int l;
        bit2card[0]=card2bit[0]=0;

        cardpos[0]=1; // positions where singletons start, the 0th element is empyset

        k=1;
        for(l=1;l<=n-1;l++) {
                main_card(&k, l, bit2card, card2bit,  n);
                cardpos[l]=(int)k;
        }
        cardpos[n]=cardpos[n-1]+1;
        
        bit2card[*m-1]=card2bit[*m-1]=*m-1;

		card2bitm=NULL;
		bit2cardm=NULL;
		cardposm=NULL;
}


void Preparations_fm_marginal(int n, int_64 *m, int Kinter)
{
	int i;
//	int_64 j;
	int sz=n;
	*m = (int_64)1 << (n);

	// do standard job, factorials and card
	Preparations_FM(n, m);

	//*m *= 2;

	// calculate the array containing factorials of i! (faster than calculating them every time)
//	m_factorials = new double[n + 1];
//	m_factorials[0] = 1;
//	for (i = 1; i <= n; i++) m_factorials[i] = m_factorials[i - 1] * i;

	// this array will contains cardinailities of subsets (coded as binaries), i.e. the number of bits in i.
//	card = new int[(int)*m];

//	card[0] = 0;
//	for (j = 1; j<*m; j++) card[j] = cardf(j);

	// these two arrays are used to pass from binary to cardinality ordering
	// they are precomputed 
	// in binary ordering the subsets are ordered as
	// 0 1 2 12 3 13 23 123 4 14 24 124 34 134 234 1234,...
	// (which corresponds to the order 0,1,2,3,... in binary form)
	// in cardinality ordering they are ordered as
	// 0 1 2 3 4 5 6 12 13 14 15 16 23 24 25 26 34 35 36 45 46 56 123 124,...
	// (empty, singletons, pairs,triples, etc.)
	// for a given subset s in cardinality ordering, to find its binary code use  card2bit[s]
	// and vice versa
	// cardpos[i] is the index at which subsets with cardinality i+1 start in the cardinality ordering
	// i.e. cardpos[0]..cardpos[1]-1 - singletons, cardpos[1]..cardpos[2]-1 - pairs, etc.

	cardposm = new int[n + 1];
	for (i = 2; i <= Kinter; i++) sz += (int)(m_factorials[n] / m_factorials[i - 1] / m_factorials[n - i]);


	bit2cardm = new int_64[*m];
	card2bitm = new int_64[sz*2];

	int_64 k; int l;
	bit2cardm[0] = card2bitm[0] = 0;

	cardposm[0] = 1; // positions where singletons start, the 0th element is empyset

	k = 1;
	for (l = 1; l <= Kinter; l++) {
		main_card_marginal(&k, l, bit2cardm, card2bitm, n, Kinter);
		cardposm[l] = (int)k;
	}
	if(Kinter<n)	cardposm[n] = cardposm[n - 1] + 1;

//	bit2card[*m - 1] = card2bit[*m - 1] = *m - 1;
}



void Preparations_FM(int n, int_64 *m, int Kinteractive)
{
	// todo: complete this procedure, and provide a set of tools for Choque, conversions and others to work with K-interactive measures
	int i;
	int_64 j;

	if (Kinteractive > n)Kinteractive = n;
	if (Kinteractive < 1)Kinteractive = 1;



	// calculate the array containing factorials of i! (faster than calculating them every time)
	m_factorials = new double[n + 1];
	m_factorials[0] = 1;
	for (i = 1; i <= n; i++) m_factorials[i] = m_factorials[i - 1] * i;

	*m = 1;
	for (i = 1; i <= Kinteractive; i++) *m += (int)(m_factorials[n] / m_factorials[i] / m_factorials[n - i]);
	*m +=  n-Kinteractive;



	// this array will contains cardinailities of subsets (coded as binaries), i.e. the number of bits in i.
	card = new int[(int)*m];
	cardpos = new int[n + 1];
	card[0] = 0;

	for (j = 1; j<(*m - (n - Kinteractive)); j++) card[j] = cardf(j);

	for (j = Kinteractive + 1; j <= (int_64)n; j++) card[j + (*m - (n - Kinteractive)) - Kinteractive - 1] = (int)j;

	// these two arrays are used to pass from binary to cardinality ordering
	// they are precomputed 
	// in binary ordering the subsets are ordered as
	// 0 1 2 12 3 13 23 123 4 14 24 124 34 134 234 1234,...
	// (which corresponds to the order 0,1,2,3,... in binary form)
	// in cardinality ordering they are ordered as
	// 0 1 2 3 4 5 6 12 13 14 15 16 23 24 25 26 34 35 36 45 46 56 123 124,...
	// (empty, singletons, pairs,triples, etc.)
	// for a given subset s in cardinality ordering, to find its binary code use  card2bit[s]
	// and vice versa
	// cardpos[i] is the index at which subsets with cardinality i+1 start in the cardinality ordering
	// i.e. cardpos[0]..cardpos[1]-1 - singletons, cardpos[1]..cardpos[2]-1 - pairs, etc.

	bit2card = new int_64[*m];
	card2bit = new int_64[*m];

	int_64 k; int l;
	bit2card[0] = card2bit[0] = 0;

	cardpos[0] = 1; // positions where singletons start, the 0th element is empyset

	k = 1;
	for (l = 1; l <= n - 1; l++) {
		main_card(&k, l, bit2card, card2bit, n);
		cardpos[l] = (int)k;
	}
	cardpos[n] = cardpos[n - 1] + 1;

	bit2card[*m - 1] = card2bit[*m - 1] = *m - 1;
}




void Cleanup_FM()
{
        delete [] card2bit;
        delete [] bit2card;

        delete [] m_factorials;
        delete [] card;
        delete [] cardpos;

		if (card2bitm!=NULL) delete[] card2bitm;
		if (bit2cardm != NULL)delete[] bit2cardm;
		if (cardposm != NULL)delete[] cardposm;
}


void ExpandKinteractive2Bit_m(double* dest, double* src, int n, int_64 m, int kint, int arraysize, double* VVC)
{
	// requires working memory
	int_64 jp;
	int j;
	double t;

	for (j = 0;j < arraysize;j++)	VVC[j] = src[j];

	j = 1; jp = 0;
	while (j <= n - kint) {
		t = VVC[arraysize - j];
		for (int_64 jj = 0; jj < choose(n - j + 1, n); jj++)
			VVC[jj + m - jp - 1] = t;
		j++;
		jp += choose(n - j + 1, n);
	}

	ConvertCard2Bit(dest, VVC, m);

}
void ExpandKinteractive2Bit(double* dest, double* src, int n, int_64 m, int kint, int arraysize)
{
	double* VVC = new double[m];

	ExpandKinteractive2Bit_m(dest, src, n, m, kint, arraysize, VVC);

	delete[] VVC;
}

void NonmodularityIndexKinteractive(double* v, double* w, int n, int kint, int_64 m, int length) // calculates  all 2^n nonmodularity indices (returned in w)
{
	double* VVC = new double[m];

	ExpandKinteractive2Bit_m(VVC, v, n, m, kint, length, w);
	NonmodularityIndex(VVC, w, n, m);

	delete[] VVC;
}

/* ================ These functions do not require initialisation by Preparations_FM, they work with 2-additive FM =============================*/

// does not require FM_preparations for 2-additive case, the code with card2bit is disabled
void dualMobKadd( myfloat* src, myfloat* dest, int m, int length, int k)
// m is number of singletons, k-additivity, length is the number of elements in the array in cardinality baser ordering
{ //dual of k-additive in Mobius in compact representation, all the same elements are nonzero
	// assumes fm has been initialised
	// the elements of m(A) are in cardinality ordering, NOT including emptyset, it src[0]=m({1})
	if (k == 1) { // additive, just copy
		for (int i = 0; i < length; i++) dest[i] = src[i]; // singletons
		return;
	}

	if (k == 2 && m <= 0) // special case, simple
	{
		for (int i = m; i < length; i++) dest[i] = -src[i]; // pairs
		for (int i = 0;i < m; i++) {
			dest[i] = src[i];
			for (int j = m;j < length;j++) // run for all pairs
				if (IsInSet(card2bit[j + 1], i)) dest[i] += src[j];    // j+1 because the pairs here start with m, as there is no emptyset here 
		}
		return;
	}

	if (k == 2) // special case, large m
	{// it's a bit complicated count the  indices. we just run over all pairs and in the upper triangular matrix
		// count elements in the th column (+m=where the pairs start), and then the ith row
		for (int i = m; i < length; i++) dest[i] = -src[i]; // pairs
		for (int i = 0;i < m; i++) {
			dest[i] = src[i]; //singleton
//			cout << endl;
			int start = m; int step = m; int row = 0;
			start += (i - 1); if (start < m) start = m; // special case i==0
			if (i > 0) step = m - 1;
			for (int j = 1;j < m;j++) {
				dest[i] += src[start];
				//				cout << start << " ";
				if (row < i) {
					step -= 1;  row++; if (row == i) start++;
				}// row not reached
				else {
					step = 1;  row++;
				}// rest of the row
				start += step;
			}

		}
		return;
	}

	// for general k (remember there is no emptyset in this array
	int mone = 1;

	for (int i = 0; i < length; i++) {
		int_64 A = card2bit[i + 1];
		mone = 1;
		if (IsOdd(Cardinality(A) + 1)) mone = -1;

		dest[i] = src[i];// itself
		for (int j = i + 1;j < length;j++) {
			int_64 B = card2bit[j + 1];
			if (IsSubset(B, A)) dest[i] += src[j];
		}
		dest[i] *= mone;

	}

}

// todo: for k-additive, should follow dualMobKadd process with right coefficients
void Shapley2addMob(double* v, double* x, int n)
// calculates the array x of Shapley values for 2 additive fm in compact representation (cardinality based)
{
	// the formula is singleton + all pairs/2
	for (int i = 0;i < n; i++) {
		x[i] = v[i];  // singleton

		int start = n; int step = n; int row = 0;
		start += (i - 1); if (start < n) start = n; // special case i==0
		if (i > 0) step = n - 1;
		for (int j = 1;j < n;j++) {
			x[i] += v[start] * 0.5;  // pair
//			cout << start << " ";
			if (row < i) {
				step -= 1;  row++; if (row == i) start++;
			}// row not reached
			else {
				step = 1;  row++;
			}// rest of the row
			start += step;
		}
	}
}

void Banzhaf2addMob(double* v, double* x, int n)
// calculates the array x of Banzhaf indices for 2 additive fm in compact representation (cardinality based)
{
	// the formula is singleton + all pairs/3
	for (int i = 0;i < n; i++) {
		x[i] = v[i];  // singleton

		int start = n; int step = n; int row = 0;
		start += (i - 1); if (start < n) start = n; // special case i==0
		if (i > 0) step = n - 1;
		for (int j = 1;j < n;j++) {
			x[i] += v[start] *0.5;  // pair
			//				cout << start << " ";
			if (row < i) {
				step -= 1;  row++; if (row == i) start++;
			}// row not reached
			else {
				step = 1;  row++;
			}// rest of the row
			start += step;
		}
	}
}


double Choquet2add(double*x, double* Mob, int n)
/* This is a calculation of the Choquet integral from the Moebius transform for 2-additive capacities.
*/
{
	double val = 0;
	// the formula is singleton + all pairs/2
	int start = n;
	for (int i = 0;i < n; i++) {
		val+= Mob[i]*x[i];  // singleton
		for (int j = i + 1;j < n;j++) {
			val += Mob[start] * minf(x[i], x[j]) ;  // pair
			start++;
		}

	}
	return val;
}
/* ====================== Sparse FM in Mobius representation ==================================*/

//#define FM_SPARSE
#ifdef FM_SPARSE


/*
data structure for pairs:  pair[i] corresponds to (pairindex[2i], pairindex[2i+1])

tuples:  tuple j is tuples[j] and the indices are in tuplecontent at position tuplestart[j] (cardinality) andcard subsequent values (tuplestart[j]+1, +2,...+ card)

indices are 1-based!


struct SparseFM {
	int n;

	vector<double>  m_singletons;
	vector<double>  m_pairs;
	vector<double>  m_tuples;

	vector<uint16_t> m_pair_index;// goes in pairs, hence  m_pair_index[2i],m_pair_index[2i+1] corresponds to m_pairs[i];

	vector<int> m_tuple_start; // points to cardinality, list of elements, stored  in m_tuple_content
	vector<uint16_t> m_tuple_content;  // for any j such that m_tules[j] is the value, m_tuple_content[m_tuple_start[j]] is the cardinality
};
*/
// just the preparation, no content yet
// takes as the argument the list of indices with cardinalities, (cardinality, tuple composition) like this 2 pairs 4-tuple and a triple:  (2,1,2,  2, 3,1,   4, 1,2,3,4,  3,3,2,1...)
void Prepare_FM_sparse(int n, int tupsize, int* tuples, struct SparseFM* cap)
{
	cap->n=n;
	cap->m_singletons.resize(n);
	cap->m_pairs.reserve(10);
	cap->m_pair_index.reserve(10);
	cap->m_tuple_content.reserve(10);
	cap->m_tuple_start.reserve(10);
	cap->m_tuples.reserve(10);

	int i = 0;
	while (i < tupsize)
	{
		int card = tuples[i];
		if (card == 2)//pair, make them ordered
		{
			cap->m_pairs.push_back(0.0);
			i++;
			int t1 = tuples[i];
			i++;
			int t2 = tuples[i];
			i++;
			cap->m_pair_index.push_back(min(t1, t2));
			cap->m_pair_index.push_back(max(t1, t2));
		}
		else // card>2
		{
			cap->m_tuple_content.push_back(card);
			cap->m_tuples.push_back(0.0);
//			cap->m_tuple_content.push_back(card);
			cap->m_tuple_start.push_back((int) cap->m_tuple_content.size() - 1);
			i++;
			for (int j = 0;j < card;j++) {
				cap->m_tuple_content.push_back(tuples[i]);
				i++;
			}

		}
	}
}

// with content
// takes as the argument the list of indices with cardinalities, (cardinality, tuple composition) like this 2 pairs 4-tuple and a triple:  (2,1,2,  2, 3,1,   4, 1,2,3,4,  3,3,2,1...)
void Prepare_FM_sparse(int n, int tupsize, double *tups, int* tuples, struct SparseFM* cap)
{
	cap->n=n;
	cap->m_singletons.resize(n);
	cap->m_pairs.reserve(10);
	cap->m_pair_index.reserve(10);
	cap->m_tuple_content.reserve(10);
	cap->m_tuple_start.reserve(10);
	cap->m_tuples.reserve(10);

	int i = 0, j=0;
	while (i < tupsize)
	{
		int card = tuples[i];
		if (card == 2)//pair, make them ordered
		{
			(tups==NULL? cap->m_pairs.push_back(0.0): cap->m_pairs.push_back(tups[j]));
			j++;
			
			i++;
			int t1 = tuples[i];
			i++;
			int t2 = tuples[i];
			i++;
			cap->m_pair_index.push_back(min(t1, t2));
			cap->m_pair_index.push_back(max(t1, t2));
		}
		else // card>2
		{
			cap->m_tuple_content.push_back(card);
			(tups==NULL? cap->m_tuples.push_back(0.0): cap->m_tuples.push_back(tups[j])); j++;
		//	cap->m_tuples.push_back(tups[i]);
	//		cap->m_tuple_content.push_back(card);
			cap->m_tuple_start.push_back((int) cap->m_tuple_content.size() - 1);
			i++;
			for (int j = 0;j < card;j++) {
				cap->m_tuple_content.push_back(tuples[i]);
				i++;
			}

		}
	}
}

void Prepare_FM_sparse0(int n, int tupsize,int* tuples, struct SparseFM* cap)
{
	Prepare_FM_sparse(n,tupsize,NULL,tuples, cap);
}

void Free_FM_sparse(struct SparseFM* cap)
{
	if (cap->n > 0) {
		cap->m_singletons.resize(0);
		cap->m_pairs.resize(0);
		cap->m_pair_index.resize(0);
		cap->m_tuple_content.resize(0);
		cap->m_tuple_start.resize(0);
		cap->m_tuples.resize(0);
		cap->n = 0;
	}
}

int TupleCardinalitySparse(int i, struct SparseFM* cap) // only for tuples
{
#ifdef	MEMCHK
	if(cap->m_tuple_start.size()<=i) return 0; else
#endif
	return cap->m_tuple_content[cap->m_tuple_start[i]];
}

int  GetSizeArrayTuples(struct SparseFM* cap)
{
	return (int) cap->m_tuple_content.size();
}

int GetNumTuples(struct SparseFM* cap)
{
	return (int) cap->m_tuples.size();
}

// now sets are indexed by A = the position of the element in the respective array (singletons, tuples or pairs)
int             IsInSetSparse(int A, int card, int i, struct SparseFM* cap)                 // does i belong to set A?
{
	if (card == 1) return (A == i);

	
	if (card == 2)  {	
#ifdef	MEMCHK	
		if(2*A >= cap->m_pair_index.size()) return 0; // out of bounds
#endif		
		return((cap->m_pair_index[2 * A] == (uint16_t)i) || (cap->m_pair_index[2 * A + 1] == (uint16_t)i));
	}
	// else process tuple
#ifdef	MEMCHK	
	if(A >= cap->m_tuple_start.size()) return 0; // out of bounds
#endif	
	
	for (int j = 1;j <= cap->m_tuple_content[cap->m_tuple_start[A]]; j++)
		if (cap->m_tuple_content[cap->m_tuple_start[A] + j] == i) return 1;

	return 0;
}

int             IsSubsetSparse(int A, int cardA, int B, int cardB, struct SparseFM* cap)       // is B subset of A ?  careful, will not work if B has repeated entries by mistake
{
	if (cardB > cardA) return 0;
	if (cardB == 1)
	{
		return IsInSetSparse(A, cardA, B, cap);
	}
	if (cardB == 2) {
		if (cardA == 1) return 0;
		if (cardA == 2) return (A == B);
#ifdef	MEMCHK	
		if(2*B >= cap->m_pair_index.size()) return 0; // out of bounds
#endif			
		
		return (IsInSetSparse(A, cardA, cap->m_pair_index[2 * B], cap) && IsInSetSparse(A, cardA, cap->m_pair_index[2 * B + 1], cap));
	}

#ifdef	MEMCHK
	if(B >= cap->m_tuple_start.size()) return 0; // out of bounds
#endif		
	
	for (int j = 1;j <= cap->m_tuple_content[cap->m_tuple_start[B]]; j++) {
		if (!IsInSetSparse(A, cardA, cap->m_tuple_content[cap->m_tuple_start[B] + j], cap)) return 0;
	}
	return 1;
}



double min_subsetSparse(double* x, int n, int S, int cardS, struct SparseFM* cap) // returns minimum of x_i, such that i belongs to set S
{
	if (cardS == 1) return x[S];
	if (cardS == 2)
	{
#ifdef	MEMCHK		
		if(2*S >= cap->m_pair_index.size()) return 0; // out of bounds
#endif			
		double t1 = x[cap->m_pair_index[2 * S] -1];
		double t2 = x[cap->m_pair_index[2 * S + 1]  -1];
		return min(t1, t2);
	}
	double t = 10e10;
#ifdef	MEMCHK	
	if(S >= cap->m_tuple_start.size()) return 0; // out of bounds
#endif		
	
	for (int j = 1;j <= cap->m_tuple_content[cap->m_tuple_start[S]]; j++)
		t = min(t, x[cap->m_tuple_content[cap->m_tuple_start[S] + j]  -1]);

	return t;
}
double max_subsetSparse(double* x, int n, int S, int cardS, struct SparseFM* cap) // returns maximum of x_i, such that i belongs to set S
{
	if (cardS == 1) return x[S];
	if (cardS == 2)
	{
#ifdef	MEMCHK		
		if(2*S >= cap->m_pair_index.size()) return 0; // out of bounds
#endif		
		double t1 = x[cap->m_pair_index[2 * S]  -1];
		double t2 = x[cap->m_pair_index[2 * S + 1]  -1];
		return max(t1, t2);
	}
	double t = -10e10;
	
#ifdef	MEMCHK	
	if(S >= cap->m_tuple_start.size()) return 0; // out of bounds
#endif		
	for (int j = 1;j <= cap->m_tuple_content[cap->m_tuple_start[S]]; j++)
		t = max(t, x[cap->m_tuple_content[cap->m_tuple_start[S] + j]  -1]);

	return t;
}

double ChoquetMobSparse(double*x, int n, struct SparseFM* cap)
{
	double t = 0;
	for (int i = 0;i < n;i++) t += x[i] * cap->m_singletons[i];

	for (size_t  i = 0;i < cap->m_pairs.size();i++)
		t += min_subsetSparse(x, n, (int)i, 2, cap) * cap->m_pairs[i];

	for (size_t  i = 0;i < cap->m_tuples.size();i++)
		t += cap->m_tuples[i] * min_subsetSparse(x, n, (int)i, 3, cap);

	return t;
}


// need Shaple/Banhzaf values 

void ShapleyMobSparse(double* v, int n, struct SparseFM* cap)
{
	for (int i = 0;i < n; i++)
		v[i] = cap->m_singletons[i];  // singleton

	// pairs, brute force way
	for (int i = 0; i < n; i++) {
		for (size_t  j = 0;j < cap->m_pairs.size(); j++)
			v[i] += 0.5 * cap->m_pairs[j] * IsInSetSparse((int)j, 2, i+1, cap);  // 1based
	}

	// tuples
	for (size_t  j = 0;j < cap->m_tuples.size(); j++) {
		double r = 1. / cap->m_tuple_content[cap->m_tuple_start[j]]; // cardinality

		for (int k = 1;k <= cap->m_tuple_content[cap->m_tuple_start[j]]; k++)
			v[cap->m_tuple_content[cap->m_tuple_start[j] + k] -1 ] += cap->m_tuples[j] * r;

	}
}

void BanzhafMobSparse(double* v, int n, struct SparseFM* cap)
{
	for (int i = 0;i < n; i++)
		v[i] = cap->m_singletons[i];  // singleton

	// pairs, brute force way
	for (int i = 0; i < n; i++) {
		for (size_t  j = 0;j < cap->m_pairs.size(); j++)
			v[i] += 0.5 * cap->m_pairs[j] * IsInSetSparse((int)j, 2, i+1, cap);
	}

	// tuples
	for (size_t  j = 0;j < cap->m_tuples.size(); j++) {
		double r = 1. / ( 1<< (cap->m_tuple_content[cap->m_tuple_start[j]] -1) ); // 2^(cardinality-1)

		for (int k = 1;k <= cap->m_tuple_content[cap->m_tuple_start[j]]; k++)
			v[cap->m_tuple_content[cap->m_tuple_start[j] + k] -1  ] += cap->m_tuples[j] * r;

	}
}



void NonmodularityIndexMobSparse(double* w, int n, int_64 m, struct SparseFM* cap) // calculates  all 2^n nonmodularity indices (returned in w) using Mobius transform of 
//a k-additive FM in cardinality ordering (of length 2^n=m), using sparse representation
{
	int_64 id, A;
	w[0] = 0;
	for (int_64 i = (int_64)0; i < m; i++) w[i] = 0;	
	
	for (id = (int_64)1; id < m; id++)
	{
		if(Cardinality(id)==1) {
			for( int i=0;i<n;i++) if(IsInSet(id,i))
				{w[id]=cap->m_singletons[i];break;}
		} else {
			for (size_t j = 0;j < cap->m_pairs.size(); j++)
			{
				A = 0;
				AddToSet(&A, (cap->m_pair_index[2 * j] - 1)); // 1based to 0-based
				AddToSet(&A, (cap->m_pair_index[2 * j + 1] - 1));
				if (IsSubset(id, A))
					w[id] += 2 * cap->m_pairs[j];
			}

			for (size_t  i = 0; i < cap->m_tuples.size();i++) {
				A = 0;
				for (int  j = 1;j <= cap->m_tuple_start[i];j++)
					AddToSet(&A, (cap->m_tuple_content[cap->m_tuple_start[i] + j] - 1));
				if (IsSubset(id, A))
					w[id] += cap->m_tuples[i] * cap->m_tuple_content[cap->m_tuple_start[i]];  // cardinality
			}
		
			w[id] /= Cardinality(id);
		}
	}
}


void PopulateFM2Add_Sparse(double* singletons, int numpairs, double* pairs, int* indicesp1, int* indicesp2 , struct SparseFM* cap)
{ //FM is already prepared, just add singletons and pairs
	
	for (int i = 0;i < cap->n;i++) cap->m_singletons[i] = singletons[i];

	for (int i = 0;i < numpairs; i++) {
		cap->m_pairs[i] = pairs[i];
		cap->m_pair_index[2 * i] = indicesp1[ i];
		cap->m_pair_index[2 * i+1] = indicesp2[i];
	}
}


void AddPairSparse(int i, int j, double* v, struct SparseFM* cap)
{
	cap->m_pairs.push_back(*v);
	cap->m_pair_index.push_back(min(i, j));
	cap->m_pair_index.push_back(max(i, j));
}
void AddTupleSparse(int tupsize, int* tuple, double* v, struct SparseFM* cap)
{
	cap->m_tuples.push_back(*v);
	cap->m_tuple_start.push_back((int) cap->m_tuple_content.size());

	cap->m_tuple_content.push_back(tupsize);

	for (int j = 0;j < tupsize;j++) {
		cap->m_tuple_content.push_back(tuple[j]);
	}
}

void PopulateFM2Add_Sparse_from2add(int n, double * v, struct SparseFM* cap)
{
	Prepare_FM_sparse(n, 0, NULL, cap);
	for (int i = 0;i < n;i++) cap->m_singletons[i] = v[i];
	
	//int len = n*(n - 1) / 2;
	int i = n;
	for(int k=0;k <n-1; k++)
		for (int j = k + 1;j < n;j++) {
			if (v[i] != 0) AddPairSparse(k+1, j+1, &(v[i]), cap);
			i++;
		}
}

void Expand2AddFull(double* v, struct SparseFM* cap)
{
	// array v needs to be n+choose(n,2) in size at least, not checked
	for (int i = 0;i < cap->n;i++) v[i] = cap->m_singletons[i];

	int len = cap->n*(cap->n - 1) / 2;
	for (int i = cap->n; i < len + cap->n ;i++) v[i] = 0;
	for (size_t  i = 0;i < cap->m_pairs.size();i++) {
		len = cap->n;
		for (int  j = 0; j < cap->m_pair_index[2 * i] - 1; j++) { len += (cap->n - j - 1);  }
		len += cap->m_pair_index[2 * i + 1] - 1 -  cap->m_pair_index[2 * i ]  ;
		v[len]= cap->m_pairs[i];
	}

}

// in bit ordering
void ExpandSparseFull(double* v, struct SparseFM* cap)
{
	//memset(v, 0,sizeof(double)*((int_64)1 << (int_64)(cap->n) ) );
	for (int_64 i = 0; i < ((int_64)1 << (int_64)(cap->n)); i++) v[i] = 0;
	int_64 A;
	for (int i = 0;i < cap->n;i++) {
		A = 0;
		AddToSet(&A, (i));
		v[A] = cap->m_singletons[i];
	}

	for (size_t i = 0;i < cap->m_pairs.size();i++) {
		A = 0;
		AddToSet(&A, (cap->m_pair_index[2*i]-1 ));
		AddToSet(&A, (cap->m_pair_index[2 * i+1]-1));
		v[A]= cap->m_pairs[i];
	}

	for (size_t  i = 0; i < cap->m_tuples.size();i++) {
		A = 0;
		for(int  j=1;j<=cap->m_tuple_start[i];j++)
			AddToSet(&A, (cap->m_tuple_content[cap->m_tuple_start[i]+j]  -1) );
		v[A] = cap->m_tuples[i];
	}
}

void ExportSparseSingletons(int n, double *v, struct SparseFM* cap)
{
	for (int i = 0;i < n;i++) v[i] = cap->m_singletons[i];
}

int ExportSparsePairs( int* pairs, double *v, struct SparseFM* cap)
{
	for (size_t  i = 0;i < cap->m_pairs.size();i++) v[i] = cap->m_pairs[i];
	for (size_t  i = 0;i < cap->m_pairs.size()*2;i++) pairs[i]= cap->m_pair_index[i];
	return (int) cap->m_pairs.size();
}

int ExportSparseTuples( int* tuples, double *v, struct SparseFM* cap)
{
	for (size_t  i = 0;i < cap->m_tuples.size();i++) v[i] = cap->m_tuples[i];
	int j = 0;
	for (size_t  i = 0;i < cap->m_tuples.size(); i++) {
		tuples[j] = cap->m_tuple_content[cap->m_tuple_start[i]];
		int r = tuples[j];
		j++;
		for (int k = 1;k <= r;k++) {
			tuples[j] = cap->m_tuple_content[cap->m_tuple_start[i] + k ];
			j++;
		}
	}
	return (int) cap->m_tuples.size();
}


// random generation in sparse form

int generate_fm_2additive_convex_sparse(int n, struct SparseFM* cap)
{
	int size;
	myfloat *vv = new myfloat[n*n];
	generate_fm_2additive_convex_withsomeindependent(1, n, &size, vv);

	PopulateFM2Add_Sparse_from2add(n, vv, cap);

	delete[] vv;
	return 0;
}

//this is actually belief measure, not just convex
int generate_fm_kadditive_convex_sparse(int n, int k, int nonzero, struct SparseFM* cap)
{
	// here randomly determine the pairs and tuples with their indices, then generate as on simplex
	std::vector<int> tuples;
	auto rng1 = std::default_random_engine();

	std::uniform_int_distribution<int> uni(2, k);

	std::vector<int> elements(n);
	for (int i = 0;i < n;i++) elements[i] = 1 + i; // 1-based

	for (int i = 0;i < nonzero;i++) {
		// generate randomly the size and then the composition
		int sz = uni(rng1);
		tuples.push_back(sz);
		//std::uniform_int_distribution<int> unituple(1, sz);
		std::shuffle(std::begin(elements), std::end(elements), rng1);
		for (int j = 0;j < sz;j++)
		{
			tuples.push_back(elements[j]); //need nonrepeated
		}
	}

	int r = n + nonzero;
	vector<myfloat>  temp(r - 1);
	vector<myfloat>  vv(r);
	{
		random_coefficients(r - 1, temp);  //decreasing sequence
		vv[0] = 1 - temp[0];
		for (int j = 1;j < r - 1;j++)
			vv[ j] = temp[j - 1] - temp[j];
		vv[ r - 1] = temp[r - 2];
	}

	Prepare_FM_sparse( n, (int) tuples.size(), &( tuples[0]),  cap);
// fill in the values vv
	for (int i = 0;i < n;i++) cap->m_singletons[i] = vv[i];
	for (size_t  i = 0; i < cap->m_pairs.size();i++) cap->m_pairs[i] = vv[i + n];
	int j = (int) cap->m_pairs.size() + n;
	for (size_t  i = 0; i < cap->m_tuples.size();i++) cap->m_tuples[i] = vv[i + j];

	return 0;
}


// need interaction indices
// need dual (same sparsity?)

#endif
