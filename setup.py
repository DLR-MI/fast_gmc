import os
from setuptools import setup
import subprocess

__version__ = '0.1.0'


def check_opencv():
    # Check if the $CONDA_PREFIX environment variable is set and if libopencv is installed.
    if not os.environ['CONDA_PREFIX']:
        print(
            'Please specify the CONDA_PREFIX environment variable. '
            'It should point to you environment folder, e.g. "/home/<user>/conda/env/<env_name>"')
        exit(-1)

    if not os.path.isdir(os.path.join(os.environ['CONDA_PREFIX'], os.path.join('include', 'opencv4'))):
        # print('Please install OpenCV using "conda install libopencv".')
        print("Installing OpenCV into your conda environment...")
        subprocess.call(args=["conda", "install", "-y", "libopencv"])


def check_cmake():
    # Check if CMake is installed
    try:
        subprocess.call("cmake")
    except FileNotFoundError:
        print(
            'CMake is not in your PATH environment variable. Please check if you installed CMake. '
            'If not, install it from: "https://cmake.org/download/"')


def init():
    check_cmake()
    check_opencv()

    # Set up the dirs
    setup_dir = os.path.dirname(os.path.realpath(__file__))
    src_dir = os.path.join(setup_dir, os.path.join('src', 'fast_gmc'))
    build_dir = os.path.join(src_dir, 'build')

    # Pull the repo for Pybind11
    pybind11_dir = os.path.join(os.path.join(src_dir, os.path.join('extern', 'pybind11')))
    if not os.path.exists(pybind11_dir):
        subprocess.call(args=["git", "clone", "https://github.com/pybind/pybind11.git", "{}".format(pybind11_dir)])

    # Build the shared library using CMake
    if not os.path.exists(build_dir):
        os.mkdir(build_dir)
        subprocess.call(args=["cmake", "-B{}".format(build_dir), "-S{}".format(src_dir)])
        subprocess.call(args=["cmake", "--build", "{}".format(build_dir)])

    setup(
        name='fast_gmc',
        version=__version__,
        author="Felix Sattler",
        author_email="felix.sattler@dlr.de",
        description='Python bindings for GMC (global camera compensation) using OpenCV in C++',
        packages=['fast_gmc'],
        package_dir={'fast_gmc': 'src/fast_gmc'},
        package_data={'fast_gmc': ['build/*.so']},
        zip_safe=False,
        url='https://gitlab.dlr.de/mi/marlin/fast-gmc',
        python_requires='>=3.7',
        keywords=['gmc', 'camera compensation', 'tracking']
    )


if __name__ == '__main__':
    init()
