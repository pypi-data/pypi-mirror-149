

#include<vector>
#include <map>
#include<random>
#include<iostream>
#include <fstream>
#include<algorithm>
#include <string>
#include <unordered_map>
#include "fuzzymeasuretools.h"

#include "fmrandom.h"

#define NO_R

using namespace std;




std::uniform_real_distribution<double> distribution(0.0, 1.0);



random_device rd;
mt19937 rng(rd());    // random-number engine used (Mersenne-Twister in this case)



template <class T> struct prec : binary_function <T, T, bool> {
	bool operator() (const T& x, const T& y) const { return x < y; }
};
template <class T> struct succ : binary_function <T, T, bool> {
	bool operator() (const T& x, const T& y) const { return x < y; }
};
// These definitions can be changed to support other data types. They sin in the .h file

//typedef uint16_t myint;
//typedef unsigned int myint;
//typedef int_64 myint;
//typedef unsigned int uint;
//typedef float  myfloat;





// the functions below are for encoding an array into strings to be used as keys in unordered_map structure (hash keys)
typedef unsigned char BYTE;

std::string base64_encode(BYTE const* buf, unsigned int bufLen);
std::vector<BYTE> base64_decode(std::string const&);

static const std::string base64_chars =
"ABCDEFGHIJKLMNOPQRSTUVWXYZ"
"abcdefghijklmnopqrstuvwxyz"
"0123456789+/";


static inline bool is_base64(BYTE c) {
	return (isalnum(c) || (c == '+') || (c == '/'));
}

std::string base64_encode(BYTE const* buf, unsigned int bufLen) {
	std::string ret;
	int i = 0;
	int j = 0;
	BYTE char_array_3[3];
	BYTE char_array_4[4];

	while (bufLen--) {
		char_array_3[i++] = *(buf++);
		if (i == 3) {
			char_array_4[0] = (char_array_3[0] & 0xfc) >> 2;
			char_array_4[1] = ((char_array_3[0] & 0x03) << 4) + ((char_array_3[1] & 0xf0) >> 4);
			char_array_4[2] = ((char_array_3[1] & 0x0f) << 2) + ((char_array_3[2] & 0xc0) >> 6);
			char_array_4[3] = char_array_3[2] & 0x3f;

			for (i = 0; (i < 4); i++)
				ret += base64_chars[char_array_4[i]];
			i = 0;
		}
	}

	if (i)
	{
		for (j = i; j < 3; j++)
			char_array_3[j] = '\0';

		char_array_4[0] = (char_array_3[0] & 0xfc) >> 2;
		char_array_4[1] = ((char_array_3[0] & 0x03) << 4) + ((char_array_3[1] & 0xf0) >> 4);
		char_array_4[2] = ((char_array_3[1] & 0x0f) << 2) + ((char_array_3[2] & 0xc0) >> 6);
		char_array_4[3] = char_array_3[2] & 0x3f;

		for (j = 0; (j < i + 1); j++)
			ret += base64_chars[char_array_4[j]];

		while ((i++ < 3))
			ret += '=';
	}

	return ret;
}

std::vector<BYTE> base64_decode(std::string const& encoded_string) {
	int in_len = (int) encoded_string.size();
	int i = 0;
	int j = 0;
	int in_ = 0;
	BYTE char_array_4[4], char_array_3[3];
	std::vector<BYTE> ret;

	while (in_len-- && (encoded_string[in_] != '=') && is_base64(encoded_string[in_])) {
		char_array_4[i++] = encoded_string[in_]; in_++;
		if (i == 4) {
			for (i = 0; i < 4; i++)
				char_array_4[i] = (BYTE)base64_chars.find(char_array_4[i]);

			char_array_3[0] = (char_array_4[0] << 2) + ((char_array_4[1] & 0x30) >> 4);
			char_array_3[1] = ((char_array_4[1] & 0xf) << 4) + ((char_array_4[2] & 0x3c) >> 2);
			char_array_3[2] = ((char_array_4[2] & 0x3) << 6) + char_array_4[3];

			for (i = 0; (i < 3); i++)
				ret.push_back(char_array_3[i]);
			i = 0;
		}
	}

	if (i) {
		for (j = i; j < 4; j++)
			char_array_4[j] = 0;

		for (j = 0; j < 4; j++)
			char_array_4[j] = (BYTE)base64_chars.find(char_array_4[j]);

		char_array_3[0] = (char_array_4[0] << 2) + ((char_array_4[1] & 0x30) >> 4);
		char_array_3[1] = ((char_array_4[1] & 0xf) << 4) + ((char_array_4[2] & 0x3c) >> 2);
		char_array_3[2] = ((char_array_4[2] & 0x3) << 6) + char_array_4[3];

		for (j = 0; (j < i - 1); j++) ret.push_back(char_array_3[j]);
	}

	return ret;
}



