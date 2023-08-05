#!/usr/bin/env python3
from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize
import sys, os
import numpy as np
sys.path.append("./include")

SOURCES = ["src/libcalculus." + ("pyx" if os.path.isfile("src/libcalculus.pyx") else "cpp")]
INCLUDE_DIRS = [np.get_include(), "./include"]

if sys.platform == "linux":
    os.environ["CC"] = os.environ.get("CC", "g++")
    os.environ["CXX"] = os.environ.get("CXX", "g++")
    os.environ["LDSHARED"] = os.environ.get("LDSHARED", "g++ -shared")
    COMPILER_ARGS = ["-DNPY_NO_DEPRECATED_API", "-std=c++2a", "-O3", "-lstdc++", "-fopenmp", "-static-libstdc++", "-static-libgcc"] + \
                    os.environ.get("CFLAGS", "").split() + os.environ.get("CXXFLAGS", "").split()
    LIBRARY_DIRS = []
    LINKER_ARGS = ["-fopenmp", "-lstdc++", "-static-libstdc++", "-static-libgcc"] + \
                  os.environ.get("LDFLAGS", "").split()
elif sys.platform == "win32":
    COMPILER_ARGS = ["/std:c++20", "/DNPY_NO_DEPRECATED_API", "/O2", "/MT"] + \
                    os.environ.get("CFLAGS", "").split() + os.environ.get("CXXFLAGS", "").split()
    LIBRARY_DIRS = [r"C:\Program Files (x86)\Windows Kits\10\Lib\10.0.18362.0\um\x64"]
    LINKER_ARGS = [] + os.environ.get("LDFLAGS", "").split()


with open("README.md", "r") as rfd:
    long_description = rfd.read()

setup(name="libcalculus",
version="1.0.2",
description="Real/Complex analysis library for Python 3.",
long_description=long_description,
long_description_content_type="text/markdown",
url="https://pypi.org/project/libcalculus",
author="Ariel Terkeltoub",
author_email="ariter777@gmail.com",
keywords=["analysis", "real", "complex", "integral", "derivative"],
install_requires=[
    "numpy>=1.21",
    "Cython>=0.29.28"
],
classifiers=[
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: BSD License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
],
license_files=["LICENSE.txt"],
project_urls = {"Documentation": "https://libcalculus.readthedocs.io/en/latest/",
                "Source Code": "https://gitlab.com/ariter777/libcalculus"},
ext_modules=cythonize(Extension("libcalculus", SOURCES,
                                extra_compile_args=COMPILER_ARGS, extra_link_args=LINKER_ARGS, library_dirs=LIBRARY_DIRS, include_dirs=INCLUDE_DIRS),
                      language_level=3, nthreads=4, annotate=False, compiler_directives={"embedsignature": True}))
