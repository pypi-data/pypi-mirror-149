


#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <fstream>
using namespace std;
#include <cmath>
#include <algorithm>



#include <map>
#include <set>
#include <unordered_set>
#include <iterator>
#include<vector>

using namespace std;
//#include <R.h>
// note that programs using this code should be linked against lp_solve library,
// which should be downloaded and installed separatly. These references are only
// to the readers of that library.

#include "fuzzymeasuretools.h"
#include "fuzzymeasurefit.h"
#include "lp_lib.h"


template <class ForwardIterator, class T>
void myiota(ForwardIterator first, ForwardIterator last, T val)
{
	while (first != last) {
		*first = val;
		++first;
		++val;
	}
}

template <typename Container>
struct compare_indirect_index
{
	const Container& container;
	compare_indirect_index(const Container& container) : container(container) { }
	bool operator () (size_t lindex, size_t rindex) const
	{
		return container[lindex] > container[rindex];
	}
};


#define mtokey(a,b)( (a)|(int_64(b)<<56))
#define setfromkey(a) ((a)& 0x00FFFFFFFFFFFFFF)
#define varfromkey(a) (((a)>>56)& 0xFF)


#ifndef byte
typedef unsigned char  byte;
#endif

struct arrayindex {
	byte* v;
};


class greaterindex {
public:
	const  byte* container;
	  int  N=0;

	  greaterindex(const byte* incontainer, const int n) { container = incontainer; N = n; };
	  bool operator() (const int& a, const int& b);

};
bool greaterindex:: operator() (const int& a, const int& b) {
	for (int i = 0; i < N; i++)
	if (container[a + i] == container[b + i]);
	else if (container[a + i] > container[b + i])
		return 1; else return 0;
	return 0;
}

typedef map<int_64, int> Mymap;
//typedef set<int, greaterindex <int*> > Myset;

byte string2number(string& s, byte i) { return (byte)s[i] - 1; }
void number2string(string& s, byte i, byte n) { s[i] = n + 1; }

void Setinsert(int_64& S, string St, byte pos){ AddToSet(&S, string2number(St, pos)); }
void Setremove(int_64& S, string St, byte pos){ RemoveFromSet(&S, string2number(St, pos)); }
void CodeMaxChain(int* chain, string & S, int n){
	for (int i = 0; i < n; i++)
		number2string(S, i, chain[i]);
}




int	FuzzyMeasureFitLPKinteractive(int n, int_64 m, int K, int Kadd, double *v, double* XYData, int options,
	double* indexlow, double* indexhigh, int option1, double* orness, double KConst)

	// in standard representation
	// K for data, Kadd for k-interactive f.m.
	// KConst the bound on the constant K for k-interactive fm

{

	int counter = 0;
	unsigned int i, j, k,  res;
	int result;
	int_64 A, B, C;
	lprec		*MyLP;
	unsigned int RowsR, RowsC, RowsC1;

	if (Kadd >= n) {
		Kadd = n - 1; KConst = 1;
	}
	if (Kadd == n - 1) KConst = 1;

	RowsC1 = (cardpos[Kadd] - n - 1); //how many non-singletons   ///Check this mu(0)=0. Also fewer variables as all are positive
	RowsR = K * 2; RowsC = n + RowsC1;  /// removed *2
	unsigned int RowsC2 = (cardpos[Kadd - 1]); // position of the second last cardinality


	MyLP = make_lp(RowsR + RowsC, 0);
	MyLP->do_presolve = FALSE;
	set_verbose(MyLP, 0);
	unsigned int itemp = RowsC + 2 + 1; // just the max number of entries per column

	double *row;
	int	 *rowno;
	row = new double[itemp];
	rowno = new int[itemp];
	int* ind=new int[n];

	// int re;

	// the first K columns
	rowno[0] = 0;
	double factor = (1.0 - KConst) / (n - Kadd - 1);
	for (k = 0; k<(unsigned int)K; k++) {
		//rowno[0] is the obj. function
		row[0] = XYData[k*(n + 1) + n];//y[k]; //
		rowno[0] = 0;
		
		myiota(ind, ind + n, 0);  // found in <numeric>
		sort(ind, ind + n, compare_indirect_index <double*>(&(XYData[k*(n + 1)]))); // decreasing order now

		for (i = 0; i < (unsigned int)(n - Kadd - 1); i++) {
			row[0] -= factor* ((&(XYData[k*(n + 1)]))[ind[n-i-1]]); 
		}
		row[0] -= ((&(XYData[k*(n + 1)]))[ind[Kadd]])*KConst;

		//todo not to include 0

		rowno[1] = k + 1;  // 1-based
		rowno[2] = k + 1 + K;
		row[1] = -1;
		row[2] = 1;
		// now the vales of h_A

		itemp = 0;
		for (i = 0; i<(unsigned int)n; i++) {// singletons
			row[2 + itemp + 1] = maxf(0, XYData[k*(n + 1) + i] - max_subset_complement(&(XYData[k*(n + 1)]), n, card2bit[i + 1]));
			rowno[2 + itemp + 1] = RowsR + i + 1;
			if (row[2 + itemp + 1] != 0) {
				counter++; itemp++;
			}
		}


		//todo: do I need zeroes?

		for (i = 0; i<RowsC1; i++) {
			row[2 + itemp  + 1] = maxf(0, min_subset(&(XYData[k*(n + 1)]), n, card2bit[i + 1 + n]) - max_subset_complement(&(XYData[k*(n + 1)]), n, card2bit[i + 1 + n]));      /// new function g_A, need max_subset_complement, also need to move 1s to the RHS with y
			rowno[2 + itemp  + 1] = RowsR + n + i + 1;  // was +n in the index

			if (row[2 + itemp  + 1] != 0) { counter++; itemp++; }
			//			row[2+i +n + RowsC1+1]= - row[2+i +n+1] ;
			//			rowno[2+i+n + RowsC1+1] = RowsR + n + i +1  + RowsC1;
		}
		


		add_columnex(MyLP, itemp+3, row, rowno);

		// now repeat everything, just change the sign
		for (i = 0; i<itemp+3; i++) row[i] = -row[i];

		add_columnex(MyLP, itemp+3, row, rowno);
		
	}

	/// I do not need this as m(N)=1

	// now monotonicity constraints for all |A|>2


	for (A = n + 1; A <= RowsC; A++){   ///check if we need <=
		//	cout<<"start subset  "<< A<<endl;
		C = card2bit[A];
		for (i = 0; i<(unsigned int)n; i++) if (IsInSet(C, i)) { ///check if inequality is reverse	
			row[0] = 0; rowno[0] = 0;
			k = 1;
			row[k] = 1;
			rowno[k] = int( A + RowsR);
			k++;
			B = C;
			RemoveFromSet(&B, i);
			row[k] = -1;
			rowno[k] = int(bit2card[B] + RowsR);
			k++;
			add_columnex(MyLP, k, row, rowno);

			counter += k;
		}

	} // A 


	for (A = RowsC2; A <= RowsC; A++){   ///check if we need <=1 ????????????????	
		row[0] = -KConst; rowno[0] = 0;
		//row[0] = 0;
		k = 1;
		row[k] = -1;
		rowno[k] = int(A + RowsR);
		k++;
		add_columnex(MyLP, k, row, rowno);

		counter += k;
	} // i 

	//} // subsets

	// add interaction indices if needed

	/// no orness or other options

	int RR = get_Nrows(MyLP);
	int CC = get_Ncolumns(MyLP);
	for (i = 1; i <= (unsigned int)RR; i++) {
		set_rh(MyLP, i, 0);
		set_constr_type(MyLP, i, LE);

	}
//	for (i = 1; i <= (unsigned int)CC; i++) {
//		set_bounds(MyLP, i, 0.0, 1.0);
//	}

	for (i = 1; i <= RowsR; i++) {
		set_rh(MyLP, i, 1.0); 
	}
//	for (i = RowsR + RowsC2; i <= RR; i++) {
//		set_rh(MyLP, i, KConst);
//	}

	set_maxim(MyLP); // well, we always do that



	double *sol = (double*)malloc(sizeof(double)*(1 + RR + CC));

//	cout << n <<"\t"<<K <<"\t"<<Kadd<<"\t"<< RR << "\t" << CC << "\t"<<counter<<endl;

//		 write_lp(MyLP, "model.lp");
//		cout<<"finished building LP "<< RR<< " " <<CC<<endl;
//		set_outputfile(MyLP, "log.txt");

	//	print_lp(MyLP);

	//  set_verbose(MyLP,5);
	//  set_outputstream(MyLP, stdout);
	//  print_lp(MyLP);
	/// change recovery from the output...

	res = solve(MyLP);
	double minval=10e10;

	if (res == OPTIMAL) {
		//		temp=0;
		get_dual_solution(MyLP, sol);
//		print_solution(MyLP, 1);
		minval = get_objective(MyLP);  // minimum

//	   for (i = 0; i < RR + 1 ; i++) cout << sol[i] << endl;
//		cout<<" min value "<<minval<<" "<<res<<endl;

		v[0] = 0;// always !!
		for (i = 1; i <= (unsigned int)n; i++)
		{
			v[i] = sol[i + RowsR]; // singletons
		}
		for (i = 0; i<RowsC1; i++)
		{
			v[i + n + 1] = sol[n + RowsR + 1 + i]; ////- sol[n+RowsR+1 + RowsC1+i]; // other subsets
			k++;
		}
		k = n + RowsC1+1;

		for (int_64 ii = k; ii < m; ii++){
			j = card[card2bit[ii]];
			if (Kadd<n - 1)
				v[ii] = KConst + (j - Kadd - 1.0)*(1. - KConst) / (n - Kadd - 1);
			else v[ii] = 1;

		}

		result = 1;
	} // no optimal
	else result = 0;

	// just to cheat the compiler
	minval = minval + 1;
	delete[] row;
	delete[] rowno;
	delete[] ind;


	free(sol);
	delete_lp(MyLP);
	return result;
}


