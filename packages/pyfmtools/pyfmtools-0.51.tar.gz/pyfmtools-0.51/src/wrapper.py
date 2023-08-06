###
# Python wrapper for Pyfmtools. Simplifies the usage of Pyfmtools by handling all Numpy and CFFI calls
###
import numpy as np
import types
import math
import re
from  _pyfmtools import ffi, lib as fm

###
# Helper functions
###

# Trace function
def trace( str):
    print( "-- ", str, " --")


# convert Python float to CFFI double * 
def convert_float_to_CFFI_double( x):
    if x.dtype != "float64": x = x.astype(float)
    px = ffi.cast( "double *", x.ctypes.data)
    return px

# use numpy to create an inc array with n zeros and cast to CFFI 
def create_intc_zeros_as_CFFI_int( n):
    x = np.zeros( n, np.intc)
    px = ffi.cast( "int *", x.ctypes.data)
    return x, px

# use numpy to create an inc array with n zeros and cast to CFFI 
def create_float_zeros_as_CFFI_double( n):
    x = np.zeros( n, float)
    px = ffi.cast( "double *", x.ctypes.data)
    return x, px

def convert_py_float_to_cffi( x):
    px = np.array( x)
    if px.dtype != "float64": px = px.astype( float)
    pxcffi = ffi.cast( "double *", px.ctypes.data)
    return pxcffi, px


def convert_py_int_to_cffi( x):
    x = x.astype( np.inc)
    px = np.array( x)
    pxcffi = ffi.cast( "int *", px.ctypes.data)
    return pxcffi, px


###
# The python minimum wrapper for py_ functions from wrapper.cpp
###

# void py_fm_init(int n, struct fm_env* env)
def fm_init( n):
    try:
        trace( "py_fm_init")
        env = ffi.new( "struct fm_env *")
        fm.py_fm_init( n, env)
        return env
    except ValueError:
        raise

# void py_fm_free( struct fm_env* env)
def fm_free( env):
    try:
        trace( "py_fm_free")
        if( env == None): raise ValueError( "Env not initialised") 
        fm.py_fm_free( env)
    except ValueError:
        raise

# void py_ShowCoalitions(int* coalition, struct fm_env* env)
def ShowCoalitions( env):
    trace( "py_ShowCoalitions")
    A, pA = create_intc_zeros_as_CFFI_int( env.m) 
    fm.py_ShowCoalitions( pA, env)
    return A

# int py_generate_fm_2additive_concave(int num, int n, double * vv)
def generate_fm_2additive_concave( ti, n, env):
    trace( "py_generate_fm_2additive_concave")
    v, pv = create_float_zeros_as_CFFI_double( env.m)
    size = fm.py_generate_fm_2additive_concave( ti, n, pv)
    return size, v

# void py_ShowCoalitionsCard(int* coalition, struct fm_env* env)
def ShowCoalitionsCard( env):
    trace( "py_ShowCoalitionsCard")
    A, pA = create_intc_zeros_as_CFFI_int( env.m) 
    A = fm.py_ShowCoalitionsCard( pA, env)
    return A

# py_generate_fmconvex_tsort(ti,n, n-1 , 1000, 8, 1, pv,env)
def generate_fmconvex_tsort( num, n, kint, markov, option, K, env):
    trace( "py_generate_fmconvex_tsort")
    v, pv = create_float_zeros_as_CFFI_double( env.m)
    size = fm.py_generate_fmconvex_tsort( num ,n, kint, markov, option, K, pv, env)
    return size, v

# py_generate_fm_tsort(ti,n, 2 , 10, 0, 0.1, pv,env)
def generate_fm_tsort( num, n, kint, markov, option, K, env):
    trace( "py_generate_fm_tsort")
    v, pv = create_float_zeros_as_CFFI_double( env.m)
    size = fm.py_generate_fm_tsort( num ,n, kint, markov, option, K, env)
    return size, v

# py_ConvertCard2Bit(pvb,pv,env)
def ConvertCard2Bit( v, env):
    trace( "py_ConvertCard2Bit")
    
    pv = convert_float_to_CFFI_double( v)
    vb, pvb = create_float_zeros_as_CFFI_double( env.m)
    fm.py_ConvertCard2Bit( pvb, pv, env)
    return vb 

# py_IsMeasureSupermodular(pvb,env)
def IsMeasureSupermodular( vb, env):
    trace( "py_IsMeasureSupermodular")
    pvb = convert_float_to_CFFI_double( vb)
    return fm.py_IsMeasureSupermodular( pvb, env)

# py_IsMeasureAdditive(pvb,env)
def IsMeasureAdditive( vb, env):
    trace( "y_IsMeasureAdditive")
    pvb = convert_float_to_CFFI_double( vb)
    return fm.py_IsMeasureAdditive( pvb, env)

# py_export_maximal_chains(n,pvb,pmc,env)
def export_maximal_chains( n, vb, env):
    trace( "py_export_maximal_chains")
    pvb = convert_float_to_CFFI_double( vb)
    mc, pmc = create_float_zeros_as_CFFI_double( math.factorial(n) * n)
    fm.py_export_maximal_chains( n, pvb, pmc, env)
    return mc

# py_Choquet(px,pvb,env)
def Choquet( x, vb, env):
    trace( "y_Choquet")
    npx = np.array( x)
    pnpx = ffi.cast( "double *", npx.ctypes.data)
    pvb = convert_float_to_CFFI_double( vb)
    return fm.py_Choquet( pnpx, pvb, env)

# double py_Sugeno(double* x, double* v, struct fm_env* env)
def Sugeno( x, vb, env):
    trace( "py_Sugeno")
    npx = np.array( x)
    pnpx = ffi.cast( "double *", npx.ctypes.data)
    pvb = convert_float_to_CFFI_double( vb)
    return fm.py_Sugeno( pnpx, pvb, env)



###
# The python wrapper for all other py_ functions from wrapper.cpp
###

# Generated python wrapper for:
#    double py_min_subset(double* x, int n, int_64 S)
def min_subset(x, n, S):
    trace( "double min_subset(double* x, int n, int_64 S)")
    px, pxnp = convert_py_float_to_cffi( x)
    yy = fm.py_min_subset( px, n, S)
    return yy


# Generated python wrapper for:
#    double py_max_subset(double* x, int n, int_64 S)
def max_subset(x, n, S):
    trace( "double max_subset(double* x, int n, int_64 S)")
    px, pxnp = convert_py_float_to_cffi( x)
    yy = fm.py_max_subset( px, n, S)
    return yy


