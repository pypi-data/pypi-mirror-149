.. _background:
.. index:: Background

Background
**********

The atoms in a material undergo regular vibrational motion around their
equilibrium positions, a phenomenon that is of fundamental importance for the
overall behavior of the material. In crystalline solids in particular these
vibrations are periodic in nature and can be described using quasi-particles
named phonons that represent *collective excitations* of the crystal lattice.

The most essential ingredient required for analyzing phonons in a
material is the set of :ref:`force constants (FCs)
<force_constants>`. :program:`hiPhive` enables one to efficiently
obtain high order FCs (e.g., of fourth or sixth order) including large
and low-symmetry systems. To this end, it employs a supercell approach similar to
`phonopy <https://atztogo.github.io/phonopy/>`_ [TogTan15]_, `shengBTE
<http://www.shengbte.org/>`_ [LiCarKat14]_, or `alamode
<http://alamode.readthedocs.io/en/latest/intro.html>`_ [TadGohTsu14]_.

:program:`hiPhive` does not rely on a specific type of input configuration
(i.e. enumerated displacements or configurations from MD
simulations). Rather it employs advanced optimization techniques that
are designed to find sparse solutions, which in the present case
reflect the short-range nature of the FCs. If the input configurations
are constructed *sensibly* this approach allows one to obtain FCs
using a much smaller number of input configurations and thus to reduce
the computational effort, usually in the form of density functional
theory (DFT) calculations, considerably. This approach becomes
genuinely advantageous already for obtaining second order FCs in large
and/or low symmetry systems (defects, interfaces, surfaces, large unit
cells etc). :program:`hiPhive` truly excels when it comes to higher
order FCs, for which a strict enumeration scheme quickly leads to an
explosion of displacement calculations.

.. toctree::
   :maxdepth: 1
   :caption: Contents

   force_constants
   workflow
