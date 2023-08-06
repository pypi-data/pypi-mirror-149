# Functions to combine NumPy arrays in C++ 
import numpy as np
import types
import math
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

# double py_min_subset(double* x, int n, int_64 S)
def min_subset(x, n, S):
    trace( "double min_subset(double* x, int n, int_64 S)")
    x, px = create_float_zeros_as_CFFI_double( n)
    yy = fm.min_subset( px, n, S)
    return yy



# double py_max_subset(double* x, int n, int_64 S)
def max_subset(x, n, S):
    trace( "double max_subset(double* x, int n, int_64 S)")
    x, px = create_float_zeros_as_CFFI_double( n)
    yy = fm.max_subset( px, n, S)
    return yy



# double py_min_subsetC(double* x, int n, int_64 S, struct_fm_env* env)
def min_subsetC(x, n, S, env):
    trace( "double min_subsetC(double* x, int n, int_64 S, struct_fm_env* env)")
    x, px = create_float_zeros_as_CFFI_double( env.m)
    yy = fm.min_subsetC( px, n, S, env)
    return yy



# double py_max_subsetNegC(double* x, int n, int_64 S, struct_fm_env* env)
def max_subsetNegC(x, n, S, env):
    trace( "double max_subsetNegC(double* x, int n, int_64 S, struct_fm_env* env)")
    x, px = create_float_zeros_as_CFFI_double( env.m)
    yy = fm.max_subsetNegC( px, n, S, env)
    return yy



# int py_SizeArraykinteractive(int n, int k, struct_fm_env* env)
def SizeArraykinteractive(n, k, env):
    trace( "int SizeArraykinteractive(int n, int k, struct_fm_env* env)")
    yy = fm.SizeArraykinteractive( n, k, env)
    return yy



# int py_IsSubsetC(int i, int j, struct_fm_env* env)
def IsSubsetC(i, j, env):
    trace( "int IsSubsetC(int i, int j, struct_fm_env* env)")
    yy = fm.IsSubsetC( i, j, env)
    return yy



# int py_IsElementC(int i, int j, struct_fm_env* env)
def IsElementC(i, j, env):
    trace( "int IsElementC(int i, int j, struct_fm_env* env)")
    yy = fm.IsElementC( i, j, env)
    return yy



# void py_ExpandKinteractive2Bit(double* dest, double* src, struct_fm_env* env, int kint, int arraysize)
def ExpandKinteractive2Bit(dest, src, env, kint, arraysize):
    trace( "void ExpandKinteractive2Bit(double* dest, double* src, struct_fm_env* env, int kint, int arraysize)")
    dest, pdest = create_float_zeros_as_CFFI_double( env.m)
    src, psrc = create_float_zeros_as_CFFI_double( env.m)
    fm.ExpandKinteractive2Bit( pdest, psrc, env, kint, arraysize)



# void py_ExpandKinteractive2Bit_m(double* dest, double* src, struct_fm_env* env, int kint, int arraysize, double* VVC)
def ExpandKinteractive2Bit_m(dest, src, env, kint, arraysize, VVC):
    trace( "void ExpandKinteractive2Bit_m(double* dest, double* src, struct_fm_env* env, int kint, int arraysize, double* VVC)")
    dest, pdest = create_float_zeros_as_CFFI_double( env.m)
    src, psrc = create_float_zeros_as_CFFI_double( env.m)
    VVC, pVVC = create_float_zeros_as_CFFI_double( env.m)
    fm.ExpandKinteractive2Bit_m( pdest, psrc, env, kint, arraysize, pVVC)



# void py_Shapley(double* v, double* x, struct_fm_env* env)
def Shapley(v, x, env):
    trace( "void Shapley(double* v, double* x, struct_fm_env* env)")
    v, pv = create_float_zeros_as_CFFI_double( env.m)
    x, px = create_float_zeros_as_CFFI_double( env.m)
    fm.Shapley( pv, px, env)



# void py_Banzhaf(double* v, double* B, struct_fm_env* env)
def Banzhaf(v, B, env):
    trace( "void Banzhaf(double* v, double* B, struct_fm_env* env)")
    v, pv = create_float_zeros_as_CFFI_double( env.m)
    B, pB = create_float_zeros_as_CFFI_double( env.m)
    fm.Banzhaf( pv, pB, env)



# void py_ShapleyMob(double* Mob, double* x, struct_fm_env* env)
def ShapleyMob(Mob, x, env):
    trace( "void ShapleyMob(double* Mob, double* x, struct_fm_env* env)")
    Mob, pMob = create_float_zeros_as_CFFI_double( env.m)
    x, px = create_float_zeros_as_CFFI_double( env.m)
    fm.ShapleyMob( pMob, px, env)



# void py_BanzhafMob(double* Mob, double* B, struct_fm_env* env)
def BanzhafMob(Mob, B, env):
    trace( "void BanzhafMob(double* Mob, double* B, struct_fm_env* env)")
    Mob, pMob = create_float_zeros_as_CFFI_double( env.m)
    B, pB = create_float_zeros_as_CFFI_double( env.m)
    fm.BanzhafMob( pMob, pB, env)



# double py_ChoquetKinter(double* x, double* v, int kint, struct_fm_env* env)
def ChoquetKinter(x, v, kint, env):
    trace( "double ChoquetKinter(double* x, double* v, int kint, struct_fm_env* env)")
    x, px = create_float_zeros_as_CFFI_double( env.m)
    v, pv = create_float_zeros_as_CFFI_double( env.m)
    yy = fm.ChoquetKinter( px, pv, kint, env)
    return yy