# Generated python wrapper for:
#    double py_min_subsetC(double* x, int n, int_64 S, struct fm_env* env)
def min_subsetC(x, n, S, env):
    trace( "double min_subsetC(double* x, int n, int_64 S, struct fm_env* env)")
    px, pxnp = convert_py_float_to_cffi( x)
    yy = fm.py_min_subsetC( px, n, S, env)
    return yy


# Generated python wrapper for:
#    double py_max_subsetNegC(double* x, int n, int_64 S, struct fm_env* env)
def max_subsetNegC(x, n, S, env):
    trace( "double max_subsetNegC(double* x, int n, int_64 S, struct fm_env* env)")
    px, pxnp = convert_py_float_to_cffi( x)
    yy = fm.py_max_subsetNegC( px, n, S, env)
    return yy


# Generated python wrapper for:
#    int py_SizeArraykinteractive(int n, int k, struct fm_env* env)
def SizeArraykinteractive(n, k, env):
    trace( "int SizeArraykinteractive(int n, int k, struct fm_env* env)")
    yy = fm.py_SizeArraykinteractive( n, k, env)
    return yy


# Generated python wrapper for:
#    int py_IsSubsetC(int i, int j, struct fm_env* env)
def IsSubsetC(i, j, env):
    trace( "int IsSubsetC(int i, int j, struct fm_env* env)")
    yy = fm.py_IsSubsetC( i, j, env)
    return yy


# Generated python wrapper for:
#    int py_IsElementC(int i, int j, struct fm_env* env)
def IsElementC(i, j, env):
    trace( "int IsElementC(int i, int j, struct fm_env* env)")
    yy = fm.py_IsElementC( i, j, env)
    return yy


# Generated python wrapper for:
#    void py_ExpandKinteractive2Bit(double* dest, double* src, struct fm_env* env, int kint, int arraysize)
def ExpandKinteractive2Bit(dest, src, env, kint, arraysize):
    trace( "void ExpandKinteractive2Bit(double* dest, double* src, struct fm_env* env, int kint, int arraysize)")
    pdest, pdestnp = convert_py_float_to_cffi( dest)
    psrc, psrcnp = convert_py_float_to_cffi( src)
    fm.py_ExpandKinteractive2Bit( pdest, psrc, env, kint, arraysize)


# Generated python wrapper for:
#    void py_ExpandKinteractive2Bit_m(double* dest, double* src, struct fm_env* env, int kint, int arraysize, double* VVC)
def ExpandKinteractive2Bit_m(dest, src, env, kint, arraysize, VVC):
    trace( "void ExpandKinteractive2Bit_m(double* dest, double* src, struct fm_env* env, int kint, int arraysize, double* VVC)")
    pdest, pdestnp = convert_py_float_to_cffi( dest)
    psrc, psrcnp = convert_py_float_to_cffi( src)
    pVVC, pVVCnp = convert_py_float_to_cffi( VVC)
    fm.py_ExpandKinteractive2Bit_m( pdest, psrc, env, kint, arraysize, pVVC)


# Generated python wrapper for:
#    void py_Shapley(double* v, double* x, struct fm_env* env)
def Shapley(v, x, env):
    trace( "void Shapley(double* v, double* x, struct fm_env* env)")
    pv, pvnp = convert_py_float_to_cffi( v)
    px, pxnp = convert_py_float_to_cffi( x)
    fm.py_Shapley( pv, px, env)


# Generated python wrapper for:
#    void py_Banzhaf(double* v, double* B, struct fm_env* env)
def Banzhaf(v, B, env):
    trace( "void Banzhaf(double* v, double* B, struct fm_env* env)")
    pv, pvnp = convert_py_float_to_cffi( v)
    pB, pBnp = convert_py_float_to_cffi( B)
    fm.py_Banzhaf( pv, pB, env)


# Generated python wrapper for:
#    void py_ShapleyMob(double* Mob, double* x, struct fm_env* env)
def ShapleyMob(Mob, x, env):
    trace( "void ShapleyMob(double* Mob, double* x, struct fm_env* env)")
    pMob, pMobnp = convert_py_float_to_cffi( Mob)
    px, pxnp = convert_py_float_to_cffi( x)
    fm.py_ShapleyMob( pMob, px, env)


# Generated python wrapper for:
#    void py_BanzhafMob(double* Mob, double* B, struct fm_env* env)
def BanzhafMob(Mob, B, env):
    trace( "void BanzhafMob(double* Mob, double* B, struct fm_env* env)")
    pMob, pMobnp = convert_py_float_to_cffi( Mob)
    pB, pBnp = convert_py_float_to_cffi( B)
    fm.py_BanzhafMob( pMob, pB, env)


# Generated python wrapper for:
#    double py_ChoquetKinter(double* x, double* v, int kint, struct fm_env* env)
def ChoquetKinter(x, v, kint, env):
    trace( "double ChoquetKinter(double* x, double* v, int kint, struct fm_env* env)")
    px, pxnp = convert_py_float_to_cffi( x)
    pv, pvnp = convert_py_float_to_cffi( v)
    yy = fm.py_ChoquetKinter( px, pv, kint, env)
    return yy


# Generated python wrapper for:
#    double py_ChoquetMob(double* x, double* Mob, struct fm_env* env)
def ChoquetMob(x, Mob, env):
    trace( "double ChoquetMob(double* x, double* Mob, struct fm_env* env)")
    px, pxnp = convert_py_float_to_cffi( x)
    pMob, pMobnp = convert_py_float_to_cffi( Mob)
    yy = fm.py_ChoquetMob( px, pMob, env)
    return yy


# Generated python wrapper for:
#    void py_ConstructLambdaMeasure(double* singletons, double* lambdax, double* v, struct fm_env* env)
def ConstructLambdaMeasure(singletons, lambdax, v, env):
    trace( "void ConstructLambdaMeasure(double* singletons, double* lambdax, double* v, struct fm_env* env)")
    psingletons, psingletonsnp = convert_py_float_to_cffi( singletons)
    plambdax, plambdaxnp = convert_py_float_to_cffi( lambdax)
    pv, pvnp = convert_py_float_to_cffi( v)
    fm.py_ConstructLambdaMeasure( psingletons, plambdax, pv, env)


