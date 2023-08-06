//
/* This is a C-wrapper for fmtools library 

   Gleb Beliakov, 2020
*/
#include "generaldefs.h" //NH
#define R_NO_REMAP

// #define __R //NH
#ifdef __R
//#include "cpp11.hpp"



#include <R.h>
#include <Rdefines.h>
#include <Rinternals.h>
#endif
//#include <Rcpp.h>


#include <stdlib.h>
#include "wrapperpy.h"

#ifdef PYTHON_
#define LIBEXP
#endif

//#if (defined(__clang__) || defined(__APPLE__) || defined(__arm64__)) && defined(_LIBCPP_VERSION)
//#if (defined(__clang__) ||  defined(__arm64__)) && defined(_LIBCPP_VERSION)	
#if  defined(_LIBCPP_VERSION)	// may be just detect libc++

#if (_LIBCPP_VERSION < 14000)
template <class T>
void wrapArrayInVector( T *sourceArray, size_t arraySize, std::vector<T,  std::allocator<T> > volatile &targetVector ) {
  typename std::__vector_base<T, std::allocator<T> > *vectorPtr =
    (typename std::__vector_base<T, std::allocator<T> > *)((void *) &targetVector);
	
    class MyDerivedClass : public std::__vector_base<T, std::allocator<T> > {
    public:
		void assignarray(T *sourceArray, size_t arraySize) {
		this->__begin_ = sourceArray;
		this->__end_ =  this-> __end_cap() = this->__begin_ + arraySize;			
		}
    };
    return static_cast<MyDerivedClass &>(*vectorPtr).assignarray(sourceArray, arraySize);	
}

template <class T>
void releaseVectorWrapper( std::vector<T,  std::allocator<T> > volatile &targetVector ) {
  typename std::__vector_base<T, std::allocator<T> > *vectorPtr =
        (typename std::__vector_base<T, std::allocator<T> > *)((void *) &targetVector);
		
    class MyDerivedClass : public std::__vector_base<T, std::allocator<T> > {
    public:
		void assignnullarray() {
			 this->__begin_ = this->__end_ =  this->__end_cap()= NULL;			
		}
    };
    return static_cast<MyDerivedClass &>(*vectorPtr).assignnullarray();		
 //  vectorPtr->__begin_ = vectorPtr->__end_ =  vectorPtr->__end_cap()= NULL;
}

#else // version 14 changed and made __begin_ private, so before I find a better solution, just copy



	template <class T>
void wrapArrayInVector( T *sourceArray, size_t arraySize, std::vector<T,  std::allocator<T> > volatile &targetVector ) {
  typename std::vector<T, std::allocator<T> > *vectorPtr =
    (typename std::vector<T, std::allocator<T> > *)((void *) &targetVector);
	
	vectorPtr->assign(sourceArray, sourceArray+ arraySize);
}
template <class T>
void releaseVectorWrapper( std::vector<T,  std::allocator<T> > volatile &targetVector )
{
	// do nothing 
	return ;
}

/* Can also do this way
template <class _Allocator>
class  myvector<bool, _Allocator>
{
	public:
	    __storage_pointer                                      __begin_;
    size_type                                              __size_;
    __compressed_pair<size_type, __storage_allocator> __cap_alloc_;

}
myvector *b = reinterpret_cast<myvector *> &targetVector; 

//now you can use b to access members of vector 

		b->__begin_ = sourceArray;
		b->__end_ =  b-> __end_cap() = b->__begin_ + arraySize;	
*/


/*
	template <class T>
void wrapArrayInVector( T *sourceArray, size_t arraySize, std::vector<T,  std::allocator<T> > volatile &targetVector ) {
  typename std::vector<T, std::allocator<T> > *vectorPtr =
    (typename std::vector<T, std::allocator<T> > *)((void *) &targetVector);
	
    class MyDerivedClass : public std::vector<T, std::allocator<T> > {
    public:
		void assignarray(T *sourceArray, size_t arraySize) {
		this->__begin_ = sourceArray;
		this->__end_ =  this-> __end_cap() = this->__begin_ + arraySize;			
		}
    };
    return static_cast<MyDerivedClass &>(*vectorPtr).assignarray(sourceArray, arraySize);	
}

template <class T>
void releaseVectorWrapper( std::vector<T,  std::allocator<T> > volatile &targetVector ) {
  typename std::vector<T, std::allocator<T> > *vectorPtr =
        (typename std::vector<T, std::allocator<T> > *)((void *) &targetVector);
		
    class MyDerivedClass : public std::vector<T, std::allocator<T> > {
    public:
		void assignnullarray() {
			 this->__begin_ = this->__end_ =  this->__end_cap()= NULL;			
		}
    };
    return static_cast<MyDerivedClass &>(*vectorPtr).assignnullarray();		
 //  vectorPtr->__begin_ = vectorPtr->__end_ =  vectorPtr->__end_cap()= NULL;
}
*/
#endif

#else

template <class T>
void wrapArrayInVector( T *sourceArray, size_t arraySize, std::vector<T,  std::allocator<T> > volatile &targetVector ) {
  typename std::_Vector_base<T, std::allocator<T> >::_Vector_impl *vectorPtr =
    (typename std::_Vector_base<T, std::allocator<T> >::_Vector_impl *)((void *) &targetVector);
  vectorPtr->_M_start = sourceArray;
  vectorPtr->_M_finish = vectorPtr->_M_end_of_storage = vectorPtr->_M_start + arraySize;
}

template <class T>
void releaseVectorWrapper( std::vector<T,  std::allocator<T> > volatile &targetVector ) {
  typename std::_Vector_base<T, std::allocator<T> >::_Vector_impl *vectorPtr =
        (typename std::_Vector_base<T, std::allocator<T> >::_Vector_impl *)((void *) &targetVector);
  vectorPtr->_M_start = vectorPtr->_M_finish = vectorPtr->_M_end_of_storage = NULL;
}
#endif



// #undef PYTHON_ commented out by NH