# double py_ChoquetMob(double* x, double* Mob, struct_fm_env* env)
def ChoquetMob(x, Mob, env):
    trace( "double ChoquetMob(double* x, double* Mob, struct_fm_env* env)")
    x, px = create_float_zeros_as_CFFI_double( env.m)
    Mob, pMob = create_float_zeros_as_CFFI_double( env.m)
    yy = fm.ChoquetMob( px, pMob, env)
    return yy



# void py_ConstructLambdaMeasure(double* singletons, double* lambdax, double* v, struct_fm_env* env)
def ConstructLambdaMeasure(singletons, lambdax, v, env):
    trace( "void ConstructLambdaMeasure(double* singletons, double* lambdax, double* v, struct_fm_env* env)")
    singletons, psingletons = create_float_zeros_as_CFFI_double( env.m)
    lambdax, plambdax = create_float_zeros_as_CFFI_double( env.m)
    v, pv = create_float_zeros_as_CFFI_double( env.m)
    fm.ConstructLambdaMeasure( psingletons, plambdax, pv, env)



# void py_ConstructLambdaMeasureMob(double* singletons, double* lambdax, double* Mob, struct_fm_env* env)
def ConstructLambdaMeasureMob(singletons, lambdax, Mob, env):
    trace( "void ConstructLambdaMeasureMob(double* singletons, double* lambdax, double* Mob, struct_fm_env* env)")
    singletons, psingletons = create_float_zeros_as_CFFI_double( env.m)
    lambdax, plambdax = create_float_zeros_as_CFFI_double( env.m)
    Mob, pMob = create_float_zeros_as_CFFI_double( env.m)
    fm.ConstructLambdaMeasureMob( psingletons, plambdax, pMob, env)



# void py_dualm(double* v, double* w, struct_fm_env* env)
def dualm(v, w, env):
    trace( "void dualm(double* v, double* w, struct_fm_env* env)")
    v, pv = create_float_zeros_as_CFFI_double( env.m)
    w, pw = create_float_zeros_as_CFFI_double( env.m)
    fm.dualm( pv, pw, env)



# void py_dualmMob(double* v, double* w, struct_fm_env* env)
def dualmMob(v, w, env):
    trace( "void dualmMob(double* v, double* w, struct_fm_env* env)")
    v, pv = create_float_zeros_as_CFFI_double( env.m)
    w, pw = create_float_zeros_as_CFFI_double( env.m)
    fm.dualmMob( pv, pw, env)



# double py_Entropy(double* v, struct_fm_env* env)
def Entropy(v, env):
    trace( "double Entropy(double* v, struct_fm_env* env)")
    v, pv = create_float_zeros_as_CFFI_double( env.m)
    yy = fm.Entropy( pv, env)
    return yy



# void py_FuzzyMeasureFit(int datanum, int additive, struct_fm_env* env, double* v, double* dataset)
def FuzzyMeasureFit(datanum, additive, env, v, dataset):
    trace( "void FuzzyMeasureFit(int datanum, int additive, struct_fm_env* env, double* v, double* dataset)")
    v, pv = create_float_zeros_as_CFFI_double( env.m)
    dataset, pdataset = create_float_zeros_as_CFFI_double( env.m)
    fm.FuzzyMeasureFit( datanum, additive, env, pv, pdataset)



# void py_FuzzyMeasureFitMob(int datanum, int additive, struct_fm_env* env, double* v, double* dataset)
def FuzzyMeasureFitMob(datanum, additive, env, v, dataset):
    trace( "void FuzzyMeasureFitMob(int datanum, int additive, struct_fm_env* env, double* v, double* dataset)")
    v, pv = create_float_zeros_as_CFFI_double( env.m)
    dataset, pdataset = create_float_zeros_as_CFFI_double( env.m)
    fm.FuzzyMeasureFitMob( datanum, additive, env, pv, pdataset)



# void py_FuzzyMeasureFitKtolerant(int datanum, int additive, struct_fm_env* env, double* v, double* dataset)
def FuzzyMeasureFitKtolerant(datanum, additive, env, v, dataset):
    trace( "void FuzzyMeasureFitKtolerant(int datanum, int additive, struct_fm_env* env, double* v, double* dataset)")
    v, pv = create_float_zeros_as_CFFI_double( env.m)
    dataset, pdataset = create_float_zeros_as_CFFI_double( env.m)
    fm.FuzzyMeasureFitKtolerant( datanum, additive, env, pv, pdataset)



# void py_FuzzyMeasureFitLPKmaxitive(int datanum, int additive, struct_fm_env* env, double* v, double* dataset)
def FuzzyMeasureFitLPKmaxitive(datanum, additive, env, v, dataset):
    trace( "void FuzzyMeasureFitLPKmaxitive(int datanum, int additive, struct_fm_env* env, double* v, double* dataset)")
    v, pv = create_float_zeros_as_CFFI_double( env.m)
    dataset, pdataset = create_float_zeros_as_CFFI_double( env.m)
    fm.FuzzyMeasureFitLPKmaxitive( datanum, additive, env, pv, pdataset)



