[![Build Status](https://travis-ci.com/aqreed/PyVLM.svg?branch=master)](https://travis-ci.com/aqreed/PyVLM)
[![codecov.io](https://codecov.io/gh/aqreed/PyVLM/branch/master/graph/badge.svg)](https://codecov.io/gh/aqreed/PyVLM/branch/master)
[![license](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](https://github.com/aqreed/PyVLM/raw/master/COPYING)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/aqreed/PyVLM/master?filepath=examples)

# PyVLM
|  |  |
| ------ | ------ |
| Description | Python Vortex Lattice Method |
| Author | AeroPython Team <aeropython@groups.io> |
| Version | 0.0.1 |
| Python Version | 3.6 |
| Requires | Numpy, Matplotlib |

### Installation

PyVLM has been written in Python3, and its version v0.1.1 is available in PyPi. It can be installed using:

```
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
PyVLM is under development and might change in the near future.

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