// m1 is for reversing sign of the relation, for dual capacities
int preceeds(myint i, myint j, int m1)
{
	myint b = i & j;
	if (b == i) // i subset of j
	{
		if (bitweight(int_64(~i & j)) == 1) return m1 * 1;
	}
	if (b == j)
	{
		if (bitweight(int_64(~j & i)) == 1) return -1 * m1;
	}
	return 0;
}

int preceedsP(myint i, myint j, myint r, int m1)
{
	//	if(j==r) return 1;
	//	if(i==r) return -1;   //  ?????????????   
	return preceeds(i, j, m1);
}

int preceedsa(myint i, myint j, int m1)
{
	myint b = i & j;
	if (b == i) // i subset of j
	{
		return 1 * m1;
	}
	if (b == j)
	{
		return -1 * m1;
	}
	return 0;
}

int preceedsaP(myint i, myint j, myint r, int m1)
{
	if (j == r) return 1 * m1;
	if (i == r) return -1 * m1;
	return preceedsa(i, j, m1);
}

//does not seem to work
inline bool preceedsB(myint i, myint j)
{
	// return 1 if i subset of j
	return ((i & j) == i);
}
inline double sqr(double a) { return a * a; }


int preceeds_convex(myint i, myint j, int m1)
{// i does not preceed j lexicographically
	myint b = i & j;

	if (b == i) // i subset of j
	{
		int_64 c = int_64(~i & j);
		if ((bitweight(c) == 1) && (i > c)) return 1 * m1;
	}
	if (b == j)
	{
		int_64 c = int_64(~j & i);
		if ((bitweight(c) == 1) && (j > c)) return -1 * m1;
	}
	return 0;
}
int preceeds_convexa(myint i, myint j, int m1)
{// i does not preceed j lexicographically
	myint b = i & j;

	if (b == i) // i subset of j
	{
		int_64 c = int_64(~i & j);
		if ((i > c)) return 1 * m1;
	}
	if (b == j)
	{
		int_64 c = int_64(~j & i);
		if ((j > c)) return -1 * m1;
	}
	return 0;
}

int preceedsPconvex(myint i, myint j, myint r, int m1)
{
	if (j == r) return 1 * m1;
	if (i == r) return -1 * m1; //??????
	return preceeds_convex(i, j, m1);
}


// Data structure to store graph edges
struct Edge {
	myint src, dest;
};

// Class to represent a graph object
class Graph
{
public:
	// construct a vector of vectors to represent an adjacency list
	vector<vector<myint> > adjList;

	// Graph Constructor
	Graph(vector<Edge> const &edges, int N)
	{
		// resize the vector to N elements of type vector<int>
		adjList.resize(N);

		// add edges to the Directed graph
		for (auto &edge : edges)
			adjList[edge.src].push_back(edge.dest);
	}
	void clear()
	{
		for (auto gi = adjList.begin();gi < adjList.end();gi++)
			gi->clear();

		adjList.clear();
	}
};

// Perform DFS on graph and set departure time of all
// vertices of the graph
void DFS(Graph const &graph, int v, vector<bool> &discovered, vector<int> &departure, int& time)
{
	// mark current node as discovered
	discovered[v] = true;

	// set arrival time
	time++;

	// do for every edge (v -> u)
	for (int u : graph.adjList[v])
	{
		// u is not discovered
		if (!discovered[u])
			DFS(graph, u, discovered, departure, time);
	}

	departure[time] = v;
	time++;
}