# void py_FuzzyMeasureFitLPKinteractive(int datanum, int additive, struct_fm_env* env, double* v, double* dataset, double* K)
def FuzzyMeasureFitLPKinteractive(datanum, additive, env, v, dataset, K):
    trace( "void FuzzyMeasureFitLPKinteractive(int datanum, int additive, struct_fm_env* env, double* v, double* dataset, double* K)")
    v, pv = create_float_zeros_as_CFFI_double( env.m)
    dataset, pdataset = create_float_zeros_as_CFFI_double( env.m)
    K, pK = create_float_zeros_as_CFFI_double( env.m)
    fm.FuzzyMeasureFitLPKinteractive( datanum, additive, env, pv, pdataset, pK)



# void py_FuzzyMeasureFitLPKinteractiveMaxChains(int datanum, int additive, struct_fm_env* env, double* v, double* dataset, double* K)
def FuzzyMeasureFitLPKinteractiveMaxChains(datanum, additive, env, v, dataset, K):
    trace( "void FuzzyMeasureFitLPKinteractiveMaxChains(int datanum, int additive, struct_fm_env* env, double* v, double* dataset, double* K)")
    v, pv = create_float_zeros_as_CFFI_double( env.m)
    dataset, pdataset = create_float_zeros_as_CFFI_double( env.m)
    K, pK = create_float_zeros_as_CFFI_double( env.m)
    fm.FuzzyMeasureFitLPKinteractiveMaxChains( datanum, additive, env, pv, pdataset, pK)



# void py_FuzzyMeasureFitLPKinteractiveAutoK(int datanum, int additive, struct_fm_env* env, double* v, double* dataset, double* K, int* maxiters)
def FuzzyMeasureFitLPKinteractiveAutoK(datanum, additive, env, v, dataset, K, maxiters):
    trace( "void FuzzyMeasureFitLPKinteractiveAutoK(int datanum, int additive, struct_fm_env* env, double* v, double* dataset, double* K, int* maxiters)")
    v, pv = create_float_zeros_as_CFFI_double( env.m)
    dataset, pdataset = create_float_zeros_as_CFFI_double( env.m)
    K, pK = create_float_zeros_as_CFFI_double( env.m)
    maxiters, pmaxiters = create_intc_zeros_as_CFFI_int( env.m)
    fm.FuzzyMeasureFitLPKinteractiveAutoK( datanum, additive, env, pv, pdataset, pK, pmaxiters)



# void py_FuzzyMeasureFitLPKinteractiveMarginal(int datanum, int additive, struct_fm_env* env, double* v, double* dataset, double* K, int submod)
def FuzzyMeasureFitLPKinteractiveMarginal(datanum, additive, env, v, dataset, K, submod):
    trace( "void FuzzyMeasureFitLPKinteractiveMarginal(int datanum, int additive, struct_fm_env* env, double* v, double* dataset, double* K, int submod)")
    v, pv = create_float_zeros_as_CFFI_double( env.m)
    dataset, pdataset = create_float_zeros_as_CFFI_double( env.m)
    K, pK = create_float_zeros_as_CFFI_double( env.m)
    fm.FuzzyMeasureFitLPKinteractiveMarginal( datanum, additive, env, pv, pdataset, pK, submod)



# void py_FuzzyMeasureFitLPKinteractiveMarginalMaxChain(int datanum, int additive, struct_fm_env* env, double* v, double* dataset, double* K, int* maxiters, int submod)
def FuzzyMeasureFitLPKinteractiveMarginalMaxChain(datanum, additive, env, v, dataset, K, maxiters, submod):
    trace( "void FuzzyMeasureFitLPKinteractiveMarginalMaxChain(int datanum, int additive, struct_fm_env* env, double* v, double* dataset, double* K, int* maxiters, int submod)")
    v, pv = create_float_zeros_as_CFFI_double( env.m)
    dataset, pdataset = create_float_zeros_as_CFFI_double( env.m)
    K, pK = create_float_zeros_as_CFFI_double( env.m)
    maxiters, pmaxiters = create_intc_zeros_as_CFFI_int( env.m)
    fm.FuzzyMeasureFitLPKinteractiveMarginalMaxChain( datanum, additive, env, pv, pdataset, pK, pmaxiters, submod)



# void py_FuzzyMeasureFitLP(int datanum, int additive, struct_fm_env* env, double* v, double* dataset, int* options, double* indexlow, double* indexhihg, int* option1, double* orness)
def FuzzyMeasureFitLP(datanum, additive, env, v, dataset, options, indexlow, indexhihg, option1, orness):
    trace( "void FuzzyMeasureFitLP(int datanum, int additive, struct_fm_env* env, double* v, double* dataset, int* options, double* indexlow, double* indexhihg, int* option1, double* orness)")
    v, pv = create_float_zeros_as_CFFI_double( env.m)
    dataset, pdataset = create_float_zeros_as_CFFI_double( env.m)
    options, poptions = create_intc_zeros_as_CFFI_int( env.m)
    indexlow, pindexlow = create_float_zeros_as_CFFI_double( env.m)
    indexhihg, pindexhihg = create_float_zeros_as_CFFI_double( env.m)
    option1, poption1 = create_intc_zeros_as_CFFI_int( env.m)
    orness, porness = create_float_zeros_as_CFFI_double( env.m)
    fm.FuzzyMeasureFitLP( datanum, additive, env, pv, pdataset, poptions, pindexlow, pindexhihg, poption1, porness)