void AddSetToVars(Mymap& MyMap, int_64& A,  int s, unsigned int& j, unsigned int& k)
{
	// existing A
	int b = int(MyMap.size());
	auto t = MyMap.insert(pair <int_64, int>(mtokey(A, 0), b));

	if (t.second) // new var inserted
		j = b;
	else
		j = (t.first)->second; // already in the set of variables

	// make set A, augment with the new element
	AddToSet(&A, s);
	b = int(MyMap.size());
	t = MyMap.insert(pair <int_64, int>(mtokey(A, 0), b));

	if (t.second) // new var inserted
		k = b;
	else
		k = (t.first)->second; // already in the set of variables

}

void AddPairSetsToVars(Mymap& MyMap, int_64& A, int_64& B, unsigned int& j, unsigned int& k)
{
	// existing A
//	int b = int(MyMap.size());
	auto t = MyMap.find(mtokey(A, 0));
	//auto t = MyMap.insert(pair <int_64, int>(mtokey(A, 0), b));

	j = t->second;

//	if (t->second) // new var inserted
//		j = b;
//	else
//		j = (t->first);// ->second; // already in the set of variables

//	b = int(MyMap.size());
	t=MyMap.find(mtokey(B, 0));

	k = t->second;



}

void AddMonotonicityConstraints(int n, int_64 m, int K, int Kadd, Mymap& MyMap, set <std::string> &MC, int* index, string& S, double KConst,
	set<pair<int, int> >& monindices, multimap<int, int_64>& CardSet, multimap<int_64, std::string>& SetChain)
{

	unsigned int j, k,j1;
	int_64 A = 0, B=0;

	set<std::string >::iterator MCcurr;
	set<int> redundant, redinitial;

	redinitial.clear();
	for (int i = 0; i < Kadd; i++) number2string(S, i, index[i]);
	if (MC.count(S)==0) {
		AddToSet(&A, index[0]);
		
		for (int i = 1; i < Kadd; i++) 
		{
//			std::cout << "insert " << ShowValue(A) << endl;
			CardSet.insert(pair<int, int_64>(i, A));
			SetChain.insert(pair<int_64, std::string>(A,S));

			AddSetToVars(MyMap, A, index[i], j, k);
//			if(i==1) redinitial.insert(j);
//			redinitial.insert(k);

			monindices.insert(pair<int, int>(k + K, j + K));
		}

		CardSet.insert(pair<int, int_64>(Kadd, A));
		SetChain.insert(pair<int_64, std::string>(A, S));

		goto L3;
		// do not forget this!!
		//set_bounds(MyLP, rowno[2], 0, KConst);

		A = 0; 
		redundant.clear();
		redundant.insert(redinitial.begin(), redinitial.end());


		AddToSet(&A, index[0]);
		// now non-trivial constraints
		for (int i = 1; i < Kadd -1; i++)
		{
			AddToSet(&A, index[i]);
			for (MCcurr = MC.begin(); MCcurr != MC.end(); MCcurr++){
				S = *MCcurr;

				B = 0;
				for (j = 0; j < cardf(A) ; j++){ k = string2number(S, j); AddToSet(&B, k); }// construct subset of size i

				for (j1 = i ; j1 >0; j1--){
					k = string2number(S, j1);		
					RemoveFromSet(&B, k);
//					std::cout << "card<<" << cardf(A) << " " << cardf(B) << endl;

					if (IsSubset(A, B)){ // add constraint and break
						AddPairSetsToVars(MyMap, B, A, j, k);
						auto r=redundant.insert(k);
						if (r.second){
							monindices.insert(pair<int, int>(k + K, j + K));

						}							
						goto L2; //break
					}
				} //
			L2:;

				
			}//all MC
		} // i


		redundant.clear();
		redundant.insert(redinitial.begin(), redinitial.end());

		A = UniversalSet(n);
		for (int i = n - 1; i >= Kadd; i--) RemoveFromSet(&A, index[i]);
		for (unsigned int i = Kadd-1; i >= 1; i--)
		{
			RemoveFromSet(&A, index[i]);
	
			for (MCcurr = MC.begin(); MCcurr != MC.end(); MCcurr++){
				S=*MCcurr;

				B = 0;
				for (j = 0; j < i; j++){ k = string2number(S, j); AddToSet(&B, k); }// construct subset of size i

				for (j1 = i ; j1 <  (unsigned int)Kadd-1; j1++){
					k = string2number(S, j1);
					AddToSet(&B, k);
					if (IsSubset(B, A)){ // add constraint and break
						AddPairSetsToVars(MyMap, A, B, j, k);
						auto r = redundant.insert(k);
						if (r.second){
							monindices.insert(pair<int, int>(k + K, j + K));
					}
					goto L1; //break
					}
				} //
			L1:;


			}//all MC
		} // i

		redundant.clear(); redinitial.clear();
	L3:;
		for (int i = 0; i < Kadd; i++) number2string(S, i, index[i]);
		MC.insert(S);

		//add to MC
	}
	else; // already in the set, no constraints are needed


}

int IndexOfDataConstraint( Mymap& MyMap, int_64 A )
{
	int j;
	int b = int(MyMap.size());
	auto t = MyMap.insert(pair <int_64, int>(mtokey(A, 0), b));

	if (t.second) // new var inserted
		j = b;
	else
		j = (t.first)->second; // already in the set of variables

	return  j;
}


