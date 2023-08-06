.. _installation:
.. index:: Installation

Installation
************


Setup
=====

In the most simple case, :program:`hiPhive` can be simply installed
via `pip`::

    pip install hiphive

If you want to get the absolutely latest version you can clone the
repo::

    git clone git@gitlab.com:materials-modeling/hiphive.git

and then install :program:`hiPhive` via::

    cd hiphive
    python3 setup.py install --user

in the root directory. This will set up :program:`hiPhive` as a Python module
for the current user. To ensure that the installation has succeeded it is
recommended to run the tests::

    python3 tests/main.py


Requirements
============

:program:`hiPhive` requires Python3 and depends on the following libraries

* `ASE <https://wiki.fysik.dtu.dk/ase>`_ (structure handling)
* `Spglib <https://atztogo.github.io/spglib/>`_ (crystal symmetries)
* `scikit-learn <http://scikit-learn.org/>`_ (optimization)
* `NumPy <http://www.numpy.org/>`_ (numerical linear algebra)
* `SymPy <http://www.sympy.org/>`_ (symbolic computation)
* `Numba <https://numba.pydata.org/>`_ (computational efficiency)

To prepare reference data for the tutorial `phonopy
<https://atztogo.github.io/phonopy/>`_ must be installed, which is also
recommended for analysis of second-order force constants.
