hiPhive
=======

**hiPhive** is a tool for efficiently extracting high-order force constants from atomistic simulations, most commonly density functional theory calculations.
A detailed description of the functionality provided as well as an extensive tutorial can be found in the `user guide <https://hiphive.materialsmodeling.org/>`_.
Complete examples of using **hiphive** for force constants extraction can be found in the `hiphive-examples repository <https://gitlab.com/materials-modeling/hiphive-examples/>`_.

**hiPhive** is written in Python, which allows easy integration with countless first-principles codes and analysis tools accessible in Python, and allows for a simple and intuitive user interface.
For example using the following snippet one can train a force constant potential:

.. code-block:: python

   cs = ClusterSpace(primitive_cell, cutoffs)
   sc = StructureContainer(cs, list_of_training_structure)
   opt = Optimizer(sc.get_fit_data())
   opt.train()
   fcp = ForceConstantPotential(cs, opt.parameters)

after which it can be used in various ways, e.g., for generating phonon dispersions, computing phonon lifetimes, or running molecular dynamics simulations.

For questions and help please use the `hiphive discussion forum on matsci.org <https://matsci.org/hiphive>`_.
**hiPhive** and its development are hosted on `gitlab <https://gitlab.com/materials-modeling/hiphive>`_.


Installation
------------

**hiPhive** can be installed via `pip`::

    pip3 install hiphive

or via `conda <https://anaconda.org/conda-forge/hiphive>`_::

    conda install -c conda-forge hiphive

**hiPhive** requires Python3 and invokes functionality from several external libraries including the
`atomic simulation environment <https://wiki.fysik.dtu.dk/ase>`_,
`scikit-learn <http://scikit-learn.org/>`_,
`spglib <https://atztogo.github.io/spglib/>`_,
`SymPy <http://www.sympy.org/en/index.html>`_, and
`trainstation <https://trainstation.materialsmodeling.org/>`_.
Please consult the `installation section of the user guide <https://hiphive.materialsmodeling.org/installation.html>`_ for details.


Credits
-------

**hiPhive** has been developed at the `Department of Physics <https://www.chalmers.se/en/departments/physics/Pages/default.aspx>`_ of `Chalmers University of Technology <https://www.chalmers.se/>`_ (Gothenburg, Sweden) in the `Condensed Matter and Materials Theory division <http://www.materialsmodeling.org>`_.

When using **hiPhive** in your research please cite the following paper:

| Fredrik Eriksson, Erik Fransson, and Paul Erhart
| *The Hiphive Package for the Extraction of High‐Order Force Constants by Machine Learning*
| Adv. Theory. Sim., 1800184 (2019)
| `doi: 10.1002/adts.201800184 <https://doi.org/10.1002/adts.201800184>`_

Please consult the `Credits <https://hiphive.materialsmodeling.org/credits>`_ page of the documentation for additional references.
