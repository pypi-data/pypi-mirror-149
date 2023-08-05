//
/* This is a C-wrapper for fmtools library for python

   Gleb Beliakov, 2020
*/



#include <stdlib.h>

#define PYTHON_
#include "generaldefs.h"

#ifdef __cplusplus

#include "fuzzymeasuretools.h"
#include "fuzzymeasurefit.h"


#if defined  (_WIN32)
#define LIBEXP 	__declspec(dllexport)  
#else
#define LIBEXP 
#endif


extern "C" {
#endif

//NH
#define LIBEXP extern

	typedef unsigned long long int_64;

	struct  fm_env {
		int n;
		int m;
		int* card;
		int* cardpos;
		double* bit2card;
		double* card2bit;
		double* factorials;

	};



	struct  fm_env_sparse { // to use in wrappers, just to keep pointers. pointers might change when vectors are growing, but steady afterwards
		int n;		
		double *m_singletons;
		double* m_pairs;
		double* m_tuples;
		int* m_pair_index;
		int* m_tuple_start;
		int* m_tuple_content;
	};



	LIBEXP double py_min_subset(double* x, int n, int_64 S);
	LIBEXP double py_max_subset(double* x, int n, int_64 S);

	LIBEXP void py_ConvertCard2Bit(double* dest, double* src, struct fm_env* env);

	LIBEXP double py_min_subsetC(double* x, int n, int_64 S, struct fm_env* env);
	LIBEXP double py_max_subsetNegC(double* x, int n, int_64 S, struct fm_env* env);

	LIBEXP int py_SizeArraykinteractive(int n, int k, struct fm_env* env);
	LIBEXP int py_IsSubsetC(int i, int j, struct fm_env* env); // is i subset j?
	LIBEXP int py_IsElementC(int i, int j, struct fm_env* env);  // is i an element of j?

	LIBEXP void py_ExpandKinteractive2Bit(double* dest, double* src, struct fm_env* env, int kint, int arraysize);
	LIBEXP void py_ExpandKinteractive2Bit_m(double* dest, double* src, struct fm_env* env, int kint, int arraysize, double* VVC);
	/* Python interface call these two methods to allocate/deallocate memory */

	LIBEXP void py_fm_init(int n, struct fm_env* env);
	LIBEXP void py_fm_free(struct fm_env* env);


	//inline?
	LIBEXP void py_Shapley(double* v, double* x, struct fm_env* env);
	LIBEXP void py_Banzhaf(double* v, double* B, struct fm_env* env);

	LIBEXP void py_ShapleyMob(double* Mob, double* B, struct fm_env* env);
	LIBEXP void py_BanzhafMob(double* Mob, double* B, struct fm_env* env);

	LIBEXP double py_Choquet(double* x, double* v, struct fm_env* env);

	LIBEXP double py_ChoquetKinter(double* x, double* v, int kint, struct fm_env* env);


	/*  Add here the rest of the C calls for all the functions */
	LIBEXP double py_ChoquetMob(double* x, double* Mob, struct fm_env* env);


	LIBEXP void py_ConstructLambdaMeasure(double* singletons, double* lambda, double* v, struct fm_env* env);

	LIBEXP void py_ConstructLambdaMeasureMob(double* singletons, double* lambda, double* Mob, struct fm_env* env); // jb


	LIBEXP void py_dualm(double* v, double* w, struct fm_env* env);

	LIBEXP void py_dualmMob(double* v, double* w, struct fm_env* env);


	LIBEXP double py_Entropy(double* v, struct fm_env* env);


	LIBEXP void py_FuzzyMeasureFit(int datanum, int additive, struct fm_env* env, double* v, double* dataset);

	LIBEXP void py_FuzzyMeasureFitMob(int datanum, int additive, struct fm_env* env, double* v, double* dataset);


	LIBEXP void py_FuzzyMeasureFitKtolerant(int datanum, int additive, struct fm_env* env, double* v, double* dataset);


	LIBEXP void py_FuzzyMeasureFitLPKmaxitive(int datanum, int additive, struct fm_env* env, double* v, double* dataset);


	LIBEXP void py_FuzzyMeasureFitLPKinteractive(int datanum, int additive, struct fm_env* env, double* v, double* dataset, double* K);


	LIBEXP void py_FuzzyMeasureFitLPKinteractiveMaxChains(int datanum, int additive, struct fm_env* env, double* v, double* dataset, double* K);


	LIBEXP void py_FuzzyMeasureFitLPKinteractiveAutoK(int datanum, int additive, struct fm_env* env, double* v, double* dataset, double* K, int* maxiters);


	LIBEXP void py_FuzzyMeasureFitLPKinteractiveMarginal(int datanum, int additive, struct fm_env* env, double* v, double* dataset, double* K, int submod);


	LIBEXP void py_FuzzyMeasureFitLPKinteractiveMarginalMaxChain(int datanum, int additive, struct fm_env* env, double* v, double* dataset, double* K, int* maxiters, int submod);


	LIBEXP void py_FuzzyMeasureFitLP(int datanum, int additive, struct fm_env* env, double* v, double* dataset, int * options, double* indexlow, double* indexhihg, int* option1, double* orness);

	LIBEXP void py_FuzzyMeasureFitLPMob(int datanum, int additive, struct fm_env* env, double* v, double* dataset, int * options, double* indexlow, double* indexhihg, int* option1, double* orness);


	LIBEXP void py_fittingOWA(int datanum, struct fm_env* env, double* v, double* dataset);

	LIBEXP void py_fittingWAM(int datanum, struct fm_env* env, double* v, double* dataset);

	LIBEXP void py_Interaction(double* v, double* w, struct fm_env* env);

	LIBEXP void py_InteractionB(double* v, double* w, struct fm_env* env);

	LIBEXP void py_InteractionMob(double* Mob, double* w, struct fm_env* env); // jb

	LIBEXP void py_InteractionBMob(double* Mob, double* w, struct fm_env* env); // jb


	LIBEXP void py_BipartitionShapleyIndex(double* v, double* w, struct fm_env* env);


	LIBEXP void py_BipartitionBanzhafIndex(double* v, double* w, struct fm_env* env);

	LIBEXP void py_BNonadditivityIndexMob(double* Mob, double* w, struct fm_env* env);


	LIBEXP void py_NonadditivityIndex(double* v, double* w, struct fm_env* env);

	LIBEXP void py_NonmodularityIndex(double* v, double* w, struct fm_env* env);

	LIBEXP void py_NonmodularityIndexMob(double* Mob, double* w, struct fm_env* env);	
	
	LIBEXP void py_NonmodularityIndexKinteractive(double* v, double* w, int kint,  struct fm_env* env);

	LIBEXP void py_NonmodularityIndexMobkadditive(double* Mob, double* w, int k, struct fm_env* env);



	/*For small n returns the names of the coalitions as decimal strings in the binary and cardinality ordering, like 0,1,2,12,3,13,23,123 , for printing */
	LIBEXP void py_ShowCoalitions(int* coalition, struct fm_env* env);
	LIBEXP void py_ShowCoalitionsCard(int* coalition, struct fm_env* env);

	LIBEXP int py_IsMeasureAdditive(double* v, struct fm_env* env);


	LIBEXP int py_IsMeasureBalanced(double* v, struct fm_env* env);


	LIBEXP int py_IsMeasureSelfdual(double* v, struct fm_env* env);


	LIBEXP int py_IsMeasureSubadditive(double* v, struct fm_env* env);


	LIBEXP int py_IsMeasureSubmodular(double* v, struct fm_env* env);


	LIBEXP int py_IsMeasureSuperadditive(double* v, struct fm_env* env);


	LIBEXP int py_IsMeasureSupermodular(double* v, struct fm_env* env);


	LIBEXP int py_IsMeasureSymmetric(double* v, struct fm_env* env);


	LIBEXP int py_IsMeasureKMaxitive(double* v, struct fm_env* env);


	LIBEXP int py_IsMeasureAdditiveMob(double* Mob, struct fm_env* env); // jb

	LIBEXP int py_IsMeasureBalancedMob(double* Mob, struct fm_env* env); // jb



	LIBEXP int py_IsMeasureSelfdualMob(double* Mob, struct fm_env* env); // jb

	LIBEXP int py_IsMeasureSubadditiveMob(double* Mob, struct fm_env* env); // jb
	
	LIBEXP int py_IsMeasureSubmodularMob(double* Mob, struct fm_env* env); // jb

	LIBEXP int py_IsMeasureSuperadditiveMob(double* Mob, struct fm_env* env); // jb

	LIBEXP int py_IsMeasureSupermodularMob(double* Mob, struct fm_env* env); // jb

	LIBEXP int py_IsMeasureSymmetricMob(double* Mob, struct fm_env* env); // jb

	LIBEXP int py_IsMeasureKMaxitiveMob(double* Mob, struct fm_env* env); // jb




	LIBEXP void py_Mobius(double* v, double* MobVal, struct fm_env* env);

	LIBEXP double py_Orness(double* Mob, struct fm_env* env);


	LIBEXP double py_OWA(double* x, double* v, struct fm_env* env);




	LIBEXP double py_Sugeno(double* x, double* v, struct fm_env* env);


	LIBEXP double py_WAM(double* x, double* v, struct fm_env* env);


	LIBEXP void py_Zeta(double* Mob, double* v, struct fm_env* env);


	// random generation and other functions


	LIBEXP void py_dualMobKadd(int m, int length, int k, double* src, double* dest, struct fm_env* env);

	LIBEXP void py_Shapley2addMob(double* v, double* x, int n);

	LIBEXP void py_Banzhaf2addMob(double* v, double* x, int n);

	LIBEXP double py_Choquet2addMob(double*x, double* Mob, int n);



	LIBEXP int py_fm_arraysize(int n, int kint, struct fm_env* env);


	LIBEXP int py_generate_fm_tsort(int num, int n, int kint, int markov, int option, double K, double * vv, struct fm_env* env);

	LIBEXP int py_generate_fmconvex_tsort(int num, int n, int kint, int markov, int option, double K, double * vv, struct fm_env* env);

	LIBEXP int py_generate_fm_minplus(int num, int n, int kint, int markov, int option, double K, double * vv, struct fm_env* env);


	LIBEXP int py_generate_fm_2additive_convex(int num, int n, double * vv);


	LIBEXP int py_generate_fm_2additive_concave(int num, int n,  double * vv);


	LIBEXP int py_generate_fm_2additive_convex_withsomeindependent(int num, int n,  double * vv);

	LIBEXP void py_export_maximal_chains(int n, double* v, double* mc, struct fm_env* env);






	/*
	Sparse representation of k-additive capacities. Thre representation is in the form of singletons, pairs and tuples with nonzero values, stored and indexed in the respective
	arrays (see above in this file)

	 Prepares an empty structure, given the list of cardinalities of the nonzero tuples (cardinality, tuple composition) like this 2 pairs 4-tuple and a triple:  (2,1,2,  2, 3,1,   4, 1,2,3,4,  3,3,2,1...)

	 It is used to allocate storage and later populate these values
	*/
	LIBEXP void py_prepare_fm_sparse(int n, int tupsize, int* tuples, struct fm_env_sparse* env);
	LIBEXP void py_free_fm_sparse( struct fm_env_sparse* env);

	/*  Returns the cardinality of the tuple numbered i in the list of tuples */
	LIBEXP int py_tuple_cardinality_sparse(int i, struct fm_env_sparse* env);

	LIBEXP int py_get_num_tuples(struct fm_env_sparse* env);
	LIBEXP int py_get_sizearray_tuples(struct fm_env_sparse* env);

	/* checks if element i (1-based!!!) belongs to the tuple indexed A (whose cardinality can be 1,2, other (automatically determined) */
	LIBEXP int py_is_inset_sparse(int A, int card, int i, struct fm_env_sparse* env);

	/* checks if tuple B is a subset of A */
	LIBEXP int py_is_subset_sparse(int A, int cardA, int B, int cardB, struct fm_env_sparse* env);

	/* calculates minimum (maximum) of (x_i) with the indices belonging to tuple indexed as S (its cardinality cardS can be 1,2, other( put 3, will be determined automatically)
	note that x is 0-based, tuples are 1-based */
	LIBEXP double py_min_subset_sparse(double* x, int n, int S, int cardS, struct fm_env_sparse* env);
	LIBEXP double py_max_subset_sparse(double* x, int n, int S, int cardS, struct fm_env_sparse* env);

	/* calculates the Choquet integral in Mobius representation */
	LIBEXP double py_ChoquetMob_sparse(double* x, int n, struct fm_env_sparse* env);


	/* Shapley and Banzhaf values vector of a capacity */
	LIBEXP void py_ShapleyMob_sparse(double* v, int n, struct fm_env_sparse* env);
	LIBEXP void py_BanzhafMob_sparse(double* v, int n, struct fm_env_sparse* env);

	/* populates 2-additive sparse capacity with nonzero values using the singletons and two arrays of indices (of size numpairs) . Indices need to be 1-based. Singletons 0-based */
	LIBEXP void py_populate_fm_2add_sparse(double* singletons, int numpairs, double* pairs, int* indicesp1, int* indicesp2, struct fm_env_sparse* env);

	/* for populating capacities. Add pair (v_ij) to the structure. indices are 1-based */
	LIBEXP void py_add_pair_sparse(int i, int j, double v, struct fm_env_sparse* env);

	/* for populating capacities, adds a tuple of size tupsize whose 1-based indices are in tuple */
	LIBEXP void py_add_tuple_sparse(int tupsize, int* tuple, double v, struct fm_env_sparse* env);

	/* Given 2-additive capacity singletons=pairs in one array v , selects nonzero pairs */
	LIBEXP void py_populate_fm_2add_sparse_from2add(int n, double * v, struct fm_env_sparse* env);

	/* from sparse to full representaiotn of 2-additive capacity (singletons and paits, augmented with 0 ) Vector v has to be allocated, size is n+ n(n-1)/2 */
	LIBEXP void py_expand_2add_full(double* v, struct fm_env_sparse* env);

	/* from sparse to full capacity (vector v, size 2^n has to be preallocated) */
	LIBEXP void py_expand_sparse_full(double* v, struct fm_env_sparse* env);

	LIBEXP void py_sparse_get_singletons(int n, double* v, struct fm_env_sparse* env);

	LIBEXP int py_sparse_get_pairs(int* pairs, double* v, struct fm_env_sparse* env);

	LIBEXP int py_sparse_get_tuples(int* tuples, double* v, struct fm_env_sparse* env);


	/* random generation of  sparse supermodular capacities */
	LIBEXP int   py_generate_fm_2additive_convex_sparse(int n, struct fm_env_sparse* env);

	LIBEXP int   py_generate_fm_kadditive_convex_sparse(int n, int k, int nonzero, struct fm_env_sparse* env);

	LIBEXP void py_Nonmodularityindex_sparse(double* w, int n, struct fm_env_sparse* env);

#ifdef __cplusplus
}
#endif