# void py_FuzzyMeasureFitLPMob(int datanum, int additive, struct_fm_env* env, double* v, double* dataset, int* options, double* indexlow, double* indexhihg, int* option1, double* orness)
def FuzzyMeasureFitLPMob(datanum, additive, env, v, dataset, options, indexlow, indexhihg, option1, orness):
    trace( "void FuzzyMeasureFitLPMob(int datanum, int additive, struct_fm_env* env, double* v, double* dataset, int* options, double* indexlow, double* indexhihg, int* option1, double* orness)")
    v, pv = create_float_zeros_as_CFFI_double( env.m)
    dataset, pdataset = create_float_zeros_as_CFFI_double( env.m)
    options, poptions = create_intc_zeros_as_CFFI_int( env.m)
    indexlow, pindexlow = create_float_zeros_as_CFFI_double( env.m)
    indexhihg, pindexhihg = create_float_zeros_as_CFFI_double( env.m)
    option1, poption1 = create_intc_zeros_as_CFFI_int( env.m)
    orness, porness = create_float_zeros_as_CFFI_double( env.m)
    fm.FuzzyMeasureFitLPMob( datanum, additive, env, pv, pdataset, poptions, pindexlow, pindexhihg, poption1, porness)



# void py_fittingOWA(int datanum, struct_fm_env* env, double* v, double* dataset)
def fittingOWA(datanum, env, v, dataset):
    trace( "void fittingOWA(int datanum, struct_fm_env* env, double* v, double* dataset)")
    v, pv = create_float_zeros_as_CFFI_double( env.m)
    dataset, pdataset = create_float_zeros_as_CFFI_double( env.m)
    fm.fittingOWA( datanum, env, pv, pdataset)



# void py_fittingWAM(int datanum, struct_fm_env* env, double* v, double* dataset)
def fittingWAM(datanum, env, v, dataset):
    trace( "void fittingWAM(int datanum, struct_fm_env* env, double* v, double* dataset)")
    v, pv = create_float_zeros_as_CFFI_double( env.m)
    dataset, pdataset = create_float_zeros_as_CFFI_double( env.m)
    fm.fittingWAM( datanum, env, pv, pdataset)



# void py_Interaction(double* Mob, double* v, struct_fm_env* env)
def Interaction(Mob, v, env):
    trace( "void Interaction(double* Mob, double* v, struct_fm_env* env)")
    Mob, pMob = create_float_zeros_as_CFFI_double( env.m)
    v, pv = create_float_zeros_as_CFFI_double( env.m)
    fm.Interaction( pMob, pv, env)



# void py_InteractionB(double* Mob, double* v, struct_fm_env* env)
def InteractionB(Mob, v, env):
    trace( "void InteractionB(double* Mob, double* v, struct_fm_env* env)")
    Mob, pMob = create_float_zeros_as_CFFI_double( env.m)
    v, pv = create_float_zeros_as_CFFI_double( env.m)
    fm.InteractionB( pMob, pv, env)



# void py_InteractionMob(double* Mob, double* v, struct_fm_env* env)
def InteractionMob(Mob, v, env):
    trace( "void InteractionMob(double* Mob, double* v, struct_fm_env* env)")
    Mob, pMob = create_float_zeros_as_CFFI_double( env.m)
    v, pv = create_float_zeros_as_CFFI_double( env.m)
    fm.InteractionMob( pMob, pv, env)



# void py_InteractionBMob(double* Mob, double* v, struct_fm_env* env)
def InteractionBMob(Mob, v, env):
    trace( "void InteractionBMob(double* Mob, double* v, struct_fm_env* env)")
    Mob, pMob = create_float_zeros_as_CFFI_double( env.m)
    v, pv = create_float_zeros_as_CFFI_double( env.m)
    fm.InteractionBMob( pMob, pv, env)



# void py_BipartitionShapleyIndex(double* v, double* w, struct_fm_env* env)
def BipartitionShapleyIndex(v, w, env):
    trace( "void BipartitionShapleyIndex(double* v, double* w, struct_fm_env* env)")
    v, pv = create_float_zeros_as_CFFI_double( env.m)
    w, pw = create_float_zeros_as_CFFI_double( env.m)
    fm.BipartitionShapleyIndex( pv, pw, env)



# void py_BipartitionBanzhafIndex(double* v, double* w, struct_fm_env* env)
def BipartitionBanzhafIndex(v, w, env):
    trace( "void BipartitionBanzhafIndex(double* v, double* w, struct_fm_env* env)")
    v, pv = create_float_zeros_as_CFFI_double( env.m)
    w, pw = create_float_zeros_as_CFFI_double( env.m)
    fm.BipartitionBanzhafIndex( pv, pw, env)



# void py_BNonadditivityIndexMob(double* Mob, double* w, struct_fm_env* env)
def BNonadditivityIndexMob(Mob, w, env):
    trace( "void BNonadditivityIndexMob(double* Mob, double* w, struct_fm_env* env)")
    Mob, pMob = create_float_zeros_as_CFFI_double( env.m)
    w, pw = create_float_zeros_as_CFFI_double( env.m)
    fm.BNonadditivityIndexMob( pMob, pw, env)



# void py_NonadditivityIndex(double* v, double* w, struct_fm_env* env)
def NonadditivityIndex(v, w, env):
    trace( "void NonadditivityIndex(double* v, double* w, struct_fm_env* env)")
    v, pv = create_float_zeros_as_CFFI_double( env.m)
    w, pw = create_float_zeros_as_CFFI_double( env.m)
    fm.NonadditivityIndex( pv, pw, env)



# void py_NonmodularityIndex(double* v, double* w, struct_fm_env* env)
def NonmodularityIndex(v, w, env):
    trace( "void NonmodularityIndex(double* v, double* w, struct_fm_env* env)")
    v, pv = create_float_zeros_as_CFFI_double( env.m)
    w, pw = create_float_zeros_as_CFFI_double( env.m)
    fm.NonmodularityIndex( pv, pw, env)



