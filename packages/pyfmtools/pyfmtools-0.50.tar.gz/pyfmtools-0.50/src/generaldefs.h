
#ifndef NO_R
#define NO_R
#endif
#define _CRT_SECURE_NO_WARNINGS

#if defined  (_WIN32)
#define LIBEXP 	__declspec(dllexport)  
//#include "../stdafx.h"
#else
#define LIBEXP 
#endif

#if defined (MSVC_DLL)
#ifdef FMTOOLS_EXPORTS
#define LIBDLL_API __declspec(dllexport)
#else
#define LIBDLL_API __declspec(dllimport)
#endif
#else
#define LIBDLL_API
#endif

#if defined (_WIN32)
#define mystrncpy(a,b,c) strcpy_s(a,c,b)
#define strdup _strdup
#else 
#define mystrncpy(a,b,c) memcpy(a,b,c)
#endif
//strncpy(a,c,b)

//typedef int_64 myint;
//typedef unsigned int myint;
//typedef uint16_t myint;
// any of the above, for m<16 use uint_16

typedef unsigned int uint;

// float or double
//typedef float  myfloat;
//using namespace std;

#define R_cpp11
