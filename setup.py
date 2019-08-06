# -*- coding: utf-8 -*-

"""Compile the Cython libraries of Pyslvs."""

from distutils.core import setup, Extension
import os

from Cython.Distutils import build_ext
import numpy

sources = []
etfe = "core/ETFE/"
ga = "core/ga_algorithm/"
adesign = ga + "Adesign/"
for folder in (etfe, ga, adesign):
    for source in os.listdir(folder):
        if source.split('.')[-1] == 'pyx':
            sources.append(folder + source)


def basename(name: str) -> str:
    """No suffix name."""
    return name.split('.')[0].replace('/', '.')


setup(
    ext_modules=[Extension(
        basename(source),
        sources=[source],  # path + file name
        include_dirs=[numpy.get_include()],
        extra_compile_args=[],
    ) for source in sources],
    cmdclass={'build_ext': build_ext},
)