void ProcessConstraints(int n, int_64 m, int K, int Kadd, Mymap& MyMap, set <std::string> &MC, string& S, double KConst,
	set<pair<int, int> >& monindices, multimap<int, int_64>& CardSet, multimap<int_64, std::string>& SetChain)
{
	int_64 B;
	int k;
	unordered_set<int> redundant;
	for (int i = 1; i < Kadd; i++)
	{
		redundant.clear();
		auto range = CardSet.equal_range(i);
		for (multimap<int, int_64>::iterator it = range.first; it != range.second; ++it)
		{
			auto Ai = MyMap.find(mtokey(it->second,0));
			for (k = 1; k <= Kadd - i; k++) {
				auto ran1 = CardSet.equal_range(i + k);
				for (multimap<int, int_64>::iterator it1 = ran1.first; it1 != ran1.second; ++it1)
				{
					if (IsSubset(it1->second, it->second))
					{
						auto Bi = MyMap.find(mtokey(it1->second, 0));
						B = it1->second;
						if (redundant.count(Bi->second) == 0)
						{

							monindices.insert(pair<int, int>(Bi->second + K, Ai->second + K));
							redundant.insert(Bi->second);
							// chain
							auto Ch = SetChain.find(it1->second);
							string S1 = Ch->second;
							for (int j = i + 1; j < Kadd; j++)
							{
								AddToSet(&B, string2number(S1, j));
								auto rr = MyMap.find(mtokey(B, 0));
								redundant.insert(rr->second);
							}
						}// redundant

					} // subset
				} //it1
			} //k
		} //it
	} //i
}


int	FuzzyMeasureFitLPKinteractiveMaxChains(int n, int_64 m, int K, int Kadd, double *v, double* XYData, int options,
	double* indexlow, double* indexhigh, int option1, double* orness, double KConst)

	// in standard representation
	// K for data, Kadd for k-interactive f.m.
	// Kconst is the smallest value of fm for |A|>k
	// fr now no other paprameters are used
{

	int counter = 0;
	unsigned int i, j, k,  res;
	int result;
	int_64 A,B;
	lprec		*MyLP;
	unsigned int RowsR, RowsC, RowsC1;

	double temp;

	vector<double> coefs;
	vector<int> indices;
	set<pair<int, int> > monindices;

	set<std::string> MC;
	multimap<int_64, std::string> SetChain;
	multimap<int, int_64> CardSet;
	Mymap MyMap;
	string S;
	S.assign(Kadd, 'a');

	// safety check

	if (Kadd >= n) {
		Kadd = n - 1; KConst = 1;
	}
	if (Kadd == n - 1) KConst = 1;

	// calculate how many rows/columns we need

	RowsC1 = (cardpos[Kadd] - n - 1); //how many non-singletons   ///Check this mu(0)=0. Also fewer variables as all are positive
	RowsR = K * 2; RowsC = n + RowsC1;  /// removed *2
//	unsigned int RowsC2 = (cardpos[Kadd - 1]); // position of the second last cardinality
	unsigned int RowsC3 = (cardpos[Kadd ]); // position of the second last cardinality

	unsigned int itemp = RowsC + 2 + 1; // just the max number of entries per column

	double *row;
	int	 *rowno;
	row = new double[itemp];
	rowno = new int[itemp];
	int* ind = new int[n];


	// the first K columns
	rowno[0] = 0;
	double factor; if (Kadd < n - 1) factor = (1.0 - KConst) / (n - Kadd - 1); else factor = 0;
	for (k = 0; k<(unsigned int)K; k++) {
		//rowno[0] is the obj. function
		row[0] = XYData[k*(n + 1) + n];//y[k]; //

		myiota(ind, ind + n, 0);  // found in <numeric>
		sort(ind, ind + n, compare_indirect_index <double*>(&(XYData[k*(n + 1)])));

		AddMonotonicityConstraints(n, m, K*2+1, Kadd, MyMap, MC, ind, S, KConst,monindices,CardSet, SetChain);
		if (n - Kadd - 1>=0)
		for (i = 0; i < (unsigned int)(n - Kadd - 1); i++) {
			row[0] -= factor* ((&(XYData[k*(n + 1)]))[ind[n-i-1]]);
			temp = ((&(XYData[k*(n + 1)]))[ind[n-i-1]]);
		}
		row[0] -= ((&(XYData[k*(n + 1)]))[ind[Kadd]])*KConst;


		/// minus sum of g_A over all subsets whose m(A)=1, at the very least m(N)=1
		//for (A = RowsC + 1; A<m; A++) row[0] -= maxf(0, min_subset(&(XYData[k*(n + 1)]), n, card2bit[A]) - max_subset_complement(&(XYData[k*(n + 1)]), n, card2bit[A]));  ///?????

		coefs.push_back(row[0]);
		indices.push_back(0);

		rowno[1] = k + 1;  // 1-based
		rowno[2] = k + 1 + K;
		row[1] = -1;
		row[2] = 1;
		
		// now the vales of h_A
		A = 0;
		for (i = 0; i < (unsigned int)Kadd; i++){
			AddToSet(&A, ind[i]);
	
			j=	IndexOfDataConstraint(MyMap, A) + 2*K+ 1; //+ offset
	
			temp=(&(XYData[k*(n + 1)]))[ind[i]] - ((i+1<(unsigned int)n)? (&(XYData[k*(n + 1)]))[ind[i+1]]:0);
			coefs.push_back(temp);
			indices.push_back(j);
		}
		// add to arrays

	}


	ProcessConstraints(n, m, K * 2 + 1, Kadd, MyMap, MC, S, KConst, monindices, CardSet, SetChain);
//	now we have the sizes
	RowsC = int(MyMap.size());

	MyLP = make_lp(0, RowsR + RowsC);
	set_add_rowmode(MyLP, TRUE);
//	MyLP = make_lp(RowsR + RowsC, 0); ///??????? w dont know the number of variables yet. reserve or not?
//	MyLP->do_presolve = FALSE;
//	set_verbose(MyLP, 3);

	for (i = 1; i <= RowsR; i++) {
		set_obj(MyLP, i, 1.0);
	}

	for (k = 0; k < (unsigned int)K; k++){
		rowno[1] = k + 1;  // 1-based
		rowno[2] = k + 1 + K;
		row[1] = -1;
		row[2] = 1;		
		j = (Kadd + 1)*k;
		row[0] = coefs[ j];
		rowno[0] = indices[j];
		for (i = 0; i < (unsigned int)Kadd; i++){
			row[3+i] = coefs[i +j+1];
			rowno[3+i] = indices[i+j+1];
		}
		add_constraintex(MyLP, Kadd + 2, row + 1, rowno + 1, EQ, row[0]);
		counter += Kadd + 2;

//		add_columnex(MyLP, Kadd + 3, row, rowno);
//		for (i = 0; i<Kadd + 3; i++) row[i] = -row[i];
//		add_columnex(MyLP, Kadd + 3, row, rowno);
	}

	row[0] = 0;
	set<pair<int, int> >::iterator is;
	for (is = monindices.begin(); is != monindices.end(); is++){
		rowno[1] =is->first;
		rowno[2] = is->second;
		row[1] = -1;
		row[2] = 1;
		add_constraintex(MyLP, 2, row + 1, rowno + 1, LE, row[0]);
		counter += 2;
		//add_columnex(MyLP,  3, row, rowno);
	}


//	printf("\n constraints : %d\n", monindices.size());
//	printf("\n chains : %d\n", MC.size());

	// boundary
	auto range = CardSet.equal_range(Kadd);
	double lowbow = 0.0;
	if (Kadd == n) lowbow = KConst = 1.0;
	for (multimap<int, int_64>::iterator it = range.first; it != range.second; ++it)
		{
			auto Ai = MyMap.find(mtokey(it->second, 0));
			set_bounds(MyLP, Ai->second + RowsR + 1, lowbow, KConst);
		}


	/// I do not need this as m(N)=1

	// next equality constraint = add to 1
	double wei = K; // this constraint is taken with that weight, to ensure it is actually satisfied 
	if (wei<1) wei = 1;

	set_add_rowmode(MyLP, FALSE);

	int RR = get_Nrows(MyLP);
	int CC = get_Ncolumns(MyLP);
//	for (i = 1; i <= (unsigned int)RR; i++) {
//		set_rh(MyLP, i, 0);
//		set_constr_type(MyLP, i, LE);
//	}
//	for (i = 1; i <= (unsigned int)CC; i++) {
//		set_bounds(MyLP, i, 0.0, 1.0);
//	}

//	for (i = 1; i <= RowsR; i++) {
//		set_rh(MyLP, i, 1.0);
//	}

//	set_maxim(MyLP); // well, we always do that
	set_minim(MyLP);

//	cout << n << "\t" << K << "\t" << Kadd << "\t" << RR << "\t" << CC << "\t" << MC.size() << "\t" <<counter<<endl;

	double *sol = (double*)malloc(sizeof(double)*(1 + RR + CC));

//		 write_lp(MyLP, "model.lp");
//		cout<<"finished building LP "<< RR<< " " <<CC<<endl;
//		set_outputfile(MyLP, "log.txt");
//		print_lp(MyLP);

	//  set_verbose(MyLP,5);
	//  set_outputstream(MyLP, stdout);
	//  print_lp(MyLP);
	/// change recovery from the output...

	res = solve(MyLP);
	double minval=10e10;

	if (res == OPTIMAL) {
		//		temp=0;
//		get_dual_solution(MyLP, sol);
		get_primal_solution(MyLP, sol);

//		print_solution(MyLP, 1);
//		for (i = 0; i < RR + 1 + CC; i++) cout << sol[i] << endl;

		minval = get_objective(MyLP);  // minimum
//		cout<<" min value "<<minval<<endl;

		v[0] = 0;// always !!
		A = 0;
		for (i = 1; i < RowsC3; i++)
		{
			A = card2bit[i];

			auto Ai = MyMap.find(mtokey(A, 0));
			if (Ai != MyMap.end()){
				
				v[i] = sol[Ai->second + RowsR + 1 + RR];  // in row mode we add RR, for dual, we don't
//				cout << Ai->second+RowsR+1 <<" "<<Ai->first <<" "<<v[i]<< endl;
			} else v[i] = 0;
			
			{
				
				for (j = (card[A]>=2)? (cardpos[ card[A] - 2]):0; j <(unsigned int) cardpos[card[A]-1]; ++j)
				{
					B = card2bit[j];
					if (IsSubset(A, B))
						v[i] = maxf(v[i], v[j]);
					//v[i] = maxf(v[i], v[j]);
				}
			}

		}
		/*
		this method will work for "compressed" FM representation to be done in the future. For now expand it into all FM values
		//remainder by cardinality
		for (i = RowsC3; i < RowsC3 + (n - Kadd); i++)
		{
			j = i - RowsC3 + Kadd + 1;
			if (Kadd<n-1)
				v[i] = KConst + (j-Kadd-1.0)*(1. - KConst)/(n-Kadd-1);
			else v[i] = 1;

		}
		*/
		for (int_64 ii = RowsC3; ii < m; ii++){
			j = card[card2bit[ii]];
			if (Kadd<n - 1)
				v[ii] = KConst + (j - Kadd - 1.0)*(1. - KConst) / (n - Kadd - 1);
			else v[ii] = 1;

		}

		result = 1;
	} // no optimal
	else result = 0;

	// just to cheat the compiler
	minval = minval + 1;
	delete[] row;
	delete[] rowno;
	delete[] ind;

	free(sol);
	delete_lp(MyLP);
	return result;
}