// performs Topological Sort on a given DAG
void doTopologicalSort(Graph const& graph, int N, vector<myint>& v, vector<myint>& v1)
{
	// departure stores the vertex number using departure time as index
	vector<int> departure(2 * N, -1);
	
	// stores vertex is discovered or not
	vector<bool> discovered(N);
	int time = 0;


	for (int i = 0; i < N; i++)
		if (!discovered[i])
			DFS(graph, i, discovered, departure, time);

	// Print the vertices in order of their decreasing
	// departure time in DFS i.e. in topological order
	for (int i = 2 * N - 1; i >= 0; i--) {
		if (departure[i] != -1)
		{
			v.push_back(v1[departure[i]]);
		}
	}
}

void DoMarkovChain(vector<myint>& v, int k, myint r, int m1)
{
#ifndef NO_R
    unif_R_class<int> uni(0, (int)v.size() - 2);
#else	
	uniform_int_distribution<int> uni(0, (int)v.size() - 2); // guaranteed unbiased
#endif
	for (int j = 0;j < k; j++)
	{
		//if(coin(rng))
		{
			int pos = uni(rng);
			if (preceedsa(v[pos], v[pos + 1], m1) == 0)  //was preceedsaP(v[pos] , v[pos+1], r)
				std::swap(v[pos], v[pos + 1]);
		}
	}


}
void DoMarkovChainConvex(vector<myint>& v, int k, myint r, int m1)
{
#ifndef NO_R
    unif_R_class<int> uni(0, (int)v.size() - 2);
#else	
	uniform_int_distribution<int> uni(0, (int)v.size() - 2); // guaranteed unbiased
#endif
	for (int j = 0;j < k; j++)
	{
		{
			int pos = uni(rng);
			if (preceeds_convexa(v[pos], v[pos + 1], m1) == 0)  //was preceedsaP(v[pos] , v[pos+1], r)
				std::swap(v[pos], v[pos + 1]);
		}
	}
}

/*  construct binary lattrices and other posets for k-interactive capacities */

#include "binarylattice.h"



/* Combarro, Diaz method included here
*/

#include "minimalsplus.h"


void random_coefficients(int n, vector<myfloat> & c)
//Generates a vector of n random real numbers 1=X1>=X1>=...>=Xn=0
{
#ifndef NO_R
    unif_R_class<double> dis(0.0, 1.0);
#else
	uniform_real_distribution<> dis(0.0, 1.0);
#endif
	


	//c[0] = 1.0;
	//c[1] = 0.0;
	for (int i = 0; i < n; i++)
		c[i] = (myfloat)dis(rng);

	sort(c.begin(), c.end(), greater<myfloat>());
}



int fm_arraysize(int m, int_64 n, int kint)
{
	// calculates the number of parameers needed in cardinal representation for kinteractive capacity

	int extra = m - kint;
	if (kint >= m) extra = 0;
	// count the number of items as the sum of Cin

	int r = 1;
	for (int i = 1;i <= kint; i++)
		r += (int)(choose(i, m));

	r += extra;  // for emptyset
	return r;
}

int fm_arraysize_kadd(int n,  int k)
{
	// calculates the number of parameers needed in cardinal representation for kadditive capacity

	// count the number of items as the sum of Cin
	int r = 1; // for emptyset
	for (int i = 1;i <= k; i++)
		r += (int)(choose(i, n));
	return r;
}

myfloat fm_delta(int m, int kint, myfloat K)
{  // delta is the fixed marginal contribution in the k-interactive fuzzy measures
//	if (m == (kint + 1)) return (myfloat)(1.0 - K);
	if (m <= kint + 1) return 0;
	return (myfloat)(1.0 - K) / (m - kint - 1);
}


int fm_arraysize_convex(int m, int_64 n, int kint)
{
	// calculates the number of parameers needed in cardinal representation for kinteractive capacity

	int extra = m - kint;
	if (kint >= m) extra = 0;
	// count the number of items as the sum of Cin

	int r = 1;
	for (int i = 1;i <= kint; i++)
		r += (int)(choose(i, m));

	r += extra;  // for emptyset
	return r;
}

