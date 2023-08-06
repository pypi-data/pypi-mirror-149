import wrapper as pyw

r=3
n=3
env = pyw.fm_init( n)

A = pyw.ShowCoalitions( env)
print( "Fuzzy measure wrt n=3 criteria has ",env.m," parameters ordered like this (binary order)")
print( A)
pyw.fm_free( env);

ti=1
n=4
env = pyw.fm_init( n);
size, v = pyw.generate_fm_2additive_concave( ti,n, env)
print( "2-additive concave FM in Mobius and its length (n=4)")
print( v)
print("has ", size, " nonzero parameters ")

print("A convex FM in cardinality ordering ")
A = pyw.ShowCoalitionsCard( env)
print( A)

size, v = pyw.generate_fmconvex_tsort( ti, n, n-1 , 1000, 8, 1, env)
print( v)
print("has ", size, " nonzero parameters ")

vb = pyw.ConvertCard2Bit( v, env)

print("a convex FM in binary ordering ")
A = pyw.ShowCoalitions( env)
print( A)
print( vb)

r = pyw.IsMeasureSupermodular( vb, env)
print( "Is it convex (test)?", r)
r = pyw.IsMeasureAdditive( vb, env)
print("Is it additive (test)?", r)

mc = pyw.export_maximal_chains( n, vb, env)
print( "Export maximal chains ")
print( mc)

x = [0.2,0.1,0.6,0.2]
z = pyw.Choquet( x, vb, env)
print( "Choquet integral of ",x, " is ",z)

z = pyw.Sugeno( x, vb, env)
print("Sugeno integral of ",x,  " is ",z)


###
# Test generated wrapper
###

x = [0.2,0.5,0.4]
v = [0,0.3,0.5,0.6,0.4,0.8,0.7,1]
kint = 2
r = pyw.ChoquetKinter( x, v, kint, env)
print( "Choquet integral of: ", kint, x, v)
print( "equals: ", r)

v = [0,0.3,0.5,0.6,0.4,0.8,0.7,1]
r = pyw.Orness(v, env)
print( "orness value of the Choquet integral wrt fuzzy measure v: ", v)
print( "equals: ", r)


kint = 2
v = [0,0.3,0.5,0.6,0.4,0.8,0.7,1]
nm = [0.0] * env.m
pnm = pyw.NonmodularityIndexKinteractive( v, nm, kint, env)
print( "nonmodularity indices of k-interactive fuzzy measure v: ", kint, v)
print( "equals: ", pnm)


pyw.fm_free( env);
