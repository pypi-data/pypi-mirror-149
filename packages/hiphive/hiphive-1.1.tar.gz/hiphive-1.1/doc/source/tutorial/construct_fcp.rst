.. _tutorial_construct_fcp:
.. highlight:: python
.. index::
   single: Force constant potential construction

Force constant potential construction
=====================================

This section is intended to provide an overview of the basic procedure for
constructing a force constant potential (FCP) using structures generated
:ref:`previously <tutorial_prepare_reference_data>`. Specifically, we will
obtain a fourth-order FCP for FCC Ni to be utilized and analyzed in the
subsequent sections.

The construction of an FCP comprises the following key steps

* set up a :term:`cluster space` using the
  :class:`ClusterSpace <hiphive.ClusterSpace>` class
* express a set of reference structures in the :term:`cluster space`
  generated previously using the
  :class:`StructureContainer <hiphive.StructureContainer>` class
* train the parameters associated with each :term:`orbit` in the
  :term:`cluster space` using an optimizer class (e.g.,
  :class:`Optimizer <trainstation.Optimizer>`,
  :class:`EnsembleOptimizer <trainstation.EnsembleOptimizer>`, or
  :class:`CrossValidationEstimator <trainstation.CrossValidationEstimator>`)
* set up an FCP from the final parameters using the
  :class:`ForceConstantPotential <hiphive.ForceConstantPotential>` class

General preparations
--------------------

After importing necessary functions and classes from :program:`ASE` and
:program:`hiPhive`, we read the structures produced in the :ref:`previous
section <tutorial_prepare_reference_data>`.

.. literalinclude:: ../../../examples/tutorial/2_construct_fcp.py
   :end-before: # set up cluster space

Preparation of cluster space
----------------------------

In order to be able to build an FCP, it is first necessary to create a
:class:`ClusterSpace <hiphive.ClusterSpace>` object based on a prototype
structure. Here, we simply employ the first structure from our reference data
set. Furthermore, one must specify the cutoffs up to the desired order. Here,
the cutoffs are set to 5, 4, and 4 Å for pairs, triplets, and quadruplets,
respectively.

.. literalinclude:: ../../../examples/tutorial/2_construct_fcp.py
   :start-after: # set up cluster space
   :end-before: # ... and structure container

As with many other :program:`hiPhive` objects, it is possible to print core
information in a tabular format by simply calling the :func:`print` function
with the instance of interest as input argument. For example ``print(cs)``
results in the following output::

  =================== Cluster Space ====================
  Spacegroup                 : Fm-3m (225)
  symprec                    : 1e-05
  Length scale               : 0.1
  Cutoffs                    : {2: 5.0, 3: 4.0, 4: 4.0}
  Cell                       :
  [[ 0.    1.76 -1.76]
   [ 1.76  1.76  0.  ]
   [ 1.76  0.   -1.76]]
  Basis                      : [[ 0.  0.  0.]]
  Numbers                    : [28]
  Total number of orbits     : 20
  Total number of parameters : 19
  Total number of clusters   : 18
  ------------------------------------------------------
  order | num-orbits | num-params | num-clusters
  ------------------------------------------------------
    2   |       1    |       2    |        3
    3   |       1    |       7    |       12
    4   |       1    |      10    |        3
  ======================================================

A special function (:func:`ClusterSpace.print_orbits
<hiphive.ClusterSpace.print_orbits>`) is available for printing a list of the
orbits associated with the cluster space::

  ===================================== List of Orbits =====================================
  index | order |      elements      |  radius  |     prototype      | clusters | parameters
  ------------------------------------------------------------------------------------------
    0   |   2   |       Ni Ni        |  0.0000  |       (0, 0)       |    1     |     1
    1   |   2   |       Ni Ni        |  1.2445  |       (0, 1)       |    6     |     3
    2   |   2   |       Ni Ni        |  2.4890  |       (0, 2)       |    6     |     3
    3   |   2   |       Ni Ni        |  2.1556  |       (0, 3)       |    12    |     4
    4   |   2   |       Ni Ni        |  1.7600  |      (0, 12)       |    3     |     2
    5   |   3   |      Ni Ni Ni      |  1.1062  |     (0, 0, 1)      |    12    |     5
    6   |   3   |      Ni Ni Ni      |  1.5644  |     (0, 0, 12)     |    6     |     3
    7   |   3   |      Ni Ni Ni      |  1.4370  |     (0, 1, 5)      |    8     |     7
    8   |   3   |      Ni Ni Ni      |  1.6279  |     (0, 1, 13)     |    12    |     7
    9   |   4   |    Ni Ni Ni Ni     |  0.0000  |    (0, 0, 0, 0)    |    1     |     2
   10   |   4   |    Ni Ni Ni Ni     |  0.9334  |    (0, 0, 0, 1)    |    12    |     9
   11   |   4   |    Ni Ni Ni Ni     |  1.3200  |   (0, 0, 0, 12)    |    6     |     5
   12   |   4   |    Ni Ni Ni Ni     |  1.2445  |    (0, 0, 1, 1)    |    6     |     9
   13   |   4   |    Ni Ni Ni Ni     |  1.3621  |    (0, 0, 1, 5)    |    24    |    30
   14   |   4   |    Ni Ni Ni Ni     |  1.4239  |   (0, 0, 1, 13)    |    12    |    17
   15   |   4   |    Ni Ni Ni Ni     |  1.6044  |   (0, 0, 1, 14)    |    24    |    28
   16   |   4   |    Ni Ni Ni Ni     |  1.7600  |   (0, 0, 12, 12)   |    3     |     6
   17   |   4   |    Ni Ni Ni Ni     |  1.5242  |   (0, 1, 5, 17)    |    2     |     6
   18   |   4   |    Ni Ni Ni Ni     |  1.6291  |   (0, 1, 5, 39)    |    12    |    24
   19   |   4   |    Ni Ni Ni Ni     |  1.7600  |   (0, 1, 13, 14)   |    3     |    10
  ==========================================================================================