/* =====================================================================
The methods below refer to marginal contribution representation


*/
void AddVarsConstraints(int n, int_64 m, int Kadd, Mymap& MyMap, int* index, double KConst, vector<double>& coefs, vector<int_64>& indices, vector<int_64>& indices1, double* X)
{
	unsigned int j, k;
	int_64 A = 0;

	k = 0;
	for (j = 0; j <= (unsigned int)Kadd; j++){
		AddToSet(&A, index[j]);
		int b = int(MyMap.size());
		auto t = MyMap.insert(pair <int_64, int>(mtokey(A, index[j]), b)); // marginal
		if (t.second) // new var inserted
			k = b;
		else
			k = (t.first)->second; // already in the set of variables	

		indices.push_back(k);
		indices1.push_back(k);		
		coefs.push_back(X[index[j]]);

		if (1|| (j > 0)){

			b = int(MyMap.size());
			t = MyMap.insert(pair <int_64, int>(mtokey(A, n), b));  // the actual set

			if (t.second) // new var inserted
				k = b;
			else
				k = (t.first)->second; // already in the set of variables	

			indices1.push_back(k);
		}

	}
}


void process_constraint_recursive(lprec		*MyLP, int* rowno, double* row, int_64 B, int level, int shift, int Kadd, set<pair<int, int> >& modindices, int parent, double bound1, double bound2)
{		
	if (level == 0) { rowno[level] = int(B+shift); 
		add_constraintex(MyLP, Kadd, row + 1, rowno , EQ, row[0]);

		if (parent >= 0) modindices.insert(pair<int, int>(parent, rowno[level]));

		return; 
	}
	for (int j=0,i = 0; i <= level; i++){
		int_64 A = setfromkey(card2bitm[i + B]);	
		
		while(Removei_th_bitFromSet(&A, j++)) ;

		card2bitm[i + B]=mtokey(card2bitm[i + B], j - 1);

		rowno[level] = int(i + B+shift);
		if (parent >= 0) modindices.insert(pair<int, int>(parent, rowno[level]));
		else
			set_bounds(MyLP, rowno[level], bound1, bound2);

		process_constraint_recursive(MyLP, rowno, row, bit2cardm[A], level - 1, shift, Kadd, modindices, rowno[level], bound1, bound2);
	}
}
void process_constraint_recursive(lprec		*MyLP, int* rowno, double* row, int_64 B, int level, int shift, int Kadd)
{
	if (level == 0) {
		rowno[level] = int(B + shift);
		add_constraintex(MyLP, Kadd, row + 1, rowno, EQ, row[0]);
		return;
	}
	for (int j = 0, i = 0; i <= level; i++){
		int_64 A = setfromkey(card2bitm[i + B]);

		while (Removei_th_bitFromSet(&A, j++));

		card2bitm[i + B] = mtokey(card2bitm[i + B], j - 1);

		rowno[level] = int(i + B + shift);
		process_constraint_recursive(MyLP, rowno, row, bit2cardm[A], level - 1, shift, Kadd);
	}
}

void process_constraint_start(lprec		*MyLP, int n, int Kadd, int shift, double KConst, int* rowno, double* row, int low, int up, set<pair<int, int> >& modindices, double bound1, double bound2)
{
	int k = 0;
	row[0] = KConst;
	rowno[0] = 0;
	for (int i = 1; i <= Kadd; i++) row[i] = 1;

	while (k < up-low){
		for (int i = 0; i < 1; i++){
			process_constraint_recursive(MyLP, rowno, row, low + k + i, Kadd - 1, shift, Kadd, modindices, -1, bound1, bound2);
		}
		k += Kadd;
	}
}
void process_constraint_start(lprec		*MyLP, int n, int Kadd, int shift, double KConst, int* rowno, double* row, int low, int up)
{
	int k = 0;
	row[0] = KConst;
	rowno[0] = 0;
	for (int i = 1; i <= Kadd; i++) row[i] = 1;

	while (k < up - low){
		for (int i = 0; i < 1; i++){
			process_constraint_recursive(MyLP, rowno, row, low + k + i, Kadd - 1, shift, Kadd);
		}
		k += Kadd;
	}
}
int DeterminePos(int_64 C, int_64 B, int_64 A,  int card)
{
	int_64  C1=C;
	for (int i = 0; i < card; i++){
		int k = varfromkey(card2bitm[B+i]);
		//A = setfromkey(card2bitm[B + i]); // this can be done once only at the start
		AddToSet(&C1, k);
		//if (prev == k) return i;
		if (C1 == A) return i;
		C1 = C;
	}
	return -1;
}

