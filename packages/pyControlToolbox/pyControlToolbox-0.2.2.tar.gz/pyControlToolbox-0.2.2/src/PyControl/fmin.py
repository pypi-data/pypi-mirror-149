import numpy as np
from inspect import signature


# startVector must be a VECTOR!!!
# error indicates how close to zero must be the derrivative
# sd = steepest descent ; sam = simulated annealing method ; ne = Nelder Mead method
def fmin(func, startVector, error=0.000001, steps=1000, stepSize=0.001, method='ne'):
    sig = signature(func)
    argNum = len(sig.parameters)
    startVector = np.array(startVector)
    startVector = np.ndarray.flatten(startVector)
    currentVector = startVector
    currentVshape = np.shape(currentVector)
    if currentVshape[0] != argNum:
        raise Exception('Number of function arguments doesn\'t match number of starting point parameters')
    else:
        if method == 'sd':
            # calculate gradient
            def grad(currx, h):
                dy = np.array([])
                for i in range(argNum):
                    currx[i] += h
                    f1 = func(*currx)
                    currx[i] -= 2 * h
                    f2 = func(*currx)
                    tmpdy = (f1 - f2) / (2 * h)
                    if i == 0:
                        dy = tmpdy
                    else:
                        dy = np.r_[dy, tmpdy]
                return dy

            i = 1
            currentVector = startVector
            grdmag = 1
            while i < steps and grdmag > error:
                grd = grad(currentVector, stepSize)
                grdmag = np.sqrt(np.array([grd]).dot(grd))
                currentVector = currentVector - 0.9 * grd
                i += 1
        #            print(f'steepest descent steps: {i}')
        elif method == 'sam':  # simulated annealing !!! doesn't work
            tmin = error
            tmax = 1000
            t = tmax
            i = 0
            bestVector = startVector
            currentVector = bestVector
            while t > tmin:
                x = np.random.random(argNum)
                randomVector = x
                dE = func(*randomVector) - func(*currentVector)
                prob = np.exp(-dE / t)
                rand = np.random.choice(a=[1, 0], size=1, p=[prob, 1 - prob])
                if rand == 1:
                    currentVector = randomVector
                else:
                    if func(*currentVector) < func(*bestVector):
                        bestVector = currentVector
                i += 1
                t = tmax / (i + 1)
            currentVector = bestVector
        elif method == 'ne':  # Nelder Mead
            bestP = startVector
            if argNum > 0:
                p = np.array([bestP])
                for h in range(argNum):
                    pnew = np.random.random(argNum)
                    p = np.vstack([p, pnew])
                alpha = 1
                gamma = 2
                rho = 0.5
                sigma = 0.5
                #               j = -1
                fpref = 1
                fpexp = 1
                fpcont = 1
                diff = 1
                while diff > error:
                    #                    j += 1
                    fvec = np.array([])
                    for h in range(argNum + 1):
                        fvec = np.append(fvec, func(*p[h]))
                    pworst = np.argmax(fvec)
                    pbest = np.argmin(fvec)
                    diff = np.abs((fvec[pworst] - fvec[pbest]) / (fvec[pbest] + 1e-9))
                    tmp = np.delete(p, pworst, 0)
                    centroid = np.sum(tmp, axis=0) / np.shape(tmp)[0]
                    bestP = centroid
                    # reflection
                    npref = centroid + alpha * (centroid - p[pworst])
                    fpref = func(*npref)
                    if fvec[pbest] <= fpref < fvec[pworst]:
                        p[pworst] = npref
                        continue
                    elif fpref < fvec[pbest]:
                        # expansion
                        npexp = npref + gamma * np.abs(npref - centroid)
                        fpexp = func(*npexp)
                        if fpexp < fpref:
                            p[pworst] = npexp
                            continue
                        else:
                            p[pworst] = npref
                            continue
                    else:
                        # contraction
                        if fpref < fvec[pworst]:
                            npcont = centroid + rho * (npref - centroid)
                        elif fpref >= fvec[pworst]:
                            npcont = centroid - rho * (centroid - p[pworst])
                        fpcont = func(*npcont)
                        if fpcont < fvec[pworst]:
                            p[pworst] = npcont
                            continue
                        # shrink
                        for k in range(np.shape(p)[0]):
                            if k == pbest:
                                continue
                            else:
                                p[k] = p[pbest] + sigma * (p[k] - p[pbest])
                currentVector = bestP
    #                print(f'ne steps: {j}')
    return currentVector
