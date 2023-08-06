import numpy as np
import matplotlib.pyplot as plt
from . import time_response as tresp
from . import helpers
from . import symbolic


# TODO:
# -root locus func
# -nyquist plots
# -function for model recognition
# -L and K matrices
# -discrete time variants

# denominator and numerator coefficients must be given in a specific order:
# numerator: a1*s^n + a2*s^(n-1) + a3*s^(n-2) + a4*s^(n-3) + ... + an =>  [a1, a2, a3, a4, ..., an]
# denominator: b1*s^n + b2*s^(n-1) + b3*s^(n-2) + b4*s^(n-3) + ... + bn => [b1, b2, b3, ..., bn]


class sys:
    def __init__(self):
        self.A = np.array([])
        self.B = np.array([])
        self.C = np.array([])
        self.D = np.array([])
        self.TFnumerator = np.array([])
        self.TFdenominator = np.array([])
        self.startCond = np.array([])

    # diagonal form
    def diag(self):  # TODO fix this
        if np.linalg.det(self.A) != 0:
            eigVals, eigVecs = np.linalg.eig(self.A)
            return eigVals, eigVecs
            # P = np.empty((np.size(eigVals), 0))  # transformation matrix
            # for eigenVector in eigVecs:
            #     P = np.column_stack((P, eigenVector))
            # invP = np.linalg.inv(P)
            # A = np.matmul(invP, np.matmul(self.A, P))
            # B = np.matmul(invP, self.B)
            # C = np.matmul(self.C, P)
            # return A, B, C
        else:
            raise Exception('Det(A) == 0, matrix A is not diagonalizable')

    # observable canonical form of SISO system
    # highest power of the s in denominator must be bigger than highest power in the numerator
    # highest power of s in denominator must have coefficient equal 1
    def obsv(self):
        num = self.TFnumerator
        den = self.TFdenominator
        numCols = np.size(self.TFnumerator)
        denCols = np.size(self.TFdenominator)
        if denCols <= numCols:
            raise Exception('Denominator must be higher order than numerator')
        if den[0] != 1:
            div = den[0]
            num = num / div
            den = den / div
        den = den[1:]
        numCols = np.size(num)
        denCols = np.size(den)
        if denCols > numCols:  # making numerator and denominator equal length filling with 0
            tempArr = np.zeros(denCols)
            tempArr[denCols - numCols:] = num
            num = tempArr
        obsvA = np.array([-1 * den]).transpose()  # column of minus denumerator values
        subMat = np.identity(denCols - 1)  # identity matrix
        subMat = np.vstack((subMat, np.zeros(denCols - 1)))  # row of 0 added to identity matrix
        obsvA = np.append(obsvA, subMat, axis=1)
        obsvB = num[..., None]  # column of numerator values
        obsvC = np.array([1])
        obsvC = np.append(obsvC, np.zeros(denCols - 1), axis=0)  # row of 0
        return obsvA, obsvB, obsvC

    # controllable canonical form of SISO system
    # highest power of the s in denominator must be bigger than highest power in the numerator
    # highest power of s in denominator must have coefficient equal 1
    def contr(self):
        num = self.TFnumerator
        den = self.TFdenominator
        numCols = np.size(self.TFnumerator)
        denCols = np.size(self.TFdenominator)
        if numCols >= denCols:
            raise Exception('Denominator must be higher order than numerator')
        if den[0] != 1:
            div = den[0]
            num = num / div
            den = den / div
        den = den[1:]
        numCols = np.size(num)
        denCols = np.size(den)
        if denCols > numCols:  # making numerator and denominator equal length filling with 0
            tempArr = np.zeros(denCols)
            tempArr[denCols - numCols:] = num
            num = tempArr
        contA = np.zeros(denCols - 1)[..., None]  # column of 0
        subMat = np.identity(denCols - 1)  # identity matrix
        contA = np.append(contA, subMat, axis=1)
        col = np.array([-1 * den])
        contA = np.append(contA, col, axis=0)
        contB = np.zeros(denCols - 1)[..., None]  # column of 0
        contB = np.vstack((contB, np.array([1])))
        contC = np.array(num)  # row of numerator values
        return contA, contB, contC


