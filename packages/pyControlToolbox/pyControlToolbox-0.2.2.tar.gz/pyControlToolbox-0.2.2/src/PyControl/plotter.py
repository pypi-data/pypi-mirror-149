from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import sys

_x = np.array([[]])
_y = np.array([[]])
_xmin = _xmax = _ymin = _ymax = 0
_xlabel = ""
_ylabel = ""
_title = ""
_fastMode = False
_sampleRate = 0
_multplot = False


def __init():
    glClearColor(1.0, 1.0, 1.0, 1.0)
    global _xmin
    global _xmax
    global _ymin
    global _ymax

    gluOrtho2D(_xmin, _xmax, 2 * _ymin, 2 * _ymax)


def __plotting():
    global _title
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(400, 400)
    glutInitWindowPosition(400, 400)
    glutCreateWindow(_title)
    glutDisplayFunc(__plotFunc)
    __init()
    glutMainLoop()


def __plotFunc():
    global _x
    global _y
    global _xmin
    global _xmax
    global _ymin
    global _ymax
    global _fastMode
    global _sampleRate
    global _multplot
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0.0, 0.0, 0.0)
    glLineWidth(2.0)
    glPointSize(2.0)

    # making plot axis
    glBegin(GL_LINES)
    glVertex2f(_xmin, 0.0)  # x axis
    glVertex2f(_xmax, 0.0)
    glVertex2f(0.0, 2 * _ymax)  # y axis
    glVertex2f(0.0, 2 * _ymin)

    glVertex2f(0.0, 2 * _ymax)  # y axis arrow
    glVertex2f(0.0 - _xmax / 40, 2 * (_ymax - _ymax / 30))
    glVertex2f(0.0, 2 * _ymax)
    glVertex2f(0.0 + _xmax / 40, 2 * (_ymax - _ymax / 30))

    glVertex2f(_xmax, 0.0)  # x axis arrow
    glVertex2f(_xmax - _xmax / 30, 0.0 + _ymax / 30)
    glVertex2f(_xmax, 0.0)
    glVertex2f(_xmax - _xmax / 30, 0.0 - _ymax / 30)

    glEnd()
    glFlush()

    clr = 0
    if _fastMode:
        if _multplot:
            rxv, cxv = np.shape(_x)
            for i in range(rxv):
                if clr == 0:
                    glColor3f(0.0, 0.0, 1.0)  # blue
                elif clr == 1:
                    glColor3f(0.0, 1.0, 0.0)  # green
                elif clr == 2:
                    glColor3f(1.0, 0.0, 0.0)  # red
                elif clr == 3:
                    glColor3f(0.0, 1.0, 1.0)  # cyan
                elif clr == 4:
                    glColor3f(1.0, 0.0, 1.0)  # pink
                elif clr == 5:
                    glColor3f(1.0, 1.0, 0.0)  # yellow
                j = 0
                while j < np.size(_x[i]):
                    glBegin(GL_POINTS)
                    glVertex2f(_x[i][j], _y[i][j])
                    glEnd()
                    glFlush()
                    j += _sampleRate  # skip size
                clr += 1
        else:
            glColor3f(0.0, 0.0, 1.0)
            j = 0
            while j < np.size(_x):
                glBegin(GL_POINTS)
                glVertex2f(_x[j], _y[j])
                glEnd()
                glFlush()
                j += _sampleRate  # skip size
    else:
        if _multplot:
            rxv, cxv = np.shape(_x)
            for i in range(rxv):
                if clr == 0:
                    glColor3f(0.0, 0.0, 1.0)  # blue
                elif clr == 1:
                    glColor3f(0.0, 1.0, 0.0)  # green
                elif clr == 2:
                    glColor3f(1.0, 0.0, 0.0)  # red
                elif clr == 3:
                    glColor3f(0.0, 1.0, 1.0)  # cyan
                elif clr == 4:
                    glColor3f(1.0, 0.0, 1.0)  # pink
                elif clr == 5:
                    glColor3f(1.0, 1.0, 0.0)  # yellow
                for j in range(np.size(_x[i]) - 1):
                    glBegin(GL_LINES)
                    glVertex2f(_x[i][j], _y[i][j])
                    glVertex2f(_x[i][j + 1], _y[i][j + 1])
                    glEnd()
                    glFlush()
                clr += 1
        else:
            glColor3f(0.0, 0.0, 1.0)
            for j in range(np.size(_x) - 1):
                glBegin(GL_LINES)
                glVertex2f(_x[j], _y[j])
                glVertex2f(_x[j + 1], _y[j + 1])
                glEnd()
                glFlush()


def plot(x, y, xlabel="x", ylabel="y", title="plot of y(x)", fastMode=False, sampleRate=0):
    global _x
    global _y
    global _xmin
    global _xmax
    global _ymin
    global _ymax
    global _xlabel
    global _ylabel
    global _title
    global _fastMode
    global _sampleRate
    if np.size(x) != np.size(y):
        raise Exception(f'x and y vectors must be the same size. Length of x={np.size(x)}, y={np.size(y)}')
    if sampleRate == 0 and fastMode:
        raise Exception("you've chosen fastMode so you need to specify sampling rate with sampleRate argument")
    else:
        _sampleRate = sampleRate
    _x = np.copy(x)
    _y = np.copy(y)
    _xmin = np.amin(_x)
    _xmax = np.amax(_x)
    _ymin = np.amin(_y)
    _ymax = np.amax(_y)
    _xlabel = xlabel
    _ylabel = ylabel
    _title = title
    _fastMode = fastMode

    __plotting()


def plotMulti(xvect, yvect, labelvect=None, title="multiple plots", fastMode=False, sampleRate=0):
    # TODO  labels and legends
    if labelvect is None:
        labelvect = []
    global _x
    global _y
    global _xmin
    global _xmax
    global _ymin
    global _ymax
    global _title
    global _multplot
    global _fastMode
    global _sampleRate
    rxv, cxv = np.shape(xvect)
    ryv, cyv = np.shape(yvect)
    tempvect = np.copy(xvect)
    if rxv < ryv:
        if rxv == 1:
            for i in range(ryv - 1):
                xvect = np.row_stack((xvect, tempvect))
    print(xvect)
    if sampleRate == 0 and fastMode:
        raise Exception("you've chosen fastMode so you need to specify sampling rate with sampleRate argument")
    else:
        _sampleRate = sampleRate
    _fastMode = fastMode
    _multplot = True
    lblvsize = np.size(labelvect)
    if lblvsize < ryv:
        for i in range(ryv - lblvsize):
            labelvect = np.append(labelvect, f'y{i}')
    _title = title
    _x = np.copy(xvect)
    _y = np.copy(yvect)
    for xv in _x, _y:
        xmintemp = np.amin(xv)
        xmaxtemp = np.amax(xv)
        if xmintemp < _xmin:
            _xmin = xmintemp
        if xmaxtemp > _xmax:
            _xmax = xmaxtemp
    for yv in _y:
        ymintemp = np.amin(yv)
        ymaxtemp = np.amax(yv)
        if ymintemp < _ymin:
            _ymin = ymintemp
        if ymaxtemp < _ymax:
            _ymax = ymaxtemp
    if (np.abs(_ymax) - np.abs(_ymin)) < 0:
        _ymax = np.abs(_ymin)
    else:
        _ymin = - np.abs(_ymax)

    if (np.abs(_xmax) - np.abs(_xmin)) < 0:
        _xmax = np.abs(_xmin)
    else:
        _xmin = - np.abs(_xmax)

    __plotting()