# Generated python wrapper for:
#    void py_ConstructLambdaMeasureMob(double* singletons, double* lambdax, double* Mob, struct fm_env* env)
def ConstructLambdaMeasureMob(singletons, lambdax, Mob, env):
    trace( "void ConstructLambdaMeasureMob(double* singletons, double* lambdax, double* Mob, struct fm_env* env)")
    psingletons, psingletonsnp = convert_py_float_to_cffi( singletons)
    plambdax, plambdaxnp = convert_py_float_to_cffi( lambdax)
    pMob, pMobnp = convert_py_float_to_cffi( Mob)
    fm.py_ConstructLambdaMeasureMob( psingletons, plambdax, pMob, env)


# Generated python wrapper for:
#    void py_dualm(double* v, double* w, struct fm_env* env)
def dualm(v, w, env):
    trace( "void dualm(double* v, double* w, struct fm_env* env)")
    pv, pvnp = convert_py_float_to_cffi( v)
    pw, pwnp = convert_py_float_to_cffi( w)
    fm.py_dualm( pv, pw, env)


# Generated python wrapper for:
#    void py_dualmMob(double* v, double* w, struct fm_env* env)
def dualmMob(v, w, env):
    trace( "void dualmMob(double* v, double* w, struct fm_env* env)")
    pv, pvnp = convert_py_float_to_cffi( v)
    pw, pwnp = convert_py_float_to_cffi( w)
    fm.py_dualmMob( pv, pw, env)


# Generated python wrapper for:
#    double py_Entropy(double* v, struct fm_env* env)
def Entropy(v, env):
    trace( "double Entropy(double* v, struct fm_env* env)")
    pv, pvnp = convert_py_float_to_cffi( v)
    yy = fm.py_Entropy( pv, env)
    return yy


# Generated python wrapper for:
#    void py_FuzzyMeasureFit(int datanum, int additive, struct fm_env* env, double* v, double* dataset)
def FuzzyMeasureFit(datanum, additive, env, v, dataset):
    trace( "void FuzzyMeasureFit(int datanum, int additive, struct fm_env* env, double* v, double* dataset)")
    pv, pvnp = convert_py_float_to_cffi( v)
    pdataset, pdatasetnp = convert_py_float_to_cffi( dataset)
    fm.py_FuzzyMeasureFit( datanum, additive, env, pv, pdataset)


# Generated python wrapper for:
#    void py_FuzzyMeasureFitMob(int datanum, int additive, struct fm_env* env, double* v, double* dataset)
def FuzzyMeasureFitMob(datanum, additive, env, v, dataset):
    trace( "void FuzzyMeasureFitMob(int datanum, int additive, struct fm_env* env, double* v, double* dataset)")
    pv, pvnp = convert_py_float_to_cffi( v)
    pdataset, pdatasetnp = convert_py_float_to_cffi( dataset)
    fm.py_FuzzyMeasureFitMob( datanum, additive, env, pv, pdataset)


# Generated python wrapper for:
#    void py_FuzzyMeasureFitKtolerant(int datanum, int additive, struct fm_env* env, double* v, double* dataset)
def FuzzyMeasureFitKtolerant(datanum, additive, env, v, dataset):
    trace( "void FuzzyMeasureFitKtolerant(int datanum, int additive, struct fm_env* env, double* v, double* dataset)")
    pv, pvnp = convert_py_float_to_cffi( v)
    pdataset, pdatasetnp = convert_py_float_to_cffi( dataset)
    fm.py_FuzzyMeasureFitKtolerant( datanum, additive, env, pv, pdataset)


# Generated python wrapper for:
#    void py_FuzzyMeasureFitLPKmaxitive(int datanum, int additive, struct fm_env* env, double* v, double* dataset)
def FuzzyMeasureFitLPKmaxitive(datanum, additive, env, v, dataset):
    trace( "void FuzzyMeasureFitLPKmaxitive(int datanum, int additive, struct fm_env* env, double* v, double* dataset)")
    pv, pvnp = convert_py_float_to_cffi( v)
    pdataset, pdatasetnp = convert_py_float_to_cffi( dataset)
    fm.py_FuzzyMeasureFitLPKmaxitive( datanum, additive, env, pv, pdataset)


# Generated python wrapper for:
#    void py_FuzzyMeasureFitLPKinteractive(int datanum, int additive, struct fm_env* env, double* v, double* dataset, double* K)
def FuzzyMeasureFitLPKinteractive(datanum, additive, env, v, dataset, K):
    trace( "void FuzzyMeasureFitLPKinteractive(int datanum, int additive, struct fm_env* env, double* v, double* dataset, double* K)")
    pv, pvnp = convert_py_float_to_cffi( v)
    pdataset, pdatasetnp = convert_py_float_to_cffi( dataset)
    pK, pKnp = convert_py_float_to_cffi( K)
    fm.py_FuzzyMeasureFitLPKinteractive( datanum, additive, env, pv, pdataset, pK)


# Generated python wrapper for:
#    void py_FuzzyMeasureFitLPKinteractiveMaxChains(int datanum, int additive, struct fm_env* env, double* v, double* dataset, double* K)
def FuzzyMeasureFitLPKinteractiveMaxChains(datanum, additive, env, v, dataset, K):
    trace( "void FuzzyMeasureFitLPKinteractiveMaxChains(int datanum, int additive, struct fm_env* env, double* v, double* dataset, double* K)")
    pv, pvnp = convert_py_float_to_cffi( v)
    pdataset, pdatasetnp = convert_py_float_to_cffi( dataset)
    pK, pKnp = convert_py_float_to_cffi( K)
    fm.py_FuzzyMeasureFitLPKinteractiveMaxChains( datanum, additive, env, pv, pdataset, pK)


# Generated python wrapper for:
#    void py_FuzzyMeasureFitLPKinteractiveAutoK(int datanum, int additive, struct fm_env* env, double* v, double* dataset, double* K, int* maxiters)
def FuzzyMeasureFitLPKinteractiveAutoK(datanum, additive, env, v, dataset, K, maxiters):
    trace( "void FuzzyMeasureFitLPKinteractiveAutoK(int datanum, int additive, struct fm_env* env, double* v, double* dataset, double* K, int* maxiters)")
    pv, pvnp = convert_py_float_to_cffi( v)
    pdataset, pdatasetnp = convert_py_float_to_cffi( dataset)
    pK, pKnp = convert_py_float_to_cffi( K)
    pmaxiters, pmaxitersnp = convert_py_int_to_cffi( maxiters)
    fm.py_FuzzyMeasureFitLPKinteractiveAutoK( datanum, additive, env, pv, pdataset, pK, pmaxiters)


# Generated python wrapper for:
#    void py_FuzzyMeasureFitLPKinteractiveMarginal(int datanum, int additive, struct fm_env* env, double* v, double* dataset, double* K, int submod)
def FuzzyMeasureFitLPKinteractiveMarginal(datanum, additive, env, v, dataset, K, submod):
    trace( "void FuzzyMeasureFitLPKinteractiveMarginal(int datanum, int additive, struct fm_env* env, double* v, double* dataset, double* K, int submod)")
    pv, pvnp = convert_py_float_to_cffi( v)
    pdataset, pdatasetnp = convert_py_float_to_cffi( dataset)
    pK, pKnp = convert_py_float_to_cffi( K)
    fm.py_FuzzyMeasureFitLPKinteractiveMarginal( datanum, additive, env, pv, pdataset, pK, submod)


# Generated python wrapper for:
#    void py_FuzzyMeasureFitLPKinteractiveMarginalMaxChain(int datanum, int additive, struct fm_env* env, double* v, double* dataset, double* K, int* maxiters, int submod)
def FuzzyMeasureFitLPKinteractiveMarginalMaxChain(datanum, additive, env, v, dataset, K, maxiters, submod):
    trace( "void FuzzyMeasureFitLPKinteractiveMarginalMaxChain(int datanum, int additive, struct fm_env* env, double* v, double* dataset, double* K, int* maxiters, int submod)")
    pv, pvnp = convert_py_float_to_cffi( v)
    pdataset, pdatasetnp = convert_py_float_to_cffi( dataset)
    pK, pKnp = convert_py_float_to_cffi( K)
    pmaxiters, pmaxitersnp = convert_py_int_to_cffi( maxiters)
    fm.py_FuzzyMeasureFitLPKinteractiveMarginalMaxChain( datanum, additive, env, pv, pdataset, pK, pmaxiters, submod)


# Generated python wrapper for:
#    void py_FuzzyMeasureFitLP(int datanum, int additive, struct fm_env* env, double* v, double* dataset, int* options, double* indexlow, double* indexhihg, int* option1, double* orness)
def FuzzyMeasureFitLP(datanum, additive, env, v, dataset, options, indexlow, indexhihg, option1, orness):
    trace( "void FuzzyMeasureFitLP(int datanum, int additive, struct fm_env* env, double* v, double* dataset, int* options, double* indexlow, double* indexhihg, int* option1, double* orness)")
    pv, pvnp = convert_py_float_to_cffi( v)
    pdataset, pdatasetnp = convert_py_float_to_cffi( dataset)
    poptions, poptionsnp = convert_py_int_to_cffi( options)
    pindexlow, pindexlownp = convert_py_float_to_cffi( indexlow)
    pindexhihg, pindexhihgnp = convert_py_float_to_cffi( indexhihg)
    poption1, poption1np = convert_py_int_to_cffi( option1)
    porness, pornessnp = convert_py_float_to_cffi( orness)
    fm.py_FuzzyMeasureFitLP( datanum, additive, env, pv, pdataset, poptions, pindexlow, pindexhihg, poption1, porness)


# Generated python wrapper for:
#    void py_FuzzyMeasureFitLPMob(int datanum, int additive, struct fm_env* env, double* v, double* dataset, int* options, double* indexlow, double* indexhihg, int* option1, double* orness)
def FuzzyMeasureFitLPMob(datanum, additive, env, v, dataset, options, indexlow, indexhihg, option1, orness):
    trace( "void FuzzyMeasureFitLPMob(int datanum, int additive, struct fm_env* env, double* v, double* dataset, int* options, double* indexlow, double* indexhihg, int* option1, double* orness)")
    pv, pvnp = convert_py_float_to_cffi( v)
    pdataset, pdatasetnp = convert_py_float_to_cffi( dataset)
    poptions, poptionsnp = convert_py_int_to_cffi( options)
    pindexlow, pindexlownp = convert_py_float_to_cffi( indexlow)
    pindexhihg, pindexhihgnp = convert_py_float_to_cffi( indexhihg)
    poption1, poption1np = convert_py_int_to_cffi( option1)
    porness, pornessnp = convert_py_float_to_cffi( orness)
    fm.py_FuzzyMeasureFitLPMob( datanum, additive, env, pv, pdataset, poptions, pindexlow, pindexhihg, poption1, porness)


# Generated python wrapper for:
#    void py_fittingOWA(int datanum, struct fm_env* env, double* v, double* dataset)
def fittingOWA(datanum, env, v, dataset):
    trace( "void fittingOWA(int datanum, struct fm_env* env, double* v, double* dataset)")
    pv, pvnp = convert_py_float_to_cffi( v)
    pdataset, pdatasetnp = convert_py_float_to_cffi( dataset)
    fm.py_fittingOWA( datanum, env, pv, pdataset)


# Generated python wrapper for:
#    void py_fittingWAM(int datanum, struct fm_env* env, double* v, double* dataset)
def fittingWAM(datanum, env, v, dataset):
    trace( "void fittingWAM(int datanum, struct fm_env* env, double* v, double* dataset)")
    pv, pvnp = convert_py_float_to_cffi( v)
    pdataset, pdatasetnp = convert_py_float_to_cffi( dataset)
    fm.py_fittingWAM( datanum, env, pv, pdataset)


# Generated python wrapper for:
#    void py_Interaction(double* Mob, double* v, struct fm_env* env)
def Interaction(Mob, v, env):
    trace( "void Interaction(double* Mob, double* v, struct fm_env* env)")
    pMob, pMobnp = convert_py_float_to_cffi( Mob)
    pv, pvnp = convert_py_float_to_cffi( v)
    fm.py_Interaction( pMob, pv, env)


# Generated python wrapper for:
#    void py_InteractionB(double* Mob, double* v, struct fm_env* env)
def InteractionB(Mob, v, env):
    trace( "void InteractionB(double* Mob, double* v, struct fm_env* env)")
    pMob, pMobnp = convert_py_float_to_cffi( Mob)
    pv, pvnp = convert_py_float_to_cffi( v)
    fm.py_InteractionB( pMob, pv, env)


# Generated python wrapper for:
#    void py_InteractionMob(double* Mob, double* v, struct fm_env* env)
def InteractionMob(Mob, v, env):
    trace( "void InteractionMob(double* Mob, double* v, struct fm_env* env)")
    pMob, pMobnp = convert_py_float_to_cffi( Mob)
    pv, pvnp = convert_py_float_to_cffi( v)
    fm.py_InteractionMob( pMob, pv, env)