int	FuzzyMeasureFitLPKinteractiveMarginal(int n, int_64 m, int K, int Kadd, double *v, double* XYData, int options,
	double* indexlow, double* indexhigh, int option1, double* orness, double KConst) {

	unsigned int i, j, k, res;
	int result;
	int_64 A,B,C;
	lprec		*MyLP;
	unsigned int RowsR;// , RowsC1;

	// calculate how many rows/columns we need

	if (Kadd >= n) {
		Kadd = n-1 ; KConst = 1;
	}
	if (Kadd == n - 1) KConst = 1;

	if (option1 == 1 && KConst > (Kadd + 1.) / n) KConst = (Kadd + 1.) / n;
	if (option1 == 2 && KConst < (Kadd + 1.) / n) KConst = (Kadd + 1.) / n;

	RowsR = K * 2; //RowsC = n + RowsC1;  /// removed *2

	unsigned int RowsC3 = (cardposm[Kadd+1]); // position of the  last cardinality

	double *row;
	int	 *rowno;
	row = new double[n+4];
	rowno = new int[n+4];
	int* ind = new int[n];
	set<pair<int, int> > modindices;

	MyLP = make_lp(0, RowsR + RowsC3-1);
	set_add_rowmode(MyLP, TRUE);

//	set_verbose(MyLP, 3);
	double factor; if (Kadd < n - 1) factor = (1.0 - KConst) / (n - Kadd - 1); else factor = 0;

	if (option1==2) // sub/supermodularity constraints
		process_constraint_start(MyLP, n, Kadd+1, (2 * K) , KConst, rowno, row, cardposm[Kadd ], cardposm[Kadd+1 ], modindices,  factor, 1.0);  // sub
	else if (option1 == 1)
		process_constraint_start(MyLP, n, Kadd + 1, (2 * K), KConst, rowno, row, cardposm[Kadd], cardposm[Kadd + 1], modindices, 0.0, factor);  //super
	else 
		process_constraint_start(MyLP, n, Kadd + 1, (2 * K), KConst, rowno, row, cardposm[Kadd], cardposm[Kadd + 1]);


	// the first K columns
	rowno[0] = 0;

	for (k = 0; k<(unsigned int)K; k++) {
		//rowno[0] is the obj. function
		row[0] = XYData[k*(n + 1) + n];//y[k]; //
		rowno[0] = 0;

		myiota(ind, ind + n, 0);  // found in <numeric>
		sort(ind, ind + n, compare_indirect_index <double*>(&(XYData[k*(n + 1)])));

		if (n - Kadd - 1 >= 0)
		for (i = 0; i < (unsigned int)(n - Kadd - 1); i++) {
			row[0] -= factor* ((&(XYData[k*(n + 1)]))[ind[n - i - 1]]);
		}
//		row[0] -= ((&(XYData[k*(n + 1)]))[ind[Kadd]])*KConst;


		/// minus sum of g_A over all subsets whose m(A)=1, at the very least m(N)=1
		//for (A = RowsC + 1; A<m; A++) row[0] -= maxf(0, min_subset(&(XYData[k*(n + 1)]), n, card2bit[A]) - max_subset_complement(&(XYData[k*(n + 1)]), n, card2bit[A]));  ///?????

		rowno[1] = k + 1; rowno[2] = k + 1 + K;
		row[1] = -1; row[2] = 1;
		A = 0;
		for (i = 0; i <= (unsigned int)Kadd; i++){
			row[3 + i] = ((&(XYData[k*(n + 1)]))[ind[ i ]]);
			C = A;
			AddToSet(&A, ind[i]);
			B = bit2cardm[A];
			if (i > 0) j = DeterminePos(C, B, A,  i+1); else j = 0;
			rowno[3 + i] = int( B + j + K * 2 ) ;
		}

		add_constraintex(MyLP, Kadd + 3, row + 1, rowno + 1, EQ, row[0]);
	}
	for (i = 1; i <= RowsR; i++) {
		set_obj(MyLP, i, 1.0);
	}

	set<pair<int, int> >::iterator is;

	if (option1 == 1) // supermodular
	for (is = modindices.begin(); is != modindices.end(); is++){
		rowno[1] = is->first;
		rowno[2] = is->second;
		row[1] = -1;
		row[2] = 1;
		add_constraintex(MyLP, 2, row + 1, rowno + 1, LE,0);
	}
	else if (option1 == 2) // submodular
	for (is = modindices.begin(); is != modindices.end(); is++){
		rowno[1] = is->first;
		rowno[2] = is->second;
		row[1] = 1;
		row[2] = -1;
		add_constraintex(MyLP, 2, row + 1, rowno + 1, LE, 0);
	}
	modindices.clear();


	set_add_rowmode(MyLP, FALSE);

	int RR = get_Nrows(MyLP);
	int CC = get_Ncolumns(MyLP);

	//	set_maxim(MyLP); // well, we always do that
	set_minim(MyLP);


	double *sol = (double*)malloc(sizeof(double)*(1 + RR + CC));

//	write_lp(MyLP, "model.lp");
//	cout << "finished building LP " << RR << " " << CC << endl;
//	set_outputfile(MyLP, "log.txt");
//	print_lp(MyLP);


	res = solve(MyLP);
	double minval=0;

	if (res == OPTIMAL) {
		//		temp=0;
		//		get_dual_solution(MyLP, sol);
		get_primal_solution(MyLP, sol);

//		print_solution(MyLP, 1);
//			for (i = 0; i < RR + 1 + CC; i++) cout << sol[i] << endl;

		minval = get_objective(MyLP);  // minimum
//		cout << " min value " << minval << " " << res << endl;
		
		v[0] = 0;// always !!
		//singletons
		for (i = 1; i <=(unsigned int) n; i++)
		{
			v[card2bitm[i]] = sol[i + RowsR + RR];
		}
		k = n + RowsR + RR+1;
		for (i = 2; i <= (unsigned int) Kadd+0; i++){
			for (B = 0; B < int_64(cardposm[i] - cardposm[i - 1]); B += i){
				C=A = setfromkey(card2bitm[B + cardposm[i - 1]]);
				j = varfromkey(card2bitm[B + cardposm[i - 1]]);
				RemoveFromSet(&A, j);
				v[C] = sol[k] + v[A];
				k+=i;
			}
		}
		
		v[m-1] = 1;
		
		for (int_64 ii = cardpos[Kadd] ; ii < m; ii++){
			j = card[card2bit[ii]];
			if (Kadd<n - 1)
				v[card2bit[ii]] = KConst + (j - Kadd - 1.0)*(1. - KConst) / (n - Kadd - 1);
			else v[card2bit[ii]] = 1;
		}
		
		result = 1;
	} // no optimal
	else result = 0;

	// should I convert to cardinality ordering? by swapping? cyclical swapping


	// just to cheat the compiler
	minval = minval + 1;
	delete[] row;
	delete[] rowno;
	delete[] ind;

	free(sol);
	delete_lp(MyLP);
	return result;
	///return 0;
}




