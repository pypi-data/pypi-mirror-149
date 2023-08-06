Structures
==========

Preparing structures for training
---------------------------------

:program:`hiphive` provides some utility functions for handling training
:structures.

For example :func:`get_displacements <hiphive.utilities.get_displacements>`
can be used to calculate the displacements of atoms given a reference
structure accounting while accounting for periodic boundary conditions.

In cases where the ordering/indexing of atoms in the training structures
differs from the reference structure, one can use :func:`find_permutation
<hiphive.utilities.find_permutation>` which finds the permutation that
re-orderes the training structures to match the reference.

The function :func:`prepare_structures <hiphive.utilities.prepare_structures>`
combines these two functions together and adds displacements and forces as
arrays to the structures such that they can be added directly a
:class:`StructureContainer`.

.. autofunction:: hiphive.utilities.get_displacements
   :noindex:

.. autofunction:: hiphive.utilities.find_permutation
   :noindex:

.. autofunction:: hiphive.utilities.prepare_structures
   :noindex:



.. index::
   single: Class reference; StructureContainer

StructureContainer
------------------

:program:`hiphive` organizes the data for training and testing in a so-called
:structure container, which provides methods for adding and accessing these
:data. The structure container is essentially a collection of
::class:`FitStructure` objects, each of which comprises an original atomic
:configuration along :with its representation in clusters and reference
:forces.

.. autoclass:: hiphive.StructureContainer
   :members:



.. index::
   single: Class reference; FitStructure

FitStructure
------------

.. autoclass:: hiphive.structure_container.FitStructure
   :members:


.. index::
   single: Structure generation



Structure generation
--------------------

.. automodule:: hiphive.structure_generation
   :members:
   :undoc-members:
   :noindex:



Other functions
---------------

.. autofunction:: hiphive.structure_container.are_configurations_equal
   :noindex:
