.. _advanced_topics_interface_sklearn:
.. highlight:: python
.. index::
   single: Interface with scikit-learn


Interface with :program:`scikit-learn`
======================================

This tutorial demonstrates how :program:`hiPhive` can be easily interfaced with
other Python libraries. Here, we specifically consider `scitkit-learn
<http://scikit-learn.org/>`_ but it is equally straightforward to interface
with e.g., `SciPy <https://www.scipy.org/>`_ or `TensorFlow
<https://www.tensorflow.org/>`_.

Regression
----------

:program:`hiPhive` provides simplified interfaces to several linear models in
:program:`scikit-learn`. Yet there are many more features of
:program:`scikit-learn` that can be of interest to advanced users. This
tutorial demonstrates how to use :program:`hiPhive` in such situations. The
following snippet illustrates for example how to use the `HuberRegressor`
linear model (which is not included among the standard fitting methods) to
find optimal parameters.

.. code-block:: python

    from sklearn.linear_model import HuberRegressor
    A, y = sc.get_fit_data()
    hr = HuberRegressor()
    hr.fit(A, y)
    fcp = ForceConstantPotential(cs, hr.coef_)


t-SNE
-----

While regression is probably the most common task, other machine learning
techniques can also be of interest. This section illustrates the utility of the
`t-distributed Stochastic Neighbor Embedding (t-SNE) algorithm
<https://en.wikipedia.org/wiki/T-distributed_stochastic_neighbor_embedding>`_
for visualizing datasets (also see
`here <http://scikit-learn.org/stable/modules/manifold.html#t-distributed-stochastic-neighbor-embedding-t-sne>`_).
Specifically, the example considers the three most common
crystalline phases of titanium (HCP, BCC, omega).

.. figure:: _static/Ti_tsne_analysis.svg

    t-SNE analysis of a Ti dataset consisting of BCC, HCP and omega structures
    as well as configurations from a high temperature molecular dynamics
    simulation.

Source code
-----------

.. |br| raw:: html

   <br />

.. container:: toggle

    .. container:: header

        Structure preparation |br|
        ``examples/advanced_topics/interface_with_sklearn/1_prepare_structures.py``

    .. literalinclude:: ../../../examples/advanced_topics/interface_with_sklearn/1_prepare_structures.py


.. container:: toggle

    .. container:: header

        t-SNE analysis |br|
        ``examples/advanced_topics/interface_with_sklearn/2_tsne_analysis.py``

    .. literalinclude:: ../../../examples/advanced_topics/interface_with_sklearn/2_tsne_analysis.py


.. container:: toggle

    .. container:: header

        Tools |br|
        ``examples/advanced_topics/interface_with_sklearn/tools.py``

    .. literalinclude:: ../../../examples/advanced_topics/interface_with_sklearn/tools.py
