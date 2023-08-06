.. _advanced_topics_compare_fcs:
.. highlight:: python
.. index::
   single: Force constants comparison

Force constants comparison
==========================

This tutorial demonstrates that :program:`hiPhive` reproduces second and third
order force constants obtained using `phonopy
<https://atztogo.github.io/phonopy/>`_ and/or `phono3py
<https://atztogo.github.io/phono3py/>`_. Please consult the respective websites
for installation instructions for these codes. The present example furthermore
employs the `lammps <http://lammps.sandia.gov/>`_ calculator from `ASE
<https://wiki.fysik.dtu.dk/ase/index.html>`_, which requires a working `lammps
<http://lammps.sandia.gov/>`_ installation.

Preparation of reference data
-----------------------------

First we generate the structures (primitive cell and training structures)

.. container:: toggle

    .. container:: header

       ``examples/advanced_topics/compare_fcs_phono3py/1_prepare_structures.py``

    .. literalinclude:: ../../../examples/advanced_topics/compare_fcs_phono3py/1_prepare_structures.py

Secondly we compute the reference force constants using :program:`phono3py`

.. container:: toggle

    .. container:: header

       ``examples/advanced_topics/compare_fcs_phono3py/3_compute_phono3py_fcs.py``

    .. literalinclude:: ../../../examples/advanced_topics/compare_fcs_phono3py/3_compute_phono3py_fcs.py


Training of force constant potentials
-------------------------------------

In order to obtain force constant matrices from :program:`hiPhive` we use the
generated training structures and compiled into a structure container.

.. container:: toggle

    .. container:: header

       ``examples/advanced_topics/compare_fcs_phono3py/2_setup_containers.py``

    .. literalinclude:: ../../../examples/advanced_topics/compare_fcs_phono3py/2_setup_containers.py

Afterwards force constant potentials are trained and used to set up force
constant matrices.

.. container:: toggle

    .. container:: header

       ``examples/advanced_topics/compare_fcs_phono3py/4_compute_hiphive_fcs.py``

    .. literalinclude:: ../../../examples/advanced_topics/compare_fcs_phono3py/4_compute_hiphive_fcs.py


Comparison of force constant matrices
-------------------------------------

Finally, the force constant matrices from :program:`hiPhive` and :program:`phono3py` are compared using the Froebenius norm.

.. math::

    \Delta = ||\matrix{\Phi}_\text{hiPhive} - \matrix{\Phi}_\text{phono3py}||_2 / ||\matrix{\Phi}_\text{phono3py}||_2

We also compute the relative error for the (easily computed), :math:`\Gamma` frequencies obtained using the different second order force constants.


.. container:: toggle

    .. container:: header

       ``examples/advanced_topics/compare_fcs_phono3py/5_compare_fcs.py``

    .. literalinclude:: ../../../examples/advanced_topics/compare_fcs_phono3py/5_compare_fcs.py

The results are compiled in the following table, which illustrates that it is
crucial to include higher-order terms in the expansion in order to recover the
(lower-order) terms of interest.

+-------------+---------------+---------------+---------------------+
| Terms       | FC2 error (%) | FC3 error (%) | Frequency error (%) |
+-------------+---------------+---------------+---------------------+
| 2nd         | 1.6209        |               | 1.5564              |
+-------------+---------------+---------------+---------------------+
| 2nd+3rd     | 0.8561        | 2.5278        | 0.4223              |
+-------------+---------------+---------------+---------------------+
| 2nd+3rd+4th | 0.1129        | 1.1812        | 0.0601              |
+-------------+---------------+---------------+---------------------+
