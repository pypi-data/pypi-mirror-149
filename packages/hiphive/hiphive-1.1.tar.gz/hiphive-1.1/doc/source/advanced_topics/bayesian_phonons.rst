.. _bayesian_phonons:
.. highlight:: python
.. index::
   single: Bayesian parameter estimation
   single: Sensitivity analysis
   single: Bagging

Bayesian phonons
================

This example demonstrates sensitivity analysis for force constants using Bayesian parameter estimation or bagging.
The source code for this example is available in the form of a jupyter notebook in the `hiphive-examples repository <https://gitlab.com/materials-modeling/hiphive-examples>`_,
see `here <https://gitlab.com/materials-modeling/hiphive-examples/-/tree/master/advanced/bayesian_phonon_dispersions>`_.

Bayesian parameter optimization allows one to find the joint probability distributions :math:`P(\boldsymbol{x})` of the parameters :math:`\boldsymbol{x}` given some training data and priors.
Here, we consider a simple harmonic force constant model for FCC Ni.
Uniform priors are used and 200 parameter vectors are drawn from :math:`P(\boldsymbol{x})` using `Markov chain Monte Carlo <https://en.wikipedia.org/wiki/Markov_chain_Monte_Carlo>`_ sampling.
These 200 models are used to predict the harmonic phonon dispersion shown in the figure below.

.. figure:: _static/Ni_bayesian_dispersion.svg

This type of sensitivity analysis can also be carried out via the :class:`EnsembleOptimizer <trainstation.EnsembleOptimizer>` using bagging, which is also demonstrated in the jupyter notebook.

Sensitivity analysis can equally be employed for other properties such ase, e.g., the free energy or the thermal conducitvity.
It also allows one to identify regions of the configurational space for which the model sensitivity is poor and thus guide the selection of additional training structures.