# Generated python wrapper for:
#    void py_InteractionBMob(double* Mob, double* v, struct fm_env* env)
def InteractionBMob(Mob, v, env):
    trace( "void InteractionBMob(double* Mob, double* v, struct fm_env* env)")
    pMob, pMobnp = convert_py_float_to_cffi( Mob)
    pv, pvnp = convert_py_float_to_cffi( v)
    fm.py_InteractionBMob( pMob, pv, env)


# Generated python wrapper for:
#    void py_BipartitionShapleyIndex(double* v, double* w, struct fm_env* env)
def BipartitionShapleyIndex(v, w, env):
    trace( "void BipartitionShapleyIndex(double* v, double* w, struct fm_env* env)")
    pv, pvnp = convert_py_float_to_cffi( v)
    pw, pwnp = convert_py_float_to_cffi( w)
    fm.py_BipartitionShapleyIndex( pv, pw, env)


# Generated python wrapper for:
#    void py_BipartitionBanzhafIndex(double* v, double* w, struct fm_env* env)
def BipartitionBanzhafIndex(v, w, env):
    trace( "void BipartitionBanzhafIndex(double* v, double* w, struct fm_env* env)")
    pv, pvnp = convert_py_float_to_cffi( v)
    pw, pwnp = convert_py_float_to_cffi( w)
    fm.py_BipartitionBanzhafIndex( pv, pw, env)


# Generated python wrapper for:
#    void py_BNonadditivityIndexMob(double* Mob, double* w, struct fm_env* env)
def BNonadditivityIndexMob(Mob, w, env):
    trace( "void BNonadditivityIndexMob(double* Mob, double* w, struct fm_env* env)")
    pMob, pMobnp = convert_py_float_to_cffi( Mob)
    pw, pwnp = convert_py_float_to_cffi( w)
    fm.py_BNonadditivityIndexMob( pMob, pw, env)


# Generated python wrapper for:
#    void py_NonadditivityIndex(double* v, double* w, struct fm_env* env)
def NonadditivityIndex(v, w, env):
    trace( "void NonadditivityIndex(double* v, double* w, struct fm_env* env)")
    pv, pvnp = convert_py_float_to_cffi( v)
    pw, pwnp = convert_py_float_to_cffi( w)
    fm.py_NonadditivityIndex( pv, pw, env)


# Generated python wrapper for:
#    void py_NonmodularityIndex(double* v, double* w, struct fm_env* env)
def NonmodularityIndex(v, w, env):
    trace( "void NonmodularityIndex(double* v, double* w, struct fm_env* env)")
    pv, pvnp = convert_py_float_to_cffi( v)
    pw, pwnp = convert_py_float_to_cffi( w)
    fm.py_NonmodularityIndex( pv, pw, env)


# Generated python wrapper for:
#    void py_NonmodularityIndexMob(double* Mob, double* w, struct fm_env* env)
def NonmodularityIndexMob(Mob, w, env):
    trace( "void NonmodularityIndexMob(double* Mob, double* w, struct fm_env* env)")
    pMob, pMobnp = convert_py_float_to_cffi( Mob)
    pw, pwnp = convert_py_float_to_cffi( w)
    fm.py_NonmodularityIndexMob( pMob, pw, env)


# Generated python wrapper for:
#    void py_NonmodularityIndexKinteractive(double* v, double* w, int kint,  struct fm_env* env)
def NonmodularityIndexKinteractive(v, w, kint, env):
    trace( "void NonmodularityIndexKinteractive(double* v, double* w, int kint,  struct fm_env* env)")
    pv, pvnp = convert_py_float_to_cffi( v)
    pw, pwnp = convert_py_float_to_cffi( w)
    fm.py_NonmodularityIndexKinteractive( pv, pw, kint, env)
    return pwnp
    
# Generated python wrapper for:
#    void py_NonmodularityIndexMobkadditive(double* Mob, double* w, int k,  struct fm_env* env)
def NonmodularityIndexMobkadditive(Mob, w, k, env):
    trace( "void NonmodularityIndexMobkadditive(double* Mob, double* w, int k,  struct fm_env* env)")
    pMob, pMobnp = convert_py_float_to_cffi( Mob)
    pw, pwnp = convert_py_float_to_cffi( w)
    fm.py_NonmodularityIndexMobkadditive( pMob, pw, k, env)


# Generated python wrapper for:
#    int py_IsMeasureBalanced(double* v, struct fm_env* env)
def IsMeasureBalanced(v, env):
    trace( "int IsMeasureBalanced(double* v, struct fm_env* env)")
    pv, pvnp = convert_py_float_to_cffi( v)
    yy = fm.py_IsMeasureBalanced( pv, env)
    return yy


# Generated python wrapper for:
#    int py_IsMeasureSelfdual(double* v, struct fm_env* env)
def IsMeasureSelfdual(v, env):
    trace( "int IsMeasureSelfdual(double* v, struct fm_env* env)")
    pv, pvnp = convert_py_float_to_cffi( v)
    yy = fm.py_IsMeasureSelfdual( pv, env)
    return yy


# Generated python wrapper for:
#    int py_IsMeasureSubadditive(double* v, struct fm_env* env)
def IsMeasureSubadditive(v, env):
    trace( "int IsMeasureSubadditive(double* v, struct fm_env* env)")
    pv, pvnp = convert_py_float_to_cffi( v)
    yy = fm.py_IsMeasureSubadditive( pv, env)
    return yy


# Generated python wrapper for:
#    int py_IsMeasureSubmodular(double* v, struct fm_env* env)
def IsMeasureSubmodular(v, env):
    trace( "int IsMeasureSubmodular(double* v, struct fm_env* env)")
    pv, pvnp = convert_py_float_to_cffi( v)
    yy = fm.py_IsMeasureSubmodular( pv, env)
    return yy


# Generated python wrapper for:
#    int py_IsMeasureSuperadditive(double* v, struct fm_env* env)
def IsMeasureSuperadditive(v, env):
    trace( "int IsMeasureSuperadditive(double* v, struct fm_env* env)")
    pv, pvnp = convert_py_float_to_cffi( v)
    yy = fm.py_IsMeasureSuperadditive( pv, env)
    return yy


# Generated python wrapper for:
#    int py_IsMeasureSymmetric(double* v, struct fm_env* env)
def IsMeasureSymmetric(v, env):
    trace( "int IsMeasureSymmetric(double* v, struct fm_env* env)")
    pv, pvnp = convert_py_float_to_cffi( v)
    yy = fm.py_IsMeasureSymmetric( pv, env)
    return yy


