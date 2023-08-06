import sympy as sp
from . import continous


def symss2tf(A, B, C, D):
    s = sp.symbols('s')
    Amat = sp.Matrix(A)
    degree = sp.shape(Amat)[0] + 1
    Bmat = sp.Matrix(B)
    Cmat = sp.Matrix(C)
    Dmat = sp.Matrix(D)
    I = sp.eye(sp.shape(Amat)[0])
    own = s * I - Amat
    detOwn = sp.det(own)
    ownReversed = own.inv()
    Gmat = sp.simplify(Cmat * ownReversed * Bmat - Dmat)
    tmp = detOwn * Gmat
    r, c = sp.shape(Gmat)
    r = max(r, c)
    Gs = []
    G = []
    for elem in range(r):
        n, d = sp.fraction(Gmat[elem])
        d = sp.Poly(d).all_coeffs()
        if len(d) != degree:
            Gs.append(1 / tmp[elem])
        else:
            Gs.append(Gmat[elem])
    for transferFun in Gs:
        num, den = sp.fraction(transferFun)
        num = sp.Poly(num).all_coeffs()
        den = sp.Poly(den).all_coeffs()
        tfsystem = continous.tf(num, den)
        G.append(tfsystem)
    return G
        

        
