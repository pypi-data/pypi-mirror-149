.. index:: FAQ

Frequently asked questions
***************************

Here are answers to some frequently asked questions.
Feel free to also read through previously asked questions by users on `matsci.org <https://matsci.org/hiphive>`_ and in the `gitlab issue tracker <https://gitlab.com/materials-modeling/hiphive/-/issues?sort=updated_desc&state=all&label_name[]=User>`_.



Failing tests
--------------

When starting to use :program:`hiphive` it is a good idea to run all
the tests to check that everything works as expected. A few common
reasons why tests may fail include

* Out of sync test and source-code. The tests have to match the version of the package.
* Old packages: If the numpy/sympy/spglib version that has been installed does not match the version requirements some tests can fail.
* Running hiphive on windows is currently not supported and if attempted strange errors and test failures can occur.


How should I select cutoffs for the ClusterSpace?
-------------------------------------------------

When selecting cutoffs for your model is often a good idea to try out
a few different choices and see if you can achieve convergence. The
easiest way to do this is to study the :term:`cross validation` score
as a function of the cutoffs. This will help you choose optimal
cutoffs and allow you to detect potential overfitting.

Often it is also possible (and advisable) to study directly the
convergence of the thermodynamic property of interest, e.g., the
frequency spectrum or thermal conductivity, as a function of the
cutoffs in order to ensure the results are converged.


How many training structures are required?
------------------------------------------

The number of training structures needed to train an accurate force
constant potential strongly depends on the number of free paramreters
(and hence crystal symmetry), the order of the expansion and desired 
accuracy.

The :class:`ClusterSpace <hiphive.ClusterSpace>` you are working with
contains the number of degrees of freedom of the force constant
potential (accessible via ``cs.n_dofs``). This will correspond to the
number of columns in the sensing matrix when optimizing the
parameters. Each training structure contains :math:`3N` force
components, i.e. each structure gives rise to :math:`3N` rows in the
sensing matrix. In general it is a good idea for the linear problem to
be solved to be overdetermined, i.e. that the sensing matrix should
contain more rows than columns. This will provide an initial
indication of the number of training structures required.

Furthermore, it is a good idea to check the convergence of the force
constant potential with respect to the number of training structures
used. For example the :term:`RMSE` score from the :term:`cross
validation` analysis, as done in :ref:`learning curve topic
<learning_curve>`, provides a good means to check convergence.


Optimizer fails with memory error
---------------------------------

When running on multi-core systems you might encounter errors such as
'RFE fails with "OSError: [Errno 12] Cannot allocate memory'. This can
occur since scikit-learn, which is used for the optimization, attempts
by default to parallelize the computation over multiple CPUs,
increasing the memory requirement as well. This behaviour can be
controlled via the `n_jobs parameter
<https://scikit-learn.org/stable/glossary.html#term-n-jobs>`_. The
default value (``n_jobs=-1``) attempts to use *all* available CPUs. To
reduce the memory consumption the maximum number of concurrently
running jobs should be set explicitly, e.g., ``n_jobs=2``.


How do I enforce rotational sum rules for force constants calculated with phonopy
---------------------------------------------------------------------------------
Enforcing rotational sum rules for force constants calculated with phonopy is possible with hiphive, but it requires several steps.

First, the phonopy-FCS must be converted to a :class:`ForceConstantPotential <hiphive.ForceConstantPotential>`. This may introduce small errors in the force constant, as discussed in :ref:`here <fcs_sensing>`.

Next, the rotational sum rules are enforced as described :ref:`here <rotational_sum_rules>`.
Here, one must use the post-processing approach, and it might be necessary to try a few different values for :math:`\alpha` to correctly enforce the rotational sum rules.
This approach generally works fine, but in our experience the best approach for enforcing rotational sum rules is to include the rotational constraints when fitting the force constants.
However, this is not possible when using force constants from e.g. phonopy.


We recommend that you compare the dispersion between the original force constants, the
ones produced by hiphive, and the ones produced by hiphive after enforcing the
rotational sum rules.
If the first two look the same, then the conversion of the force-constants to a :class:`ForceConstantPotential <hiphive.ForceConstantPotential>` likely worked correctly. 


The code below can serve as a template and starting point when enforcing rotational sum rules for force constants calculated with phonopy.::

        from ase.io import read
        from hiphive import ClusterSpace, ForceConstantPotential, enforce_rotational_sum_rules
        from hiphive.cutoffs import estimate_maximum_cutoff
        from hiphive.utilities import extract_parameters

        prim = read('POSCAR')
        supercell = read('SPOSCAR')
        
        # Define a cluster space using the largest cutoff you can
        max_cutoff = estimate_maximum_cutoff(supercell) - 0.01
        cutoffs = [max_cutoff]  # only second order needed
        cs = ClusterSpace(prim, cutoffs)

        # import the phonopy force constants using the correct supercell also provided by phonopy
        fcs = ForceConstants.read_phonopy(supercell, 'fc2.hdf5')

        # Find the parameters that best fits the force constants given you cluster space
        parameters = extract_parameters(fcs, cs)

        # Enforce the rotational sum rules
        parameters_rot = enforce_rotational_sum_rules(cs, parameters, ['Huang', 'Born-Huang'])

        # use the new parameters to make a fcp and then create the force constants and write to a phonopy file
        fcp = ForceConstantPotential(cs, parameters_rot)
        fcs = fcp.get_force_constants(supercell)
        fcs.write_to_phonopy('fc2_rotinv.hdf5', format='hdf5')


If you're unsure about any line try the search function in the documentation.
Relevant pages include:

* `Constructing a cluster space <https://hiphive.materialsmodeling.org/tutorial/construct_fcp.html#preparation-of-cluster-space>`_
* `Module reference about reading phonopy force constants <https://hiphive.materialsmodeling.org/moduleref/force_constants.html#hiphive.force_constants.ForceConstants.read_phonopy>`_
* `Example using reading force constants functionality <https://hiphive.materialsmodeling.org/advanced_topics/compare_fcs.html#comparison-of-force-constant-matrices>`_
* `Representing force constants from phonopy <https://hiphive.materialsmodeling.org/advanced_topics/fcs_sensing.html>`_
* `Enforcing rotation sum rules <https://hiphive.materialsmodeling.org/advanced_topics/rotational_sum_rules.html>`_
* `Module reference about writing force constants <https://hiphive.materialsmodeling.org/moduleref/force_constants.html#hiphive.force_constants.ForceConstants.write_to_phonopy>`_
* `Example using write force constants functionality <https://hiphive.materialsmodeling.org/tutorial/compute_third_order_properties.html>`_