extern "C" {

// todo: add cases i==3,4 explicit formulas
inline int_64 choose(int i, int n, struct fm_env* env)
{
	if (i == 1) return n;
	if (i == 2) return (int_64)(n*(n - 1)) / 2;
	if (i == 3) return (int_64)(n*(n - 1)*(n - 2)) / 6;
	if (i == 4) return (int_64)(n*(n - 1)*(n - 2)*(n - 3)) / 24;
	if (i == 5) return (int_64)(n*(n - 1)*(n - 2)*(n - 3)*(n - 4)) / 120;

	return (int_64)(env->factorials[n] / env->factorials[i] / env->factorials[n - i]);
}

#ifdef PYTHON_
LIBEXP double py_min_subset(double* x, int n, int_64 S)
	{
		return min_subset(x, n, S);
	}
LIBEXP double py_max_subset(double* x, int n, int_64 S)
{
	return max_subset(x, n, S);
}

LIBEXP void py_ConvertCard2Bit(double* dest, double* src, struct fm_env* env)
	{
		int_64 *r = (int_64*)(env->card2bit);
		for (int_64 i = 0; i < (int_64) (env->m); i++)
				dest[r[i]] = src[i];
	}

LIBEXP double py_min_subsetC(double* x, int n, int_64 S, struct fm_env* env)
	{
		int_64 *r = (int_64*)(env->card2bit);
		return min_subset(x, n, r[S]);
	}


LIBEXP double py_max_subsetNegC(double* x, int n, int_64 S, struct fm_env* env)
	{
		int_64 *r = (int_64*)(env->card2bit);
		int_64 N = UniversalSet(n);
		N = Setdiff(N, r[S]);
		double ret = max_subset(x, n, N);
		return ret;
	}

LIBEXP int py_SizeArraykinteractive(int n, int k, struct fm_env* env)
	{
		int r = 1;
		for (int i = 1;i <= k; i++)
			r += (int) choose(i, n, env);
		return r;
	}

LIBEXP int py_IsSubsetC(int i, int j, struct fm_env* env) // is i subset j? In cardinality ordering both
	{
		int_64 *r= (int_64*)(env->card2bit);
		return IsSubset(r[j], r[i]);
	}
LIBEXP int py_IsElementC(int i, int j, struct fm_env* env) // is i element of j (cardinality-based)?
	{
		if (i <= env->n) return py_IsSubsetC(i, j, env); else return 0;
	}
	//todo sparse representation

#endif


int log2int(const int_64 u) {
	int l=0;
	int_64 m=u;
	while (m >>= 1) { ++l; }
	return l;
}

void BanzhafCall(double* v, double* x, int* n,
	int* m, int* Rcard, int* Rcardpos, double* Rbit2card, double* Rcard2bit, double* Rfactorials)

{
	int nn = *n;
	int_64 mm = (int_64)*m;

	card=Rcard;
 	cardpos=Rcardpos;
	bit2card=(int_64*)Rbit2card;
	card2bit = (int_64*)Rcard2bit;
	m_factorials=Rfactorials;
	Banzhaf(v, x, nn, mm);	

}
void BanzhafMobCall(double* v, double* x, int* n,
	int* m, int* Rcard, int* Rcardpos, double* Rbit2card, double* Rcard2bit, double* Rfactorials)

{
	int nn = *n;
	int_64 mm = (int_64)*m;

	card = Rcard;
	cardpos = Rcardpos;
	bit2card = (int_64*)Rbit2card;
	card2bit = (int_64*)Rcard2bit;
	m_factorials = Rfactorials;
	BanzhafMob(v, x, nn, mm);
}
void ShapleyMobCall(double* v, double* x, int* n,
	int* m, int* Rcard, int* Rcardpos, double* Rbit2card, double* Rcard2bit, double* Rfactorials)

{
	int nn = *n;
	int_64 mm = (int_64)*m;

	card = Rcard;
	cardpos = Rcardpos;
	bit2card = (int_64*)Rbit2card;
	card2bit = (int_64*)Rcard2bit;
	m_factorials = Rfactorials;
	ShapleyMob(v, x, nn, mm);
}

void ChoquetCall(double* x, double* v, int* n, double& cho,
	int* m, int* Rcard, int* Rcardpos, double* Rbit2card, double* Rcard2bit, double* Rfactorials)
{
	int nn = *n;
	int_64 mm = (int_64)*m;
	card=Rcard;
 	cardpos=Rcardpos;
	bit2card = (int_64*)Rbit2card;
	card2bit = (int_64*)Rcard2bit;
	m_factorials=Rfactorials;;
	cho  = Choquet(x, v, nn, mm);

}

void ChoquetkinterCall(double* x, double* v, int* n, double& cho, int* kint,
	int* m, int* Rcard, int* Rcardpos, double* Rbit2card, double* Rcard2bit, double* Rfactorials)
{
	int nn = *n;
	int_64 mm = (int_64)*m;
	card = Rcard;
	cardpos = Rcardpos;
	bit2card = (int_64*)Rbit2card;
	card2bit = (int_64*)Rcard2bit;
	m_factorials = Rfactorials;;
	cho = ChoquetKinter(x, v, nn, mm, *kint);
}



void ChoquetMobCall(double*x, double* Mob, int *n, double& choMob,
	int* m, int* Rcard, int* Rcardpos, double* Rbit2card, double* Rcard2bit, double* Rfactorials)

{
	int nn = *n;
	int_64 mm = (int_64)*m;
	card=Rcard;
 	cardpos=Rcardpos;
	bit2card = (int_64*)Rbit2card;
	card2bit = (int_64*)Rcard2bit;
	m_factorials=Rfactorials; 
    choMob = ChoquetMob(x, Mob, nn, mm);
}


void ConstructLambdaMeasureCall(double* singletons, double* lambda, double* v, int &n,
	int* m, int* Rcard, int* Rcardpos, double* Rbit2card, double* Rcard2bit, double* Rfactorials)
{
	int nn = n;
	int_64 mm = (int_64)*m;
	card=Rcard;
 	cardpos=Rcardpos;
	bit2card = (int_64*)Rbit2card;
	card2bit = (int_64*)Rcard2bit;
	m_factorials=Rfactorials; 

    ConstructLambdaMeasure(singletons, lambda, v, nn, mm);

}

void ConstructLambdaMeasureMobCall(double* singletons, double* lambda, double* Mob, int& n,
	int* m, int* Rcard, int* Rcardpos, double* Rbit2card, double* Rcard2bit, double* Rfactorials)
{
	int nn = n;
	int_64 mm = (int_64)*m;
	card = Rcard;
	cardpos = Rcardpos;
	bit2card = (int_64*)Rbit2card;
	card2bit = (int_64*)Rcard2bit;
	m_factorials = Rfactorials;

	double *v = new double[mm];

	ConstructLambdaMeasure(singletons, lambda, v, nn, mm);
	Mobius(v, Mob, nn, mm);
	delete[] v;
}

void dualmCall(double* v, double* w, int &n,
	int* m, int* Rcard, int* Rcardpos, double* Rbit2card, double* Rcard2bit, double* Rfactorials)
{
	int nn = log2int(n);
	int_64 mm = (int_64)*m;
	card=Rcard;
 	cardpos=Rcardpos;
	bit2card = (int_64*)Rbit2card;
	card2bit = (int_64*)Rcard2bit;
	m_factorials=Rfactorials;
       dualm(v, w, nn, mm);
}
void dualMobCall(double* Mob, double* w, int &n,
	int* m, int* Rcard, int* Rcardpos, double* Rbit2card, double* Rcard2bit, double* Rfactorials)
{
	card = Rcard;
	cardpos = Rcardpos;
	bit2card = (int_64*)Rbit2card;
	card2bit = (int_64*)Rcard2bit;
	m_factorials = Rfactorials;
	dualMob( Mob, w, *m);
}

void EntropyChoquetCall(double* v, int& n, double& cho,
	int* m, int* Rcard, int* Rcardpos, double* Rbit2card, double* Rcard2bit, double* Rfactorials)

{
	int nn = n;
	int_64 mm = (int_64)*m;
	card=Rcard;
 	cardpos=Rcardpos;
	bit2card = (int_64*)Rbit2card;
	card2bit = (int_64*)Rcard2bit;
	m_factorials=Rfactorials;
	cho  = Entropy(v, nn, mm);
}


int  fittingCallMob(int *n, int* datanum, int* Kadd, double *v, double *Dataset)
{
	// reurns Mobius in binary ordering
	double orness[2];
	orness[0]=0; 
	orness[1]=1;
	int res;
	int nn = *n;
	int_64 m;
	int datanums = *datanum;
	int additive = *Kadd;

	Preparations_FM(nn,&m);

	double *w = new double[m];

	res = FuzzyMeasureFitLP(nn,  m,  datanums,  additive, w,  Dataset, 0, NULL , NULL, 0, orness);

	for(unsigned int i=0; i<m ; i++)  {
			v[card2bit[i]] = w[i];
	}

	Cleanup_FM();
	delete [] w;
	return res;
}

int  fittingCall(int *n, int* datanum, int* Kadd, double *v, double *Dataset)
{
	// reurns Mobius in binary ordering
	double orness[2];
	orness[0] = 0;
	orness[1] = 1;
	int res;
	int nn = *n;
	int_64 m;
	int datanums = *datanum;
	int additive = *Kadd;

	Preparations_FM(nn, &m);

	double *w = new double[m];

	res = FuzzyMeasureFitLP(nn, m, datanums, additive, w, Dataset, 0, NULL, NULL, 0, orness);

	for (unsigned int i = 0; i < m; i++) {
		v[card2bit[i]] = w[i];
	}

	for (unsigned int i = 0; i < m; i++)
		w[i] = v[i];
	Zeta(w, v, nn, m);

	Cleanup_FM();
	delete[] w;
	return res;
}

int  fittingCallKtolerant(int *n, int* datanum, int* Kadd, double *v, double *Dataset)
{
	double orness[2];
	orness[0]=0; 
	orness[1]=1;
	int res;
	int nn = *n;
	int_64 m;
	int datanums = *datanum;
	int additive = *Kadd;

	Preparations_FM(nn,&m);

	double *w = new double[m];

	res = FuzzyMeasureFitLPStandard(nn,  m,  datanums,  additive, w,  Dataset, 0, NULL , NULL, 0, orness);

	for(unsigned int i=0; i<m ; i++)  {
			v[card2bit[i]] = w[i];
	}

	Cleanup_FM();
	delete [] w;
	return res;
}
int  fittingCallKmaxitive(int *n, int* datanum, int* Kadd, double *v, double *Dataset)
{
	int res;
	int nn = *n;
	int_64 m;
	int datanums = *datanum;
	int additive = *Kadd;

	Preparations_FM(nn,&m);

	double *w = new double[m];
	if (nn<6 || (nn - additive<3))
	res = FuzzyMeasureFitLPMIP(nn,  m,  datanums,  additive, w,  Dataset);
	else 
		res = FuzzyMeasureFitLP_relaxation(nn, m, datanums, additive, w, Dataset);
	for(unsigned int i=0; i<m ; i++)  {
			v[card2bit[i]] = w[i];
	}

	Cleanup_FM();
	delete [] w;
	return res;
}



int  fittingCallKinteractive(int *n, int* datanum, int* Kadd, double *v, double *Dataset, double *K)
{
	double orness[2];
	orness[0] = 0;
	orness[1] = 1;
	int res;
	int nn = *n;
	int_64 m;
	int datanums = *datanum;
	int additive = *Kadd;

	Preparations_FM(nn, &m);

	double *w = new double[m];
	res=FuzzyMeasureFitLPKinteractive(nn, m, datanums, additive, w, Dataset, 0, NULL, NULL, 0, orness, *K);


	for (unsigned int i = 0; i<m; i++)  {
		v[card2bit[i]] = w[i];
	}

	Cleanup_FM();
	delete[] w;
	return res;
}


int  fittingCallKinteractiveMC(int *n, int* datanum, int* Kadd, double *v, double *Dataset, double *K)
{
	double orness[2];
	orness[0] = 0;
	orness[1] = 1;
	int res;
	int nn = *n;
	int_64 m;
	int datanums = *datanum;
	int additive = *Kadd;

	Preparations_FM(nn, &m);

	double *w = new double[m];
	res = FuzzyMeasureFitLPKinteractiveMaxChains(nn, m, datanums, additive, w, Dataset, 0, NULL, NULL, 0, orness, *K);


	for (unsigned int i = 0; i<m; i++)  {
		v[card2bit[i]] = w[i];
	}

	Cleanup_FM();
	delete[] w;
	return res;
}
int  fittingCallKinteractiveAuto(int *n, int* datanum, int* Kadd, double *v, double *Dataset, double *K, int* maxiters)
{
	double orness[2];
	orness[0] = 0;
	orness[1] = 1;
	int res;
	int nn = *n;
	int_64 m;
	int datanums = *datanum;
	int additive = *Kadd;
	double KK = 0;

	Preparations_FM(nn, &m);

	double *w = new double[m];
	res = FuzzyMeasureFitLPKinteractiveAutoK(nn, m, datanums, additive, w, Dataset, 0, NULL, NULL, 0, orness, &KK, *maxiters);
	*K = KK;

	for (unsigned int i = 0; i<m; i++)  {
		v[card2bit[i]] = w[i];
	}

	Cleanup_FM();
	delete[] w;
	return res;
}

int  fittingCallKinteractiveMarginal(int *n, int* datanum, int* Kadd, double *v, double *Dataset, double *K, int submod)
{
	double orness[2];
	orness[0] = 0;
	orness[1] = 1;
	int res;
	int nn = *n;
	int_64 m;
	int datanums = *datanum;
	int additive = *Kadd;

	int option1 = 0;
	if (submod == 1) option1 = 2;
	if (submod == -1) option1 = 1;

	Preparations_fm_marginal(nn, &m, ((additive < nn) ? additive + 1 : nn));
	//Preparations_FM(nn, &m);

//	double *w = new double[m];
	res = FuzzyMeasureFitLPKinteractiveMarginal(nn, m, datanums, additive, v, Dataset, 0, NULL, NULL, option1, orness, *K); //FuzzyMeasureFitLPKinteractiveMarginalMaxChain


//	for (unsigned int i = 0; i<m; i++)  {
//		v[i] = w[i];
//	}

	Cleanup_FM();
//	delete[] w;
	return res;
}

int  fittingCallKinteractiveMarginalMC(int *n, int* datanum, int* Kadd, double *v, double *Dataset, double *K, int* maxiters, int submod)
{
	double orness[2];
	orness[0] = 0;
	orness[1] = 1;
	int res;
	int nn = *n;
	int_64 m;
	int datanums = *datanum;
	int additive = *Kadd;

	int option1 = 0;
	if (submod == 1) option1 = 2;
	if (submod == -1) option1 = 1;

	Preparations_fm_marginal(nn, &m, ((additive < nn) ? additive + 1 : nn));
	//Preparations_FM(nn, &m);

	double *w = new double[m];
	res = FuzzyMeasureFitLPKinteractiveMarginalMaxChain(nn, m, datanums, additive, w, Dataset, 0, NULL, NULL, option1, orness, *K);


	for (unsigned int i = 0; i<m; i++)  {
		v[card2bit[i]] = w[i];
	}

	Cleanup_FM();
	delete[] w;
	return res;
}

int FuzzyMeasureFitLPCall(int *n, int* datanum, int* Kadd, double *v, double *Dataset,
    int *options=0, double* indexlow=NULL, double* indexhigh=NULL , int *option1=0, double* orness=NULL)
{
    // int FuzzyMeasureFitLP(int n, int m, int K, int Kadd, double *v, double* XYData, int options=0, 
    //    double* indexlow=NULL, double* indexhigh=NULL , int option1=0, double* orness=NULL);
    // Input parameters: 
    // n - the dimension of inputs, m = 2^n - the number of fuzzy measure values
    // K - the number of empirical data
    // Kadd - k in k-additive f. measures, 1 < Kadd < n+1. Kdd=n - f.m. is unrestricted
    // XYData - an array of size K x (n+1), where each row is the pair (x,y), K data altogether
    // options (default value is 0)
    //    1 - lower bounds on Shapley values supplied in indexlow
    //    2 - upper bounds on Shapley values supplied in indexhigh
    //    3 - lower and upper bounds on Shapley values supplied in indexlow and indexhigh
    //    4 - lower bounds on all interaction indices supplied in indexlow
    //    5 - upper bounds on all interaction indices supplied in indexhigh
    //    6 - lower and upper bounds on all interaction indices supplied inindexlow and indexhigh
    //    all these value will be treated as additional constraints in the LP
    // indexlow, indexhigh - array of size n (options =1,2,3) or m (options=4,5,6)
    // containing the lower and upper bounds on the Shapley values or interaction indices

	// double orness[2];
	// orness[0]=0; 
	// orness[1]=1;
	int res;
	int nn = *n;
	int_64 m;
	int datanums = *datanum;
	int additive = *Kadd;

	Preparations_FM(nn,&m);

	double *w = new double[m];
//Rprintf("%d,%d,%d %d\n",m,additive,options,option1);
//Rprintf("%f %f\n",orness[0],orness[1]);



	// res = FuzzyMeasureFitLP(nn,  m,  datanums,  additive, w,  Dataset, 0, NULL , NULL, 0, orness);
	res = FuzzyMeasureFitLP(nn,  m,  datanums,  additive, w,  Dataset, 
                  *options, indexlow, indexhigh, *option1, orness);

	for(unsigned int i=0; i<m ; i++)  {
			v[card2bit[i]] = w[i];
	}

	if (*options & 128) {
		// convert to  standard rep
		for (unsigned int i = 0; i < m; i++)
			w[i] = v[i];
		Zeta(w, v, nn, m);
	}
//Rprintf("output %d\n",res);

	Cleanup_FM();
	delete [] w;
return res;
}


int fittingOWACall(int *n, int* datanum, double *v, double *Dataset)
{
	double orness[2];
	orness[0]=0; 
	orness[1]=1;
	int res;
	int nn = *n;
	int datanums = *datanum;

	double *w = new double[nn];

	res = FuzzyMeasureFitLPsymmetric(nn,  datanums, w, Dataset, 0, NULL, NULL, 0, orness);
	
	for(int i=0; i<nn ; i++)  {
			v[i] = w[i];
	}
	
	delete [] w;
	return res;
}	


int fittingWAMCall(int *n, int* datanum, double *v, double *Dataset)
{
	double orness[2];
	orness[0]=0; 
	orness[1]=1;
	int res;
	int nn = *n;
	int datanums = *datanum;

	double *w=new double[nn];

	res = FuzzyMeasureFitLPsymmetric(nn,  datanums, w,  Dataset, 1, NULL , NULL, 0, orness);
	
	for(int i=0; i<nn ; i++)  {
			v[i] = w[i];
	}
	
	delete [] w;
	return res;
}	


void InteractionCall(double* v, double* w,  
	int* m, int* Rcard, int* Rcardpos, double* Rbit2card, double* Rcard2bit, double* Rfactorials)
{
	int_64 mm = (int_64)*m;  // should I not cast?
	card=Rcard;
 	cardpos=Rcardpos;
	bit2card = (int_64*)Rbit2card;
	card2bit = (int_64*)Rcard2bit;
	m_factorials=Rfactorials;
	int nn = int(log2int(mm));
	double *Mob = new double[mm];
	Mobius(v,Mob, nn, mm);
	InteractionMob(Mob, w, mm);	
	delete[] Mob;

}	


void InteractionBCall(double* v, double* w,
	int* m, int* Rcard, int* Rcardpos, double* Rbit2card, double* Rcard2bit, double* Rfactorials)

{
	int_64 mm = (int_64)*m;
	card=Rcard;
 	cardpos=Rcardpos;
	bit2card = (int_64*)Rbit2card;
	card2bit = (int_64*)Rcard2bit;
	m_factorials=Rfactorials;
	int nn = log2int(mm);

	double *Mob = new double[mm];
	Mobius(v, Mob, nn, mm);
	InteractionBMob(Mob, w, mm);	
	delete[] Mob;
}	

void InteractionMobCall(double* Mob, double* w,
	int* m, int* Rcard, int* Rcardpos, double* Rbit2card, double* Rcard2bit, double* Rfactorials)

{
	int_64 mm = (int_64)*m;
	card = Rcard;
	cardpos = Rcardpos;
	bit2card = (int_64*)Rbit2card;
	card2bit = (int_64*)Rcard2bit;
	m_factorials = Rfactorials;

	InteractionMob(Mob, w, mm);
}
void InteractionBMobCall(double* Mob, double* w,
	int* m, int* Rcard, int* Rcardpos, double* Rbit2card, double* Rcard2bit, double* Rfactorials)
{
	int_64 mm = (int_64)*m;
	card = Rcard;
	cardpos = Rcardpos;
	bit2card = (int_64*)Rbit2card;
	card2bit = (int_64*)Rcard2bit;
	m_factorials = Rfactorials;

	InteractionBMob(Mob, w, mm);
}

void BipartitionShapleyCall(double *v, double* w, int *n, 
	int* m, int* Rcard, int* Rcardpos, double* Rbit2card, double* Rcard2bit, double* Rfactorials)
{
	card = Rcard;
	cardpos = Rcardpos;
	bit2card = (int_64*)Rbit2card;
	card2bit = (int_64*)Rcard2bit;
	m_factorials = Rfactorials;

	BipartitionShapleyIndex(v, w, *n, (int_64)(*m));
}
void BipartitionBanzhafCall(double *v, double* w, int *n, 
	int* m, int* Rcard, int* Rcardpos, double* Rbit2card, double* Rcard2bit, double* Rfactorials)
{
	card = Rcard;
	cardpos = Rcardpos;
	bit2card = (int_64*)Rbit2card;
	card2bit = (int_64*)Rcard2bit;
	m_factorials = Rfactorials;

	BipartitionBanzhafIndex(v, w, *n, (int_64)(*m));

}
void NonadditivityIndexMobCall(double *Mob, double* w, int *n,
	int* m, int* Rcard, int* Rcardpos, double* Rbit2card, double* Rcard2bit, double* Rfactorials)
{
	card = Rcard;
	cardpos = Rcardpos;
	bit2card = (int_64*)Rbit2card;
	card2bit = (int_64*)Rcard2bit;
	m_factorials = Rfactorials;

	NonadditivityIndexMob(Mob, w, *n, (int_64)(*m));
}
void NonadditivityIndexCall(double *v, double* w, int *n, 
	int* m, int* Rcard, int* Rcardpos, double* Rbit2card, double* Rcard2bit, double* Rfactorials)
{
	card = Rcard;
	cardpos = Rcardpos;
	bit2card = (int_64*)Rbit2card;
	card2bit = (int_64*)Rcard2bit;
	m_factorials = Rfactorials;

	NonadditivityIndex(v, w, *n, (int_64)(*m));
}


void NonmodularityIndexCall(double *v, double* w, int *n,
	int* m, int* Rcard, int* Rcardpos, double* Rbit2card, double* Rcard2bit, double* Rfactorials)
{
	card = Rcard;
	cardpos = Rcardpos;
	bit2card = (int_64*)Rbit2card;
	card2bit = (int_64*)Rcard2bit;
	m_factorials = Rfactorials;

	NonmodularityIndex(v, w, *n, (int_64)(*m));
}
void NonmodularityIndexMobCall(double *Mob, double* w, int *n,
	int* m, int* Rcard, int* Rcardpos, double* Rbit2card, double* Rcard2bit, double* Rfactorials)
{
	card = Rcard;
	cardpos = Rcardpos;
	bit2card = (int_64*)Rbit2card;
	card2bit = (int_64*)Rcard2bit;
	m_factorials = Rfactorials;

	NonmodularityIndexMob(Mob, w, *n, (int_64)(*m));
}
void NonmodularityIndexMobkadditiveCall(double *v, double* w, int *n, int* k,
	int* m, int* Rcard, int* Rcardpos, double* Rbit2card, double* Rcard2bit, double* Rfactorials)
{
	card = Rcard;
	cardpos = Rcardpos;
	bit2card = (int_64*)Rbit2card;
	card2bit = (int_64*)Rcard2bit;
	m_factorials = Rfactorials;

	/*   int len = fm_arraysize_kadd(*n, *k);*/
	NonmodularityIndexMobkadditive(v, w, *n, *k ,(int_64)(*m));
}
void NonmodularityIndexKinteractiveCall(double *v, double* w, int *n, int* k,
	int* m, int* Rcard, int* Rcardpos, double* Rbit2card, double* Rcard2bit, double* Rfactorials)
{
	card = Rcard;
	cardpos = Rcardpos;
	bit2card = (int_64*)Rbit2card;
	card2bit = (int_64*)Rcard2bit;
	m_factorials = Rfactorials;

	int len = fm_arraysize(*n, (int_64)(*m), *k);
	//Rprintf("Len %d \n", len);
	NonmodularityIndexKinteractive(v, w, *n, *k, (int_64)(*m), len);
}




void ShowCoalitionsCall(int* m, int* coalition)
{
	for (int i = 0; i < (int)*m; i++)
	{
		coalition[i] = ShowValue(i);
	}
}

void ShowCoalitionsCardCall(int* m, int* coalition, double* Rcard2bit )
{
	card2bit = (int_64*)Rcard2bit;
	for (int i = 0; i < (int)*m; i++)
	{
		coalition[i] = ShowValue(card2bit[ i]);
	}
}


void ZetaCall(double* Mob, double* v, int *n,
	int* m, int* Rcard, int* Rcardpos, double* Rbit2card, double* Rcard2bit, double* Rfactorials)

{
	card = Rcard;
	cardpos = Rcardpos;
	bit2card = (int_64*)Rbit2card;
	card2bit = (int_64*)Rcard2bit;
	m_factorials = Rfactorials;
	Zeta(Mob, v, *n, (int_64)(*m));
}


int IsMeasureAdditiveCall(double* v,  int& result,
	int* m, int* Rcard, int* Rcardpos, double* Rbit2card, double* Rcard2bit, double* Rfactorials)

{
	// Returns 1 if yes, 0 if no;
    // v is a fuzzy measure in standard representation.
    //unsigned int m;
	int nn = log2int(*m);
	int_64 mm = (int_64)*m;
//	Preparations_FM(nn,&m);

	card=Rcard;
 	cardpos=Rcardpos;
	bit2card = (int_64*)Rbit2card;
	card2bit = (int_64*)Rcard2bit;
	m_factorials=Rfactorials;

	result= IsMeasureAdditive(v, nn, mm);
	
//	Cleanup_FM();
	return(result);
}	


int IsMeasureBalancedCall(double* v,  int& result,
	int* m, int* Rcard, int* Rcardpos, double* Rbit2card, double* Rcard2bit, double* Rfactorials)

{
	// Returns 1 if yes, 0 if no;
    // v is a fuzzy measure in standard representation.
	int_64 mm = *m;
   
	//	Preparations_FM(nn,&m);

	card=Rcard;
 	cardpos=Rcardpos;
	bit2card = (int_64*)Rbit2card;
	card2bit = (int_64*)Rcard2bit;
	m_factorials=Rfactorials;

	result= IsMeasureBalanced(v, mm);
	
//	Cleanup_FM();
	return(result);
}	


int IsMeasureSelfdualCall(double* v,  int& result,
	int* m, int* Rcard, int* Rcardpos, double* Rbit2card, double* Rcard2bit, double* Rfactorials)

{
	// Returns 1 if yes, 0 if no;
    // v is a fuzzy measure in standard representation.
 //   unsigned int m;
//	int nn = log2int(n);
//Rprintf("%d  %d \n",n,nn);
	int_64 mm = (int_64)*m;
	card=Rcard;
 	cardpos=Rcardpos;
	bit2card = (int_64*)Rbit2card;
	card2bit = (int_64*)Rcard2bit;
	m_factorials=Rfactorials;

	result= IsMeasureSelfdual(v, mm);
//Rprintf("%d %d %d ",result,m,nn);
//Rprintf("%f %f %f %f\n",v[0],v[1],v[2],v[3]);
	
//	Cleanup_FM();
	return(result);
}	


int IsMeasureSubadditiveCall(double* v,  int& result,
	int* m, int* Rcard, int* Rcardpos, double* Rbit2card, double* Rcard2bit, double* Rfactorials)

{
	// Returns 1 if yes, 0 if no;
    // v is a fuzzy measure in standard representation.
  //  unsigned int m;
//	int nn = log2int(n);
	int_64 mm = (int_64)*m;
	card=Rcard;
 	cardpos=Rcardpos;
	bit2card = (int_64*)Rbit2card;
	card2bit = (int_64*)Rcard2bit;
	m_factorials=Rfactorials;

//	Preparations_FM(nn,&m);

	result= IsMeasureSubadditive(v, mm);
	
//	Cleanup_FM();
	return(result);
}	


int IsMeasureSubmodularCall(double* v,  int& result,
	int* m, int* Rcard, int* Rcardpos, double* Rbit2card, double* Rcard2bit, double* Rfactorials)

{
	// Returns 1 if yes, 0 if no;
    // v is a fuzzy measure in standard representation.
   // unsigned int m;
//	int nn = log2int(n);
	int_64 mm = (int_64)*m;
//	Preparations_FM(nn,&m);
	card=Rcard;
 	cardpos=Rcardpos;
	bit2card = (int_64*)Rbit2card;
	card2bit = (int_64*)Rcard2bit;
	m_factorials=Rfactorials;

	result= IsMeasureSubmodular(v, mm);
	
//	Cleanup_FM();
	return(result);
}	


int IsMeasureSuperadditiveCall(double* v,  int& result,
	int* m, int* Rcard, int* Rcardpos, double* Rbit2card, double* Rcard2bit, double* Rfactorials)

{
	// Returns 1 if yes, 0 if no;
    // v is a fuzzy measure in standard representation.
//    unsigned int m;
//	int nn = log2int(n);
	int_64 mm = (int_64)*m;
//	Preparations_FM(nn,&m);
	card=Rcard;
 	cardpos=Rcardpos;
	bit2card = (int_64*)Rbit2card;
	card2bit = (int_64*)Rcard2bit;
	m_factorials=Rfactorials;
	result= IsMeasureSuperadditive(v, mm);
	
//	Cleanup_FM();
	return(result);
}	


int IsMeasureSupermodularCall(double* v, int& result,
	int* m, int* Rcard, int* Rcardpos, double* Rbit2card, double* Rcard2bit, double* Rfactorials)
{
	// Returns 1 if yes, 0 if no;
    // v is a fuzzy measure in standard representation.
    //unsigned int m;
//	int nn = log2int(n);
	int_64 mm = (int_64)*m;
//	Preparations_FM(nn,&m);
	card=Rcard;
 	cardpos=Rcardpos;
	bit2card = (int_64*)Rbit2card;
	card2bit = (int_64*)Rcard2bit;
	m_factorials=Rfactorials;
	result= IsMeasureSupermodular(v, mm);
	
//	Cleanup_FM();
	return(result);
}	


int IsMeasureSymmetricCall(double* v,  int& result, 
	int* m, int* Rcard, int* Rcardpos, double* Rbit2card, double* Rcard2bit, double* Rfactorials)
{
	// Returns 1 if yes, 0 if no;
    // v is a fuzzy measure in standard representation.
    //unsigned int m;
	int nn = log2int(*m);
	int_64 mm = (int_64)*m;
//	Preparations_FM(nn,&m);

	card=Rcard;
 	cardpos=Rcardpos;
	bit2card = (int_64*)Rbit2card;
	card2bit = (int_64*)Rcard2bit;
	m_factorials=Rfactorials;

//Rprintf("%d %d %d %d %d %d\n", nn,*m, card[0], cardpos[1],bit2card[2], card2bit[2]);

	result=IsMeasureSymmetric(v, nn, mm);
	
//	Cleanup_FM();
	return(result);
}	

int IsMeasureKmaxitiveCall(double* v, int& result,
	int* m, int* Rcard, int* Rcardpos, double* Rbit2card, double* Rcard2bit, double* Rfactorials)

{
	// Returns 1 if yes, 0 if no;
	// v is a fuzzy measure in standard representation.
	// unsigned int m;
	int nn = log2int(*m);

	//	Preparations_FM(nn,&m);
	card = Rcard;
	cardpos = Rcardpos;
	bit2card = (int_64*)Rbit2card;
	card2bit = (int_64*)Rcard2bit;
	m_factorials = Rfactorials;

	result = IsMeasureKMaxitive(v, nn, (int_64)(*m));

	//	Cleanup_FM();
	return(result);
}



int IsMeasureAdditiveMobCall(double* Mob, int& result,
	int* m, int* Rcard, int* Rcardpos, double* Rbit2card, double* Rcard2bit, double* Rfactorials)
{
	// Returns 1 if yes, 0 if no;
	// Mob is a fuzzy measure in Mob representation.
	// todo : can certainly improve it by just checking Mobius as 0

	double* v = new double[*m];
	int nn = log2int(*m);
	ZetaCall(Mob, v, &nn, m, Rcard, Rcardpos, Rbit2card, Rcard2bit, Rfactorials);
	IsMeasureAdditiveCall( v, result, m, Rcard, Rcardpos, Rbit2card, Rcard2bit, Rfactorials);
	delete[] v;
	return(result);
}

int IsMeasureBalancedMobCall(double* Mob, int& result,
	int* m, int* Rcard, int* Rcardpos, double* Rbit2card, double* Rcard2bit, double* Rfactorials)
{
	// Returns 1 if yes, 0 if no;
	// Mob is a fuzzy measure in Mob representation.
	double* v = new double[*m];
	int nn = log2int(*m);
	ZetaCall(Mob, v, &nn, m, Rcard, Rcardpos, Rbit2card, Rcard2bit, Rfactorials);
	IsMeasureBalancedCall(v, result, m, Rcard, Rcardpos, Rbit2card, Rcard2bit, Rfactorials);
	delete[] v;
	return(result);
}
	int IsMeasureSelfdualMobCall(double* Mob, int& result,
		int* m, int* Rcard, int* Rcardpos, double* Rbit2card, double* Rcard2bit, double* Rfactorials)
	{
		// Returns 1 if yes, 0 if no;
		// Mob is a fuzzy measure in Mob representation.
		double* v = new double[*m];
		int nn = log2int(*m);
		ZetaCall(Mob, v, &nn, m, Rcard, Rcardpos, Rbit2card, Rcard2bit, Rfactorials);
		IsMeasureSelfdualCall(v, result, m, Rcard, Rcardpos, Rbit2card, Rcard2bit, Rfactorials);
		delete[] v;
		return(result);
	}

	int IsMeasureSubadditiveMobCall(double* Mob, int& result,
		int* m, int* Rcard, int* Rcardpos, double* Rbit2card, double* Rcard2bit, double* Rfactorials)
	{
		// Returns 1 if yes, 0 if no;
		// Mob is a fuzzy measure in Mob representation.
		double* v = new double[*m];
		int nn = log2int(*m);
		ZetaCall(Mob, v, &nn, m, Rcard, Rcardpos, Rbit2card, Rcard2bit, Rfactorials);
		IsMeasureSubadditiveCall(v, result, m, Rcard, Rcardpos, Rbit2card, Rcard2bit, Rfactorials);
		delete[] v;
		return(result);
	}

	int IsMeasureSubmodularMobCall(double* Mob, int& result,
		int* m, int* Rcard, int* Rcardpos, double* Rbit2card, double* Rcard2bit, double* Rfactorials)
	{
		// Returns 1 if yes, 0 if no;
		// Mob is a fuzzy measure in Mob representation.
		double* v = new double[*m];
		int nn = log2int(*m);
		ZetaCall(Mob, v, &nn, m, Rcard, Rcardpos, Rbit2card, Rcard2bit, Rfactorials);
		IsMeasureSubmodularCall(v, result, m, Rcard, Rcardpos, Rbit2card, Rcard2bit, Rfactorials);
		delete[] v;
		return(result);
	}
	int IsMeasureSuperadditiveMobCall(double* Mob, int& result,
		int* m, int* Rcard, int* Rcardpos, double* Rbit2card, double* Rcard2bit, double* Rfactorials)
	{
		// Returns 1 if yes, 0 if no;
		// Mob is a fuzzy measure in Mob representation.
		double* v = new double[*m];
		int nn = log2int(*m);
		ZetaCall(Mob, v, &nn, m, Rcard, Rcardpos, Rbit2card, Rcard2bit, Rfactorials);
		IsMeasureSuperadditiveCall(v, result, m, Rcard, Rcardpos, Rbit2card, Rcard2bit, Rfactorials);
		delete[] v;
		return(result);
	}
	int IsMeasureSupermodularMobCall(double* Mob, int& result,
		int* m, int* Rcard, int* Rcardpos, double* Rbit2card, double* Rcard2bit, double* Rfactorials)
	{
		// Returns 1 if yes, 0 if no;
		// Mob is a fuzzy measure in Mob representation.
		double* v = new double[*m];
		int nn = log2int(*m);
		ZetaCall(Mob, v, &nn, m, Rcard, Rcardpos, Rbit2card, Rcard2bit, Rfactorials);
		IsMeasureSupermodularCall(v, result, m, Rcard, Rcardpos, Rbit2card, Rcard2bit, Rfactorials);
		delete[] v;
		return(result);
	}
	int IsMeasureSymmetricMobCall(double* Mob, int& result,
		int* m, int* Rcard, int* Rcardpos, double* Rbit2card, double* Rcard2bit, double* Rfactorials)
	{
		// Returns 1 if yes, 0 if no;
		// Mob is a fuzzy measure in Mob representation.
		double* v = new double[*m];
		int nn = log2int(*m);
		ZetaCall(Mob, v, &nn, m, Rcard, Rcardpos, Rbit2card, Rcard2bit, Rfactorials);
		IsMeasureSymmetricCall(v, result, m, Rcard, Rcardpos, Rbit2card, Rcard2bit, Rfactorials);
		delete[] v;
		return(result);
	}
	int IsMeasureKmaxitiveMobCall(double* Mob, int& result,
		int* m, int* Rcard, int* Rcardpos, double* Rbit2card, double* Rcard2bit, double* Rfactorials)
	{
		// Returns 1 if yes, 0 if no;
		// Mob is a fuzzy measure in Mob representation.
		double* v = new double[*m];
		int nn = log2int(*m);
		ZetaCall(Mob, v, &nn, m, Rcard, Rcardpos, Rbit2card, Rcard2bit, Rfactorials);
		IsMeasureKmaxitiveCall(v, result, m, Rcard, Rcardpos, Rbit2card, Rcard2bit, Rfactorials);
		delete[] v;
		return(result);
	}


void MobiusCall(double* v, double* MobVal, int *n,
	int* m, int* Rcard, int* Rcardpos, double* Rbit2card, double* Rcard2bit, double* Rfactorials)

{
	card=Rcard;
 	cardpos=Rcardpos;
	bit2card = (int_64*)Rbit2card;
	card2bit = (int_64*)Rcard2bit;
	m_factorials=Rfactorials;
	Mobius(v, MobVal, *n, (int_64)(*m));
}


void OrnessChoquetMobCall(double* Mob, int *n, double& choMob,
	int* m, int* Rcard, int* Rcardpos, double* Rbit2card, double* Rcard2bit, double* Rfactorials)
{
	int_64 mm = (int_64)(*m);
	int nn = *n;

//	Preparations_FM(nn,&m);

	card=Rcard;
 	cardpos=Rcardpos;
	bit2card = (int_64*)Rbit2card;
	card2bit = (int_64*)Rcard2bit;
	m_factorials=Rfactorials;
    choMob = Orness(Mob, nn, mm);
//	Cleanup_FM();
}


void OWACall(double* x, double* v, int* n, double& owaval)
{
	int nn = *n;
	owaval  =  OWA(x,v,nn);
}


void ShapleyCall(double* v, double* x, int *n,
	int* m, int* Rcard, int* Rcardpos, double* Rbit2card, double* Rcard2bit, double* Rfactorials)
{
	int_64 mm = (int_64)(*m);
	int nn = *n;
//	Preparations_FM(nn,&m);

	card=Rcard;
 	cardpos=Rcardpos;
	bit2card = (int_64*)Rbit2card;
	card2bit = (int_64*)Rcard2bit;
	m_factorials=Rfactorials;
	Shapley(v, x,nn,mm);	
//	Cleanup_FM();
}


void SugenoCall(double* x, double* v, int* n, double& cho,
	int* m, int* Rcard, int* Rcardpos, double* Rbit2card, double* Rcard2bit, double* Rfactorials)

{
	int_64 mm = (int_64)(*m);
	int nn = *n;

	card=Rcard;
 	cardpos=Rcardpos;
	bit2card = (int_64*)Rbit2card;
	card2bit = (int_64*)Rcard2bit;
	m_factorials=Rfactorials;
	cho  = Sugeno(x, v, nn, mm);
}


  void WAMCall(double* x, double* v, int* n, double& wamval)
{
	int nn = *n;
	wamval  =  WAM(x,v,nn);
}





// this is a recursive procedure which helps build all subsets of a given cardinality, and 
// set up conversion arrays
void recursive_card(unsigned int* k, unsigned int level, unsigned int maxlevel, 
                                        unsigned int start, unsigned int finish,
										int_64* b2c, int_64* c2b, int_64 *s, int n)
{
	unsigned int i1;
        for(i1=start; i1 <= finish; i1++) { AddToSet(s,i1);
                if(level == maxlevel) {
                        b2c[*s]=*k;
                        c2b[*k]=*s;
                        (*k)++;
                } else {
                        recursive_card(k,level+1,maxlevel,i1+1,finish+1,b2c,c2b,s,n);
                }
                RemoveFromSet(s,i1);
        }
}
void main_card(unsigned int* k, unsigned int level, int_64* b2c, int_64* c2b, int n)
{
        // we recursively construct all subsets of cardinality "level"
	    int_64 s = 0;
        recursive_card(k,1,level,0, n-level, b2c,c2b, &s,n);
}

#ifdef __R
SEXP
#else
int 
#endif 

Preparations_FMCall(int* Rn, int* Rm, int* Rcard, int*  Rcardpos, double*  Rbit2card, double*  Rcard2bit, double* m_factorials)
{
        int i;
        unsigned int j;


		int   *cardpos;
		int_64 *bit2card, *card2bit;
int* card;
//	double*  m_factorials;
int n; int_64 m;
  n=*(Rn);
  m=(int_64)*(Rm);
  card=Rcard;
  cardpos=Rcardpos;
  bit2card=(int_64*)Rbit2card;
  card2bit=(int_64*)Rcard2bit;
  

//Rprintf("%d %d %d\n",n,m, card[1]);



   //     *m= 1<<(n);

    // calculate the array containing factorials of i! (faster than calculating them every time)
 //   m_factorials=new double[n+1];
        m_factorials[0]=1;
        for(i=1;i<=n;i++) m_factorials[i] = m_factorials[i-1]*i;

    // this array will contains cardinailities of subsets (coded as binaries), i.e. the number of bits in i.
    //    card=new int[(int) *m];
    //    cardpos=new int[n+1];


        card[0]=0; card[1]=0;
        for(j=1;j<m;j++) card[j] = cardf(j);

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

   //     bit2card=new unsigned int[*m];
   //     card2bit=new unsigned int[*m];

        unsigned int k; int l;
        bit2card[0]=card2bit[0]=0;

        cardpos[0]=1; // positions where singletons start, the 0th element is empyset

        k=1;
        for(l=1;l<=n-1;l++) {
                main_card(&k, l, bit2card, card2bit,  n);
                cardpos[l]=int(k);
        }
        cardpos[n]=cardpos[n-1]+1;
        
        bit2card[m-1]=card2bit[m-1]=m-1;
return 0;
}


#ifdef PYTHON_
/* Python interface call these two methods to allocate/deallocate memory */

LIBEXP void py_fm_init(int n, struct fm_env* env)
{
	env->n=n;
	int_64 m;
	m=env->m = ((int_64)1 << n);
	env->card=(int*) malloc(m*sizeof(int));
	env->cardpos=(int*) malloc((n+1)*sizeof(int));
	env->bit2card=(double* ) malloc((m)*sizeof(double));
	env->card2bit=(double* ) malloc((m)*sizeof(double));
	env->factorials=(double* ) malloc((n+1)*sizeof(double));
	
	Preparations_FMCall(&n,&(env->m),env->card,env->cardpos, env->bit2card, env->card2bit,env->factorials );

}
LIBEXP void py_fm_free( struct fm_env* env)
{
	free(env->card);
	free(env->cardpos);
	free(env->bit2card);
	free(env->card2bit);
	free(env->factorials);
	env->n=0;
	env->m=0;
}
LIBEXP void py_ExpandKinteractive2Bit(double* dest, double* src, struct fm_env* env, int kint, int arraysize) {

	 ExpandKinteractive2Bit( dest,  src, env-> n,env-> m,  kint,  arraysize);
	 
}
LIBEXP void py_ExpandKinteractive2Bit_m(double* dest, double* src, struct fm_env* env, int kint, int arraysize, double* VVC) {
	ExpandKinteractive2Bit_m( dest,  src, env-> n, env-> m,  kint,  arraysize,  VVC);
}
//inline?
LIBEXP void py_Banzhaf(double* v, double* B, struct fm_env* env)
{
    // Calculates an array of Banzhaf indices
	BanzhafCall(v, B, &(env->n), &(env->m), env->card, env->cardpos, env->bit2card, env->card2bit, env->factorials);
}

LIBEXP double py_Choquet(double* x, double* v,  struct fm_env* env)
{
    // Calculates Choquet integral	
	double c;
	ChoquetCall(x, v, &(env->n), c, &(env->m), env->card, env->cardpos, env->bit2card, env->card2bit, env->factorials);
	return c;
}

LIBEXP double py_ChoquetKinter(double* x, double* v, int kint, struct fm_env* env)
{
	// Calculates Choquet integral kinteractive	
	double c;
	ChoquetkinterCall(x, v, &(env->n), c, &kint, &(env->m),  env->card, env->cardpos, env->bit2card, env->card2bit, env->factorials);
	return c;
}

/*  Add here the rest of the C calls for all the functions */
LIBEXP double py_ChoquetMob(double* x, double* Mob, struct fm_env* env)
{
	// Calculates ChoquetMob integral
	double c;
	ChoquetMobCall(x, Mob, &(env->n), c, &(env->m), env->card, env->cardpos, env->bit2card, env->card2bit, env->factorials);
	return c;
}

LIBEXP void py_ConstructLambdaMeasure(double* singletons, double* lambda, double* v, struct fm_env* env)
{
	// Calculates an array of ConstructLambdaMeasure indices
	ConstructLambdaMeasureCall(singletons, lambda, v, (env->n), &(env->m), env->card, env->cardpos, env->bit2card, env->card2bit, env->factorials);
}
LIBEXP void py_ConstructLambdaMeasureMob(double* singletons, double* lambda, double* Mob, struct fm_env* env)
{
	// Calculates an array of ConstructLambdaMeasureMob indices
	ConstructLambdaMeasureMobCall(singletons, lambda, Mob, (env->n), &(env->m), env->card, env->cardpos, env->bit2card, env->card2bit, env->factorials);
}

LIBEXP void py_dualm(double* v, double* w, struct fm_env* env)
{
	// Calculates an array of dualm indices
	dualmCall(v, w, (env->n), &(env->m), env->card, env->cardpos, env->bit2card, env->card2bit, env->factorials);
}
LIBEXP void py_dualmMob(double* v, double* w, struct fm_env* env)
{
	// Calculates an array of dualm indices
	dualMobCall(v, w, (env->n), &(env->m), env->card, env->cardpos, env->bit2card, env->card2bit, env->factorials);
}

LIBEXP double py_Entropy(double* v, struct fm_env* env)
{
	// Calculates EntropyChoquet integral
	double c;
	EntropyChoquetCall(v, (env->n), c, &(env->m), env->card, env->cardpos, env->bit2card, env->card2bit, env->factorials);
	return c;
}

LIBEXP void py_FuzzyMeasureFit(int datanum, int additive, struct fm_env* env, double* v, double* dataset)
{
	// Calculates an array of FuzzyMeasureFitLP indices

	int opt = 128;
	double orness[2];
	orness[0] = 0;
	orness[1] = 1;
	int opt1=0;

	FuzzyMeasureFitLPCall(&(env->n), &datanum, &additive, v, dataset, &opt, NULL, NULL, &opt1, orness);
}

LIBEXP void py_FuzzyMeasureFitMob(int datanum, int additive, struct fm_env* env, double* v, double* dataset)
{
	// Calculates an array of FuzzyMeasureFitLP indices
		fittingCall(&(env->n), &datanum, &additive, v, dataset);
}	

LIBEXP void py_FuzzyMeasureFitKtolerant(int datanum, int additive, struct fm_env* env, double* v, double* dataset)
{
	// Calculates an array of FuzzyMeasureFitLPStandard indices
	fittingCallKtolerant(&(env->n), &datanum, &additive, v, dataset);
}

LIBEXP void py_FuzzyMeasureFitLPKmaxitive(int datanum, int additive, struct fm_env* env, double* v, double* dataset)
{
	// Calculates an array of FuzzyMeasureFitLP_relaxation indices
	fittingCallKmaxitive(&(env->n), &datanum, &additive, v, dataset);
}

LIBEXP void py_FuzzyMeasureFitLPKinteractive(int datanum, int additive, struct fm_env* env, double* v, double* dataset, double* K)
{
	// Calculates an array of FuzzyMeasureFitLPKinteractive indices
	fittingCallKinteractive(&(env->n), &datanum, &additive, v, dataset, K);
}

LIBEXP void py_FuzzyMeasureFitLPKinteractiveMaxChains(int datanum, int additive, struct fm_env* env, double* v, double* dataset, double* K)
{
	// Calculates an array of FuzzyMeasureFitLPKinteractiveMaxChains indices
	fittingCallKinteractiveMC(&(env->n), &datanum, &additive, v, dataset, K);
}

LIBEXP void py_FuzzyMeasureFitLPKinteractiveAutoK(int datanum, int additive, struct fm_env* env, double* v, double* dataset, double* K,int* maxiters )
{
	// Calculates an array of FuzzyMeasureFitLPKinteractiveAutoK indices
	fittingCallKinteractiveAuto(&(env->n), &datanum, &additive, v, dataset, K, maxiters);
}

LIBEXP void py_FuzzyMeasureFitLPKinteractiveMarginal(int datanum, int additive, struct fm_env* env, double* v, double* dataset, double* K , int submod)
{
	// Calculates an array of FuzzyMeasureFitLPKinteractiveMarginal indices
	fittingCallKinteractiveMarginal(&(env->n), &datanum, &additive, v, dataset, K, submod);
}

LIBEXP void py_FuzzyMeasureFitLPKinteractiveMarginalMaxChain(int datanum, int additive, struct fm_env* env, double* v, double* dataset, double* K, int* maxiters,int submod )
{
	// Calculates an array of FuzzyMeasureFitLPKinteractiveMarginalMaxChain indices
	fittingCallKinteractiveMarginalMC(&(env->n), &datanum, &additive, v, dataset, K, maxiters,submod);
}

LIBEXP void py_FuzzyMeasureFitLP(int datanum, int additive, struct fm_env* env, double* v, double* dataset, int * options, double* indexlow, double* indexhihg, int* option1, double* orness)
{
	//Calculates an array of FuzzyMeasureFitLP indices, in standard representation
	int opt = *options;
	opt |= 128;
	FuzzyMeasureFitLPCall(&(env->n), &datanum, &additive, v, dataset, &opt, indexlow, indexhihg, option1, orness);
	// converted to standard because of the flag set in options 

}
LIBEXP void py_FuzzyMeasureFitLPMob(int datanum, int additive, struct fm_env* env, double* v, double* dataset, int * options, double* indexlow, double* indexhihg, int* option1, double* orness)
{
	//Calculates an array of FuzzyMeasureFitLP indices
	FuzzyMeasureFitLPCall(&(env->n), &datanum, &additive, v, dataset, options, indexlow, indexhihg, option1, orness);
}

LIBEXP void py_fittingOWA(int datanum, struct fm_env* env, double* v, double* dataset)
{
	// Calculates an array of FuzzyMeasureFitLPsymmetric indices
	fittingOWACall(&(env->n), &datanum, v, dataset);
}

LIBEXP void py_fittingWAM(int datanum, struct fm_env* env, double* v, double* dataset)
{
	// Calculates an array of FuzzyMeasureFitLPsymmetric2 indices
	fittingWAMCall(&(env->n), &datanum, v, dataset);
}


LIBEXP void py_Interaction(double* v, double* w, struct fm_env* env)
{
	// Calculates an array of Interaction indices
	InteractionCall(v, w,  &(env->m), env->card, env->cardpos, env->bit2card, env->card2bit, env->factorials);
}

LIBEXP void py_InteractionMob(double* Mob, double* v, struct fm_env* env)
{
	// Calculates an array of InteractionMob indices
	InteractionMobCall(Mob, v, &(env->m), env->card, env->cardpos, env->bit2card, env->card2bit, env->factorials);
}

LIBEXP void py_InteractionB(double* v, double* w, struct fm_env* env)
{
	// Calculates an array of InteractionB indices
	InteractionBCall(v, w, &(env->m), env->card, env->cardpos, env->bit2card, env->card2bit, env->factorials);
}

LIBEXP void py_InteractionBMob(double* Mob, double* v, struct fm_env* env)
{
	// Calculates an array of InteractionBMob indices
	InteractionBMobCall(Mob, v, &(env->m), env->card, env->cardpos, env->bit2card, env->card2bit, env->factorials);
}

LIBEXP void py_BipartitionShapleyIndex(double* v, double* w, struct fm_env* env)
{
	// Calculates an array of BipartitionShapleyIndex indices
	BipartitionShapleyCall(v, w, &(env->n),  &(env->m), env->card, env->cardpos, env->bit2card, env->card2bit, env->factorials);
}

LIBEXP void py_BipartitionBanzhafIndex(double* v, double* w, struct fm_env* env)
{
	// Calculates an array of BipartitionBanzhafIndex indices
	BipartitionBanzhafCall(v, w, &(env->n), &(env->m), env->card, env->cardpos, env->bit2card, env->card2bit, env->factorials);
}

LIBEXP void py_BNonadditivityIndexMob(double* Mob, double* w, struct fm_env* env)
{
	// Calculates an array of NonadditivityIndexMob indices
	NonadditivityIndexMobCall(Mob, w, &(env->n),  &(env->m), env->card, env->cardpos, env->bit2card, env->card2bit, env->factorials);
}

LIBEXP void py_NonadditivityIndex(double* v, double* w, struct fm_env* env)
{
	// Calculates an array of NonadditivityIndex indices
	NonadditivityIndexCall(v, w, &(env->n), &(env->m), env->card, env->cardpos, env->bit2card, env->card2bit, env->factorials);
}

LIBEXP void py_NonmodularityIndex(double* v, double* w, struct fm_env* env)
{
	NonmodularityIndexCall(v, w, &(env->n), &(env->m), env->card, env->cardpos, env->bit2card, env->card2bit, env->factorials);
}

LIBEXP void py_NonmodularityIndexKinteractive(double* v, double* w, int kint,  struct fm_env* env)
{
	NonmodularityIndexKinteractiveCall(v, w, &(env->n), &kint, &(env->m), env->card, env->cardpos, env->bit2card, env->card2bit, env->factorials);
}

LIBEXP void py_NonmodularityIndexMob(double* Mob, double* w, struct fm_env*env)
{
	NonmodularityIndexMobCall(Mob, w, &(env->n), &(env->m), env->card, env->cardpos, env->bit2card, env->card2bit, env->factorials);
}

LIBEXP void py_NonmodularityIndexMobkadditive(double* Mob, double* w, int k,struct fm_env* env)
{
	NonmodularityIndexMobkadditiveCall(Mob, w, &(env->n), &k, &(env->m), env->card, env->cardpos, env->bit2card, env->card2bit, env->factorials);
}

LIBEXP void py_ShapleyMob(double* Mob, double* S, struct fm_env* env)
{
	ShapleyMobCall( Mob, S, &(env->n), &(env->m), env->card, env->cardpos, env->bit2card, env->card2bit, env->factorials);
}
LIBEXP void py_BanzhafMob(double* Mob, double* B, struct fm_env* env)
{
	BanzhafMobCall( Mob, B, &(env->n), &(env->m), env->card, env->cardpos, env->bit2card, env->card2bit, env->factorials);
}

LIBEXP void py_ShowCoalitions(int* coalition, struct fm_env* env)
{
	ShowCoalitionsCall(&(env->m), coalition);
}

LIBEXP void py_ShowCoalitionsCard( int* coalition, struct fm_env* env)
{
	ShowCoalitionsCardCall(&(env->m), coalition, env->card2bit);
}


/*end coalition check*/
/*----------------------------*/


LIBEXP int py_IsMeasureAdditive(double* v, struct fm_env* env)
{
	// Calculates IsMeasureAdditive
	int c;
	IsMeasureAdditiveCall(v, c, &(env->m), env->card, env->cardpos, env->bit2card, env->card2bit, env->factorials);
	return c;
}

LIBEXP int py_IsMeasureBalanced(double* v, struct fm_env* env)
{
	// Calculates IsMeasureBalanced
	int c;
	IsMeasureBalancedCall(v, c, &(env->m), env->card, env->cardpos, env->bit2card, env->card2bit, env->factorials);
	return c;
}

LIBEXP int py_IsMeasureSelfdual(double* v, struct fm_env* env)
{
	// Calculates IsMeasureSelfdual
	int c;
	IsMeasureSelfdualCall(v, c, &(env->m), env->card, env->cardpos, env->bit2card, env->card2bit, env->factorials);
	return c;
}

LIBEXP int py_IsMeasureSubadditive(double* v, struct fm_env* env)
{
	// Calculates IsMeasureSubadditive
	int c;
	IsMeasureSubadditiveCall(v, c, &(env->m), env->card, env->cardpos, env->bit2card, env->card2bit, env->factorials);
	return c;
}


LIBEXP int py_IsMeasureSubmodular(double* v, struct fm_env* env)
{
	// Calculates IsMeasureSubmodular
	int c;
	IsMeasureSubmodularCall(v, c, &(env->m), env->card, env->cardpos, env->bit2card, env->card2bit, env->factorials);
	return c;
}

LIBEXP int py_IsMeasureSuperadditive(double* v, struct fm_env* env)
{
	// Calculates IsMeasureSuperadditive
	int c;
	IsMeasureSuperadditiveCall(v, c, &(env->m), env->card, env->cardpos, env->bit2card, env->card2bit, env->factorials);
	return c;
}

LIBEXP int py_IsMeasureSupermodular(double* v, struct fm_env* env)
{
	// Calculates IsMeasureSupermodular
	int c;
	IsMeasureSupermodularCall(v, c, &(env->m), env->card, env->cardpos, env->bit2card, env->card2bit, env->factorials);
	return c;
}

LIBEXP int py_IsMeasureSymmetric(double* v, struct fm_env* env)
{
	// Calculates IsMeasureSymmetric
	int c;
	IsMeasureSymmetricCall(v, c, &(env->m), env->card, env->cardpos, env->bit2card, env->card2bit, env->factorials);
	return c;
}

LIBEXP int py_IsMeasureKMaxitive(double* v, struct fm_env* env)
{
	// Calculates IsMeasureKMaxitive
	int c;
	IsMeasureKmaxitiveCall(v, c, &(env->m), env->card, env->cardpos, env->bit2card, env->card2bit, env->factorials);
	return c;
}

LIBEXP int py_IsMeasureAdditiveMob(double* Mob, struct fm_env* env)
{
	// Calculates IsMeasureBalancedMob
	int c;
	IsMeasureAdditiveMobCall(Mob, c, &(env->m), env->card, env->cardpos, env->bit2card, env->card2bit, env->factorials);
	return c;
}

LIBEXP int py_IsMeasureBalancedMob(double* Mob, struct fm_env* env)
{
	// Calculates IsMeasureBalancedMob
	int c;
	IsMeasureBalancedMobCall(Mob, c, &(env->m), env->card, env->cardpos, env->bit2card, env->card2bit, env->factorials);
	return c;
}
LIBEXP int py_IsMeasureSelfdualMob(double* Mob, struct fm_env* env)
{
	// Calculates IsMeasureSelfdual
	int c;
	IsMeasureSelfdualMobCall(Mob, c, &(env->m), env->card, env->cardpos, env->bit2card, env->card2bit, env->factorials);
	return c;
}
LIBEXP int py_IsMeasureSubadditiveMob(double* v, struct fm_env* env)
{
	// Calculates IsMeasureSubadditiveMob
	int c;
	IsMeasureSubadditiveMobCall(v, c, &(env->m), env->card, env->cardpos, env->bit2card, env->card2bit, env->factorials);
	return c;
}
LIBEXP int py_IsMeasureSubmodularMob(double* Mob, struct fm_env* env)
{
	// Calculates IsMeasureSubmodularMob
	int c;
	IsMeasureSubmodularMobCall(Mob, c, &(env->m), env->card, env->cardpos, env->bit2card, env->card2bit, env->factorials);
	return c;
}
LIBEXP int py_IsMeasureSuperadditiveMob(double* Mob, struct fm_env* env)
{
	// Calculates IsMeasureSuperadditiveMob
	int c;
	IsMeasureSuperadditiveMobCall(Mob, c, &(env->m), env->card, env->cardpos, env->bit2card, env->card2bit, env->factorials);
	return c;
}

LIBEXP int py_IsMeasureSupermodularMob(double* Mob, struct fm_env* env)
{
	// Calculates IsMeasureSupermodularMob
	int c;
	IsMeasureSupermodularMobCall(Mob, c, &(env->m), env->card, env->cardpos, env->bit2card, env->card2bit, env->factorials);
	return c;
}
LIBEXP int py_IsMeasureSymmetricMob(double* Mob, struct fm_env* env)
{
	// Calculates IsMeasureSymmetricMob
	int c;
	IsMeasureSymmetricMobCall(Mob, c, &(env->m), env->card, env->cardpos, env->bit2card, env->card2bit, env->factorials);
	return c;
}
LIBEXP int py_IsMeasureKMaxitiveMob(double* Mob, struct fm_env* env)
{
	// Calculates IsMeasureKMaxitiveMob
	int c;
	IsMeasureKmaxitiveMobCall(Mob, c, &(env->m), env->card, env->cardpos, env->bit2card, env->card2bit, env->factorials);
	return c;
}


LIBEXP void py_Mobius(double* v, double* MobVal, struct fm_env* env)
{
	// Calculates an array of Mobius indices
	MobiusCall(v, MobVal, &(env->n), &(env->m), env->card, env->cardpos, env->bit2card, env->card2bit,env->factorials);
}

LIBEXP double py_Orness(double* Mob, struct fm_env* env)
{
	// Calculates OrnessChoquetMob
	double c;
	OrnessChoquetMobCall(Mob, &(env->n), c, &(env->m), env->card, env->cardpos, env->bit2card, env->card2bit, env->factorials);
	return c;
}

LIBEXP double py_OWA(double* x, double* v, struct fm_env* env)
{
	//Calculates OWA
	double c;
	OWACall(x, v, &(env->n), c);
	return c;
}

LIBEXP void py_Shapley(double* v, double* x, struct fm_env* env)
{
	// Calculates an array of Shapley indices
	ShapleyCall(v, x, &(env->n), &(env->m), env->card, env->cardpos, env->bit2card, env->card2bit,env->factorials);
}

LIBEXP double py_Sugeno(double* x, double* v, struct fm_env* env)
{
	// Calculates Sugeno
	double c;
	SugenoCall(x, v, &(env->n), c, &(env->m), env->card, env->cardpos, env->bit2card, env->card2bit,env->factorials);
	return c;
}

LIBEXP double py_WAM(double* x, double* v, struct fm_env* env)
{
	// Calculates WAM
	double c;
	WAMCall(x, v, &(env->n), c);
	return c;
}

LIBEXP void py_Zeta(double* Mob, double* v, struct fm_env* env)
{
	// Calculates an array of Zeta indices
	ZetaCall(Mob, v, &(env->n), &(env->m), env->card, env->cardpos, env->bit2card, env->card2bit,env->factorials);
}

#endif

/* duplicate??
void ExpandKinteractive2BitCall(double* dest, double* src, int* n, int_64* m, int* kint, int* arraysize, int* Rcard, int*  Rcardpos, double*  Rbit2card, double*  Rcard2bit, double* Rfactorials)

// converts compact k-interactive representation to full length binary ordering. 
{
	card = Rcard;
	cardpos = Rcardpos;
	bit2card = (int_64*)Rbit2card;
	card2bit = (int_64*)Rcard2bit;
	m_factorials = Rfactorials;
	ExpandKinteractive2Bit(dest,src, *n, *m, *kint, *arraysize);
}
*/

void dualMobKaddCall(int* m, int* length, int* k, double* src, double* dest, int* Rcard, int*  Rcardpos, double*  Rbit2card, double*  Rcard2bit, double* Rfactorials)
{
	card = Rcard;
	cardpos = Rcardpos;
	bit2card = (int_64*)Rbit2card;
	card2bit = (int_64*)Rcard2bit;
	m_factorials = Rfactorials;
	dualMobKadd(src, dest, *m, *length, *k );
}

void Shapley2addMobCall(double* v, double* x, int* n)
// calculates the array x of Shapley values for 2 additive fm in compact representation (cardinality based)
{
	Shapley2addMob(v, x, *n);
}

void Banzhaf2addMobCall(double* v, double* x, int *n)
// calculates the array x of Banzhaf indices for 2 additive fm in compact representation (cardinality based)
{
	Banzhaf2addMob( v,  x, *n);
}

void Choquet2addMobCall(double* v, double* x, double* out, int *n)
// calculates the array x of Banzhaf indices for 2 additive fm in compact representation (cardinality based)
{
	*out= Choquet2add(x, v, *n);// Note it is x,v in that order here
}
int fm_arraysizeCall(int* n, int_64* m, int* kint,  double* Rfactorials)
// calculates the size of the array to store one k-interctive fuzzy measure
{
	m_factorials = Rfactorials;
	int_64 m1=*m;
	return fm_arraysize(*n, m1, *kint);
}

void fm_arraysizeCallR(int* n, int* m, int* kint, int* out, double* Rfactorials)
// calculates the size of the array to store one k-interctive fuzzy measure
{
	m_factorials = Rfactorials;
	int_64 m1=*m;
	*out= fm_arraysize(*n, m1, *kint);
}

// generate fuzzy measures randomly using topological sort
int generate_fm_tsortCall(int_64* num, int* n, int* kint, int* markov, int* option, double* K, double * vv, int* Rcard, int*  Rcardpos, double*  Rbit2card, double*  Rcard2bit, double* Rfactorials)
{
    card = Rcard;
    cardpos = Rcardpos;
    bit2card = (int_64*)Rbit2card;
    card2bit = (int_64*)Rcard2bit;
    m_factorials = Rfactorials;
    return generate_fm_tsort(*num, *n, *kint, *markov, *option, *K, vv);
}



// generate convex (supermodular)  fuzzy measures randomly using topological sort
int generate_fmconvex_tsortCall(int_64* num, int* n, int* kint, int* markov, int* option, double* K, double * vv, int* Rcard, int*  Rcardpos, double*  Rbit2card, double*  Rcard2bit, double* Rfactorials)
{
    card = Rcard;
    cardpos = Rcardpos;
    bit2card = (int_64*)Rbit2card;
    card2bit = (int_64*)Rcard2bit;
    m_factorials = Rfactorials;
    int opt = (*option) | 8; // means we do rejections inside for 1000 steps
    return generate_fmconvex_tsort(*num, *n, *kint, *markov, opt, *K,  vv);
}

// generate fuzzy measures randomly using MinimalsPlus method
int generate_fm_minplusCall(int_64* num, int* n, int* kint, int* markov, int* option, double* K, double * vv, int* Rcard, int*  Rcardpos, double*  Rbit2card, double*  Rcard2bit, double* Rfactorials)
{
    card = Rcard;
    cardpos = Rcardpos;
    bit2card = (int_64*)Rbit2card;
    card2bit = (int_64*)Rcard2bit;
    m_factorials = Rfactorials;
    return generate_fm_minplus(*num, *n, *kint, *markov, *option, *K, vv);
}

// generate simple 2 additive supermodular (convex) and submodular capacities
// size is the returned size of each vector in compact representation (singletons and pairs only
int generate_fm_2additive_convexCall(int_64* num, int* n, int * size, double * vv)
{
    return  generate_fm_2additive_convex(*num, *n,  size,  vv);
}

int generate_fm_2additive_concaveCall(int_64* num, int* n, int * size, double * vv)
{
    return  generate_fm_2additive_concave(*num, *n, size, vv);
}

int generate_fm_2additive_convex_withsomeindependentCall(int_64* num, int* n, int * size, double * vv)
// as above, but resets randomly some interactions to 0
{
    return generate_fm_2additive_convex_withsomeindependent(*num, *n, size, vv);
}



#ifdef NH_USED_IN_R_INTERFACE 

// generate fuzzy measures randomly using topological sort
void generate_fm_tsortCall(int* num1, int* n, int* kint, int* markov, int* option, double* K, double * vv, int* Rcard, int*  Rcardpos, double*  Rbit2card, double*  Rcard2bit, double* Rfactorials)
{
	card = Rcard;
	cardpos = Rcardpos;
	bit2card = (int_64*)Rbit2card;
	card2bit = (int_64*)Rcard2bit;
	m_factorials = Rfactorials;
	int_64 num=*num1;
	 generate_fm_tsort(num, *n, *kint, *markov, *option, *K, vv);
}



// generate convex (supermodular)  fuzzy measures randomly using topological sort
void generate_fmconvex_tsortCall(int* num1, int* n, int* kint, int* markov, int* option, double* K, double * vv, int* Rcard, int*  Rcardpos, double*  Rbit2card, double*  Rcard2bit, double* Rfactorials)
{
	card = Rcard;
	cardpos = Rcardpos;
	bit2card = (int_64*)Rbit2card;
	card2bit = (int_64*)Rcard2bit;
	m_factorials = Rfactorials;
	int opt = (*option) | 8; // means we do rejections inside for 1000 steps
		int_64 num=*num1;
	 generate_fmconvex_tsort(num, *n, *kint, *markov, opt, *K,  vv);
}

// generate fuzzy measures randomly using MinimalsPlus method
void generate_fm_minplusCall(int* num1, int* n, int* kint, int* markov, int* option, double* K, double * vv, int* Rcard, int*  Rcardpos, double*  Rbit2card, double*  Rcard2bit, double* Rfactorials)
{
	card = Rcard;
	cardpos = Rcardpos;
	bit2card = (int_64*)Rbit2card;
	card2bit = (int_64*)Rcard2bit;
	m_factorials = Rfactorials;
	int_64 num=*num1;
	 generate_fm_minplus(num, *n, *kint, *markov, *option, *K, vv);
}

// generate simple 2 additive supermodular (convex) and submodular capacities
// size is the returned size of each vector in compact representation (singletons and pairs only
void generate_fm_2additive_convexCall(int* num1, int* n, int * size, double * vv)
{
			int_64 num=*num1;
	  generate_fm_2additive_convex(num, *n,  size,  vv);
}

void generate_fm_2additive_concaveCall(int* num1, int* n, int * size, double * vv)
{
			int_64 num=*num1;
	  generate_fm_2additive_concave(num, *n, size, vv);
}

void generate_fm_2additive_convex_withsomeindependentCall(int* num1, int* n, int * size, double * vv)
// as above, but resets randomly some interactions to 0
{
			int_64 num=*num1;
	 generate_fm_2additive_convex_withsomeindependent(num, *n, size, vv);
}

#endif // NH_USED_IN_R_INTERFACE

void export_maximal_chainsCall(int* n,  double * v, double * mc, double* Rfactorials)
{
	m_factorials = Rfactorials;
	int_64 m = (int_64)1 << (*n);
	export_maximal_chains(*n, m, v, mc);
}
void export_maximal_chainsCall1(int* n, int_64* m, double * v, double * mc, double* Rfactorials)
{
	m_factorials = Rfactorials;
	export_maximal_chains(*n, *m, v, mc);
}


#ifdef PYTHON_

// python wrapper
LIBEXP void py_export_maximal_chains(int n, double* v, double* mc, struct fm_env* env)
{
	int_64 m = (int_64)1 << (n);
	export_maximal_chainsCall1(&n, &m, v, mc, env->factorials);
}

LIBEXP void py_dualMobKadd(int m, int length, int k, double* src, double* dest, struct fm_env* env)
{
	dualMobKaddCall(&m, &length, &k, src,dest, env->card, env->cardpos, env->bit2card, env->card2bit, env->factorials);
}
LIBEXP void py_Shapley2addMob(double* v, double* x, int n)
{
	Shapley2addMobCall(v, x, &n);
}
LIBEXP void py_Banzhaf2addMob(double* v, double* x, int n)
{
	Banzhaf2addMobCall(v, x, &n);
}

LIBEXP double py_Choquet2addMob(double*x, double* Mob, int n) {
	return Choquet2add(x, Mob, n);
}


LIBEXP int py_fm_arraysize(int n, int kint, struct fm_env* env)
{
	int_64 m = (int_64)1 << (n);
	return fm_arraysizeCall(&n, &m, &kint, env->factorials);
}

LIBEXP int py_generate_fm_tsort(int num, int n, int kint, int markov, int option, double K, double * vv, struct fm_env* env)
{
	int_64 num1 = num;
	// NH: change num to num1 in parameter list
	generate_fm_tsortCall(&num1, &n, &kint, &markov, &option, &K, vv, env->card, env->cardpos, env->bit2card, env->card2bit, env->factorials);
	return num;
}

LIBEXP int py_generate_fmconvex_tsort(int num, int n, int kint, int markov, int option, double K, double * vv, struct fm_env* env)
{
	int_64 num1 = num;
	// NH: change num to num1 in parameter list
	return generate_fmconvex_tsortCall(&num1, &n, &kint, &markov, &option, &K, vv, env->card, env->cardpos, env->bit2card, env->card2bit, env->factorials);
}
LIBEXP int py_generate_fm_minplus(int num, int n, int kint, int markov, int option, double K, double * vv, struct fm_env* env)
{
	int_64 num1 = num;
	// NH: change num to num1 in parameter list
	return generate_fm_minplusCall(&num1, &n, &kint, &markov, &option, &K, vv, env->card, env->cardpos, env->bit2card, env->card2bit, env->factorials);
}

LIBEXP int py_generate_fm_2additive_convex(int num, int n,  double * vv)
{
	int_64 num1 = num;
	int size;
	// NH: change num to num1 in parameter list
	generate_fm_2additive_convexCall(&num1, &n, &size, vv);
	return size;
}

LIBEXP int py_generate_fm_2additive_concave(int num, int n, double * vv)
{
	int_64 num1 = num;
	int size;
	// NH: change num to num1 in parameter list
	generate_fm_2additive_concaveCall(&num1, &n, &size, vv);
	return size;
}

LIBEXP int py_generate_fm_2additive_convex_withsomeindependent(int num, int n,  double * vv)
{
	int_64 num1 = num;
	int size;
	// NH: change num to num1 in parameter list
	generate_fm_2additive_convex_withsomeindependentCall(&num1, &n, &size, vv);
	return size;
}


/*
Sparse representation of k-additive capacities. Thre representation is in the form of singletons, pairs and tuples with nonzero values, stored and indexed in the respective
arrays (see above in this file)

 Prepares an empty structure, given the list of cardinalities of the nonzero tuples (cardinality, tuple composition) like this 2 pairs 4-tuple and a triple:  (2,1,2,  2, 3,1,   4, 1,2,3,4,  3,3,2,1...)

 It is used to allocate storage and later populate these values
*/
LIBEXP void py_prepare_fm_sparse( int n, int tupsize, int* tuples, struct fm_env_sparse* env)
{
	 Prepare_FM_sparse0(n, tupsize, tuples, (SparseFM*)env);
}
LIBEXP void py_free_fm_sparse(struct fm_env_sparse* env) {
	Free_FM_sparse((SparseFM*)env);
}

/*  Returns the cardinality of the tuple numbered i in the list of tuples */
LIBEXP int py_tuple_cardinality_sparse(int i, struct fm_env_sparse* env)
{
	return TupleCardinalitySparse(i, (SparseFM*)env);
}

LIBEXP int py_get_num_tuples(struct fm_env_sparse* env)
{
	return GetNumTuples((SparseFM*)env);
}
LIBEXP int py_get_sizearray_tuples(struct fm_env_sparse* env)
{
	return GetSizeArrayTuples((SparseFM*)env);
}

/* checks if element i (1-based!!!) belongs to the tuple indexed A (whose cardinality can be 1,2, other (automatically determined) */
LIBEXP int py_is_inset_sparse(int A, int card, int i, struct fm_env_sparse* env) 
{
	return IsInSetSparse(A, card, i, (SparseFM*)env);
}
/* checks if tuple B is a subset of A */
LIBEXP int py_is_subset_sparse(int A, int cardA, int B, int cardB, struct fm_env_sparse* env)
{
	return IsSubsetSparse(A, cardA, B, cardB, (SparseFM*)env);
}

/* calculates minimum (maximum) of (x_i) with the indices belonging to tuple indexed as S (its cardinality cardS can be 1,2, other( put 3, will be determined automatically)
note that x is 0-based, tuples are 1-based */
LIBEXP double py_min_subset_sparse(double* x, int n, int S, int cardS, struct fm_env_sparse* env)
{
	return min_subsetSparse(x, n, S, cardS, (SparseFM*)env);
}

LIBEXP double py_max_subset_sparse(double* x, int n, int S, int cardS, struct fm_env_sparse* env)
{
	return max_subsetSparse(x, n, S, cardS, (SparseFM*)env);
}

/* calculates the Choquet integral in Mobius representation */
LIBEXP double py_ChoquetMob_sparse(double* x, int n, struct fm_env_sparse* env)
{
	return ChoquetMobSparse(x, n, (SparseFM*)env);
}

/* Shapley and Banzhaf values vector of a capacity */
LIBEXP void py_ShapleyMob_sparse(double* v, int n, struct fm_env_sparse* env)
{
	ShapleyMobSparse(v, n, (SparseFM*)env);
}
LIBEXP void py_BanzhafMob_sparse(double* v, int n, struct fm_env_sparse* env)
{
	BanzhafMobSparse(v, n, (SparseFM*)env);
}


/* populates 2-additive sparse capacity with nonzero values using the singletons and two arrays of indices (of size numpairs) . Indices need to be 1-based. Singletons 0-based */
LIBEXP void py_populate_fm_2add_sparse(double* singletons, int numpairs, double* pairs, int* indicesp1, int* indicesp2, struct fm_env_sparse* env)
{
	PopulateFM2Add_Sparse(singletons, numpairs, pairs, indicesp1, indicesp2, (SparseFM*)env);
}

/* for populating capacities. Add pair (v_ij) to the structure. indices are 1-based */
LIBEXP void py_add_pair_sparse(int i, int j, double v, struct fm_env_sparse* env)
{
	double u = v;  // in case of types incompatiblity
	AddPairSparse(i, j, &u, (SparseFM*)env);
}


/* for populating capacities, adds a tuple of size tupsize whose 1-based indices are in tuple */
LIBEXP void py_add_tuple_sparse(int tupsize, int* tuple, double v, struct fm_env_sparse* env)
{
	double u = v;
	AddTupleSparse(tupsize, tuple, &u, (SparseFM*)env);
}


/* Given 2-additive capacity singletons=pairs in one array v , selects nonzero pairs */
LIBEXP void py_populate_fm_2add_sparse_from2add(int n, double * v, struct fm_env_sparse* env)
{
	PopulateFM2Add_Sparse_from2add(n,v, (SparseFM*)env);
}


/* from sparse to full representaiotn of 2-additive capacity (singletons and paits, augmented with 0 ) Vector v has to be allocated, size is n+ n(n-1)/2 */
LIBEXP void py_expand_2add_full(double* v, struct fm_env_sparse* env)
{
	 Expand2AddFull(v, (SparseFM*)env);
}


/* from sparse to full capacity (vector v, size 2^n has to be preallocated) */
LIBEXP void py_expand_sparse_full(double* v, struct fm_env_sparse* env)
{
	ExpandSparseFull(v, (SparseFM*)env);
}

LIBEXP void py_sparse_get_singletons(int n, double* v, struct fm_env_sparse* env) 
{ 
	ExportSparseSingletons(n, v, (SparseFM*)env); 
}

LIBEXP int py_sparse_get_pairs(int* pairs, double* v, struct fm_env_sparse* env)
{
	return ExportSparsePairs(pairs, v, (SparseFM*)env);
}

LIBEXP int py_sparse_get_tuples(int* tuples, double* v, struct fm_env_sparse* env)
{
	return ExportSparseTuples(tuples, v, (SparseFM*)env);
}


/* random generation of  sparse supermodular capacities */
LIBEXP int   py_generate_fm_2additive_convex_sparse(int n, struct fm_env_sparse* env)
{
	return generate_fm_2additive_convex_sparse(n, (SparseFM*)env);
}

LIBEXP int   py_generate_fm_kadditive_convex_sparse(int n, int k, int nonzero, struct fm_env_sparse* env)
{
	return generate_fm_kadditive_convex_sparse(n, k, nonzero, (SparseFM*)env);
}


LIBEXP void py_Nonmodularityindex_sparse( double* w, int n, struct fm_env_sparse* env)
{
	 int_64 m = (int_64)1 << n;
	 NonmodularityIndexMobSparse(w, n, m, (SparseFM*)env);
}

#endif


//}  // end extern "C"




void copycontent(struct SparseFM* env, double* singletons, double* pairs, double* tuples, int* pairsidx, int* tuplesidx, int* tuplescon, int* dims)
{
	dims[0]=env->m_pairs.size();
	dims[1]=env->m_tuples.size();
	dims[2]=env->m_tuple_start.size();
	dims[3]=env->m_tuple_content.size();	
	
	for(int i=0;i<env->n;++i) singletons[i]=env->m_singletons[i];
		for(int i=0;i<dims[0];++i) pairs[i]=env->m_pairs[i];
		for(int i=0;i<dims[1];++i) tuples[i]=env->m_tuples[i];	
		for(int i=0;i<dims[0]*2;++i) pairsidx[i]=env->m_pair_index[i];	
		for(int i=0;i<dims[2];++i) tuplesidx[i]=env->m_tuple_start[i];	
		for(int i=0;i<dims[3];++i) tuplescon[i]=env->m_tuple_content[i];		
}
 

 void populateenv(struct SparseFM* env, int* n,
     double* singletons, double* pairs, double* tuples, int* pairsidx, int* tuplesidx, int* tuplescon, int* dims)
 { // copies the arrays to vector<>, only the required part in dim, so vectors lengths are correct
	 env->n=*n;
	env->m_singletons.assign(singletons, singletons+ *n);
	env->m_pairs.assign(pairs,pairs+dims[0]);
	env->m_tuples.assign(tuples,tuples+dims[1]);

	env->m_pair_index.assign(pairsidx,pairsidx+dims[0]*2);// goes in pairs, hence  m_pair_index[2i],m_pair_index[2i+1] corresponds to m_pairs[i];

	env->m_tuple_start.assign(tuplesidx,tuplesidx+dims[2]); // pints to cardinality, list of elements, stored  in m_tuple_content
	env->m_tuple_content.assign(tuplescon,tuplescon+dims[3]); 
 }
 
  void populateenvConst(volatile struct SparseFM* env, int* n,
     double* singletons, double* pairs, double* tuples, int* pairsidx, int* tuplesidx, int* tuplescon, int* dims)
 {
	 env->n=*n;
// GB temporary fix for tests
	 
//	 populateenv((struct SparseFM*) env,  n,  singletons,  pairs,  tuples,  pairsidx,  tuplesidx,  tuplescon,  dims);
//	 return;
	 
	 wrapArrayInVector(singletons,*n, env->m_singletons);
	 wrapArrayInVector(pairs, dims[0], env->m_pairs);
	 wrapArrayInVector(tuples, dims[1], env->m_tuples );
	 wrapArrayInVector(pairsidx, dims[0]*2, env->m_pair_index);
	 wrapArrayInVector(tuplesidx,dims[2], env->m_tuple_start);
	 wrapArrayInVector(tuplescon,dims[3], env->m_tuple_content);	 
 }
 
 void releaseenv(volatile struct SparseFM* env) // should be called after populateenvConst to avoid freeing memory
 {  
 //return;
 
	releaseVectorWrapper( env->m_singletons );
	releaseVectorWrapper( env->m_pairs );
	releaseVectorWrapper( env->m_tuples );
	releaseVectorWrapper( env->m_pair_index );
	releaseVectorWrapper( env->m_tuple_start );
 	releaseVectorWrapper( env->m_tuple_content );
 }

 
 

 


#ifdef __R
#include <R_ext/Rdynload.h>    
#include <R_ext/Visibility.h>

#include <Rdefines.h>

/*
static void _finalizer(SEXP ext)
{
	struct SparseFM *ptr = (struct SparseFM*) R_ExternalPtrAddr(ext);
//	Free_FM_sparse(ptr);
//	Free(ptr);
}

SEXP create()
{
	struct SparseFM *envsp =new(struct SparseFM );
	
	envsp->n = 0;

//	SEXP ext = PROTECT(R_MakeExternalPtr(envsp, mkString("My ext pointer"), R_NilValue ));//
//	R_RegisterCFinalizerEx(ext, _finalizer, TRUE);
	
//	R_PreserveObject(ext);
//	MARK_NOT_MUTABLE(ext);
//	UNPROTECT(1);
//	Rprintf("setaddr %x %x\n",envsp ,ext );
	SEXP ext;
	return ext;
}

*/
//SEXP
void* GetEnvAddr(SEXP ext)
{
	//struct SparseFM *envsp = (struct SparseFM*) R_ExternalPtrAddr(ext);
	void* envsp = (void*) (R_ExternalPtrAddr(ext));

	return (void*) envsp;
}



 
 
 
 
void Prepare_FM_sparseCall(int*   n, int* tupsz, double* tup, int*  tupidx,
double* singletons, double* pairs, double* tuples, int* pairsidx, int* tuplesidx, int* tuplescon, int* dims 
)
{
	struct SparseFM env;
//Rprintf("tups %d %d %d\n", *tupsz, tupidx[0], tupidx[3]);
	Prepare_FM_sparse(*n, *tupsz, tup, tupidx, &env);
	
	// pass the content
	copycontent(&env, singletons, pairs, tuples, pairsidx,tuplesidx,tuplescon,dims);
	
	
	// not ready yet, check passing structiores in R, managing memory in C
//Rprintf("getaddr %x %x\n",env,env->m_pairs);
//	Rprintf("adds n %d %d\n",env->n, n1);

	Free_FM_sparse(&env);
}

//void Prepare_FM_sparseCall(int* n, int* tupsize, int* ntuples, SEXP envsp)
void Prepare_FM_sparseCallold(SEXP  n, SEXP  tupsize, SEXP  ntuples, SEXP envsp)
{
//SEXP ext = PROTECT(R_MakeExternalPtr(envsp, R_NilValue, R_NilValue));
	struct SparseFM* env = (struct SparseFM*)GetEnvAddr(PROTECT(envsp));

//Rprintf("%u %u %x %x\n",asInteger(n), asInteger(tupsize), (env),envsp);
	int n1=Rf_asInteger(n);
	env->n=n1;
	
//	Prepare_FM_sparse(n1, 0, NULL, env);
	// not ready yet, check passing structiores in R, managing memory in C
//Rprintf("getaddr %x %x\n",env,env->m_pairs);
//	Rprintf("adds n %d %d\n",env->n, n1);

 UNPROTECT(1);
}

void Free_FM_sparseCall(SEXP envsp)
{
	struct SparseFM* env = (struct SparseFM*)GetEnvAddr(PROTECT((envsp)));
	Free_FM_sparse(env);

	UNPROTECT(1);
}



void Nonmodularityindex_sparseCall(double* val, int* n,
     double* singletons, double* pairs, double* tuples, int* pairsidx, int* tuplesidx, int* tuplescon, int* dims)
{
	struct SparseFM env;
	populateenvConst(&env, n, singletons,  pairs,  tuples,  pairsidx,  tuplesidx,  tuplescon,  dims);
	int_64 m= (int_64)1<<(env.n);
	NonmodularityIndexMobSparse(val, env.n,  m, &env);
	releaseenv(&env);
/*	
	struct SparseFM* env = (struct SparseFM*)GetEnvAddr(PROTECT((envsp)));
	double* valp=NUMERIC_POINTER(PROTECT(val));

	int_64 m= (int_64)1<<(env->n);
		 Rprintf("getaddr %x %x %x\n",env,env->m_pairs, valp);
		  Rprintf("getaddr %x %x %x\n",env->m_pairs, env->n,m);
	NonmodularityIndexMobSparse(valp, env->n,  m, (SparseFM*)env);
		 Rprintf("getaddr %x %x %x\n",env,env->m_pairs, env->m_pairs.size());
	UNPROTECT(2);	
*/	
}
void generate_fm_kadditive_convex_sparseCall(int* n, int* kadd, int* nonzero, int* out,
     double* singletons, double* pairs, double* tuples, int* pairsidx, int* tuplesidx, int* tuplescon, int* dims) 
{
	struct SparseFM env;
	populateenv(&env, n, singletons,  pairs,  tuples,  pairsidx,  tuplesidx,  tuplescon,  dims);
	*out=generate_fm_kadditive_convex_sparse(*n, *kadd, *nonzero, &env);
	copycontent(&env, singletons, pairs, tuples, pairsidx,tuplesidx,tuplescon,dims);
}

void generate_fm_2additive_convex_sparseCall(int* n,  int* out, 
     double* singletons, double* pairs, double* tuples, int* pairsidx, int* tuplesidx, int* tuplescon, int* dims) 
{
	struct SparseFM env;
	populateenv(&env, n, singletons,  pairs,  tuples,  pairsidx,  tuplesidx,  tuplescon,  dims);
	*out=generate_fm_2additive_convex_sparse(*n, &env);
	copycontent(&env,  singletons, pairs, tuples, pairsidx,tuplesidx,tuplescon,dims);
}
void sparse_get_tuplesCall(int* outidx, double* out, int* sz,  int* n,
     double* singletons, double* pairs, double* tuples, int* pairsidx, int* tuplesidx, int* tuplescon, int* dims) 
{
	
	volatile struct SparseFM env;
	populateenvConst(&env, n, singletons,  pairs,  tuples,  pairsidx,  tuplesidx,  tuplescon,  dims);

	sz[0]=ExportSparseTuples(outidx, out, (struct SparseFM *) &env);
	releaseenv(&env);	
}

void sparse_get_pairsCall(int* outidx, double* out, int* sz,  int* n,
     double* singletons, double* pairs, double* tuples, int* pairsidx, int* tuplesidx, int* tuplescon, int* dims) 
{
	volatile struct SparseFM env;
	populateenvConst(&env, n, singletons,  pairs,  tuples,  pairsidx,  tuplesidx,  tuplescon,  dims);

	sz[0]=ExportSparsePairs(outidx, out, (struct SparseFM *)&env);
	releaseenv(&env);

}

void sparse_get_singletonsCall( double* v,  int* n,
     double* singletons, double* pairs, double* tuples, int* pairsidx, int* tuplesidx, int* tuplescon, int* dims) 
{	for(int i=0;i<*n; i++) v[i]=singletons[i]; }

void expand_sparse_fullCall( double* v,  int* n,
     double* singletons, double* pairs, double* tuples, int* pairsidx, int* tuplesidx, int* tuplescon, int* dims) 
{
	volatile struct SparseFM env;
	populateenvConst(&env, n, singletons,  pairs,  tuples,  pairsidx,  tuplesidx,  tuplescon,  dims);

	ExpandSparseFull(v, (struct SparseFM *)&env);
	releaseenv(&env);	
}

void expand_2add_fullCall(double* v,  int* n,
     double* singletons, double* pairs, double* tuples, int* pairsidx, int* tuplesidx, int* tuplescon, int* dims) // expnds sparse into 2add
{
	volatile struct SparseFM env;
	populateenvConst(&env, n, singletons,  pairs,  tuples,  pairsidx,  tuplesidx,  tuplescon,  dims);

	Expand2AddFull(v, (struct SparseFM *)&env);
	releaseenv(&env);
}

void populate_fm_2add_sparse_from2addCall( int* n, double* v, 
     double* singletons, double* pairs, double* tuples, int* pairsidx, int* tuplesidx, int* tuplescon, int* dims)
{
	struct SparseFM env;
	struct SparseFM * cap = &env;
	populateenv(&env, n, singletons,  pairs,  tuples,  pairsidx,  tuplesidx,  tuplescon,  dims);
	
	cap->m_singletons.resize(*n);
	cap->m_pairs.clear();
	cap->m_pair_index.clear();
	cap->m_tuple_content.clear();
	cap->m_tuple_start.clear();
	cap->m_tuples.clear();
	
	PopulateFM2Add_Sparse_from2add(*n, v, &env);
// copy back, updated dims
	copycontent(&env,  singletons, pairs, tuples, pairsidx,tuplesidx,tuplescon,dims);
}

void populate_fm_2add_sparseCall(double* nsingletons, int* np, double* npairs, int* idx1, int* idx2,
	int* n,  
     double* singletons, double* pairs, double* tuples, int* pairsidx, int* tuplesidx, int* tuplescon, int* dims)
{
	struct SparseFM env;
	populateenv(&env, n, singletons,  pairs,  tuples,  pairsidx,  tuplesidx,  tuplescon,  dims);
	PopulateFM2Add_Sparse(nsingletons, *np, npairs, idx1, idx2,  &env);
	copycontent(&env,  singletons, pairs, tuples, pairsidx,tuplesidx,tuplescon,dims);	
}



void add_pair_sparseCall(int* i, int* j, double* v,  int* n,
     double* singletons, double* pairs, double* tuples, int* pairsidx, int* tuplesidx, int* tuplescon, int* dims)
{
	
	struct SparseFM env;
	populateenv(&env, n, singletons,  pairs,  tuples,  pairsidx,  tuplesidx,  tuplescon,  dims);
	AddPairSparse(*i,*j, v, &env);
// copy back, updated dims
	copycontent(&env,  singletons, pairs, tuples, pairsidx,tuplesidx,tuplescon,dims);
}


void add_tuple_sparseCall(int* i, int* jp, double* v,  int* n,
     double* singletons, double* pairs, double* tuples, int* pairsidx, int* tuplesidx, int* tuplescon, int* dims)
{
	struct SparseFM env;
	populateenv(&env, n, singletons,  pairs,  tuples,  pairsidx,  tuplesidx,  tuplescon,  dims);
	AddTupleSparse(*i,jp, v, &env);
// copy back
	copycontent(&env,  singletons, pairs, tuples, pairsidx,tuplesidx,tuplescon,dims);
}

void add_singletons_sparseCall( double* v,  int* n, double* singletons)
 { // here all is simple, singletons preallocated
	for(int i=0;i<*n;i++) singletons[i]=v[i];
}



void BanzhafMob_sparseCall(double* val, int* n,
     double* singletons, double* pairs, double* tuples, int* pairsidx, int* tuplesidx, int* tuplescon, int* dims)
{
	volatile struct SparseFM env;
	populateenvConst(&env, n, singletons,  pairs,  tuples,  pairsidx,  tuplesidx,  tuplescon,  dims);
//	int_64 m= (int_64)1<<(env.n);
	BanzhafMobSparse(val, env.n,  (struct SparseFM *)&env);
	releaseenv(&env);
}


void ShapleyMobsparse_Call(double* val, int* n,
     double* singletons, double* pairs, double* tuples, int* pairsidx, int* tuplesidx, int* tuplescon, int* dims)
{
	volatile struct SparseFM env;
	populateenvConst(&env, n, singletons,  pairs,  tuples,  pairsidx,  tuplesidx,  tuplescon,  dims);
//	int_64 m= (int_64)1<<(env.n);
	ShapleyMobSparse(val, env.n,  (struct SparseFM *)&env);
	releaseenv(&env);
}

void ChoquetMob_sparseCall(double* x, double* val, int* n,
     double* singletons, double* pairs, double* tuples, int* pairsidx, int* tuplesidx, int* tuplescon, int* dims)
{
	volatile struct SparseFM env;
	populateenvConst(&env, n, singletons,  pairs,  tuples,  pairsidx,  tuplesidx,  tuplescon,  dims);
//	int_64 m= (int_64)1<<(env.n);
	val[0]=ChoquetMobSparse(x, env.n,  (struct SparseFM *)&env);
	releaseenv(&env);
}


void max_subset_sparseCall(double* x, int* S, int* cardS, double* val, int* n,
     double* singletons, double* pairs, double* tuples, int* pairsidx, int* tuplesidx, int* tuplescon, int* dims)
{
	volatile struct SparseFM env;	
	populateenvConst(&env, n, singletons,  pairs,  tuples,  pairsidx,  tuplesidx,  tuplescon,  dims);
	*val=  max_subsetSparse(x, *n, *S,*cardS,  (struct SparseFM *)&env);
	releaseenv(&env);
}

void min_subset_sparseCall(double* x, int* S, int* cardS, double* val, int* n,
     double* singletons, double* pairs, double* tuples, int* pairsidx, int* tuplesidx, int* tuplescon, int* dims)
{
	volatile struct SparseFM env;	
	populateenvConst(&env, n, singletons,  pairs,  tuples,  pairsidx,  tuplesidx,  tuplescon,  dims);
	*val=  min_subsetSparse(x, *n, *S,*cardS,  (struct SparseFM *)&env);
	releaseenv(&env);
}

void is_subset_sparseCall(int* A, int* cardA, int* B, int* cardB, int* val, int* n,
     double* singletons, double* pairs, double* tuples, int* pairsidx, int* tuplesidx, int* tuplescon, int* dims)
{
	volatile struct SparseFM env;	
	populateenvConst(&env, n, singletons,  pairs,  tuples,  pairsidx,  tuplesidx,  tuplescon,  dims);
	*val=  IsSubsetSparse(*A, *cardA, *B, *cardB ,  (struct SparseFM *)&env);
	releaseenv(&env);
}

void is_inset_sparseCall(int* A, int* cardA, int* i,  int* val, int* n,
     double* singletons, double* pairs, double* tuples, int* pairsidx, int* tuplesidx, int* tuplescon, int* dims)
{
	volatile struct SparseFM env;	
	populateenvConst(&env, n, singletons,  pairs,  tuples,  pairsidx,  tuplesidx,  tuplescon,  dims);
	*val=  IsInSetSparse(*A, *cardA, *i,  (struct SparseFM *) &env);
	releaseenv(&env);
}

void get_sizearray_tuplesCall(int* val, int* n,
     double* singletons, double* pairs, double* tuples, int* pairsidx, int* tuplesidx, int* tuplescon, int* dims)
{
	volatile struct SparseFM env;	
	populateenvConst(&env, n, singletons,  pairs,  tuples,  pairsidx,  tuplesidx,  tuplescon,  dims);
	val[0]=  GetSizeArrayTuples( (struct SparseFM *)&env);
	releaseenv(&env);
}
void get_num_tuplesCall(int* val, int* n,
     double* singletons, double* pairs, double* tuples, int* pairsidx, int* tuplesidx, int* tuplescon, int* dims)
{
	volatile struct SparseFM env;	
	populateenvConst(&env, n, singletons,  pairs,  tuples,  pairsidx,  tuplesidx,  tuplescon,  dims);
	val[0]=  GetNumTuples( (struct SparseFM *)&env);
//	Rprintf("tup %d %d\n", dims[1],env.m_tuples.size());
	releaseenv(&env);
}
void tuple_cardinality_sparseCall(int* i, int* val, int* n,
     double* singletons, double* pairs, double* tuples, int* pairsidx, int* tuplesidx, int* tuplescon, int* dims)
{
	volatile struct SparseFM env;	
	populateenvConst(&env, n, singletons,  pairs,  tuples,  pairsidx,  tuplesidx,  tuplescon,  dims);
	*val=  TupleCardinalitySparse(*i, (struct SparseFM *)&env);
	releaseenv(&env);
}





/*
void TupleCardinalitySparseCall(int* i, int* car, struct SEXP envsp)
{
	SparseFM* env = (SparseFM*)GetEnvAddr(envsp);

	*car = TupleCardinalitySparse(*i, env);
}*/

//#endif





static const R_CallMethodDef callMethods[]  = {
  {NULL, NULL, 0}
};

static R_NativePrimitiveArgType myC_t[] = {
    INTSXP, INTSXP, INTSXP, INTSXP, REALSXP, REALSXP, REALSXP
};


/*
static R_NativePrimitiveArgType myC_t1[] = {
    INTSXP, INTSXP, INTSXP, INTSXP};
*/

static const R_CMethodDef cMethods[] = {
   {"Preparations_FMCall", (DL_FUNC) &Preparations_FMCall, 7, myC_t},
   {NULL, NULL, 0, NULL}
};

//static const R_CallMethodDef cMethods1[] = {
//   {"Prepare_FM_sparseCall", (DL_FUNC) &Prepare_FM_sparseCall, 4, myC_t1},
//   {NULL, NULL, 0}
//};



//Rfmtool
void
R_init_Rfmtool(DllInfo *info)
{
   R_registerRoutines(info, cMethods, callMethods, NULL, NULL);
/////   R_registerRoutines(info, cMethods1, callMethods, NULL, NULL);
   R_useDynamicSymbols(info, TRUE); 
}





#endif

}
