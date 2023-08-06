.. _fcs_sensing:
.. highlight:: python
.. index::
   single: Force constant sensing

.. |br| raw:: html

  <br/>


Representing FCs from external sources as a FCP
===============================================

There exist several codes that allow one to compute force constants and
:program:`hiphive` provides :ref:`functionality to import some of these formats
<force_constants_io>`, including :program:`phonopy`, :program:`phono3py`, and
:program:`thirdorder.py` (ShengBTE). It can be convenient to represent these
force constants as :class:`ForceConstantPotential
<hiphive.ForceConstantPotential>` objects, for example in order :ref:`to
enforce rotational sum rules <rotational_sum_rules>`.

Firstly these force constants :ref:`have to be imported <force_constants_io>`
as a :class:`ForceConstants <hiphive.force_constants.ForceConstants>` object.
Secondly, one has to construct the :class:`ClusterSpace <hiphive.ClusterSpace>` on which the force constants will be projected.
Here, we recommend using the longest possible cutoffs for the supercell when constructing the :class:`ClusterSpace <hiphive.ClusterSpace>`.
Then one can obtain the parameters as follows::

    from hiphive.utilities import extract_parameters
    parameters = extract_parameters(fcs, cs)

Now a :class:`ForceConstantPotential <hiphive.ForceConstantPotential>` can be
created by combining the :class:`ClusterSpace <hiphive.ClusterSpace>` and the
parameters in the usual manner::

    fcp = ForceConstantPotential(cs, parameters)

Note that the :class:`ForceConstantPotential <hiphive.ForceConstantPotential>` might not
correspond perfectly to underlying (external) force constants. Small errors can arise during the projection due to e.g.

1. If the external force constants do not obey the same crystal symmetries or acoustic sum rules as the ClusterSpace, then there will be some errors in the projection.
2. The force constants outside the cutoff for the :class:`ClusterSpace <hiphive.ClusterSpace>` will not be captured in the FCP.
3. Potentially some issues with supercell/force constant folding.

Here, we note that 1. is often not a problem as most programs calculating force constants enforce symmetries and acoustic sum rules.
Problems regarding 2. and 3. might be an indication that the supercell used for the force constant calculation is too small, and using a larger supercell will likely resolves these problems.


.. container:: toggle

    .. container:: header

       A minimal example can be found in |br|
       ``tests/integration/fcs_sensing.py``

    .. literalinclude:: ../../../tests/integration/test_fcs_sensing.py
