from __future__ import annotations

from math import gcd
from functools import reduce
from pathlib import Path
from html import escape
from mpmath import mp

mp.dps = 330

P = (30921, -32972, 8240)
Q = (33750, -36000, 9000)


def raw_matrix(n: int):
    m11 = (-2*n-5)*(n+3)**2*(136*n**4+1424*n**3+5548*n**2+9551*n+6141)
    m12 = 384*n**6+6384*n**5+44168*n**4+162698*n**3+336377*n**2+369933*n+169011
    m13 = -(480*n**4+4980*n**3+19210*n**2+32690*n+20730)
    m21 = (n+2)**2*(n+3)**2*(4*n+10)*(48*n**3+386*n**2+1017*n+879)
    m22 = (n+2)**2*(-272*n**5-3848*n**4-21732*n**3-61184*n**2-85761*n-47808)
    m23 = (n+2)**2*(320*n**3+2540*n**2+6610*n+5640)
    m31 = (-4*n-10)*(n+2)**2*(n+3)**2*(32*n**4+302*n**3+1037*n**2+1530*n+813)
    m32 = (n+2)**2*(192*n**6+2984*n**5+19116*n**4+64452*n**3+120256*n**2+117279*n+46476)
    m33 = (n+2)**2*(-16*n**5-408*n**4-2912*n**3-8884*n**2-12254*n-6240)
    return ((m11,m12,m13),(m21,m22,m23),(m31,m32,m33))


def content(v):
    return reduce(gcd, (abs(x) for x in v if x), 0) or 1