# Generated python wrapper for:
#    int py_IsMeasureKMaxitive(double* v, struct fm_env* env)
def IsMeasureKMaxitive(v, env):
    trace( "int IsMeasureKMaxitive(double* v, struct fm_env* env)")
    pv, pvnp = convert_py_float_to_cffi( v)
    yy = fm.py_IsMeasureKMaxitive( pv, env)
    return yy


# Generated python wrapper for:
#    int py_IsMeasureAdditiveMob(double* Mob, struct fm_env* env)
def IsMeasureAdditiveMob(Mob, env):
    trace( "int IsMeasureAdditiveMob(double* Mob, struct fm_env* env)")
    pMob, pMobnp = convert_py_float_to_cffi( Mob)
    yy = fm.py_IsMeasureAdditiveMob( pMob, env)
    return yy


# Generated python wrapper for:
#    int py_IsMeasureBalancedMob(double* Mob, struct fm_env* env)
def IsMeasureBalancedMob(Mob, env):
    trace( "int IsMeasureBalancedMob(double* Mob, struct fm_env* env)")
    pMob, pMobnp = convert_py_float_to_cffi( Mob)
    yy = fm.py_IsMeasureBalancedMob( pMob, env)
    return yy


# Generated python wrapper for:
#    int py_IsMeasureSelfdualMob(double* Mob, struct fm_env* env)
def IsMeasureSelfdualMob(Mob, env):
    trace( "int IsMeasureSelfdualMob(double* Mob, struct fm_env* env)")
    pMob, pMobnp = convert_py_float_to_cffi( Mob)
    yy = fm.py_IsMeasureSelfdualMob( pMob, env)
    return yy


# Generated python wrapper for:
#    int py_IsMeasureSubadditiveMob(double* Mob, struct fm_env* env)
def IsMeasureSubadditiveMob(Mob, env):
    trace( "int IsMeasureSubadditiveMob(double* Mob, struct fm_env* env)")
    pMob, pMobnp = convert_py_float_to_cffi( Mob)
    yy = fm.py_IsMeasureSubadditiveMob( pMob, env)
    return yy


# Generated python wrapper for:
#    int py_IsMeasureSubmodularMob(double* Mob, struct fm_env* env)
def IsMeasureSubmodularMob(Mob, env):
    trace( "int IsMeasureSubmodularMob(double* Mob, struct fm_env* env)")
    pMob, pMobnp = convert_py_float_to_cffi( Mob)
    yy = fm.py_IsMeasureSubmodularMob( pMob, env)
    return yy


# Generated python wrapper for:
#    int py_IsMeasureSuperadditiveMob(double* Mob, struct fm_env* env)
def IsMeasureSuperadditiveMob(Mob, env):
    trace( "int IsMeasureSuperadditiveMob(double* Mob, struct fm_env* env)")
    pMob, pMobnp = convert_py_float_to_cffi( Mob)
    yy = fm.py_IsMeasureSuperadditiveMob( pMob, env)
    return yy


# Generated python wrapper for:
#    int py_IsMeasureSupermodularMob(double* Mob, struct fm_env* env)
def IsMeasureSupermodularMob(Mob, env):
    trace( "int IsMeasureSupermodularMob(double* Mob, struct fm_env* env)")
    pMob, pMobnp = convert_py_float_to_cffi( Mob)
    yy = fm.py_IsMeasureSupermodularMob( pMob, env)
    return yy


# Generated python wrapper for:
#    int py_IsMeasureSymmetricMob(double* Mob, struct fm_env* env)
def IsMeasureSymmetricMob(Mob, env):
    trace( "int IsMeasureSymmetricMob(double* Mob, struct fm_env* env)")
    pMob, pMobnp = convert_py_float_to_cffi( Mob)
    yy = fm.py_IsMeasureSymmetricMob( pMob, env)
    return yy


# Generated python wrapper for:
#    int py_IsMeasureKMaxitiveMob(double* Mob, struct fm_env* env)
def IsMeasureKMaxitiveMob(Mob, env):
    trace( "int IsMeasureKMaxitiveMob(double* Mob, struct fm_env* env)")
    pMob, pMobnp = convert_py_float_to_cffi( Mob)
    yy = fm.py_IsMeasureKMaxitiveMob( pMob, env)
    return yy


# Generated python wrapper for:
#    void py_Mobius(double* v, double* MobVal, struct fm_env* env)
def Mobius(v, MobVal, env):
    trace( "void Mobius(double* v, double* MobVal, struct fm_env* env)")
    pv, pvnp = convert_py_float_to_cffi( v)
    pMobVal, pMobValnp = convert_py_float_to_cffi( MobVal)
    fm.py_Mobius( pv, pMobVal, env)


# Generated python wrapper for:
#    double py_Orness(double* Mob, struct fm_env* env)
def Orness(Mob, env):
    trace( "double Orness(double* Mob, struct fm_env* env)")
    pMob, pMobnp = convert_py_float_to_cffi( Mob)
    yy = fm.py_Orness( pMob, env)
    return yy


# Generated python wrapper for:
#    double py_OWA(double* x, double* v, struct fm_env* env)
def OWA(x, v, env):
    trace( "double OWA(double* x, double* v, struct fm_env* env)")
    px, pxnp = convert_py_float_to_cffi( x)
    pv, pvnp = convert_py_float_to_cffi( v)
    yy = fm.py_OWA( px, pv, env)
    return yy


# Generated python wrapper for:
#    double py_WAM(double* x, double* v, struct fm_env* env)
def WAM(x, v, env):
    trace( "double WAM(double* x, double* v, struct fm_env* env)")
    px, pxnp = convert_py_float_to_cffi( x)
    pv, pvnp = convert_py_float_to_cffi( v)
    yy = fm.py_WAM( px, pv, env)
    return yy


# Generated python wrapper for:
#    void py_Zeta(double* Mob, double* v, struct fm_env* env)
def Zeta(Mob, v, env):
    trace( "void Zeta(double* Mob, double* v, struct fm_env* env)")
    pMob, pMobnp = convert_py_float_to_cffi( Mob)
    pv, pvnp = convert_py_float_to_cffi( v)
    fm.py_Zeta( pMob, pv, env)


# Generated python wrapper for:
#    void py_dualMobKadd(int m, int length, int k, double* src, double* dest, struct fm_env* env)
def dualMobKadd(m, length, k, src, dest, env):
    trace( "void dualMobKadd(int m, int length, int k, double* src, double* dest, struct fm_env* env)")
    psrc, psrcnp = convert_py_float_to_cffi( src)
    pdest, pdestnp = convert_py_float_to_cffi( dest)
    fm.py_dualMobKadd( m, length, k, psrc, pdest, env)