int generate_fm_minplus(int_64 num, int m, int kint, int markov, int option, myfloat K, myfloat * vv)
{
	/* generates num random vectors representing kinteractive fuzzy measures of m arguments in cardinality ordering
	uses markov iterations of markov chain
	kint and K are parameters for k-interactivity
	option reserved, unused
	vv output, needs to be allocated by the calling routine, which also needs to call Preparations_FM(m, &n);
	method: uses minimalsPlus algorithm by Combarro et al followed by Markov chain
	*/
	unordered_map<string, myint> mymap;

	int_64 n = (int_64)1 << m; //Number of coefficients of the fuzzy measure
	int r;

	r = (int)n;// initially for compatibility

//	Preparations_FM(m, &n); in the calling routine
	if (kint >= m) kint = m - 1;
	int arraysize = fm_arraysize(m, n, kint);
	myfloat delta = fm_delta(m, kint, K);

	vector<bool> P = booleanlatticerestricted(m, kint, r);

	//	vector<bool> PNR = booleanlatticerestrictednonredundant(m, kint, r);

		/* for minplus */
	/*
		vector<float> A((int)n*m*r);
		vector<float> b(m*r);
		vector<int> dir(m*r);

		int numcon = convertintomatrix(PNR, A, b, dir, r);

		cout << numcon << endl;
		*/

	int j1, j;

	int length = r - 1;// no need 0 and 1, but the  top one is needed. Although ay be not, but just leave it for now.

	vector<myint> w = losw(P, r);

	// for counting linear xtensions
	string s5, s6;
	std::vector<BYTE> decodedData1;

	vector<myint> v1;

	for (auto i = 0;i < length;i++) v1.push_back((myint) card2bit[i + 1]);

	vector<myfloat> coef(length);

	for (int_64 i = 0; i < num; i++)
	{
		vector<myint> le = minimals_w(P, w, r);

		vector<myint> new_le = markovKKclassic(P, r, le, markov);

		/*  this is for counting different linear extensions
		s5 = base64_encode((BYTE *)&new_le[0], length * sizeof(myint));
		unordered_map<string, myint>::iterator it = mymap.find(s5);
		if (it != mymap.end())
			it->second++; else
			mymap[s5] = 1;
		*/
		/**/
		random_coefficients(length, coef);

		// generate on simplex
		vv[i* arraysize + 0] = 0; //emptyset
		for (j = 0;j < length;j++) vv[i* arraysize + new_le[j]] = coef[j] * K;
		for (j = arraysize - 1, j1 = m; j1 >= kint + 1; j--, j1--) vv[i*arraysize + j] = (myfloat)(1.0 - delta * (m - j1));
		/**/

	}

	return 0;
}


int generate_fm_2additive_convex(int_64 num, int n, int * size, myfloat * vv)
{
	//int_64 m = (int_64)1 << m;

	int r = 0;
	for (int i = 1;i <= 2; i++)
		r += (int)(choose(i, n));
	*size = r;

	// here we just generate the Mobius transform on the unit simplex
	vector<myfloat>  temp(r - 1);

	for (int_64 i = 0;i < num;i++) {

		random_coefficients(r - 1, temp);  //decreasing sequence
		vv[i*r] = 1 - temp[0];
		for (int j = 1;j < r - 1;j++)
			vv[i*r + j] = temp[j - 1] - temp[j];
		vv[i*r + r - 1] = temp[r - 2];

	}

	return *size;
}


int generate_fm_2additive_convex_withsomeindependent(int_64 num, int m, int * size, myfloat * vv)
{
	// as above, but now we also set randomly some interactions to 0 and re-normalise
	generate_fm_2additive_convex(num, m, size, vv);

#ifndef NO_R
    unif_R_class<int> uni(m, *size);
#else	
	uniform_int_distribution<int> uni(m, *size); // guaranteed unbiased
#endif

	double t = 0;
	for (int_64 i = 0;i < num;i++) {
		t = 0;
		// randomly set some selection of components of pairs to 0
		// how many?
		for (int j = 0;j < m;j++)  t += vv[i* *size + j];// singletons

		for (int iter = 0; iter < *size / 2; iter++) {
			int k = uni(rng);
			vv[i * *size + k] = 0;
		}

		for (int j = m;j < *size;j++) {
			t += vv[i* *size + j];// pairs
		}

		t = 1.0 / t; //hope nonzero

		for (int j = 0;j < *size;j++) {
			vv[i* *size + j] *= t;   // all renormalise
		}

	}
	return *size;
}