def backward_column(N: int, seed: int = 0, transpose: bool = False):
    # This computes M(0)...M(N-1)e_seed up to a scalar.  Replacing M by
    # M_H=M/delta_H does not change the projective column.
    v = [0,0,0]
    v[seed] = 1
    for n in range(N-1, -1, -1):
        M = raw_matrix(n)
        if transpose:
            w = [sum(M[j][i]*v[j] for j in range(3)) for i in range(3)]
        else:
            w = [sum(M[i][j]*v[j] for j in range(3)) for i in range(3)]
        g = content(w)
        v = [x//g for x in w]
        # Fix a harmless projective sign for reproducibility.
        k = next((x for x in v if x), 1)
        if k < 0:
            v = [-x for x in v]
    return tuple(v)


def mpq(a: int, b: int):
    return mp.mpf(a)/mp.mpf(b)


def normalized(v):
    return [mpq(x,v[0]) for x in v]


def dot_int(row, v):
    return sum(row[i]*v[i] for i in range(3))


def ratio_from_column(v):
    return mpq(dot_int(P,v), dot_int(Q,v))


def rel_digits(x,y):
    e = abs(x-y)/max(mp.mpf(1),abs(x),abs(y))
    return mp.inf if e == 0 else -mp.log10(e)


def pslq(vals, maxcoeff=10**14, tol_exp=230, maxsteps=100000):
    try:
        from mpmath.identification import pslq as _pslq
        return _pslq(mp, [mp.mpf(x) for x in vals],
                     tol=mp.mpf(10)**(-tol_exp),
                     maxcoeff=maxcoeff, maxsteps=maxsteps)
    except Exception as exc:
        return 'ERROR: %s: %s' % (type(exc).__name__, exc)


def fmt(x, d=235):
    return mp.nstr(x,d)

Ns = [100,120,140,160,180,200,220]
cols = {N: backward_column(N,0,False) for N in Ns}
v = cols[220]
V = normalized(v)

p_num = dot_int(P,v)
q_num = dot_int(Q,v)
pV = mpq(p_num,v[0])
qV = mpq(q_num,v[0])
ratio = mpq(p_num,q_num)
G = mp.catalan
resid = pV-G*qV

# Unit Euclidean normalization, included to expose scale dependence.
norm = mp.sqrt(sum(x*x for x in V))
Vunit = [x/norm for x in V]
if sum(mp.mpf(Q[i])*Vunit[i] for i in range(3)) < 0:
    Vunit = [-x for x in Vunit]
pVu = sum(mp.mpf(P[i])*Vunit[i] for i in range(3))
qVu = sum(mp.mpf(Q[i])*Vunit[i] for i in range(3))

# All three terminal columns, and the incorrect transpose convention.
seeds = {j: backward_column(220,j,False) for j in range(3)}
wrong = backward_column(220,0,True)
wrongV = normalized(wrong)
wrongratio = ratio_from_column(wrong)

sqrt2 = mp.sqrt(2); pi=mp.pi; log2=mp.log(2); zeta3=mp.zeta(3)
Khalf=mp.ellipk(mp.mpf('0.5'))
Ksilver=mp.ellipk((sqrt2-1)**2)
Kminus1=mp.ellipk(-1)
basis_names=['1','G','pi','log(2)','pi^2','G^2','pi*G','pi*log(2)','G*log(2)','zeta(3)','K(1/2)','K((sqrt2-1)^2)','K(-1)']
basis=[1,G,pi,log2,pi*pi,G*G,pi*G,pi*log2,G*log2,zeta3,Khalf,Ksilver,Kminus1]

relations = {
 'pV_vs_GqV': pslq([pV,G*qV],10**8,230),
 'requested_triple': pslq([pV,qV,G*qV-pV],10**8,230),
 'qV_broad': pslq([qV]+basis,10**12,210),
 'pV_broad': pslq([pV]+basis,10**12,210),
 'V1_broad': pslq([V[1]]+basis,10**12,210),
 'V2_broad': pslq([V[2]]+basis,10**12,210),
 'qV_basic': pslq([qV,1,G,pi,log2],10**20,220),
 'pV_basic': pslq([pV,1,G,pi,log2],10**20,220),
 'qV_elliptic': pslq([qV,1,pi,Khalf,Ksilver,Kminus1],10**20,220),
 'pV_elliptic': pslq([pV,1,pi,Khalf,Ksilver,Kminus1],10**20,220),
}

lines=[]
lines.append('Q4913 exact projective Birkhoff computation')
lines.append('mpmath precision: 330 decimal digits')
lines.append('Normalization: V[0]=1 unless explicitly marked unit norm.')
lines.append('')
lines.append('STABILITY OF PROJECTIVE COLUMN')
for a,b in zip(Ns[:-1],Ns[1:]):
    Va=normalized(cols[a]); Vb=normalized(cols[b])
    d=min(rel_digits(Va[i],Vb[i]) for i in range(3))
    lines.append('N=%d vs N=%d: %.20s decimal digits' % (a,b,fmt(d,25)))
lines.append('')
lines.append('V WITH V[0]=1')
for i,x in enumerate(V): lines.append('V[%d] = %s' % (i,fmt(x)))
lines.append('')
lines.append('p.V = '+fmt(pV))
lines.append('q.V = '+fmt(qV))
lines.append('(p.V)/(q.V) = '+fmt(ratio))
lines.append('Catalan G = '+fmt(G))
lines.append('ratio-G = '+fmt(ratio-G))
lines.append('p.V-G*q.V = '+fmt(resid))
lines.append('')
lines.append('UNIT NORM NORMALIZATION')
for i,x in enumerate(Vunit): lines.append('Vunit[%d] = %s' % (i,fmt(x)))
lines.append('p.Vunit = '+fmt(pVu))
lines.append('q.Vunit = '+fmt(qVu))
lines.append('ratio_unit-G = '+fmt(pVu/qVu-G))
lines.append('')
lines.append('TERMINAL-SEED AUDIT')
for j,c in seeds.items():
    VV=normalized(c)
    lines.append('seed e%d: ratio-G=%s' % (j+1,fmt(ratio_from_column(c)-G,90)))
    lines.append('  V1=%s' % fmt(VV[1],90))
    lines.append('  V2=%s' % fmt(VV[2],90))
lines.append('')
lines.append('INCORRECT TRANSPOSE BACKWARD TRANSPORT')
lines.append('wrong V1='+fmt(wrongV[1],90))
lines.append('wrong V2='+fmt(wrongV[2],90))
lines.append('wrong ratio-G='+fmt(wrongratio-G,90))
lines.append('')
lines.append('PSLQ')
lines.append('basis order: '+', '.join(basis_names))
for k,r in relations.items(): lines.append(k+' = '+repr(r))
lines.append('')
lines.append('ELLIPTIC CONSTANTS')
lines.append('K(1/2)='+fmt(Khalf,100))
lines.append('K((sqrt(2)-1)^2)='+fmt(Ksilver,100))
lines.append('K(-1)='+fmt(Kminus1,100))

text='\n'.join(lines)+'\n'
print(text)
Path('static/q4913/index.html').write_text(
    '<!doctype html><meta charset="utf-8"><title>Q4913 result</title>'
    '<pre>'+escape(text)+'</pre>', encoding='utf-8')
