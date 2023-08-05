# Functions to combine NumPy arrays in C++ 
import numpy as np
import types
import math
from  _pyfmtools import ffi, lib as fm

# Trace function
def trace( str):
    print( "-- ", str, " --")


# convert Python float to CFFI double * 
def convert_float_to_CFFI_double( x):
    if x.dtype != "float64": x = x.astype(float)
    px = ffi.cast( "double *", x.ctypes.data)
    return px


def py_fm_init( n):
    try:
        trace( "py_fm_init")
        env = ffi.new( "struct fm_env *")
        fm.py_fm_init( n, env)
        return env
    except ValueError:
        raise


def py_fm_free( env):
    try:
        trace( "py_fm_free")
        if( env == None): raise ValueError( "Env not initialised") 
        fm.py_fm_free( env)
    except ValueError:
        raise


def py_ShowCoalitions( env):
    trace( "py_ShowCoalitions")
    A = np.zeros( env.m, int)
    pA = ffi.cast( "int *", A.ctypes.data)
    fm.py_ShowCoalitions( pA, env)
    return A


def py_generate_fm_2additive_concave( ti, n, env):
    trace( "py_generate_fm_2additive_concave")
    v = np.zeros( env.m, float)
    pv = ffi.cast( "double *", v.ctypes.data)
    size = fm.py_generate_fm_2additive_concave( ti, n, pv)
    return size, v


def py_ShowCoalitionsCard( env):
    trace( "py_ShowCoalitionsCard")
    A = np.zeros( env.m, int)
    pA = ffi.cast( "int *", A.ctypes.data)
    A = fm.py_ShowCoalitionsCard( pA, env)
    return A


def py_generate_fmconvex_tsort( num, n, kint, markov, option, K, env):
    trace( "py_generate_fmconvex_tsort")
    v = np.zeros( env.m, float)
    pv = ffi.cast( "double *", v.ctypes.data)
    size = fm.py_generate_fmconvex_tsort( num ,n, kint, markov, option, K, pv, env)
    return size, v


def py_generate_fm_tsort( num, n, kint, markov, option, K, env):
    trace( "py_generate_fm_tsort")
    v = np.zeros( env.m, float)
    pv = ffi.cast( "double *", v.ctypes.data)
    size = fm.py_generate_fm_tsort( num ,n, kint, markov, option, K, env)
    return size, v


def py_ConvertCard2Bit( v, env):
    trace( "py_ConvertCard2Bit")
    
    pv = convert_float_to_CFFI_double( v)
    vb = np.zeros( env.m, float)
    pvb = ffi.cast( "double *", vb.ctypes.data)
    fm.py_ConvertCard2Bit( pvb, pv, env)
    return vb 


def py_IsMeasureSupermodular( vb, env):
    trace( "py_IsMeasureSupermodular")
    pvb = convert_float_to_CFFI_double( vb)
    return fm.py_IsMeasureSupermodular( pvb, env)


def py_IsMeasureAdditive( vb, env):
    trace( "y_IsMeasureAdditive")
    pvb = convert_float_to_CFFI_double( vb)
    return fm.py_IsMeasureAdditive( pvb, env)


def py_export_maximal_chains( n, vb, env):
    trace( "py_export_maximal_chains")
    pvb = convert_float_to_CFFI_double( vb)
    mc = np.zeros( math.factorial(n) * n, float)
    pmc = ffi.cast( "double *", mc.ctypes.data)
    fm.py_export_maximal_chains( n, pvb, pmc, env)
    return mc


def py_Choquet( x, vb, env):
    trace( "y_Choquet")
    npx = np.array( x)
    pnpx = ffi.cast( "double *", npx.ctypes.data)
    pvb = convert_float_to_CFFI_double( vb)
    return fm.py_Choquet( pnpx, pvb, env)


def py_Sugeno( x, vb, env):
    trace( "py_Sugeno")
    npx = np.array( x)
    pnpx = ffi.cast( "double *", npx.ctypes.data)
    pvb = convert_float_to_CFFI_double( vb)
    return fm.py_Sugeno( pnpx, pvb, env)





