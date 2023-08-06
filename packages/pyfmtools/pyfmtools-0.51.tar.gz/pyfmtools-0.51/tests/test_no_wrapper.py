import numpy as np
import math

from  _pyfmtools import ffi,lib as fm


r=3
n=3
env=ffi.new( "struct fm_env *")
fm.py_fm_init( n, env)

A=np.zeros(env.m, np.intc)
pA = ffi.cast("int *", A.ctypes.data)
fm.py_ShowCoalitions(pA, env)
print("Fuzzy measure wrt n=3 criteria has ",env.m," parameters ordered like this (binary order)")
print(A)
fm.py_fm_free( env);

ti=1
n=4
fm.py_fm_init(n,  env);
v=np.zeros(env.m,float);
pv = ffi.cast("double *", v.ctypes.data);
vb=np.zeros(env.m,float);
pvb = ffi.cast("double *", vb.ctypes.data);


size=fm.py_generate_fm_2additive_concave(ti,n,pv)
print("2-additive concave FM in Mobius and its length (n=4)")
print(v)
print("has ", size, " nonzero parameters ")

print("A convex FM in cardinality ordering ")
A=np.zeros(env.m, np.intc)
pA = ffi.cast("int *", A.ctypes.data)
fm.py_ShowCoalitionsCard(pA, env)
print(A)

size=fm.py_generate_fmconvex_tsort(ti,n, n-1 , 1000, 8, 1, pv,env)
#size=fm.py_generate_fm_tsort(ti,n, 2 , 10, 0, 0.1, pv,env)
print(v)

fm.py_ConvertCard2Bit(pvb,pv,env)
print("a convex FM in binary ordering ")
fm.py_ShowCoalitions(pA, env)
print(A)
print(vb)
r=fm.py_IsMeasureSupermodular(pvb,env)
print("Is it convex (test)?", r)
r=fm.py_IsMeasureAdditive(pvb,env)
print("Is it additive (test)?", r)



mc=np.zeros(math.factorial(n)*n,float)
pmc = ffi.cast("double *", mc.ctypes.data)


fm.py_export_maximal_chains(n,pvb,pmc,env)
print("Export maximal chains ")
print(mc)

x=np.array([0.2,0.1,0.6,0.2])
px = ffi.cast("double *", x.ctypes.data)

z=fm.py_Choquet(px,pvb,env)
print("Choquet integral of ",x, " is ",z)
z=fm.py_Sugeno(px,pvb,env)
print("Sugeno integral of ",x,  " is ",z)


fm.py_fm_free( env);
