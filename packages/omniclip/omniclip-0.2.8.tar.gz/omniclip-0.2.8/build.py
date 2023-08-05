from distutils.command.build_ext import build_ext

import numpy as np
from Cython.Build import cythonize
from setuptools import Extension
from setuptools.dist import Distribution


def build(setup_kwargs):
    """Needed for the poetry building interface."""
    extensions = [
        Extension(
            "omniCLIP.viterbi",
            sources=["omniCLIP/omni_stat/viterbi.pyx"],
            include_dirs=[np.get_include()],
        ),
    ]
    extensions = cythonize(
        extensions,
        compiler_directives={"language_level": 3, "linetrace": True},
    )
    setup_kwargs.update(
        {
            "ext_modules": extensions,
            "cmdclass": {"build_ext": build_ext},
            "include_dirs": [np.get_include()],
            "zip_safe": False,
        }
    )
    return setup_kwargs
