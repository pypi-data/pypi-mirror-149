from . import continous as cont


# python's pow() function couldn't handle complex numbers and was trying to cast it into something else
def __imagPow(base, power):
    res = 1
    for i in range(power-1):
        res *= base
    return res


# creates sinusodial transfer function G(jw)
def __sinTF(system):
    num = []
    den = []
    if isinstance(system, cont.tf):
        for i in range(len(system.TFnumerator)):
            num.append(complex(system.TFnumerator[i], 0))
        for i in range(len(system.TFdenominator)):
            den.append(complex(system.TFdenominator[i], 0))
        for i in range(len(num)):
            t = __imagPow(1j, len(num) - 1 - i)
            num[i] *= t
        for k in range(len(den)):
            den[k] *= __imagPow(1j, len(den) - 1 - k)
        return num, den
    elif isinstance(system, cont.ss):
        systemTF = cont.ss2tf(system)
        __sinTF(systemTF)
