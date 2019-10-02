[![Build Status](https://travis-ci.com/aqreed/PyVLM.svg?branch=master)](https://travis-ci.com/aqreed/PyVLM)
[![codecov.io](https://codecov.io/gh/aqreed/PyVLM/branch/master/graph/badge.svg)](https://codecov.io/gh/aqreed/PyVLM/branch/master)
[![license](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](https://github.com/aqreed/PyVLM/raw/master/COPYING)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/aqreed/PyVLM/master?filepath=examples)

# PyVLM
|  |  |
| ------ | ------ |
| Description | Python Vortex Lattice Method |
| Maintainer | aqreed <aqreed@protonmail.com> |
| Author | see `AUTHORS` file |
| Version | 0.0.2 |
| Python Version | 3.6 |
| Requires | Numpy, Matplotlib |

#### Example
Taking the example 7.2 from Bertin, J.J. and Smith, M.L., "Aerodynamics for Engineer":

```Python
from numpy import array
import matplotlib.pyplot as plt
from vlm import PyVLM

plane = PyVLM()

A = array([0, 0])
B = array([0.5, 0.5])
leading_edges_position = [A, B]
chord_length = [.2, .2]
n, m = 1, 4

plane.add_surface(leading_edges_position, chord_length, n, m,
	              mirror=True, airfoil=flat_plate())
plane.show_mesh(print_mesh=False, plot_mesh=True)
```

This would produce the following plotting:

<p align="center">
	<img src="/img/bs_show_mesh.png" alt="drawing" width="450"/>
</p>

With a surface already define, the Vortex Lattice Method can be used:

```Python
alpha = 1  # AOA in degrees
plane.vlm(alpha, print_output=True)
```

This would produce the following print:

<p align="center">
	<img src="/img/bs_print_output.png" alt="drawing" width="600" align="center"/>
</p>

### Installation

PyVLM has been written in Python3, and its version v0.1.1 is available in PyPi. It can be installed using:

```sh
$ pip install vlm
```

To install in development mode:

```sh
$ git clone https://github.com/aqreed/PyVLM.git
$ cd PyVLM
$ pip install -e .
```

Please find a example notebook on the ['examples'](https://github.com/aqreed/PyVLM/tree/master/examples) folder that you can open locally, or just try [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/aqreed/PyVLM/master?filepath=examples) to launch online interactive Jupyter notebooks.

---
**NOTE**:
PyVLM is under development and might change in the near future. In particular, we are working on improving the drag calculation method.

---

### Dependencies

This package depends on Python, NumPy and Matplotlib and is usually tested on Linux with the following versions:

Python 3.6, NumPy 1.16, Matplotlib 3.0

### Testing

PyVLM recommends py.test for running the test suite. Running from the top directory:

```sh
$ pytest
```

To test coverage (also from the top directory):

```sh
$ pytest --cov
```

### Bug reporting

Please feel free to open an [issue](https://github.com/aqreed/PyVLM/issues) on GitHub!

### License

MIT (see `COPYING`)