int	FuzzyMeasureFitLPKinteractiveMarginalMaxChain(int n, int_64 m, int K, int Kadd, double *v, double* XYData, int options,
	double* indexlow, double* indexhigh, int option1, double* orness, double KConst) {

	unsigned int i, j, k, res;
	int result;
	int_64 A, B;
	lprec		*MyLP;
	unsigned int RowsR, RowsC, RowsC1;

	//	valindex *tempyk;
//	double temp;

	vector<double> coefs;
	vector<int_64> indices, indices1;
	set<pair<int, int> > modindices;

	// calculate how many rows/columns we need

	if (Kadd >= n) {
		Kadd = n - 1; KConst = 1;
	}
	if (Kadd == n - 1) KConst = 1;
	if (option1 == 1 && KConst > (Kadd + 1.) / n) KConst = (Kadd + 1.) / n;
	if (option1 == 2 && KConst < (Kadd + 1.) / n) KConst = (Kadd + 1.) / n;


	RowsC1 = (cardpos[Kadd] - n - 1); //how many non-singletons   ///Check this mu(0)=0. Also fewer variables as all are positive
	RowsR = K * 2; RowsC = n + RowsC1;  /// removed *2
//	unsigned int RowsC2 = (cardpos[Kadd - 1]); // position of the second last cardinality
	unsigned int RowsC3 = (cardpos[Kadd]); // position of the second last cardinality


//	unsigned int itemp = RowsC + 2 + 1; // just the max number of entries per column

	double *row;
	int	 *rowno;
	row = new double[n + 4];
	rowno = new int[n + 4];
	int* rownoSave = new int[n + 4];
	double* rowSave = new double[n + 4];
	int* ind = new int[n];

	multimap<int_64, int> SetIndex;
	multimap<int, int_64> CardSet;
	Mymap MyMap;
	string S;
	S.assign(Kadd, 'a');


	// the first K columns
	rowno[0] = 0;
	double factor; if (Kadd < n - 1) factor = (1.0 - KConst) / (n - Kadd - 1); else factor = 0;
	double bound1=0, bound2=0;

	if (option1 == 2) // sub/supermodularity constraints
	{
		bound1 = factor; bound2 = 1.0;
	}// sub
	else if (option1 == 1)
	{
		bound1 = 0.0; bound2= factor;
	} //super


	for (k = 0; k<(unsigned int)K; k++) {
		//rowno[0] is the obj. function
		row[0] = XYData[k*(n + 1) + n];//y[k]; //


		myiota(ind, ind + n, 0);  // found in <numeric>
		sort(ind, ind + n, compare_indirect_index <double*>(&(XYData[k*(n + 1)])));

		if (n - Kadd - 1 >= 0)
		for (i = 0; i < (unsigned int)(n - Kadd - 1); i++) {
			row[0] -= factor* ((&(XYData[k*(n + 1)]))[ind[n - i - 1]]);
//			temp = ((&(XYData[k*(n + 1)]))[ind[n - i - 1]]);
		}
		//		row[0] -= ((&(XYData[k*(n + 1)]))[ind[Kadd]])*KConst;

		coefs.push_back(row[0]);
		indices.push_back(0);

		AddVarsConstraints(n, m, Kadd, MyMap, ind, KConst, coefs, indices, indices1, (&(XYData[k*(n + 1)])));
	}

	RowsC = int(MyMap.size());

	MyLP = make_lp(0, RowsR + RowsC);
	set_add_rowmode(MyLP, TRUE);
	//	MyLP = make_lp(RowsR + RowsC, 0); ///??????? w dont know the number of variables yet. reserve or not?
	//	MyLP->do_presolve = FALSE;
//	set_verbose(MyLP, 3);
	for (i = 1; i <= RowsR; i++) {
		set_obj(MyLP, i, 1.0);
	}

	for (k = 0; k < (unsigned int)K; k++){
		rowno[1] = k + 1;  // 1-based
		rowno[2] = k + 1 + K;
		row[1] = -1;
		row[2] = 1;
		j = (Kadd + 2)*k;
		row[0] = coefs[j];
		rowno[0] = int(indices[j]);
		for (i = 0; i <= (unsigned int)Kadd; i++){
			row[3 + i] = coefs[i + j + 1];
			rowno[3 + i] = int(indices[i + j + 1] + K * 2 + 1);
		}
		add_constraintex(MyLP, Kadd + 3, row + 1, rowno + 1, EQ, row[0]);
	}

	unordered_set<int> redundant;
	int parent;
	for (k = 0; k < (unsigned int)K; k++){

		parent = -1;

		j = (Kadd + Kadd + 2)*k;
		row[0] = 0;
		rowno[0] = 0;
		for (i = 0; i <= (unsigned int)Kadd; i++){
			row[1 + i] = 1;
			rowno[1 + i] = int(indices1[2 * i + j] + 2 * K + 1);

			row[2 + i] = -1;
			rowno[2 + i] = int(indices1[2 * i + j + 1] + 2 * K + 1);

			if (option1 != 0){
				if (parent >= 0 )  modindices.insert(pair<int, int>(parent, rowno[1 + i]));
				parent = rowno[1 + i];
				if ( i == (unsigned int)Kadd) set_bounds(MyLP, rowno[1 + i], bound1, bound2);
			}

			//if (i > 0)
			{
				memcpy(rownoSave, rowno, (i + 3)*sizeof(int));
				memcpy(rowSave, row, (i + 3)*sizeof(double));
				add_constraintex(MyLP, i + 2, row + 1, rowno + 1, EQ, row[0]);
				memcpy(rowno, rownoSave, (i + 3)*sizeof(int));
				memcpy(row, rowSave, (i + 3)*sizeof(double));
			}
		}

		//  last one, constraint at level Kadd+1,  but if not redundant! check set
		row[0] = 1; rowno[0] = int(indices1[2 * Kadd + j + 1] + 2 * K + 1);

		if (redundant.count(rowno[0]) == 0){
			add_constraintex(MyLP, 1, row, rowno, EQ, KConst);
			redundant.insert(rowno[0]);
		}

	}

	redundant.clear();

	set<pair<int, int> >::iterator is;

	if (option1 == 1) // supermodular
	for (is = modindices.begin(); is != modindices.end(); is++){
		rowno[1] = is->first;
		rowno[2] = is->second;
		row[1] = 1;
		row[2] = -1;
		add_constraintex(MyLP, 2, row + 1, rowno + 1, LE, 0);
	}

	else if (option1 == 2) // submodular
	for (is = modindices.begin(); is != modindices.end(); is++){
		rowno[1] = is->first;
		rowno[2] = is->second;
		row[1] = -1;
		row[2] = 1;
		add_constraintex(MyLP, 2, row + 1, rowno + 1, LE, 0);
	}
	modindices.clear();


	set_add_rowmode(MyLP, FALSE);



	int RR = get_Nrows(MyLP);
	int CC = get_Ncolumns(MyLP);

	//	set_maxim(MyLP); // well, we always do that
	set_minim(MyLP);

	double *sol = (double*)malloc(sizeof(double)*(1 + RR + CC));

//	write_lp(MyLP, "model.lp");
//	cout << "finished building LP " << RR << " " << CC << endl;
	//	set_outputfile(MyLP, "log.txt");
	//	print_lp(MyLP);


	res = solve(MyLP);
	double minval = 0;

	if (res == OPTIMAL) {
		//		temp=0;
		//		get_dual_solution(MyLP, sol);
		get_primal_solution(MyLP, sol);

//		print_solution(MyLP, 1);
		//			for (i = 0; i < RR + 1 + CC; i++) cout << sol[i] << endl;

		minval = get_objective(MyLP);  // minimum

		v[0] = 0;// always !!
		A = 0;
		for (i = 1; i < RowsC3; i++)
		{
			A = card2bit[i];

			auto Ai = MyMap.find(mtokey(A, n));

			if (Ai != MyMap.end()){
				v[i] = sol[Ai->second + RowsR + 1 + RR];  // in row mode we add RR, for dual, we don't
				//				cout << Ai->second + RowsR + 1 << " " << (setfromkey(Ai->first)) << " " << v[i] << endl;			

				//				cout << v[i] << " \t{" << ShowValue(A) << "}" << " \t(" << Ai->second + RowsR + 1  << ")" << endl;
			}
			else v[i] = 0;

			if (1){
				// others??
				for (j = (card[A] >= 2) ? (cardpos[card[A] - 2]) : 0; j <(unsigned int)cardpos[card[A] - 1]; ++j)
				{
					B = card2bit[j];
					if (IsSubset(A, B))
						v[i] = maxf(v[i], v[j]);
					// it looks this is only for superadditive, it should be the other way around for subadditive. Postpone for now.
				}
			}

			//			cout << v[i] << " \t{" << ShowValue(A) << "}" << endl;
		}
		/**/
		/*
		this method will work for "compressed" FM representation to be done in the future. For now expand it into all FM values
		//remainder by cardinality
		for (i = RowsC3; i < RowsC3 + (n - Kadd); i++)
		{
		j = i - RowsC3 + Kadd + 1;
		if (Kadd<n-1)
		v[i] = KConst + (j-Kadd-1.0)*(1. - KConst)/(n-Kadd-1);
		else v[i] = 1;

		}
		*/

		for (int_64 ii = RowsC3; ii < m; ii++){
			j = card[card2bit[ii]];
			if (Kadd<n - 1)
				v[ii] = KConst + (j - Kadd - 1.0)*(1. - KConst) / (n - Kadd - 1);
			else v[ii] = 1;

		}

		result = 1;
	} // no optimal
	else result = 0;

	// just to cheat the compiler
	minval = minval + 1;
	delete[] row;
	delete[] rowno;
	delete[] rownoSave;
	delete[] rowSave;
	delete[] ind;

	free(sol);
	delete_lp(MyLP);
	return result;


//	return 0;
}





