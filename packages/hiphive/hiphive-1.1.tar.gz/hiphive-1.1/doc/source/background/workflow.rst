.. _workflow:
.. index:: Workflow

.. raw:: html

    <style> .orange {color:orange} </style>
    <style> .blue {color:CornflowerBlue} </style>
    <style> .green {color:darkgreen} </style>

.. role:: orange
.. role:: blue
.. role:: green


Workflow
********

Overview
========

The following figure illustrates the :program:`hiPhive` *workflow*. Here,
classes are shown in :blue:`blue`, input parameters and data in
:orange:`orange`, and functionalities invoked via external libraries are
indicated in :green:`green`.

.. graphviz:: _static/workflow.dot

The typical workflow involves the following steps:

#. :ref:`generate a set of input structures
   <advanced_topics_structure_generation>` and :ref:`compute the forces in
   these structures using a reference method
   <advanced_topics_reference_calculations>`, most commonly density
   functional theory

#. initialize a :ref:`cluster space <cluster_space>` (via :class:`ClusterSpace
   <hiphive.ClusterSpace>`) by providing a :orange:`prototype structure`
   (typically a primitive cell) as well as :orange:`cutoff radii for clusters
   of different orders`

#. initialize a :ref:`structure container <structure_container>` (via
   :class:`StructureContainer <hiphive.StructureContainer>`) using the
   cluster space from the second step and the :orange:`set of input
   structures with reference forces` from the first step for training
   and validation

#. fit the parameters using an :ref:`optimizer <overview_optimizers>` (e.g.,
   :class:`Optimizer <trainstation.Optimizer>`,
   :class:`EnsembleOptimizer <trainstation.EnsembleOptimizer>`, or
   :class:`CrossValidationEstimator <trainstation.CrossValidationEstimator>` from the :program:`trainstation` package)


#. construct a :ref:`force constant potential <force_constant_potential>`
   (via :class:`ForceConstantPotential <hiphive.ForceConstantPotential>`)
   by combining the cluster space with a set of parameters obtained by
   optimization

The final FCP can be used in a number of ways. For example one can

* create :ref:`force constant matrices <force_constant_matrices>`
  (via :class:`ForceConstants <hiphive.force_constants.ForceConstants>`) for a specific
  :orange:`supercell structure` and analyze :green:`properties related to
  phonons` using
  `phonopy <https://atztogo.github.io/phonopy/>`_,
  `phono3py <https://atztogo.github.io/phono3py/>`_ or
  `shengBTE <http://www.shengbte.org/>`_, or

* create a :ref:`force constant calculator <force_constant_calculator>`
  (via :class:`ForceConstantCalculator
  <hiphive.calculators.ForceConstantCalculator>`) for a specific
  :orange:`supercell structure` and run :green:`molecular dynamics
  simulations` using the `atomic simulation environment
  <https://wiki.fysik.dtu.dk/ase/index.html>`_, from which one can extract
  various quantities including e.g., the thermal conductivity, phonon
  dispersions, phonon lifetimes, and free energies while fully including
  anharmonic effects.

This basic workflow is illustrated in detail in the :ref:`tutorial section
<tutorial>`. Further applications are discussed in the :ref:`additional
topics <advanced_topics>` section.


Key concepts
============

.. _cluster_space:

Cluster spaces
--------------

A cluster space (represented by the :class:`ClusterSpace
<hiphive.ClusterSpace>` class) is defined by providing a prototype structure
along with a set of cutoffs for each (cluster) order to be included, as
demonstrated in the tutorial section that illustrates the :ref:`construction of
a force constant potential <tutorial_construct_fcp>`. It contains the set of
clusters (pairs, triplets, quadruplets etc) and orbits into which a prototype
structure can be decomposed. (An orbit is a set of symmetry equivalent
clusters, see Figure below). A cluster space furthermore contains information
pertaining to the symmetry operations that connect the clusters belonging to
the same orbit and that ultimately define the relation between the parameters
of a :ref:`force constant potential <force_constant_potential>` and the force
constants.

.. _structure_container:

Structure containers
--------------------

A structure container (represented by the :class:`StructureContainer
<hiphive.StructureContainer>` class) is a collection of structures along with
their decomposition into a specific :ref:`cluster space <cluster_space>`.
Structure containers allow one to easily compile structures for training and
validation, as demonstrated in the tutorial on :ref:`force constant potential
construction <tutorial_construct_fcp>`. They can also be written to file for
later use.

.. _overview_optimizers:

Optimizers
----------

Optimizers allow one to train the parameters associated with each :term:`orbit`
in the :ref:`cluster space <cluster_space>`. They are available in the form of
optimizer classes such as :class:`Optimizer <trainstation.Optimizer>`,
:class:`EnsembleOptimizer <trainstation.EnsembleOptimizer>`, or
:class:`CrossValidationEstimator <trainstation.CrossValidationEstimator>`.

.. _force_constant_potential:

Force constant potentials
-------------------------

A force constant potential (FCP; represented by the
:class:`ForceConstantPotential <hiphive.ForceConstantPotential>` class) is
obtained by combining a cluster space with a set of parameters as illustrated
in the tutorial on :ref:`force constant potential construction
<tutorial_construct_fcp>`. FCPs are the main output of the :program:`hiPhive`
model construction cycle. While they are specific for a given prototype
structure and cluster space they are *not* tied to a specific supercell
structure. FCPs can be written to file for later use.

.. _force_constant_matrices:

Force constant matrices
-----------------------

Force constant matrices (represented by the :class:`ForceConstants
<hiphive.force_constants.ForceConstants>` class) are obtained by
applying an FCP to a specific supercell structure. This allows one to
conduct further analyses e.g., via `phonopy
<https://atztogo.github.io/phonopy/>`_, `phono3py
<https://atztogo.github.io/phono3py/>`_ or `shengBTE
<http://www.shengbte.org/>`_. This functionality is demonstrated in
the tutorials on :ref:`thermal properties in the harmonic
approximations <tutorial_harmonic_thermal_properties>` and
:ref:`phonon lifetimes <tutorial_phonon_lifetimes>`.

.. _force_constant_calculator:

Force constant calculators
--------------------------

An `ASE <https://wiki.fysik.dtu.dk/ase/index.html>`_ calculator object
(provided by the :class:`ForceConstantCalculator
<hiphive.calculators.ForceConstantCalculator>` class) can be generated by
applying an FCP to a specific supercell and can be subsequently employed to
carry out e.g., molecular dynamics (MD) simulations as shown in :ref:`the MD
tutorial section <tutorial_molecular_dynamics_simulations>`.