# Generated python wrapper for:
#    void py_Shapley2addMob(double* v, double* x, int n)
def Shapley2addMob(v, x, n):
    trace( "void Shapley2addMob(double* v, double* x, int n)")
    pv, pvnp = convert_py_float_to_cffi( v)
    px, pxnp = convert_py_float_to_cffi( x)
    fm.py_Shapley2addMob( pv, px, n)


# Generated python wrapper for:
#    void py_Banzhaf2addMob(double* v, double* x, int n)
def Banzhaf2addMob(v, x, n):
    trace( "void Banzhaf2addMob(double* v, double* x, int n)")
    pv, pvnp = convert_py_float_to_cffi( v)
    px, pxnp = convert_py_float_to_cffi( x)
    fm.py_Banzhaf2addMob( pv, px, n)


# Generated python wrapper for:
#    double py_Choquet2addMob(double* x, double* Mob, int n)
def Choquet2addMob(x, Mob, n):
    trace( "double Choquet2addMob(double* x, double* Mob, int n)")
    px, pxnp = convert_py_float_to_cffi( x)
    pMob, pMobnp = convert_py_float_to_cffi( Mob)
    yy = fm.py_Choquet2addMob( px, pMob, n)
    return yy


# Generated python wrapper for:
#    int py_fm_arraysize(int n, int kint, struct fm_env* env)
def fm_arraysize(n, kint, env):
    trace( "int fm_arraysize(int n, int kint, struct fm_env* env)")
    yy = fm.py_fm_arraysize( n, kint, env)
    return yy


# Generated python wrapper for:
#    int py_generate_fm_minplus(int num, int n, int kint, int markov, int option, double K, double* vv, struct fm_env* env)
def generate_fm_minplus(num, n, kint, markov, option, K, vv, env):
    trace( "int generate_fm_minplus(int num, int n, int kint, int markov, int option, double K, double* vv, struct fm_env* env)")
    pvv, pvvnp = convert_py_float_to_cffi( vv)
    yy = fm.py_generate_fm_minplus( num, n, kint, markov, option, K, pvv, env)
    return yy


# Generated python wrapper for:
#    int py_generate_fm_2additive_convex(int num, int n,  double* vv)
def generate_fm_2additive_convex(num, n, vv):
    trace( "int generate_fm_2additive_convex(int num, int n,  double* vv)")
    pvv, pvvnp = convert_py_float_to_cffi( vv)
    yy = fm.py_generate_fm_2additive_convex( num, n, pvv)
    return yy


# Generated python wrapper for:
#    int py_generate_fm_2additive_convex_withsomeindependent(int num, int n, double* vv)
def generate_fm_2additive_convex_withsomeindependent(num, n, vv):
    trace( "int generate_fm_2additive_convex_withsomeindependent(int num, int n, double* vv)")
    pvv, pvvnp = convert_py_float_to_cffi( vv)
    yy = fm.py_generate_fm_2additive_convex_withsomeindependent( num, n, pvv)
    return yy


# Generated python wrapper for:
#    void py_prepare_fm_sparse(int n, int tupsize, int* tuples, struct fm_env_sparse* env)
def prepare_fm_sparse(n, tupsize, tuples, env):
    trace( "void prepare_fm_sparse(int n, int tupsize, int* tuples, struct fm_env_sparse* env)")
    ptuples, ptuplesnp = convert_py_int_to_cffi( tuples)
    fm.py_prepare_fm_sparse( n, tupsize, ptuples, env)


# Generated python wrapper for:
#    int py_tuple_cardinality_sparse(int i, struct fm_env_sparse* env)
def tuple_cardinality_sparse(i, env):
    trace( "int tuple_cardinality_sparse(int i, struct fm_env_sparse* env)")
    yy = fm.py_tuple_cardinality_sparse( i, env)
    return yy


# Generated python wrapper for:
#    int py_get_num_tuples(struct fm_env_sparse* env)
def get_num_tuples(env):
    trace( "int get_num_tuples(struct fm_env_sparse* env)")
    yy = fm.py_get_num_tuples( env)
    return yy


# Generated python wrapper for:
#    int py_get_sizearray_tuples(struct fm_env_sparse* env)
def get_sizearray_tuples(env):
    trace( "int get_sizearray_tuples(struct fm_env_sparse* env)")
    yy = fm.py_get_sizearray_tuples( env)
    return yy


# Generated python wrapper for:
#    int py_is_inset_sparse(int A, int card, int i, struct fm_env_sparse* env)
def is_inset_sparse(A, card, i, env):
    trace( "int is_inset_sparse(int A, int card, int i, struct fm_env_sparse* env)")
    yy = fm.py_is_inset_sparse( A, card, i, env)
    return yy


# Generated python wrapper for:
#    int py_is_subset_sparse(int A, int cardA, int B, int cardB, struct fm_env_sparse* env)
def is_subset_sparse(A, cardA, B, cardB, env):
    trace( "int is_subset_sparse(int A, int cardA, int B, int cardB, struct fm_env_sparse* env)")
    yy = fm.py_is_subset_sparse( A, cardA, B, cardB, env)
    return yy


# Generated python wrapper for:
#    double py_min_subset_sparse(double* x, int n, int S, int cardS, struct fm_env_sparse* env)
def min_subset_sparse(x, n, S, cardS, env):
    trace( "double min_subset_sparse(double* x, int n, int S, int cardS, struct fm_env_sparse* env)")
    px, pxnp = convert_py_float_to_cffi( x)
    yy = fm.py_min_subset_sparse( px, n, S, cardS, env)
    return yy


# Generated python wrapper for:
#    double py_max_subset_sparse(double* x, int n, int S, int cardS, struct fm_env_sparse* env)
def max_subset_sparse(x, n, S, cardS, env):
    trace( "double max_subset_sparse(double* x, int n, int S, int cardS, struct fm_env_sparse* env)")
    px, pxnp = convert_py_float_to_cffi( x)
    yy = fm.py_max_subset_sparse( px, n, S, cardS, env)
    return yy


# Generated python wrapper for:
#    double py_ChoquetMob_sparse(double* x, int n, struct fm_env_sparse* env)
def ChoquetMob_sparse(x, n, env):
    trace( "double ChoquetMob_sparse(double* x, int n, struct fm_env_sparse* env)")
    px, pxnp = convert_py_float_to_cffi( x)
    yy = fm.py_ChoquetMob_sparse( px, n, env)
    return yy