/* =====================================================================
The methods below refer to automatic  selection of the value of KConst


*/

double SolveLP(lprec *MyLP, double KConst, int Kadd, int n, int K, int CC, int RowsR, int RowsC2, int RowsC, double* Coefs1, double* Coefs2, double* Coefs3)
{
	double factor = (1.0 - KConst) / (n - Kadd - 1);

	for (int k = 0; k < K; k++){
		double temp = Coefs3[k] - factor*Coefs1[k] - KConst*Coefs2[k];
		set_obj(MyLP, 2 * k + 1, temp);
		set_obj(MyLP, 2 * k + 2, -temp);
	}
	for (int A = RowsC2; A <= RowsC; A++){
		int k = CC - (RowsC - A);
		set_obj(MyLP, k, -KConst);
	}
	for (int i = 1; i <= RowsR; i++) {
		set_rh(MyLP, i, 1.0);
	}

	//	write_lp(MyLP, "model.lp");

	double minval = 0;

	int res = solve(MyLP);

	if (res == OPTIMAL)
		minval = get_objective(MyLP);  // minimum
	else minval = 10e10;

	return minval;

}
int	FuzzyMeasureFitLPKinteractiveAutoK(int n, int_64 m, int K, int Kadd, double *v, double* XYData, int options,
	double* indexlow, double* indexhigh, int option1, double* orness, double* KConst1, int maxiter)

	// in standard representation
	// K for data, Kadd for k-interactive f.m.
	// KConst the bound on the constant K for k-interactive fm

