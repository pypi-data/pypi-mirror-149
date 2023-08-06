.. _tutorial_prepare_reference_data:
.. highlight:: python
.. index::
   single: Preparing reference data

Preparation of reference data
=============================

Throughout the tutorial we will be using reference data for training and
comparison. The present section provides a short description of the code to
generate these data.


General preparations
--------------------

We first set a few parameters that define the structures to be generated. This
includes

* the size of the supercell (``cell_size``),
* the number of structures (``number_of_structures``),
* the standard deviation of the distribution of displacements (``rattle_std``),
* the minimum separation of any two atoms in the "rattled" structures
  (``minimum_distance``), and
* the name of the output file (``structures_fname``).

In addition, we specify a primitive structure and an :program:`ASE` calculator
object. For simplicity, here, we will employ the very simple `effective medium
theory (EMT) calculator provide by ASE
<https://wiki.fysik.dtu.dk/ase/ase/calculators/emt.html>`_. In practice, one
would commonly resort to higher quality method such as density functional
theory (DFT).

.. literalinclude:: ../../../examples/tutorial/1_prepare_reference_data.py
   :end-before: # generate structures


Structure generation
--------------------

One could easily generate structures with randomized displacements by drawing
components of the atomic displacement vector from a normal distribution with a
specific standard deviation (``rattle_std``). This procedure, however, tends to
produce structures with some very large forces, which poorly mimic the
distribution of forces observed in molecular dynamics simulations.
This behavior occurs since the _uncorrelated_ application of
displacements can lead to very short interatomic distances as shown in
the following figure. Such situations are heavily penalized in e.g.,
MD simulations because of the steep repulsive interaction.

.. figure:: ../advanced_topics/_static/structure_generation_distributions.svg

  Distribution of forces for structures obtained by molecular
  dynamics (MD) simulation, standard rattle, as well as the Monte
  Carlo rattle procedure implemented by the
  :func:`generate_mc_rattled_structures
  <hiphive.structure_generation.generate_mc_rattled_structures>`
  function.  The scripts used for generating data and figure can be
  found in :ref:`an example of the advanceed topics section
  <advanced_topics_structure_generation>`.

The :func:`generate_mc_rattled_structures
<hiphive.structure_generation.generate_mc_rattled_structures>` function
provides a means to overcome this issue. It implements a simple Monte Carlo
procedure, which enforces a lower limit on any interatomic distance in the
final structure (``minimum_distance``). Here, it is used to generate structures
with randomized displacements. A more detailed discussion of this subject can
be found :ref:`here <advanced_topics_structure_generation>`, and we recommend
looking into the phonon-rattle approach for generating large but physical displacements.

.. warning::

  Please note that calling functions that rely on the generation of pseudo-
  random numbers *repeatedly with the same seed* (i.e., repeatedly falling back
  to the default value) is **strongly** discouraged as it will lead to
  correlation. To circumvent this problem one can for example seed a sequence
  of random numbers and then use these numbers in turn as seeds.

For each randomized structure we then compute the atomic forces. The final set
of structures is written to file for later use.

.. literalinclude:: ../../../examples/tutorial/1_prepare_reference_data.py
   :start-after: # generate structures


Source code
-----------

.. container:: toggle

    .. container:: header

       The complete source code is available in
       ``examples/tutorial/1_prepare_reference_data.py``

    .. literalinclude:: ../../../examples/tutorial/1_prepare_reference_data.py