class ss(sys):
    def __init__(self, A, B, C, D=[0], stCond=None):
        super().__init__()
        if stCond is None:
            stCond = []
        self.A = np.array(A)
        tempB = np.array(B)
        self.B = np.reshape(tempB, (np.shape(tempB)[0], 1))
        self.C = np.array([C])
        self.D = np.array([D])
        if np.size(np.array(stCond)) < np.size(A, axis=0):  # if starting conditions vector is too short
            self.startCond = np.array(stCond)
            for i in range(np.size(A, axis=0) - np.size(self.startCond)):
                np.append(self.startCond, np.array([0]))
        else:
            raise Exception('number of starting conditions must be equal to the order of the system')

    def __str__(self):
        strA = str(self.A)
        strB = str(self.B)
        strC = str(self.C)
        strD = str(self.D)
        strRes = 'A = ' + strA + '\n' + 'B = ' + strB + '\n' + 'C = ' + strC + '\n' + 'D = ' + strD + '\n'
        return strRes


class tf(sys):
    def __init__(self, num, denum):
        super().__init__()
        self.TFnumerator = np.array(num)
        self.TFdenominator = np.array(denum)

    def __mul__(self, otherSys):
        newNumerator = np.polymul(self.TFnumerator, otherSys.TFnumerator)
        newDenominator = np.polymul(self.TFdenominator, otherSys.TFdenominator)
        newSys = tf(newNumerator, newDenominator)
        return newSys

    def __str__(self):
        numerator = ''
        denominator = ''
        line = ''
        strRes = ''
        if np.size(self.TFnumerator) == 1:
            numerator += str(self.TFnumerator[0])
        else:
            for n, num in enumerate(self.TFnumerator):
                if num != 0:
                    if n == np.size(self.TFnumerator) - 1:
                        numerator += ' + ' + str(num)
                    else:
                        if n == 0:
                            pass
                        else:
                            numerator += ' + '
                        numerator += str(num) + f's^{np.size(self.TFnumerator) - n - 1}'
        for n, num in enumerate(self.TFdenominator):
            if num != 0:
                if n == 0:
                    denominator += f'{num}s^{np.size(self.TFdenominator) - 1}'
                else:
                    if n == np.size(self.TFdenominator) - 1:
                        denominator += ' + ' + str(num)
                    else:
                        denominator += ' + ' + str(num) + f's^{np.size(self.TFdenominator) - n - 1}'

        largestLength = max(len(numerator), len(denominator))
        for i in range(largestLength):
            line += '-'
        line += '--\n'
        strRes += numerator + '\n' + line + denominator + '\n'
        return strRes


# returns ss system in a observable canonical form based on given tf
def tf2ss(system):
    if isinstance(system, tf):
        A, B, C = system.obsv()
        D = [0]
        systemSS = ss(A, B, C, D)
        return systemSS
    else:
        raise Exception('You need to pass tf system as the argument')


def ss2tf(system):
    if isinstance(system, ss):
        tfsys = symbolic.symss2tf(system.A, system.B, system.C, system.D)
        return tfsys
    else:
        raise Exception('You need to pass ss system as the argument')


# returns array of poles of system
def poles(system):
    roots = np.array([])
    if isinstance(system, tf):
        roots = np.roots(system.TFdenominator)
    elif isinstance(system, ss):
        roots, eigvecs = np.linalg.eig(system.A)
    else:
        raise Exception('Argument must be tf or ss system')
    return roots


# returns array of zeros of system
def zeros(system):
    if isinstance(system, tf):
        roots = np.roots(system.TFnumerator)
    elif isinstance(system, ss):
        pass
    else:
        raise Exception('Argument must be tf or ss system')
    return roots


