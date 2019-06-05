# -*- coding: utf-8 -*-

"""Compile the Cython libraries of ControlDesign."""

from distutils.core import setup, Extension
import os

from Cython.Distutils import build_ext
import numpy

sources = []
for source in os.listdir("."):
    if source.split('.')[-1] == 'pyx':
        sources.append(source)

extra_compile_args = []


def basename(name: str) -> str:
    """No suffix name."""
    return name.split('.')[0]


# Original src
ext_modules = []
for source in sources:
    ext_modules.append(Extension(
        basename(source),
        sources=['./' + source],  # path + file name

        include_dirs=[numpy.get_include()],
        extra_compile_args=extra_compile_args,
    ))

setup(
    ext_modules=ext_modules,
    cmdclass={'build_ext': build_ext},
)
