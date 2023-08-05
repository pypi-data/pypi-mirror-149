from py_wrapper import py_fm_init
from py_wrapper import py_fm_free
from py_wrapper import py_ShowCoalitions
from py_wrapper import py_generate_fm_2additive_concave
from py_wrapper import py_ShowCoalitionsCard
from py_wrapper import py_generate_fmconvex_tsort
from py_wrapper import py_generate_fm_tsort
from py_wrapper import py_ConvertCard2Bit
from py_wrapper import py_ShowCoalitions
from py_wrapper import py_IsMeasureSupermodular
from py_wrapper import py_IsMeasureAdditive
from py_wrapper import py_export_maximal_chains
from py_wrapper import py_Choquet
from py_wrapper import py_Sugeno


r=3
n=3
env = py_fm_init( n)

A = py_ShowCoalitions( env)
print( "Fuzzy measure wrt n=3 criteria has ",env.m," parameters ordered like this (binary order)")
print( A)
py_fm_free( env);

ti=1
n=4
env = py_fm_init( n);
size, v = py_generate_fm_2additive_concave( ti,n, env)
print( "2-additive concave FM in Mobius and its length (n=4)")
print( v)
print("has ", size, " nonzero parameters ")

print("A convex FM in cardinality ordering ")
A = py_ShowCoalitionsCard( env)
print( A)

size, v = py_generate_fmconvex_tsort( ti, n, n-1 , 1000, 8, 1, env)
print( v)
print("has ", size, " nonzero parameters ")

vb = py_ConvertCard2Bit( v, env)

print("a convex FM in binary ordering ")
A = py_ShowCoalitions( env)
print( A)
print( vb)

r = py_IsMeasureSupermodular( vb, env)
print( "Is it convex (test)?", r)
r = py_IsMeasureAdditive( vb, env)
print("Is it additive (test)?", r)

mc = py_export_maximal_chains( n, vb, env)
print( "Export maximal chains ")
print( mc)

x = [0.2,0.1,0.6,0.2]
z = py_Choquet( x, vb, env)
print( "Choquet integral of ",x, " is ",z)

z = py_Sugeno( x, vb, env)
print("Sugeno integral of ",x,  " is ",z)


py_fm_free( env);
