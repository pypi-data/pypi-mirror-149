.. _advanced_topics:
.. index::
   single: Advanced topics

Advanced topics
***************

The following tutorial sections illustrate applications of
:program:`hiPhive`.

Some of the following examples employ `phonopy
<https://atztogo.github.io/phonopy/>`_ and `phono3py
<https://atztogo.github.io/phono3py/>`_ for analyzing force constants from
:program:`hiPhive`. Please consult the respective websites for installation
instructions.

The scripts and database that are required for the advanced topics can
be `downloaded as a single zip archive
<https://hiphive.materialsmodeling.org/advanced_topics.zip>`_. These
scripts will be compatible with the latest stable release. If you want
to download the scripst from the development version `download this
archive
<https://hiphive.materialsmodeling.org/dev/advanced_topics.zip>`_
instead.

Additional examples can be found in the
`hiphive-examples repository <https://gitlab.com/materials-modeling/hiphive-examples>`_,
this includes, e.g.,
`folding of force constants onto smaller cells <https://gitlab.com/materials-modeling/hiphive-examples/-/tree/master/advanced/force_constant_folding_onto_small_cells>`_
and
`using Bayesian statistics to carry out a sensitivity analyses <https://gitlab.com/materials-modeling/hiphive-examples/-/tree/master/advanced/bayesian_phonon_dispersions>`_.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   structure_generation
   reference_calculations
   long_range_forces
   cutoffs_and_cluster_filters
   cluster_analysis
   force_constants_io
   learning_curve
   feature_selection
   interface_with_sklearn
   compare_fcs
   effective_harmonic_models
   self_consistent_phonons
   anharmonic_energy_surface
   fcs_sensing
   rotational_sum_rules
   bayesian_phonons
