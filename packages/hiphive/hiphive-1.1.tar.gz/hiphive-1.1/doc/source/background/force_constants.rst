.. _background:
.. index:: Force constants

.. _force_constants:
.. _displacement_vector:

Force constants
===============

Energy expansion
----------------

Commonly descriptions of the vibrational dynamics of a crystal start with a
Taylor expansion of the potential energy of the system in terms of the ionic
displacements :math:`u_i` away from a set of static equilibrium positions
:math:`R_i`

.. math::
    H = H_0
    + \Phi_i^\alpha u^\alpha_i
    + \frac{1}{2}\Phi_{ij}^{\alpha\beta} u^\alpha_i u^\beta_j
    + \frac{1}{6}\Phi_{ijk}^{\alpha\beta\gamma} u^\alpha_i u^\beta_j u^\gamma_k
    + \dots

Here, the Einstein summation convention applies for all repeated indices. Roman
letters denote atom labels while Greek letters denote the Cartesian directions
:math:`\alpha={x,y,z}`. The first term :math:`H_0` is a constant energy shift
and can thus be chosen as the reference for a particular equilibrium lattice.
The second term vanishes since the expansion is carried around the static
equilibrium positions, for which the forces vanish by definition.

The expansion coefficients :math:`\Phi` are the so-called force constants. They
relate the displacements :math:`u_i` not only to the potential energy :math:`H`
of the system but also the atomic forces :math:`F_i^\alpha` according to

.. math::
   F_i^\alpha
   =
   - \Phi_{ij}^{\alpha\beta} u^\beta_j
   - \frac{1}{2}\Phi_{ijk}^{\alpha\beta\gamma} u^\beta_j u^\gamma_k
   - \dots

The force constants encode essential information about the vibrational
properties of a system and form the basis for a systematic treatment of the
lattice dynamics in terms of phonons. An extensive description of phonon theory
can be found for example in the classic text books by Ziman [Zim60]_, Wallace
[Wal98]_, or Born and Huang [BorHua98]_. A more recent review including
applications has been provided by Fultz [Ful10]_.


Extracting force constants
--------------------------

The calculation of the force constants commonly represents the computationally
most demanding task in a theoretical analysis of the lattice dynamics of a
system. The force constants can in principled be obtained via a direct (real
space) approach using simple finite differences. For example in the case of the
second order force constant matrix (using for simplicity a forward difference)

.. math::

    \Phi_{ij}^{\alpha\beta}
    = \frac{\partial^2 H}{\partial u_i^\alpha \partial u_j^\beta}
    = - \frac{\partial F_i^\alpha}{\partial u_j^\beta}
    \approx - \frac{\partial F_i^\alpha(h) - F_i^\alpha(0)}{h},

where :math:`h` denotes a finite displacement of atom :math:`j` along the
Cartesian direction :math:`\beta`. While this approach can be readily extended
to higher order differences, the number of calculations needed quickly
increases even if the crystal symmetry and intrinsic symmetries of the force
constant tensors are taken into account.

.. figure:: ../advanced_topics/_static/clusters.svg

  Number of orbits, clusters, and parameters as a function of cutoff radius
  for FCC Al.

To circumvent this problem :program:`hiPhive` takes a somewhat different
approach. Instead of *systematically* computing all terms (equivalent to an
enumeration of the terms) it treats the elements of the force constant tensors
as fit parameters and uses advanced regression algorithms to obtain sparse
solutions.
Specifically, the task of finding the fit parameters :math:`\vec{a}`
is cast in the form of a linear equation
:math:`\vec{f}=\matrix{M}\vec{a}`, where :math:`\vec{f}` is a vector
of target forces and :math:`\matrix{M}` is the fit matrix [EsfSto08]_.
Different regression techniques can be applied to solving this linear problem
[EsfSto08]_, [HelAbrSim11]_, [TadGohTsu14]_, [ZhoNieXia14]_, [SanAndAsp15]_.

:program:`hiPhive` is not restricted to a specific optimization strategy but
uses `scitkit-learn <http://scikit-learn.org/>`_ [PedVarGra11]_ to provides a
simple interface to several powerful optimization algorithms, including but not
limited to the `least absolute shrinkage and selection operator (LASSO)
<scikit-learn.org/stable/modules/generated/sklearn.linear_model.Lasso.html>`_,
`Bayesian ridge regression
<http://scikit-learn.org/stable/auto_examples/linear_model/plot_bayesian_ridge.html>`_,
`automatic relevance determination regression (ARDR)
<http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.ARDRegression.html>`_
and conventional :math:`\ell_2`-norm based local minimization techniques.
Furthermore, it is straightforward to include other optimization algorithms
available via Python libraries such as e.g., `scipy <https://www.scipy.org/>`_
or `TensorFlow <https://www.tensorflow.org/>`_.

:program:`hiPhive` exploits crystal symmetries (via `Spglib
<https://atztogo.github.io/spglib/>`_) and sum rules to minimize the
number of independent parameters and has been designed for flexibility
while maintaining a high execution speed (aided by `NumPy
<http://www.numpy.org/>`_ and `Numba
<https://numba.pydata.org/>`_). The implementation focuses on the
handling of the force constants and provides interfaces to other codes
and libraries for carrying out further analysis, including

* `ASE <https://wiki.fysik.dtu.dk/ase/index.html>`_
  (e.g., for molecular dynamics simulations)
* `dynasor <https://dynasor.materialsmodeling.org>`_ (e.g., for
  obtaining temperature dependent phonon frequencies and life times)
* `phonopy <https://atztogo.github.io/phonopy/>`_ [TogTan15]_ (for
  analyzing harmonic phonons and properties derived thereof)
* `phono3py <https://atztogo.github.io/phono3py/>`_ [TogChaTan15]_
  (for phonon lifetimes in the perturbative limit and Boltzmann
  transport theory)
* `shengBTE <http://www.shengbte.org/>`_ [LiCarKat14]_ (for phonon
  lifetimes in the perturbative limit and Boltzmann transport theory)