# draws phase portrait on phase plane of min 2nd order system, var1 and var2 describes which state variables need to
# be plot: 0 - x1 1 - x2 etc.
def phasePortrait(system, Xinit=None, var1=0, var2=1, t=1):
    if Xinit is None:
        Xinit = [[-1, -2], [-3, -4], [5, 6], [7, 8]]
    if isinstance(system, tf):
        systemSS = tf2ss(system)
        phasePortrait(systemSS, var1, var2)
    elif isinstance(system, ss):
        fig = plt.figure()
        ax = fig.add_subplot()
        plt.grid(linestyle='--')
        ax.set_title('Phase portrait')
        ax.set_ylabel(f'x{var1 + 1}(t)')
        ax.set_xlabel(f'x{var2 + 1}(t)')
        legendList = []
        if np.shape(system.A)[0] >= 2:
            Xinit = np.array(Xinit)
            for i in range(np.shape(Xinit)[0]):
                Y = T = Xtmp = X = np.array([[]])
                Y, T, Xtmp = tresp.solveRK4(system, 0, Xinit[i], time=t)
                X = Xtmp
                stateNum = np.shape(system.A)[0]
                XrowsNum = np.shape(X)[0]
                if stateNum >= var1 or stateNum >= var2:
                    # for k in range(0, XrowsNum, stateNum):
                    #     ax.plot(X[k + var1], X[k + var2])
                    ax.plot(X[var1], X[var2])
                    legendList.append(f'xo={Xinit[i]}')
                else:
                    raise Exception("System doesn't have that many state variables. Lower var1 or var2")

            plt.legend(legendList)
            plt.show()
        else:
            raise Exception('System needs to be at least 2nd order')


# takes system and returns tuple of vectors (Y,T,X) - response and time vectors and state trajectory matrix
def step(system, Tpts=None, plot=False, solver='rk4'):
    Y = T = X = np.array([])
    if isinstance(system, tf):
        systemSS = tf2ss(system)
        step(systemSS)
    elif isinstance(system, ss):
        if solver == 'ee':  # explicit (forward) Euler
            Y, T, X = tresp.solveEE(system, 1)
        elif solver == 'ie':  # implicit (backward) Euler
            Y, T, X = tresp.solveIE(system, 1)
        elif solver == 'trap':  # trapezoidal
            Y, T, X = tresp.solveTrap(system, 1)
        elif solver == 'rk4':
            Y, T, X = tresp.solveRK4(system, 1)
        else:
            raise Exception('Wrong solver chosen, choose: ee, ie, trap or rk4')
        if Tpts is not None:
            Yi = np.interp(Tpts, T, Y)
            Y = Yi
            T = Tpts
        if plot:
            fig = plt.figure()
            ax = fig.add_subplot()
            ax.plot(T, Y)
            ax.set_title('Step response')
            ax.set_ylabel('y(t)')
            ax.set_xlabel('t [s]')
            plt.show()
        else:
            return Y, T, X
    else:
        raise Exception('Argument must be a tf or ss system')


# takes system and returns tuple of vectors (Y,T) - response and time vectors
def pulse(system, plot=False, solver='rk4'):
    Y = T = X = np.array([])
    if isinstance(system, tf):
        systemSS = tf2ss(system)
        step(systemSS)
    elif isinstance(system, ss):
        if solver == 'ee':  # explicit (forward) Euler
            Y, T, X = tresp.solveEE(system, 'delta')
        elif solver == 'ie':  # implicit (backward) Euler
            Y, T, X = tresp.solveIE(system, 'delta')
        elif solver == 'trap':  # trapezoidal
            Y, T, X = tresp.solveTrap(system, 'delta')
        elif solver == 'rk4':
            Y, T, X = tresp.solveRK4(system, 'delta')
        else:
            raise Exception('wrong solver chosen, choose: ee, ie, trap or rk4')
        if plot:
            fig = plt.figure()
            ax = fig.add_subplot()
            ax.plot(T, Y)
            ax.set_title('Impulse response')
            ax.set_ylabel('y(t)')
            ax.set_xlabel('t [s]')
            plt.show()
        else:
            return Y, T, X
    else:
        raise Exception('Argument must be a tf or ss system')