inline int Cardinality(int_64 A) { return bitweight(A); }



int generate_fm_2additive_concave(int_64 num, int m, int* size, myfloat * vv)
{
	// first generate convex and then take the dual

	generate_fm_2additive_convex(num, m, size, vv);
	vector<myfloat> temp(*size);

	// dual is also 2-additive
	for (int_64 i = 0;i < num;i++) {
		dualMobKadd( &(vv[i* *size]), &(temp[0]), m, *size, 2);

		for (int j = 0;j < *size;j++) vv[i * *size + j] = temp[j]; //copy it to vv
	}

	return *size;
}


int generate_fm_tsort(int_64 num, int m, int kint, int markov, int option, myfloat K, myfloat * vv)
{
	/* generates num random vectors representing kinteractive fuzzy measures of m arguments in cardinality ordering
	uses markov iterations of markov chain
	kint and K are parameters for k-interactivity
	option 1 if using rejection (memory hungry) 0 otherwise
	vv output, needs to be allocated by the calling routine, which also needs to call Preparations_FM(m, &n);

	Method: randomised topological sotring of the preorder to get a linear extension, followed by Markov chain and optionally by rejection mthod,
	which records all generated linear extensions and attempts to reject the ones that have been already seen. Uses reservoir sampling for that.
	*/
	unordered_map<string, myint> mymap;

	int m1 = 1;

	int_64 n = (int_64)1 << m; //Number of coefficients of the fuzzy measure
	int r;

	r = (int)n;// initially for compatibility

	//Preparations_FM(m, &n);  done before in the calling routine

	int dorejection = 0;

	int arraysize = fm_arraysize(m, n, kint);
	myfloat delta = fm_delta(m, kint, K);


	//	vector<bool> P = booleanlatticerestricted(m, kint, r);
	//	vector<bool> PNR = booleanlatticerestrictednonredundant(m, kint, r);
	// We do not need matrix representation of adjacency, just count the number of vertices r
	if (kint >= m) kint = m - 1;
	sizeindependent(m, kint, r);


	vector<myint>  v;

	int length;// = n - 2;
	length = (int)r - 2;// no need 0 and 1, but the  top one is needed. Although may be not, but just leave it for now.

	if (option == 1 && length*num < 20 * 200000) dorejection = 1;

	vector<myint>  v1, v2, v0(length);

	string s5, s6;

	std::vector<BYTE> decodedData1;


	int NN = 0;
	myint i, j1, j;
	double Wei, WeiS, p, u;
	Edge E;
	vector<Edge> edges;

	for (i = 0;i < length;i++) v1.push_back((myint)card2bit[i + 1]);

	vector<myfloat> coef(length);

	for (int_64 j2 = 0;j2 < num;j2++) {

		NN = 0;
		WeiS = 0;
		edges.clear();

		std::shuffle(std::begin(v1), std::end(v1), rng);

		for (i = 0; i < length;i++) {
			for (j = i + 1; j < length;j++)
				if (i != j) switch (preceeds(v1[i], v1[j], m1)) { // was preceedsP(v1[i], v1[j], card2bit[length])
				case 1:
					E.src = i; E.dest = j; edges.push_back(E);
					break;
				case -1:
					E.src = j; E.dest = i; edges.push_back(E);
					break;
					//case 1: on1<<i<<" "<<j<<endl; break;	
					//case -1: on1<<j<<" "<<i<<endl; break;	
				}

		}

		// topological sort here
		Graph graph(edges, length);

		doTopologicalSort(graph, length, v2, v1);
		graph.clear();

		DoMarkovChain(v2, markov, (myint)card2bit[length], m1);

		if (dorejection) {
			s5 = base64_encode((BYTE *)&v2[0], length * sizeof(myint));
			s6 = s5;
			unordered_map<string, myint>::iterator it = mymap.find(s5);
			if (it != mymap.end()) Wei = 1. / sqr(sqr(it->second + 0.4)); else Wei = 1;
			WeiS = Wei;
			//			it->second++; else
			//		mymap[s5]=1;

			for (i = 1;i < length;i++) {
				if (preceedsa(v2[i - 1], v2[i], m1) == 0) {  //was preceedsaP(v2[i - 1], v2[i], card2bit[length])
					NN++;
					std::swap(v2[i - 1], v2[i]);
					s5 = base64_encode((BYTE *)&v2[0], length * sizeof(myint));

					/* reservoir sampling */
					it = mymap.find(s5);
					if (it != mymap.end()) Wei = 1. / sqr(sqr(it->second + 0.4)); else Wei = 1;
					WeiS += Wei;

					p = Wei / WeiS;
					u = distribution(rng);

					if (u <= p) s6 = s5;

					std::swap(v2[i - 1], v2[i]);
				}

			}// for i
			it = mymap.find(s6);
			if (it != mymap.end()) it->second++;
			else
				mymap[s6] = 1;

			//decode s6
			decodedData1 = base64_decode(s6);
			for (i = 0;i < length;i++) v2[i] = *((myint*)(&decodedData1[i * sizeof(myint)]));
		}  // do rejection

		random_coefficients(length, coef);
		// use v2
		vv[j2* arraysize + 0] = 0; //emptyset
//		for (i = 0; i < length; i++) cout<<" "<<bit2card[v2[i]]<<" ";
//		cout << endl;
		for (i = 0; i < length; i++) vv[j2* arraysize + bit2card[v2[i]]] = coef[length - i - 1] * K;
		for (i = arraysize - 1, j1 = m; j1 >= kint + 1; i--, j1--) vv[j2*arraysize + i] = myfloat(1.0 - delta * (m - j1));

		v2.clear();
	}
	//cout<<mymap.size()<<" "<<num<< endl;

	return arraysize;
}