Compilation of structure container
----------------------------------

Next one needs to compile a :class:`StructureContainer
<hiphive.StructureContainer>` that will be used for training the parameters
associated with each orbit. The latter is initialized by providing a
:class:`ClusterSpace <hiphive.ClusterSpace>` object, after which several
structures are added to the container.

.. literalinclude:: ../../../examples/tutorial/2_construct_fcp.py
   :start-after: # ... and structure container
   :end-before: # train model

We can print a concise summary of the :class:`StructureContainer
<hiphive.StructureContainer>` via ``print(sc)``, which yields::

  =============== Structure Container ================
  Total number of structures : 5
  ----------------------------------------------------
  index | num-atoms | avg-disp | avg-force | max-force
  ----------------------------------------------------
   0    |    256    |  0.1294  |   1.6524  |   3.7407 
   1    |    256    |  0.1395  |   1.7285  |   4.6880 
   2    |    256    |  0.1296  |   1.5673  |   3.6984 
   3    |    256    |  0.1275  |   1.5965  |   5.0317 
   4    |    256    |  0.1243  |   1.6245  |   3.4472 
  ====================================================


Training of parameters
----------------------

The :class:`StructureContainer <hiphive.StructureContainer>` object
created in the previous section contains all the information required
for constructing an FCP. The next step is thus to train the parameters
using the target data. More precisely, the goal is to achieve the best
possible agreement with a set of training data, which represents a
subset of all the data stored in the :class:`StructureContainer
<hiphive.StructureContainer>`. In practice, this is a two step process
that involves (1) the initiation of an :class:`Optimizer
<trainstation.Optimizer>` object with the list of target properties
produced by the :func:`StructureContainer.get_fit_data
<hiphive.StructureContainer.get_fit_data>` method as input argument,
and (2) calling the :func:`train <trainstation.Optimizer.train>`
function of the optimizer object.

.. literalinclude:: ../../../examples/tutorial/2_construct_fcp.py
   :start-after: # train model
   :end-before: # construct force constant potential

Note 1: By default the optimizer will employ a least-squares optimization
algorithm. Other algorithms can be easily selected via the ``fit_method``
keyword of the optimizer object.

Note 2: More elaborate optimizers are available via the
:class:`EnsembleOptimizer <trainstation.EnsembleOptimizer>` and
:class:`CrossValidationEstimator <trainstation.CrossValidationEstimator>`
class.

A concise overview of state of the optimizer after training is obtained via
``print(opt)``::

  ===================== Optimizer ======================
  fit_method                : least-squares
  number_of_target-values   : 3840
  number_of_parameters      : 119
  rmse_train                : 0.01469551
  rmse_test                 : 0.0161488
  train_size                : 2880
  test_size                 : 960
  ======================================================

Various data can also be accessed directly as attributes of the
:class:`Optimizer <trainstation.Optimizer>` object. For example one can
access the root-mean-squared errors (RMSE) over the training and testing sets as
follows::

  print('RMSE train : {:.4f}'.format(opt.rmse_train))
  print('RMSE test  : {:.4f}'.format(opt.rmse_test))

Set up force constant potential
-------------------------------

Finally, we join the final parameters from the optimization step with the
orbits of the cluster space into a :class:`ForceConstantPotential
<hiphive.ForceConstantPotential>` that can be written to file for later
use.

.. literalinclude:: ../../../examples/tutorial/2_construct_fcp.py
   :start-after: # construct force constant potential


Source code
-----------

.. container:: toggle

    .. container:: header

       The complete source code is available in
       ``examples/tutorial/2_construct_fcp.py``

    .. literalinclude:: ../../../examples/tutorial/2_construct_fcp.py