# Generated python wrapper for:
#    void py_ShapleyMob_sparse(double* v, int n, struct fm_env_sparse* env)
def ShapleyMob_sparse(v, n, env):
    trace( "void ShapleyMob_sparse(double* v, int n, struct fm_env_sparse* env)")
    pv, pvnp = convert_py_float_to_cffi( v)
    fm.py_ShapleyMob_sparse( pv, n, env)


# Generated python wrapper for:
#    void py_BanzhafMob_sparse(double* v, int n, struct fm_env_sparse* env)
def BanzhafMob_sparse(v, n, env):
    trace( "void BanzhafMob_sparse(double* v, int n, struct fm_env_sparse* env)")
    pv, pvnp = convert_py_float_to_cffi( v)
    fm.py_BanzhafMob_sparse( pv, n, env)


# Generated python wrapper for:
#    void py_populate_fm_2add_sparse(double* singletons, int numpairs, double* pairs, int* indicesp1, int* indicesp2, struct fm_env_sparse* env)
def populate_fm_2add_sparse(singletons, numpairs, pairs, indicesp1, indicesp2, env):
    trace( "void populate_fm_2add_sparse(double* singletons, int numpairs, double* pairs, int* indicesp1, int* indicesp2, struct fm_env_sparse* env)")
    psingletons, psingletonsnp = convert_py_float_to_cffi( singletons)
    ppairs, ppairsnp = convert_py_float_to_cffi( pairs)
    pindicesp1, pindicesp1np = convert_py_int_to_cffi( indicesp1)
    pindicesp2, pindicesp2np = convert_py_int_to_cffi( indicesp2)
    fm.py_populate_fm_2add_sparse( psingletons, numpairs, ppairs, pindicesp1, pindicesp2, env)


# Generated python wrapper for:
#    void py_add_pair_sparse(int i, int j, double v, struct fm_env_sparse* env)
def add_pair_sparse(i, j, v, env):
    trace( "void add_pair_sparse(int i, int j, double v, struct fm_env_sparse* env)")
    fm.py_add_pair_sparse( i, j, v, env)


# Generated python wrapper for:
#    void py_add_tuple_sparse(int tupsize, int* tuple, double v, struct fm_env_sparse* env)
def add_tuple_sparse(tupsize, tuple, v, env):
    trace( "void add_tuple_sparse(int tupsize, int* tuple, double v, struct fm_env_sparse* env)")
    ptuple, ptuplenp = convert_py_int_to_cffi( tuple)
    fm.py_add_tuple_sparse( tupsize, ptuple, v, env)


# Generated python wrapper for:
#    void py_populate_fm_2add_sparse_from2add(int n, double* v, struct fm_env_sparse* env)
def populate_fm_2add_sparse_from2add(n, v, env):
    trace( "void populate_fm_2add_sparse_from2add(int n, double* v, struct fm_env_sparse* env)")
    pv, pvnp = convert_py_float_to_cffi( v)
    fm.py_populate_fm_2add_sparse_from2add( n, pv, env)


# Generated python wrapper for:
#    void py_expand_2add_full(double* v, struct fm_env_sparse* env)
def expand_2add_full(v, env):
    trace( "void expand_2add_full(double* v, struct fm_env_sparse* env)")
    pv, pvnp = convert_py_float_to_cffi( v)
    fm.py_expand_2add_full( pv, env)


# Generated python wrapper for:
#    void py_expand_sparse_full(double* v, struct fm_env_sparse* env)
def expand_sparse_full(v, env):
    trace( "void expand_sparse_full(double* v, struct fm_env_sparse* env)")
    pv, pvnp = convert_py_float_to_cffi( v)
    fm.py_expand_sparse_full( pv, env)


# Generated python wrapper for:
#    void py_sparse_get_singletons(int n, double* v, struct fm_env_sparse* env)
def sparse_get_singletons(n, v, env):
    trace( "void sparse_get_singletons(int n, double* v, struct fm_env_sparse* env)")
    pv, pvnp = convert_py_float_to_cffi( v)
    fm.py_sparse_get_singletons( n, pv, env)


# Generated python wrapper for:
#    int py_sparse_get_pairs(int* pairs, double* v, struct fm_env_sparse* env)
def sparse_get_pairs(pairs, v, env):
    trace( "int sparse_get_pairs(int* pairs, double* v, struct fm_env_sparse* env)")
    ppairs, ppairsnp = convert_py_int_to_cffi( pairs)
    pv, pvnp = convert_py_float_to_cffi( v)
    yy = fm.py_sparse_get_pairs( ppairs, pv, env)
    return yy


# Generated python wrapper for:
#    int py_sparse_get_tuples(int* tuples, double* v, struct fm_env_sparse* env)
def sparse_get_tuples(tuples, v, env):
    trace( "int sparse_get_tuples(int* tuples, double* v, struct fm_env_sparse* env)")
    ptuples, ptuplesnp = convert_py_int_to_cffi( tuples)
    pv, pvnp = convert_py_float_to_cffi( v)
    yy = fm.py_sparse_get_tuples( ptuples, pv, env)
    return yy


# Generated python wrapper for:
#    int   py_generate_fm_2additive_convex_sparse(int n, struct fm_env_sparse* env)
def generate_fm_2additive_convex_sparse(n, env):
    trace( "int   generate_fm_2additive_convex_sparse(int n, struct fm_env_sparse* env)")
    yy = fm.py_generate_fm_2additive_convex_sparse( n, env)
    return yy


# Generated python wrapper for:
#    int   py_generate_fm_kadditive_convex_sparse(int n, int k, int nonzero, struct fm_env_sparse* env)
def generate_fm_kadditive_convex_sparse(n, k, nonzero, env):
    trace( "int   generate_fm_kadditive_convex_sparse(int n, int k, int nonzero, struct fm_env_sparse* env)")
    yy = fm.py_generate_fm_kadditive_convex_sparse( n, k, nonzero, env)
    return yy


# Generated python wrapper for:
#    void py_Nonmodularityindex_sparse(double* w, int n, struct fm_env_sparse* env)
def Nonmodularityindex_sparse(w, n, env):
    trace( "void Nonmodularityindex_sparse(double* w, int n, struct fm_env_sparse* env)")
    pw, pwnp = convert_py_float_to_cffi( w)
    fm.py_Nonmodularityindex_sparse( pw, n, env)