int_64 swapbits(int_64 a, int i, int j)
{
	bool ai = IsInSet(a, i);
	bool aj = IsInSet(a, j);

	if (ai && aj) return a;// do nothing
	if (!ai && !aj) return a;// both 0
	if (ai) { // and not aj then
		RemoveFromSet(&a, i);
		AddToSet(&a, j);
		return a;
	}
	// else aj not ai
	RemoveFromSet(&a, j);
	AddToSet(&a, i);
	return a;
}
int_64 swapbits(int_64 a, vector<int>& perm, int n)
{
	int_64 b = 0;
	for (int i = 0;i < n; ++i)
	{
		if (IsInSet(a, i))
			AddToSet(&b, perm[i]);
	}

	return b;
}


int generate_fmconvexconcave_tsort(int_64 num, int m, int kint, int markov, int option, myfloat K, myfloat * vv, int m1)
{

	/* generates num random vectors representing kinteractive convex (supermodular) fuzzy measures of m arguments in cardinality ordering
	uses markov iterations of markov chain
	kint and K are parameters for k-interactivity
	option 1 if using rejection (memory hungry) for inear extensions 0 otherwise
	option & 0x8 (4th bit set) means we do rejection based on supermodularity
	vv output, needs to be allocated by the calling routine, which also needs to call Preparations_FM(m, &n);

	Method: randomised topological sotring of the preorder to get a linear extension, followed by Markov chain and optionally by rejection mthod,
	which records all generated linear extensions and attempts to reject the ones that have been already seen. Uses reservoir sampling for that.
	*/
	unordered_map<string, myint> mymap;

	int opt1 = (option & 0x1); // just first bit
	int opt8 = (option & 0x8); // 4th bit = means rejection 1000 times

	int_64 n = (int_64)1 << m; //Number of coefficients of the fuzzy measure
	int r;

	r = (int)n;// initially for compatibility

	//Preparations_FM(m, &n);  done before in the calling routine

	int dorejection = 0;
	int counter1 = 0;
	int counter2 = 0;
	int C1lim = 10;
	int C2lim = 1000;
	int mymarkov = markov;
	int mypow = 2;

	int arraysize = fm_arraysize_convex(m, n, kint);
	myfloat delta = fm_delta(m, kint, K);

	// We do not need matrix representation of adjacency, just count the number of vertices r
	if (kint >= m) kint = m - 1;
	sizeindependent(m, kint, r);

	vector<myint>  v;

	int length;
	length = (int)r - 1;// no need 0 but needs 1.



	if (opt1 == 1 && length*num < 20 * 200000) dorejection = 1;

	vector<myint>  v1, v2, v0(length);

	string s5, s6;
	std::vector<BYTE> decodedData1;
	
	int NN = 0;
	myint i, j1, j;
	double Wei, WeiS, p, u;
	Edge E;
	vector<Edge> edges;

	for (i = 0;i < length;i++) v1.push_back((myint)card2bit[i + 1]);

	vector<myfloat> coef(length+1);

	vector<int> perm;
	for (int ii = 0; ii < m; ++ii) perm.push_back(ii);
	vector<int_64> cardbitswapped;
	for (int_64 ii = 0; ii < n; ++ii) cardbitswapped.push_back(card2bit[ii]);

	for (int_64 j2 = 0;j2 < num;j2++) {
		NN = 0;
		WeiS = 0;
		edges.clear();
		mymarkov = markov; mypow = 2;

		std::shuffle(std::begin(v1), std::end(v1), rng);

		for (i = 0; i < length;i++) {
			for (j = i + 1; j < length;j++)
				if (i != j) switch (preceeds_convex(v1[i], v1[j], m1)) {
				case 1:
					E.src = i; E.dest = j; edges.push_back(E);
					break;
				case -1:
					E.src = j; E.dest = i; edges.push_back(E);
					break;
				}
		}

		// topological sort here
		Graph graph(edges, length);

		doTopologicalSort(graph, length, v2, v1);
		graph.clear();

	Repeat:

		DoMarkovChainConvex(v2, mymarkov, (myint)card2bit[length], m1);

		if (dorejection) {
			s5 = base64_encode((BYTE *)&v2[0], length * sizeof(myint));
			s6 = s5;
			unordered_map<string, myint>::iterator it = mymap.find(s5);
			if (it != mymap.end()) Wei = 1. / sqr(sqr(it->second + 0.4)); else Wei = 1;
			WeiS = Wei;
			//			it->second++; else
			//		mymap[s5]=1;

			for (i = 1;i < length;i++) {
				if (preceeds_convexa(v2[i - 1], v2[i], m1) == 0) {
					NN++;
					std::swap(v2[i - 1], v2[i]);
					s5 = base64_encode((BYTE *)&v2[0], length * sizeof(myint));

					/* reservoir sampling */
					it = mymap.find(s5);
					if (it != mymap.end()) Wei = 1. / sqr(sqr(it->second + 0.4)); else Wei = 1;
					WeiS += Wei;

					p = Wei / WeiS;
					u = distribution(rng);

					if (u <= p) s6 = s5;
					std::swap(v2[i - 1], v2[i]);
				}

			}// for i
			it = mymap.find(s6);
			if (it != mymap.end()) it->second++;
			else
				mymap[s6] = 1;

			//decode s6
			decodedData1 = base64_decode(s6);
			for (i = 0;i < length;i++) v2[i] = *((myint*)(&decodedData1[i * sizeof(myint)]));
		}  // do rejection


	L1:;
		random_coefficients(length, coef);
		// these coefficients are in decreasing order and correspond to length-i-1 rather than i
		// use v2
		// normalise sum tops 

		// GB this seems to work for now
		for (i = 0;i < length; i++) // if (!TopElement(v2[i])) 
			if (v2[i] != n - 1) coef[length - i - 1] = pow(coef[length - i - 1] / (m - bitweight(v2[i])), mypow);
		// GB can pow be applied to denominator only?


		myfloat Sum = 0;
		for (i = 0;i < length; i++) {
			if (HasBitsAboveK(v2[i], kint + 1)) coef[length - i - 1] *= delta; // first normalisation
			else if (TopElement(v2[i])) {
				Sum += coef[length - i - 1];
			}
		}
		if (Sum == 0) Sum = 1;
		Sum = K / Sum;
		for (i = 0;i < length; i++)
			if (!HasBitsAboveK(v2[i], kint + 1))
				coef[length - i - 1] *= Sum; // now second normalised

		vv[j2* arraysize + 0] = 0; //emptyset

		// now put them into v and augment with Delta for k-interactivity

		for (i = 0; i < length; i++) vv[j2* arraysize + bit2card[v2[i]]] = coef[length - i - 1];

		// now vv is in the increasin order as it should be

		// Now derivatives in cardinality ordering, translate into the actual capacity values
		for (i = 0; i < length; i++) vv[j2* arraysize + i] += vv[j2*arraysize + bit2card[RemoveHighestBit(card2bit[i], m)]];

				// also need to randomise the singletons after renormalisations
		std::shuffle(perm.begin(), perm.end(), rng);
		
		
		for (int_64 ii = 0; ii < n; ++ii) cardbitswapped[ii] = swapbits(card2bit[ii], perm, m); // initialise

		for (i = 0; i < length; i++)  coef[cardbitswapped[i]] = vv[j2* arraysize + i];

// here can test supermodularity and reject if needed, we have coef in bit ordering, 2 levels of rejection: point in simplex (count1) and the simplex (count2)

		int ret = 0;

		coef[arraysize - 1] = 1;
		if (opt8 && counter2 < C2lim) {
			if (m1 == 1) { if (IsMeasureSupermodular(&(coef[0]), arraysize) != 1) ret = 1; }
			if (m1 == -1) { if (IsMeasureSubmodular(&(coef[0]), arraysize) != 1) ret = 1; }
			if (ret && counter1 < C1lim) { counter1++; goto L1; }
			if (ret) {
				counter2++; counter1 = 0; /*mymarkov = 5000;*/ mypow += 1;  goto Repeat;   // increase aggressiveness of scaling
			} 
			//else
			//	for (i = 0; i < length; i++) cout << coef[i] << " ";
	
		}
		counter2 = 0; counter1 = 0;


		for (i = 0; i < length; i++)  vv[j2* arraysize + bit2card[i]] = coef[i];


		// for kinteractivity
		for (i = arraysize - 1, j1 = m; j1 >= kint + 1; i--, j1--) vv[j2*arraysize + i] = myfloat(1.0 - delta * (m - j1));

		v2.clear();
	}
	return arraysize;
}


