# FastGMC 🚀

This repo provides an implementation of global camera compensation (GMC) using OpenCVs Video Stabilization classes. As these are not available for Python directly, we provide a C++ Wrapper using modern and seamless Numpy integration
through [Pybind11](https://github.com/pybind/pybind11).

### Usage
```python
import numpy as np
import cv2 as cv
from fast_gmc import gmc

prev = cv.imread('warp_test_0.jpg')
curr = cv.imread('warp_test_1.jpg')

# Run the actual gmc
mat = gmc(curr, prev, downscale=4)

print("Transformation matrix:\n{}".format(mat))
```

## How to install
Installation can be done through ```pip``` or by building the extensions directly.

### Dependencies
This build depends ```CMake (>=3.0)```.
#### Local install (Linux / Windows)
Download and install from CMake website: [official site](https://cmake.org/download/)
Be sure to update your environment variables to contain your downloaded CMake.
On Linux this can be done with ```export PATH=<path-to-cmake-dir>/bin:$PATH```.
#### Global install (Linux)
```sudo apt-get install cmake```
CMake will be automatically added to PATH variable.

### Install using PIP (recommended)
This works currently ONLY inside a Conda environment.
```bash
pip install git+https://github.com/DLR-MI/fast_gmc.git
```

### Install using CMake (Advanced)
```bash
git clone https://github.com/DLR-MI/fast_gmc.git gmc_pybind
cd gmc_pybind/src/fast_gmc/build/
cmake ../
cmake --build .
# You can now copy the *.so file and use it in your project.
```

## Testing
You can test if the installation worked by doing the following:
```bash
git clone https://github.com/DLR-MI/fast_gmc.git gmc_pybind
# run a test (optional)
pip install opencv-python
python gmc_pybind/test/test.py
# Expected output:
# Previous to current frame = 12.25531005859375 (RMSE)
# Warped to current frame = 9.708952903747559 (RMSE)
# Transformation matrix:
# [[ 1.0105095e+00 -3.5821529e-05 -1.0788696e+01]
#  [ 3.5821529e-05  1.0105095e+00 -6.7262573e+00]
#  [ 0.0000000e+00  0.0000000e+00  1.0000000e+00]]
```