{

	int counter = 0;
	unsigned int i, j, k, res;
	int result;
	int_64 A, B, C;
	lprec		*MyLP, *MyLPSave;
	unsigned int RowsR, RowsC, RowsC1;
	double KConst;
	*KConst1=KConst = 0.1;	

	if (Kadd >= n) {
		Kadd = n - 1; KConst = 1;
	}
	if (Kadd == n - 1) KConst = 1;




	RowsC1 = (cardpos[Kadd] - n - 1); //how many non-singletons   ///Check this mu(0)=0. Also fewer variables as all are positive
	RowsR = K * 2; RowsC = n + RowsC1;  /// removed *2
	unsigned int RowsC2 = (cardpos[Kadd - 1]); // position of the second last cardinality


	MyLP = make_lp(RowsR + RowsC, 0);
	MyLP->do_presolve = FALSE;
	set_verbose(MyLP, 0);
	unsigned int itemp = RowsC + 2 + 1; // just the max number of entries per column

	double *row;
	int	 *rowno;
	row = new double[itemp];
	rowno = new int[itemp];
	int* ind = new int[n];

	double *Coefs1 = new double[K];
	double *Coefs2 = new double[K];
	double *Coefs3 = new double[K];





	// the first K columns
	rowno[0] = 0;
	double factor = (1.0 - KConst) / (n - Kadd - 1);
	for (k = 0; k<(unsigned int)K; k++) {
		//rowno[0] is the obj. function
		row[0] = XYData[k*(n + 1) + n];//y[k]; //
		rowno[0] = 0;

		Coefs3[k] = row[0];
		Coefs1[k] = 0;

		myiota(ind, ind + n, 0);  // found in <numeric>
		sort(ind, ind + n, compare_indirect_index <double*>(&(XYData[k*(n + 1)]))); // decreasing order now

		for (i = 0; i < (unsigned int)(n - Kadd - 1); i++) {
			row[0] -= factor* ((&(XYData[k*(n + 1)]))[ind[n - i - 1]]);
			Coefs1[k] += ((&(XYData[k*(n + 1)]))[ind[n - i - 1]]); // saving
		}
		row[0] -= ((&(XYData[k*(n + 1)]))[ind[Kadd]])*   KConst;

		Coefs2[k] = ((&(XYData[k*(n + 1)]))[ind[Kadd]]);

		//todo not to include 0

		rowno[1] = k + 1;  // 1-based
		rowno[2] = k + 1 + K;
		row[1] = -1;
		row[2] = 1;
		// now the vales of h_A

		itemp = 0;
		for (i = 0; i<(unsigned int)n; i++) {// singletons
			row[2 + itemp + 1] = maxf(0, XYData[k*(n + 1) + i] - max_subset_complement(&(XYData[k*(n + 1)]), n, card2bit[i + 1]));
			rowno[2 + itemp + 1] = RowsR + i + 1;
			if (row[2 + itemp + 1] != 0) {
				counter++; itemp++;
			}
		}



		for (i = 0; i<RowsC1; i++) {
			row[2 + itemp + 1] = maxf(0, min_subset(&(XYData[k*(n + 1)]), n, card2bit[i + 1 + n]) - max_subset_complement(&(XYData[k*(n + 1)]), n, card2bit[i + 1 + n]));      /// new function g_A, need max_subset_complement, also need to move 1s to the RHS with y
			rowno[2 + itemp + 1] = RowsR + n + i + 1;  // was +n in the index

			if (row[2 + itemp + 1] != 0) { counter++; itemp++; }
			//			row[2+i +n + RowsC1+1]= - row[2+i +n+1] ;
			//			rowno[2+i+n + RowsC1+1] = RowsR + n + i +1  + RowsC1;
		}

		add_columnex(MyLP, itemp + 3, row, rowno);
		// now repeat everything, just change the sign
		for (i = 0; i<itemp + 3; i++) row[i] = -row[i];
		add_columnex(MyLP, itemp + 3, row, rowno);
	}

	/// I do not need this as m(N)=1
	// now monotonicity constraints for all |A|>2
	
	for (A = n + 1; A <= RowsC; A++){   ///check if we need <=
		//	cout<<"start subset  "<< A<<endl;
		C = card2bit[A];
		for (i = 0; i<(unsigned int)n; i++) if (IsInSet(C, i)) { ///check if inequality is reverse	
			row[0] = 0; rowno[0] = 0;
			k = 1;
			row[k] = 1;
			rowno[k] = int(A + RowsR);
			k++;
			B = C;
			RemoveFromSet(&B, i);
			row[k] = -1;
			rowno[k] = int(bit2card[B] + RowsR);
			k++;
			add_columnex(MyLP, k, row, rowno);

			counter += k;
		}

	} // A 

	for (A = RowsC2; A <= RowsC; A++){   ///check if we need <=1 ????????????????	
		row[0] = - KConst; rowno[0] = 0;
		//row[0] = 0;
		k = 1;
		row[k] = -1;
		rowno[k] = int(A + RowsR);
		k++;
		add_columnex(MyLP, k, row, rowno);

		counter += k;
	} // i 

	//} // subsets

	// add interaction indices if needed
	/// no orness or other options

	int RR = get_Nrows(MyLP);
	int CC = get_Ncolumns(MyLP);
	for (i = 1; i <= (unsigned int)RR; i++) {
		set_rh(MyLP, i, 0);
		set_constr_type(MyLP, i, LE);
	}

	for (i = 1; i <= RowsR; i++) {
		set_rh(MyLP, i, 1.0);
	}

	set_maxim(MyLP); // well, we always do that

	double *sol = (double*)malloc(sizeof(double)*(1 + RR + CC));

	//	cout << n <<"\t"<<K <<"\t"<<Kadd<<"\t"<< RR << "\t" << CC << "\t"<<counter<<endl;

	//		 write_lp(MyLP, "model.lp");
	//		cout<<"finished building LP "<< RR<< " " <<CC<<endl;
	//		set_outputfile(MyLP, "log.txt");

	//	print_lp(MyLP);

	//  set_verbose(MyLP,5);
	//  set_outputstream(MyLP, stdout);
	//  print_lp(MyLP);
	/// change recovery from the output...


	/* We now do search for KConst */

//	double KConstSave = KConst;
//	double minsave=10e20;
	double minval;

	if (Kadd < n - 1)
		MyLPSave = copy_lp(MyLP); else MyLPSave = NULL;

//	write_lp(MyLP, "model.lp");


// Golden section method=================================================================================

	double Ag = 0.0;  
	double Bg = 1;
	double   G = (-1. + sqrt(5.)) / 2.; //The golden section 

	// Iinitialize variables 
	double tol = (Bg - Ag)*0.0001;
	double alf1 = Ag + (1 - G)*(Bg - Ag);
	double alf2 = Bg - (1 - G)*(Bg - Ag);

	double falf1;
	double falf2;
	res = solve(MyLP);
	if (res == OPTIMAL)
		minval = get_objective(MyLP);  // minimum
	else minval = 10e10;

//	KConstSave = minval;

	if (Kadd == n - 1) goto Lcont; // no need to solve, the only solution is KConst=1


	delete_lp(MyLP);
	MyLP = copy_lp(MyLPSave);
	// setup new LP
	KConst = alf1;
	falf1 = minval = SolveLP(MyLP, KConst, Kadd, n, K, CC, RowsR, RowsC2, RowsC, Coefs1, Coefs2, Coefs3);

	delete_lp(MyLP);
	MyLP = copy_lp(MyLPSave);
	// setup new LP
	KConst = alf2;
	falf2 = minval = SolveLP(MyLP, KConst, Kadd, n, K, CC, RowsR, RowsC2, RowsC, Coefs1, Coefs2, Coefs3);

	for (i = 0; i<(unsigned int) maxiter; i++){

	//	cout << i << endl;
		if (fabs(alf1 - alf2)<tol) goto GoldenExit;
		// Use the left hand interval, if the function value at the
		// right hand golden point is the larger
		if (falf2>falf1) {
			// Shift re-usable results left
			Bg = alf2;
			alf2 = alf1;
			falf2 = falf1;

			// Compute new alf1 and function value
			alf1 = Ag + (1 - G)*(Bg - Ag);

			delete_lp(MyLP);
			MyLP = copy_lp(MyLPSave);
			KConst = alf1;
			falf1 = minval = SolveLP(MyLP, KConst, Kadd, n, K, CC, RowsR, RowsC2, RowsC, Coefs1, Coefs2, Coefs3);
		}

		// otherwise, use the right hand interval
		else if (falf2 < falf1) {
			// Shift re-usable results left
			Ag = alf1;
			alf1 = alf2;
			falf1 = falf2;
			// Compute new Alpha2 and function value
			alf2 = Bg - (1 - G)*(Bg - Ag);

			delete_lp(MyLP);
			MyLP = copy_lp(MyLPSave);
			KConst = alf2;
			falf2 = minval = SolveLP(MyLP, KConst, Kadd, n, K, CC, RowsR, RowsC2, RowsC, Coefs1, Coefs2, Coefs3);

		}
		else { //==
			KConst = alf1;
		}
	}  // Golden section loop

	GoldenExit: 
	// Return the midpoint of the interval when it is small enough 
	KConst = (alf1 + alf2) / 2;
	*KConst1 = KConst;

	/*
	int iter = 0;
		res = solve(MyLP);
		if (res == OPTIMAL)
			minval = get_objective(MyLP);  // minimum
		else minval = 10e10;

		if (minval<minsave){ minsave = minval; KConstSave = KConst; }

	while (1){

		if (iter > 5){
			KConst = KConstSave;
			goto Lcont;
		}

		delete_lp(MyLP);
		MyLP = copy_lp(MyLPSave);

		// setup new LP
		KConst = 0.1*(iter+1);
		factor = (1.0 - KConst) / (n - Kadd - 1);

		minval= SolveLP(MyLP,  KConst,  Kadd,  n,  K,  CC,  RowsR,  RowsC2,  RowsC,  Coefs1, Coefs2,  Coefs3);
		if (minval<minsave){ minsave = minval; KConstSave = KConst; }

//		write_lp(MyLP, "model.lp");
		iter++;
	}


	*/







	delete_lp(MyLP);
	MyLP = copy_lp(MyLPSave);

	// setup new LP
	factor = (1.0 - KConst) / (n - Kadd - 1);

	for (k = 0; k < (unsigned int)K; k++){
		double temp = Coefs3[k] - factor*Coefs1[k] - KConst*Coefs2[k];
		set_obj(MyLP, 2 * k + 1, temp);
		set_obj(MyLP, 2 * k + 2, -temp);
	}
	for (A = RowsC2; A <= RowsC; A++){
		k = CC - (RowsC - (int) A);
		set_obj(MyLP, k, -  KConst);
	}
	for (i = 1; i <= RowsR; i++) {
		set_rh(MyLP, i, 1.0);
	}

//	write_lp(MyLP, "model.lp");


	res = solve(MyLP);
Lcont:;
	if (res == OPTIMAL) {
		//		temp=0;
		get_dual_solution(MyLP, sol);
		//		print_solution(MyLP, 1);
		minval = get_objective(MyLP);  // minimum

		//	   for (i = 0; i < RR + 1 ; i++) cout << sol[i] << endl;
		//		cout<<" min value "<<minval<<" "<<res<<endl;

		v[0] = 0;// always !!
		for (i = 1; i <= (unsigned int)n; i++)
		{
			v[i] = sol[i + RowsR]; // singletons
		}
		for (i = 0; i<RowsC1; i++)
		{
			v[i + n + 1] = sol[n + RowsR + 1 + i]; ////- sol[n+RowsR+1 + RowsC1+i]; // other subsets
			k++;
		}
		k = n + RowsC1 + 1;

		for (int_64 ii = k; ii < m; ii++){
			j = card[card2bit[ii]];
			if (Kadd<n - 1)
				v[ii] = KConst + (j - Kadd - 1.0)*(1. - KConst) / (n - Kadd - 1);
			else v[ii] = 1;

		}

		result = 1;
	} // no optimal
	else result = 0;

	*KConst1 = KConst;
	// just to cheat the compiler
	minval = minval + 1;
	delete[] row;
	delete[] rowno;
	delete[] ind;
	delete[] Coefs1;
	delete[] Coefs2;
	delete[] Coefs3;

	free(sol);
	delete_lp(MyLP);
	delete_lp(MyLPSave);
	return result;
}