int generate_fmconvex_tsort(int_64 num, int m, int markov, int option, myfloat K, myfloat * vv) // no k-interactivity here
{
	return generate_fmconvexconcave_tsort(num, m, m, markov, option, K, vv, 1);
}
int generate_fmconcave_tsort(int_64 num, int m, int markov, int option, myfloat K, myfloat * vv)
{
	return generate_fmconvexconcave_tsort(num, m, m, markov, option, K, vv, -1);
}

int generate_fmconvex_tsort(int_64 num, int m, int kint, int markov, int option, myfloat K, myfloat * vv)
{
	// here generate dual concave kinteractive, then invert
	// this is not yet finished, a placeholder

	return  generate_fmconvex_tsort(num,m,markov,option,K,vv);
}

void export_maximal_chains(int n, int_64 m,  double * v, double * mc)
{
	// there are n! maximal chains (less so for kinteractive fm), the discrete derivatives of fm are expored in mc (n! rows, the length of each is n)
	// by going throgh all permutations of (1,2,...n)
	       
	int i;
	
	vector<int> temp(n);
	for (i = 0;i < n;i++) { temp[i] = i; }
	//auto rng = std::default_random_engine{};
	
	for (int j = 0;j < m_factorials[n];j++) {
		int_64 id = 0; 

		AddToSet(&id, temp[0]);
		double t = v[id];
		mc[j*n+temp[0]] = v[id];
		for (i = 1;i < n;i++) {
			AddToSet(&id, temp[i]);
//			mc[j*n + i] = v[id] - t;
			mc[j*n + temp[i]] = v[id] - t;


			t = v[id];
		}
		// reshuffle
		// is it guaranteed no repeats?
		//std::shuffle(std::begin(temp), std::end(temp), rng);
		std::next_permutation(temp.begin(), temp.end());
	}
}