# void py_NonmodularityIndexMob(double* Mob, double* w, struct_fm_env* env)
def NonmodularityIndexMob(Mob, w, env):
    trace( "void NonmodularityIndexMob(double* Mob, double* w, struct_fm_env* env)")
    Mob, pMob = create_float_zeros_as_CFFI_double( env.m)
    w, pw = create_float_zeros_as_CFFI_double( env.m)
    fm.NonmodularityIndexMob( pMob, pw, env)



# void py_NonmodularityIndexKinteractive(double* v, double* w, int kint,  struct_fm_env* env)
def NonmodularityIndexKinteractive(v, w, kint, env):
    trace( "void NonmodularityIndexKinteractive(double* v, double* w, int kint,  struct_fm_env* env)")
    v, pv = create_float_zeros_as_CFFI_double( env.m)
    w, pw = create_float_zeros_as_CFFI_double( env.m)
    fm.NonmodularityIndexKinteractive( pv, pw, kint, env)



# void py_NonmodularityIndexMobkadditive(double* Mob, double* w, int k,  struct_fm_env* env)
def NonmodularityIndexMobkadditive(Mob, w, k, env):
    trace( "void NonmodularityIndexMobkadditive(double* Mob, double* w, int k,  struct_fm_env* env)")
    Mob, pMob = create_float_zeros_as_CFFI_double( env.m)
    w, pw = create_float_zeros_as_CFFI_double( env.m)
    fm.NonmodularityIndexMobkadditive( pMob, pw, k, env)



# int py_IsMeasureBalanced(double* v, struct_fm_env* env)
def IsMeasureBalanced(v, env):
    trace( "int IsMeasureBalanced(double* v, struct_fm_env* env)")
    v, pv = create_float_zeros_as_CFFI_double( env.m)
    yy = fm.IsMeasureBalanced( pv, env)
    return yy



# int py_IsMeasureSelfdual(double* v, struct_fm_env* env)
def IsMeasureSelfdual(v, env):
    trace( "int IsMeasureSelfdual(double* v, struct_fm_env* env)")
    v, pv = create_float_zeros_as_CFFI_double( env.m)
    yy = fm.IsMeasureSelfdual( pv, env)
    return yy



# int py_IsMeasureSubadditive(double* v, struct_fm_env* env)
def IsMeasureSubadditive(v, env):
    trace( "int IsMeasureSubadditive(double* v, struct_fm_env* env)")
    v, pv = create_float_zeros_as_CFFI_double( env.m)
    yy = fm.IsMeasureSubadditive( pv, env)
    return yy



# int py_IsMeasureSubmodular(double* v, struct_fm_env* env)
def IsMeasureSubmodular(v, env):
    trace( "int IsMeasureSubmodular(double* v, struct_fm_env* env)")
    v, pv = create_float_zeros_as_CFFI_double( env.m)
    yy = fm.IsMeasureSubmodular( pv, env)
    return yy



# int py_IsMeasureSuperadditive(double* v, struct_fm_env* env)
def IsMeasureSuperadditive(v, env):
    trace( "int IsMeasureSuperadditive(double* v, struct_fm_env* env)")
    v, pv = create_float_zeros_as_CFFI_double( env.m)
    yy = fm.IsMeasureSuperadditive( pv, env)
    return yy



# int py_IsMeasureSymmetric(double* v, struct_fm_env* env)
def IsMeasureSymmetric(v, env):
    trace( "int IsMeasureSymmetric(double* v, struct_fm_env* env)")
    v, pv = create_float_zeros_as_CFFI_double( env.m)
    yy = fm.IsMeasureSymmetric( pv, env)
    return yy



# int py_IsMeasureKMaxitive(double* v, struct_fm_env* env)
def IsMeasureKMaxitive(v, env):
    trace( "int IsMeasureKMaxitive(double* v, struct_fm_env* env)")
    v, pv = create_float_zeros_as_CFFI_double( env.m)
    yy = fm.IsMeasureKMaxitive( pv, env)
    return yy



# int py_IsMeasureAdditiveMob(double* Mob, struct_fm_env* env)
def IsMeasureAdditiveMob(Mob, env):
    trace( "int IsMeasureAdditiveMob(double* Mob, struct_fm_env* env)")
    Mob, pMob = create_float_zeros_as_CFFI_double( env.m)
    yy = fm.IsMeasureAdditiveMob( pMob, env)
    return yy



# int py_IsMeasureBalancedMob(double* Mob, struct_fm_env* env)
def IsMeasureBalancedMob(Mob, env):
    trace( "int IsMeasureBalancedMob(double* Mob, struct_fm_env* env)")
    Mob, pMob = create_float_zeros_as_CFFI_double( env.m)
    yy = fm.IsMeasureBalancedMob( pMob, env)
    return yy



# int py_IsMeasureSelfdualMob(double* Mob, struct_fm_env* env)
def IsMeasureSelfdualMob(Mob, env):
    trace( "int IsMeasureSelfdualMob(double* Mob, struct_fm_env* env)")
    Mob, pMob = create_float_zeros_as_CFFI_double( env.m)
    yy = fm.IsMeasureSelfdualMob( pMob, env)
    return yy



