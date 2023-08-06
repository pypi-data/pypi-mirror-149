.. _advanced_topics_reference_calculations:
.. highlight:: python
.. index::
   single: Reference calculations

Reference calculations
======================

For training a force constant potential one requires reference data in
the form of forces (and displacements).  To this end, one must first
:ref:`generate configurations <advanced_topics_structure_generation>` and
then carry out calculations at a higher level of theory, typically
density functional theory (DFT). The latter can be conveniently
handled via the `atomic simulation environment (ASE)
<https://wiki.fysik.dtu.dk/ase/>`_, which provides interfaces to
various first-principles codes including for example
`Abinit <https://wiki.fysik.dtu.dk/ase/ase/calculators/abinit.html>`_,
`GPAW <http://wiki.fysik.dtu.dk/gpaw>`_,
`NWChem <https://wiki.fysik.dtu.dk/ase/ase/calculators/nwchem.html>`_,
`Quantum Espresso <https://wiki.fysik.dtu.dk/ase/ase/calculators/espresso.html>`_,
`Siesta <https://wiki.fysik.dtu.dk/ase/ase/calculators/siesta.html>`_, and
`VASP <https://wiki.fysik.dtu.dk/ase/ase/calculators/vasp.html>`_.
For most of these codes ASE enables one to both run the actual
calculations from within Python scripts and/or to parse the results.


Forces from DFT calculations
----------------------------

The primary objective is to compute forces with very high numerical
accuracy.  For any technique that relies on a numerical evaluation of
the forces (including practically all DFT methods) this requires
tightening the convergence parameters. This advice does not only
applies when generating input for :program:`hiphive` but any time
when dealing with forces and phonons.

Below we provide specific recommendations for calculating reference
forces using `VASP <https://www.vasp.at/>`__. The remaining sections
are code-independent again.

Assuming a set of configurations :ref:`has been generated
<advanced_topics_structure_generation>`, one has to compute the reference
forces. The numerical quality of the latter is very important whence
the calculations should be converged rather tightly.  In the case of
silicon a typical ``INCAR`` file would be:

.. code-block:: none

    NSW      = 0     ! do not update the configuration
    ISMEAR   = 0     ! Gaussian smearing with a rather small smearing
    SIGMA    = 0.05  ! ... parameter suitable for a semiconductor
    ALGO     = norm  ! blocked Davidson iteration scheme for SCF cycle
    EDIFF    = 1e-6  ! tight energy convergence
    PREC     = acc   ! dense FFT grids
    LREAL    = F     ! reciprocal space projection scheme
    ADDGRID  = T     ! additional support grid for force calculations
    LCHARG   = F     ! do not store the charge density or
    LWAVE    = F     ! ... the wave function (unnecessary expense)

For computational efficiency one should also set the `parallelization
parameters
<https://cms.mpi.univie.ac.at/wiki/index.php/Category:Parallelization>`_
according to the available hardware. One also requires a ``KPOINTS``
file that defines the **k**-point mesh used for sampling the Brillouin
zone.

For other materials some adjustments are probably in order (e.g., in
the case of metals one can switch to Methfessel-Paxton smearing
``ISMEAR>0`` but the general settings with regard to the accuracy of
the calculations (e.g., ``PREC``, ``EDIFF``, ``LREAL``) should be kept
or at least similar. In some cases the accuracy of the forces might be
further improved by raising the ``ENAUG`` parameter above its default
value. More information regarding these tags can be found in the `VASP
manual <https://cms.mpi.univie.ac.at/wiki/index.php/Category:INCAR>`_.


Compilation of output data
--------------------------

After the calculations have been completed one can parse the output
files. It is often a good idea to organize the calculations using the
`ASE database functionality
<https://wiki.fysik.dtu.dk/ase/ase/db/db.html>`_. This can be
accomplished using code such as the following::

    from ase.db import connect
    from ase.io import read
    from glob import glob

    path_to_database = '<update accordingly>'
    path_to_output_files = '<accordingly>'
    db = connect(path_to_database)
    for fname in glob(path_to_output_files):
        atoms = read(fname)
        db.write(atoms, filename=fname)

Here, the file name is stored along the structural data to serve as an
identifier during subsequent analysis.


Compilation of structure container
----------------------------------

These data can then be easily prepared for further processing::

    atoms_ideal = read(path_to_ideal_cell)
    db = connect(path_to_database)

    structures = []
    for row in db.select():

      # Get forces and displacements.
      atoms = row.toatoms()
      displacements = get_displacements(atoms, atoms_ideal)
      forces = atoms.get_forces()

      # Sanity check, displacements should not be abnormally large
      # (here taken as 1.0 A)
      assert np.linalg.norm(displacements, axis=1).max() < 1.0

      # Finalize.
      # The structure container should see the ideal structure in
      # order to be able to process the symmetry.
      atoms_tmp = atoms_ideal.copy()
      # The displacements and forces are attached as separate arrays.
      atoms_tmp.new_array('displacements', displacements)
      atoms_tmp.new_array('forces', forces)
      structures.append(atoms_tmp)

The list of structures is then compiled into a structure container for
subsequent use::

    from hiphive import ClusterSpace, StructureContainer

    # Set up cluster space.
    cs = ClusterSpace(atoms_ideal, cutoffs)

    # Set up structure container.
    sc = StructureContainer(cs)
    for i, atoms in enumerate(configurations):
        sc.add_structure(atoms)
    sc.write(path_to_structure_container_filename)

It is often good practice to write the structure container to file as
it needs to compiled only once for a given set of cutoffs.  Afterwards
one can apply different optimization and validation methods for
constructing a force constant potential.
