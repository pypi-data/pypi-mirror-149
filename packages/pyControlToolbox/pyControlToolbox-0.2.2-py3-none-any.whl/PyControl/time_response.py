import numpy as np
from . import continous as cont


def __setupArrs(system, U, initX=0, time=10, h=0.001, to=0):
    A = B = C = D = np.array([])
    if isinstance(system, cont.tf):
        systemSS = cont.tf2ss(system)
        A = systemSS.A
        B = systemSS.B
        C = systemSS.C
        D = systemSS.D
    else:
        A = system.A
        B = system.B
        C = system.C
        D = system.D
    rowNum = np.shape(A)[0]
    if isinstance(initX, np.ndarray):
        Xo = np.array([initX])
    elif initX == 0:
        Xo = np.zeros((1, rowNum))
    else:
        temp = np.full((rowNum, 1), initX)
        Xo = temp
    X = np.transpose(Xo)
    Y = np.array([])
    C = np.array([C])
    Yo = np.dot(C, X) + D
    Y = np.append(Y, Yo)
    T = np.array([])
    T = np.append(T, to)
    t = to
    N = int((time - to) / h)  # number of simulation steps
    return A, B, C, D, X, Y, T, N, t


# calculating time domain response and state trajectory of LTI system using Explicit (Forward) Euler method [time in
# seconds]
def solveEE(system, U, initX=0, time=10, h=0.001, to=0):
    A, B, C, D, X, Y, T, N, t = __setupArrs(system, U, initX, time, h, to)
    Udlt = False
    if U == 'delta':
        U = 1
        Udlt = True
    for i in range(N):
        t += h
        Xprev = X[:, [i]]  # ith column of X
        Xnext = Xprev + h * (np.dot(A, Xprev) + np.dot(B, U))  # Forward Euler formula
        X = np.c_[X, Xnext]  # adding new column
        Ytemp = np.dot(C, Xnext)
        Y = np.append(Y, Ytemp)
        T = np.append(T, t)
        if Udlt:
            U = 0
            Udlt = False
    return Y, T, X


# calculating time domain response and state trajectory of LTI system using Implicit (Backward) Euler method
def solveIE(system, U, initX=0, time=10, h=0.001, to=0):
    A, B, C, D, X, Y, T, N, t = __setupArrs(system, U, initX, time, h, to)
    Udlt = False
    if U == 'delta':
        U = 1
        Udlt = True
    for i in range(N):
        t += h
        Xprev = X[:, [i]]
        XFE = Xprev + h * (np.dot(A, Xprev) + np.dot(B, U))  # takes Implicit Euler method's step for approximation
        Xnext = Xprev + h * (np.dot(A, XFE) + np.dot(B, U))
        X = np.c_[X, Xnext]
        Ytemp = np.dot(C, Xnext)
        Y = np.append(Y, Ytemp)
        T = np.append(T, t)
        if Udlt:
            U = 0
            Udlt = False
    return Y, T, X


# calculating time domain response and state trajectory of LTI system using Trapezoidal method
def solveTrap(system, U, initX=0, time=10, h=0.001, to=0):
    A, B, C, D, X, Y, T, N, t = __setupArrs(system, U, initX, time, h, to)
    Udlt = False
    if U == 'delta':
        U = 1
        Udlt = True
    for i in range(N):
        t += h
        Xprev = X[:, [i]]
        Xnprim = np.dot(A, Xprev) + np.dot(B, U)
        XFE = Xprev + h * Xnprim
        Xnext = Xprev + (h / 2) * (
                    Xnprim + (np.dot(A, XFE) + np.dot(B, U)))  # takes average of the slopes from IE and EE methods
        X = np.c_[X, Xnext]
        Ytemp = np.dot(C, Xnext)
        Y = np.append(Y, Ytemp)
        T = np.append(T, t)
        if Udlt:
            U = 0
            Udlt = False
    return Y, T, X


# calculating time domain response and state trajectory of LTI system using Runge-Kutta 4 method
# X' = f(X) => X' = A*X + B*U
def solveRK4(system, U, initX=0, time=10, h=0.001, to=0):
    A, B, C, D, X, Y, T, N, t = __setupArrs(system, U, initX, time, h, to)
    k1 = k2 = k3 = k4 = np.array([])
    Udlt = False
    if U == 'delta':
        U = 1
        Udlt = True
    for i in range(N):
        t += h
        Xprev = X[:, [i]]
        f = np.dot(A, Xprev) + np.dot(B, U)
        k1 = h * f
        k2 = h * (f + k1 / 2)
        k3 = h * (f + k2 / 2)
        k4 = h * (f + k3)
        Xnext = Xprev + (k1 + 2 * k2 + 2 * k3 + k4) / 6
        X = np.c_[X, Xnext]
        Ytemp = np.dot(C, Xnext)
        Y = np.append(Y, Ytemp)
        T = np.append(T, t)
        if Udlt:
            U = 0
            Udlt = False
    return Y, T, X