# draws bode diagrams for system
def bode(system, maxW=10 ** 3, plot=False):
    n, d = helpers.__sinTF(system)
    Gvec = np.array([])
    Phvec = np.array([])
    Wvec = np.array([])
    # calculating the amplitude and phase characteristics
    for w in np.linspace(0.1, maxW, 10000):
        num = den = 0
        for i in range(len(n)):
            num += n[i] * pow(w, len(n) - i)
        for k in range(len(d)):
            den += d[k] * pow(w, len(d) - k)
        print(num)
        print(den)
        G = 20 * np.log10(abs(num / den))
        Ph = np.angle((num / den), deg=True)
        Wvec = np.append(Wvec, w)
        Gvec = np.append(Gvec, G)
        Phvec = np.append(Phvec, Ph)
    if plot:
        fig, ax = plt.subplots(2)
        ax[0].grid(linestyle='--')
        ax[1].grid(linestyle='--')
        ax[0].set_title('Bode diagrams')
        ax[0].set_ylabel('Magnitude [dB]')
        ax[0].set_xlabel('ω [rad/s]')
        ax[0].set_xscale('log')
        ax[1].set_ylabel('Phase shift [°]')
        ax[1].set_xlabel('ω [rad/s]')
        ax[1].set_xscale('log')
        ax[0].plot(Wvec, Gvec)
        ax[1].plot(Wvec, Phvec)
        plt.show()
    else:
        return Gvec, Phvec, Wvec


# draws nyquist plot of system
# FIXME weird plots (a bit different to matlab/octave)
def nyquist(system, maxW=10 ** 4):
    n, d = helpers.__sinTF(system)
    Pvec = np.array([])
    Qvec = np.array([])
    Wvec = np.array([])
    for w in np.linspace(0.01, maxW, 30000):
        num = den = 0
        for i in range(len(n)):
            num += n[i] * pow(w, len(n) - i)
        for k in range(len(d)):
            den += d[k] * pow(w, len(d) - k)
        P = (num / den).real
        Q = (num / den).imag
        Wvec = np.append(Wvec, w)
        Pvec = np.append(Pvec, P)
        Qvec = np.append(Qvec, Q)
    fig = plt.figure()
    plt.grid(linestyle='--')
    ax = fig.add_subplot()
    ax.set_title('Nyquist plot G(jω) = P(ω) + jQ(ω)')
    ax.set_ylabel('Q(ω)')
    ax.set_xlabel('P(ω)')
    ax.plot(Pvec, Qvec)
    ax.plot(Pvec, -1 * Qvec)
    plt.show()


def rlocus(system, CLtf=tf([1], [1])):
    if isinstance(system, tf):
        k = 0
        OLpoles = np.roots(system.TFdenominator)
        OLzeros = np.roots(system.TFnumerator)
        temp1 = np.polynomial.polynomial.polymul(CLtf.TFdenominator, system.TFdenominator)
        temp2 = np.polynomial.polynomial.polymul(CLtf.TFnumerator, system.TFnumerator)
        CLdenominator = np.polynomial.polynomial.polyadd(temp1, temp2)
        CLnumerator = np.polynomial.polynomial.polymul(CLtf.TFdenominator, system.TFnumerator)
        CLpoles = np.roots(CLdenominator)
        CLzeros = np.roots(CLnumerator)
    # continue

    elif isinstance(system, ss):
        pass
    else:
        pass


def isControllable(system):
    if isinstance(system, tf):
        ssSys = tf2ss(system)
        res = isControllable(ssSys)
        return res
    elif isinstance(system, ss):
        degree = np.shape(system.A)[0]
        Cmat = np.array([[]])
        for n in range(degree):
            item = np.dot(np.linalg.matrix_power(system.A, n), system.B)
            if n == 0:
                Cmat = item
            else:
                Cmat = np.hstack((Cmat, item))
        rank = np.linalg.matrix_rank(Cmat)
        if rank != degree:
            return False
        else:
            return True
    else:
        raise Exception('Argument must be a tf or ss system')


def isObservable(system):
    if isinstance(system, tf):
        ssSys = tf2ss(system)
        res = isObservable(ssSys)
        return res
    elif isinstance(system, ss):
        degree = np.shape(system.A)[0]
        Omat = np.array([[]])
        for n in range(degree):
            item = np.dot(system.C, np.linalg.matrix_power(system.A, n))
            if n == 0:
                Omat = item
            else:
                Omat = np.vstack((Omat, item))
        rank = np.linalg.matrix_rank(Omat)
        if rank != degree:
            return False
        else:
            return True
    else:
        raise Exception('Argument must be a tf or ss system')

