# PyControl

Python library for simulating and designing control systems. Available on PyPi under the name [pyControlToolbox](https://pypi.org/project/pyControlToolbox/). The backbone of the library is numpy (for matrix operations), sympy (symbolic engine) and matplotlib (for plots).
> unfortunately pyControl was already taken by project not even related to control systems

## Functionalities
### State space and transfer function model declaration
```python
from PyControl.continous import *
numerator = [1, 2, 3]
denominator = [4, 5, 6, 7]
tfSystem = tf(numerator, denominator)

A = [[2, 5.4],
	[1.85, 3]]
B = [1.12, 3.14]
C = [1, 0]
D = [0]
ssSystem = ss(A, B, C, D)
print(tfSystem)
print(ssSystem)
```
### Step and impulse response simulation
```python
from PyControl.continous import *

A = [[-1, 2],
	[0, -1]]
B = [1, 2]
C = [1, 1]
D = [0]
ssSystem = ss(A, B, C, D)
step(ssSystem, plot=True)
```
**Output:**  
![Step response](https://github.com/btcHehe/PyControl/blob/master/img/exmplStep.png "step response")
```python
from PyControl.continous import *

A = [[-4, 0],
	[1.5, -2.1]]
B = [1, 5]
C = [3.2, 1]
D = [0]
ssSystem = ss(A, B, C, D)
pulse(ssSystem, plot=True)
```
**Output:**  
![Pulse response](https://github.com/btcHehe/PyControl/blob/master/img/exmplPulse.png "pulse response")
### Phase portrait plotting
```python
from PyControl.continous import *

A = [[-1, 2],
	[0, -1]]
B = [1, 2]
C = [1, 1]
D = [0]
ssSystem = ss(A, B, C, D)
phasePortrait(ssSystem, t=10)
```
**Output:**  
![phase portrait](https://github.com/btcHehe/PyControl/blob/master/img/exmplPhasePortrait.png "phase portrait")
