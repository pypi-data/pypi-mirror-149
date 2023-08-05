# libcalculus: A comprehensive real and complex analysis library for Python

[![pipeline status](https://gitlab.com/ariter777/libcalculus/badges/master/pipeline.svg)](https://gitlab.com/ariter777/libcalculus/commits/master)

libcalculus is fully written in C++ and Cython for bindings to Python; all numeric calculations take place in C++ and take full advantage of SIMD vectorization and OpenMP threading wherever available.

## Features

- Functional programming approach to analysis in Python
- Numeric integration and differentiation of real and complex functions
- Full integration with NumPy: functions support array inputs
- LaTeX support: every function object has a `.latex()` that produces its LaTeX markup

## Technology
libcalculus is written in C\+\+20 and bound to Python via Cython; operations between functions are performed using C++ lambdas, and all calculations happen at the C++ level, with Python only interfacing methods and results.

## Installation
libcalculus can be installed from pip:
```
pip install libcalculus
```

## Examples
Here is a snippet demonstrating some of the library's features:
```python
>>> import libcalculus, numpy as np
>>> f = libcalculus.csc @ (1 / libcalculus.identity)
>>> f(1 + 2j)
(1.0316491868272164+1.9336686363989997j)
>>> libcalculus.residue(f, 0, tol=1e-4)
(0.16666666639893526-8.181230860681676e-06j)

>>> print(f.latex("z"))
\csc\left( \frac{1}{z}\right)

>>> contour = libcalculus.line(2, 1 + 1j) # 2(1 - t) + (1 + 1i)t
>>> libcalculus.integrate(f, contour, 0, 1) # integrate along the contour between t=0 and t=1
(-2.0551412843830605+1.1351565349386723j)

>>> libcalculus.threads(4) # Enable threading
>>> arr = np.array([[1, 2j, 3], [4 + 1j, 5 + 2j, 7 + 3j]])
>>> print(f(arr))
[[ 1.18839511+0.j         -0.        +1.91903475j  3.05628425+0.j        ]
 [ 4.03942207+0.99000843j  5.02878731+1.98839211j  7.02013025+2.99133798j]]
```

## License
Copyright (c) 2022, Ariel Terkeltoub
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

    * Redistributions of source code must retain the above copyright
       notice, this list of conditions and the following disclaimer.

    * Redistributions in binary form must reproduce the above
       copyright notice, this list of conditions and the following
       disclaimer in the documentation and/or other materials provided
       with the distribution.

    * Neither the name of the libcalculus developers nor the names of any
       contributors may be used to endorse or promote products derived
       from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE
