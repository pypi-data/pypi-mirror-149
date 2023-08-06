.. raw:: html

  <p>
  <a href="https://badge.fury.io/py/hiphive"><img src="https://badge.fury.io/py/hiphive.svg" alt="PyPI version" height="18"></a>
  </p>


:program:`hiPhive` — High-order force constants for the masses
**************************************************************

**hiPhive** is a tool for efficiently extracting high-order force constants from atomistic simulations, most commonly density functional theory calculations.
A detailed description of the functionality provided as well as an extensive tutorial can be found in the `user guide <https://hiphive.materialsmodeling.org/>`_.
Complete examples of using **hiphive** for force constants extraction can be found in the `hiphive-examples repository <https://gitlab.com/materials-modeling/hiphive-examples/>`_.
:program:`hiPhive` is written in Python, which allows easy integration with countless first-principles codes and analysis tools accessible in Python, and allows for a simple and intuitive user interface.

The following snippet illustrates the construction of a force constant potential object (``fcp``), which can be subsequently used, e.g., for generating phonon dispersions, computing phonon lifetimes, or running molecular dynamics simulations::

    cs = ClusterSpace(ideal_cell, cutoffs=[6.0, 4.5])
    sc = StructureContainer(cs)
    for atoms in list_of_training_structures:
        sc.add_structure(atoms)
    opt = Optimizer(sc.get_fit_data())
    opt.train()
    fcp = ForceConstantPotential(cs, opt.parameters)

:program:`hiPhive` has been developed at the `Department of Physics <https://www.chalmers.se/en/departments/physics/Pages/default.aspx>`_ of `Chalmers University of Technology <https://www.chalmers.se/>`_ (Gothenburg, Sweden) in the `Condensed Matter and Materials Theory division <http://www.materialsmodeling.org>`_.
Please consult the :ref:`credits page <credits>` for information on how to cite :program:`hiphive`.

For questions and help please use the `hiphive discussion forum on matsci.org <https://matsci.org/hiphive>`_.
:program:`hiPhive` and its development are hosted on `gitlab <https://gitlab.com/materials-modeling/hiphive>`_.

.. toctree::
   :maxdepth: 2
   :caption: Main

   background/index
   installation
   tutorial/index
   advanced_topics/index
   faq
   credits
   related_codes

.. toctree::
   :maxdepth: 2
   :caption: Function reference

   moduleref/index

.. toctree::
   :maxdepth: 2
   :caption: Backmatter

   bibliography
   glossary
   genindex