# int py_IsMeasureSubadditiveMob(double* Mob, struct_fm_env* env)
def IsMeasureSubadditiveMob(Mob, env):
    trace( "int IsMeasureSubadditiveMob(double* Mob, struct_fm_env* env)")
    Mob, pMob = create_float_zeros_as_CFFI_double( env.m)
    yy = fm.IsMeasureSubadditiveMob( pMob, env)
    return yy



# int py_IsMeasureSubmodularMob(double* Mob, struct_fm_env* env)
def IsMeasureSubmodularMob(Mob, env):
    trace( "int IsMeasureSubmodularMob(double* Mob, struct_fm_env* env)")
    Mob, pMob = create_float_zeros_as_CFFI_double( env.m)
    yy = fm.IsMeasureSubmodularMob( pMob, env)
    return yy



# int py_IsMeasureSuperadditiveMob(double* Mob, struct_fm_env* env)
def IsMeasureSuperadditiveMob(Mob, env):
    trace( "int IsMeasureSuperadditiveMob(double* Mob, struct_fm_env* env)")
    Mob, pMob = create_float_zeros_as_CFFI_double( env.m)
    yy = fm.IsMeasureSuperadditiveMob( pMob, env)
    return yy



# int py_IsMeasureSupermodularMob(double* Mob, struct_fm_env* env)
def IsMeasureSupermodularMob(Mob, env):
    trace( "int IsMeasureSupermodularMob(double* Mob, struct_fm_env* env)")
    Mob, pMob = create_float_zeros_as_CFFI_double( env.m)
    yy = fm.IsMeasureSupermodularMob( pMob, env)
    return yy



# int py_IsMeasureSymmetricMob(double* Mob, struct_fm_env* env)
def IsMeasureSymmetricMob(Mob, env):
    trace( "int IsMeasureSymmetricMob(double* Mob, struct_fm_env* env)")
    Mob, pMob = create_float_zeros_as_CFFI_double( env.m)
    yy = fm.IsMeasureSymmetricMob( pMob, env)
    return yy



# int py_IsMeasureKMaxitiveMob(double* Mob, struct_fm_env* env)
def IsMeasureKMaxitiveMob(Mob, env):
    trace( "int IsMeasureKMaxitiveMob(double* Mob, struct_fm_env* env)")
    Mob, pMob = create_float_zeros_as_CFFI_double( env.m)
    yy = fm.IsMeasureKMaxitiveMob( pMob, env)
    return yy



# void py_Mobius(double* v, double* MobVal, struct_fm_env* env)
def Mobius(v, MobVal, env):
    trace( "void Mobius(double* v, double* MobVal, struct_fm_env* env)")
    v, pv = create_float_zeros_as_CFFI_double( env.m)
    MobVal, pMobVal = create_float_zeros_as_CFFI_double( env.m)
    fm.Mobius( pv, pMobVal, env)



# double py_Orness(double* Mob, struct_fm_env* env)
def Orness(Mob, env):
    trace( "double Orness(double* Mob, struct_fm_env* env)")
    Mob, pMob = create_float_zeros_as_CFFI_double( env.m)
    yy = fm.Orness( pMob, env)
    return yy



# double py_OWA(double* x, double* v, struct_fm_env* env)
def OWA(x, v, env):
    trace( "double OWA(double* x, double* v, struct_fm_env* env)")
    x, px = create_float_zeros_as_CFFI_double( env.m)
    v, pv = create_float_zeros_as_CFFI_double( env.m)
    yy = fm.OWA( px, pv, env)
    return yy



# double py_WAM(double* x, double* v, struct_fm_env* env)
def WAM(x, v, env):
    trace( "double WAM(double* x, double* v, struct_fm_env* env)")
    x, px = create_float_zeros_as_CFFI_double( env.m)
    v, pv = create_float_zeros_as_CFFI_double( env.m)
    yy = fm.WAM( px, pv, env)
    return yy



# void py_Zeta(double* Mob, double* v, struct_fm_env* env)
def Zeta(Mob, v, env):
    trace( "void Zeta(double* Mob, double* v, struct_fm_env* env)")
    Mob, pMob = create_float_zeros_as_CFFI_double( env.m)
    v, pv = create_float_zeros_as_CFFI_double( env.m)
    fm.Zeta( pMob, pv, env)



# void py_dualMobKadd(int m, int length, int k, double* src, double* dest, struct_fm_env* env)
def dualMobKadd(m, length, k, src, dest, env):
    trace( "void dualMobKadd(int m, int length, int k, double* src, double* dest, struct_fm_env* env)")
    src, psrc = create_float_zeros_as_CFFI_double( env.m)
    dest, pdest = create_float_zeros_as_CFFI_double( env.m)
    fm.dualMobKadd( m, length, k, psrc, pdest, env)



# void py_Shapley2addMob(double* v, double* x, int n)
def Shapley2addMob(v, x, n):
    trace( "void Shapley2addMob(double* v, double* x, int n)")
    v, pv = create_float_zeros_as_CFFI_double( n)
    x, px = create_float_zeros_as_CFFI_double( n)
    fm.Shapley2addMob( pv, px, n)



# void py_Banzhaf2addMob(double* v, double* x, int n)
def Banzhaf2addMob(v, x, n):
    trace( "void Banzhaf2addMob(double* v, double* x, int n)")
    v, pv = create_float_zeros_as_CFFI_double( n)
    x, px = create_float_zeros_as_CFFI_double( n)
    fm.Banzhaf2addMob( pv, px, n)



