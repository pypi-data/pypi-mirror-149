#!/usr/bin/env python3

import re
import sys
from setuptools import setup, find_packages

if sys.version_info < (3, 6, 0, 'final', 0):
    raise SystemExit('Python 3.6 or later is required!')

with open('README.rst', encoding='utf-8') as fd:
    long_description = fd.read()

with open('hiphive/__init__.py') as fd:
    lines = '\n'.join(fd.readlines())

version = re.search("__version__ = '(.*)'", lines).group(1)
maintainer = re.search("__maintainer__ = '(.*)'", lines).group(1)
maintainer_email = re.search("__maintainer_email__ = '(.*)'", lines).group(1)
url = re.search("__url__ = '(.*)'", lines).group(1)
license = re.search("__license__ = '(.*)'", lines).group(1)
description = re.search("__description__ = '(.*)'", lines).group(1)

# PyPI name
name = 'hiphive'

setup(name=name,
      version=version,
      description=description,
      long_description=long_description,
      url=url,
      maintainer=maintainer,
      maintainer_email=maintainer_email,
      platforms=['unix'],
      install_requires=['ase',
                        'h5py',
                        'numba>=0.55',
                        'numpy>=1.18,<1.22',  # imposed by numba
                        'pandas',
                        'scipy>=1.0.0',  # imposed by numba
                        'scikit-learn',
                        'spglib',
                        'sympy>=1.1',
                        'trainstation>=0.2'],
      packages=find_packages(),
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3 :: Only',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Intended Audience :: Science/Research',
          f'License :: OSI Approved :: {license}',
          'Topic :: Scientific/Engineering :: Physics'])