# double py_Choquet2addMob(double* x, double* Mob, int n)
#def Choquet2addMob(double* x, int):
#    trace( "double Choquet2addMob(double*x, double* Mob, int n)")
#    double*, pdouble* = create_float_zeros_as_CFFI_double( n)
#    yy = fm.Choquet2addMob( pdouble, int)
#    return yy



# int py_fm_arraysize(int n, int kint, struct_fm_env* env)
def fm_arraysize(n, kint, env):
    trace( "int fm_arraysize(int n, int kint, struct_fm_env* env)")
    yy = fm.fm_arraysize( n, kint, env)
    return yy



# int py_generate_fm_minplus(int num, int n, int kint, int markov, int option, double K, double* vv, struct_fm_env* env)
def generate_fm_minplus(num, n, kint, markov, option, K, vv, env):
    trace( "int generate_fm_minplus(int num, int n, int kint, int markov, int option, double K, double* vv, struct_fm_env* env)")
    vv, pvv = create_float_zeros_as_CFFI_double( env.m)
    yy = fm.generate_fm_minplus( num, n, kint, markov, option, K, pvv, env)
    return yy



# int py_generate_fm_2additive_convex(int num, int n,  double * vv)
#def generate_fm_2additive_convex(num, n, *):
#    trace( "int generate_fm_2additive_convex(int num, int n,  double * vv)")
#    yy = fm.generate_fm_2additive_convex( num, n, )
#    return yy



# int py_generate_fm_2additive_convex_withsomeindependent(int num, int n, double * vv)
#def generate_fm_2additive_convex_withsomeindependent(num, n, *):
#    trace( "int generate_fm_2additive_convex_withsomeindependent(int num, int n, double * vv)")
#    yy = fm.generate_fm_2additive_convex_withsomeindependent( num, n, )
#    return yy



# void py_prepare_fm_sparse(int n, int tupsize, int* tuples, struct_fm_env_sparse* env)
def prepare_fm_sparse(n, tupsize, tuples, env):
    trace( "void prepare_fm_sparse(int n, int tupsize, int* tuples, struct_fm_env_sparse* env)")
    tuples, ptuples = create_intc_zeros_as_CFFI_int( env.m)
    fm.prepare_fm_sparse( n, tupsize, ptuples, env)



# int py_tuple_cardinality_sparse(int i, struct_fm_env_sparse* env)
def tuple_cardinality_sparse(i, env):
    trace( "int tuple_cardinality_sparse(int i, struct_fm_env_sparse* env)")
    yy = fm.tuple_cardinality_sparse( i, env)
    return yy



# int py_get_num_tuples(struct_fm_env_sparse* env)
def get_num_tuples(env):
    trace( "int get_num_tuples(struct_fm_env_sparse* env)")
    yy = fm.get_num_tuples( env)
    return yy



# int py_get_sizearray_tuples(struct_fm_env_sparse* env)
def get_sizearray_tuples(env):
    trace( "int get_sizearray_tuples(struct_fm_env_sparse* env)")
    yy = fm.get_sizearray_tuples( env)
    return yy



# int py_is_inset_sparse(int A, int card, int i, struct_fm_env_sparse* env)
def is_inset_sparse(A, card, i, env):
    trace( "int is_inset_sparse(int A, int card, int i, struct_fm_env_sparse* env)")
    yy = fm.is_inset_sparse( A, card, i, env)
    return yy



# int py_is_subset_sparse(int A, int cardA, int B, int cardB, struct_fm_env_sparse* env)
def is_subset_sparse(A, cardA, B, cardB, env):
    trace( "int is_subset_sparse(int A, int cardA, int B, int cardB, struct_fm_env_sparse* env)")
    yy = fm.is_subset_sparse( A, cardA, B, cardB, env)
    return yy



# double py_min_subset_sparse(double* x, int n, int S, int cardS, struct_fm_env_sparse* env)
def min_subset_sparse(x, n, S, cardS, env):
    trace( "double min_subset_sparse(double* x, int n, int S, int cardS, struct_fm_env_sparse* env)")
    x, px = create_float_zeros_as_CFFI_double( env.m)
    yy = fm.min_subset_sparse( px, n, S, cardS, env)
    return yy



# double py_max_subset_sparse(double* x, int n, int S, int cardS, struct_fm_env_sparse* env)
def max_subset_sparse(x, n, S, cardS, env):
    trace( "double max_subset_sparse(double* x, int n, int S, int cardS, struct_fm_env_sparse* env)")
    x, px = create_float_zeros_as_CFFI_double( env.m)
    yy = fm.max_subset_sparse( px, n, S, cardS, env)
    return yy



# double py_ChoquetMob_sparse(double* x, int n, struct_fm_env_sparse* env)
def ChoquetMob_sparse(x, n, env):
    trace( "double ChoquetMob_sparse(double* x, int n, struct_fm_env_sparse* env)")
    x, px = create_float_zeros_as_CFFI_double( env.m)
    yy = fm.ChoquetMob_sparse( px, n, env)
    return yy



# void py_ShapleyMob_sparse(double* v, int n, struct_fm_env_sparse* env)
def ShapleyMob_sparse(v, n, env):
    trace( "void ShapleyMob_sparse(double* v, int n, struct_fm_env_sparse* env)")
    v, pv = create_float_zeros_as_CFFI_double( env.m)
    fm.ShapleyMob_sparse( pv, n, env)



# void py_BanzhafMob_sparse(double* v, int n, struct_fm_env_sparse* env)
def BanzhafMob_sparse(v, n, env):
    trace( "void BanzhafMob_sparse(double* v, int n, struct_fm_env_sparse* env)")
    v, pv = create_float_zeros_as_CFFI_double( env.m)
    fm.BanzhafMob_sparse( pv, n, env)



# void py_populate_fm_2add_sparse(double* singletons, int numpairs, double* pairs, int* indicesp1, int* indicesp2, struct_fm_env_sparse* env)
def populate_fm_2add_sparse(singletons, numpairs, pairs, indicesp1, indicesp2, env):
    trace( "void populate_fm_2add_sparse(double* singletons, int numpairs, double* pairs, int* indicesp1, int* indicesp2, struct_fm_env_sparse* env)")
    singletons, psingletons = create_float_zeros_as_CFFI_double( env.m)
    pairs, ppairs = create_float_zeros_as_CFFI_double( env.m)
    indicesp1, pindicesp1 = create_intc_zeros_as_CFFI_int( env.m)
    indicesp2, pindicesp2 = create_intc_zeros_as_CFFI_int( env.m)
    fm.populate_fm_2add_sparse( psingletons, numpairs, ppairs, pindicesp1, pindicesp2, env)



# void py_add_pair_sparse(int i, int j, double v, struct_fm_env_sparse* env)
def add_pair_sparse(i, j, v, env):
    trace( "void add_pair_sparse(int i, int j, double v, struct_fm_env_sparse* env)")
    fm.add_pair_sparse( i, j, v, env)



# void py_add_tuple_sparse(int tupsize, int* tuple, double v, struct_fm_env_sparse* env)
def add_tuple_sparse(tupsize, tuple, v, env):
    trace( "void add_tuple_sparse(int tupsize, int* tuple, double v, struct_fm_env_sparse* env)")
    tuple, ptuple = create_intc_zeros_as_CFFI_int( env.m)
    fm.add_tuple_sparse( tupsize, ptuple, v, env)



# void py_populate_fm_2add_sparse_from2add(int n, double* v, struct_fm_env_sparse* env)
def populate_fm_2add_sparse_from2add(n, v, env):
    trace( "void populate_fm_2add_sparse_from2add(int n, double* v, struct_fm_env_sparse* env)")
    v, pv = create_float_zeros_as_CFFI_double( env.m)
    fm.populate_fm_2add_sparse_from2add( n, pv, env)



# void py_expand_2add_full(double* v, struct_fm_env_sparse* env)
def expand_2add_full(v, env):
    trace( "void expand_2add_full(double* v, struct_fm_env_sparse* env)")
    v, pv = create_float_zeros_as_CFFI_double( env.m)
    fm.expand_2add_full( pv, env)



# void py_expand_sparse_full(double* v, struct_fm_env_sparse* env)
def expand_sparse_full(v, env):
    trace( "void expand_sparse_full(double* v, struct_fm_env_sparse* env)")
    v, pv = create_float_zeros_as_CFFI_double( env.m)
    fm.expand_sparse_full( pv, env)



# void py_sparse_get_singletons(int n, double* v, struct_fm_env_sparse* env)
def sparse_get_singletons(n, v, env):
    trace( "void sparse_get_singletons(int n, double* v, struct_fm_env_sparse* env)")
    v, pv = create_float_zeros_as_CFFI_double( env.m)
    fm.sparse_get_singletons( n, pv, env)



# int py_sparse_get_pairs(int* pairs, double* v, struct_fm_env_sparse* env)
def sparse_get_pairs(pairs, v, env):
    trace( "int sparse_get_pairs(int* pairs, double* v, struct_fm_env_sparse* env)")
    pairs, ppairs = create_intc_zeros_as_CFFI_int( env.m)
    v, pv = create_float_zeros_as_CFFI_double( env.m)
    yy = fm.sparse_get_pairs( ppairs, pv, env)
    return yy



# int py_sparse_get_tuples(int* tuples, double* v, struct_fm_env_sparse* env)
def sparse_get_tuples(tuples, v, env):
    trace( "int sparse_get_tuples(int* tuples, double* v, struct_fm_env_sparse* env)")
    tuples, ptuples = create_intc_zeros_as_CFFI_int( env.m)
    v, pv = create_float_zeros_as_CFFI_double( env.m)
    yy = fm.sparse_get_tuples( ptuples, pv, env)
    return yy



# int   py_generate_fm_2additive_convex_sparse(int n, struct_fm_env_sparse* env)
def generate_fm_2additive_convex_sparse(n, env):
    trace( "int   generate_fm_2additive_convex_sparse(int n, struct_fm_env_sparse* env)")
    yy = fm.generate_fm_2additive_convex_sparse( n, env)
    return yy



# int   py_generate_fm_kadditive_convex_sparse(int n, int k, int nonzero, struct_fm_env_sparse* env)
def generate_fm_kadditive_convex_sparse(n, k, nonzero, env):
    trace( "int   generate_fm_kadditive_convex_sparse(int n, int k, int nonzero, struct_fm_env_sparse* env)")
    yy = fm.generate_fm_kadditive_convex_sparse( n, k, nonzero, env)
    return yy



# void py_Nonmodularityindex_sparse(double* w, int n, struct_fm_env_sparse* env)
def Nonmodularityindex_sparse(w, n, env):
    trace( "void Nonmodularityindex_sparse(double* w, int n, struct_fm_env_sparse* env)")
    w, pw = create_float_zeros_as_CFFI_double( env.m)
    fm.Nonmodularityindex_sparse( pw, n, env)




