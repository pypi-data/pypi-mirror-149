.. _credits:
.. index:: Credits

.. |br| raw:: html

  <br/>


Credits
*******

:program:`hiphive` has been developed by `Fredrik Eriksson
<https://materialsmodeling.org/people/fredrik-eriksson/>`_, `Erik Fransson
<https://www.chalmers.se/en/staff/Pages/erikfr.aspx>`_, and `Paul Erhart
<https://materialsmodeling.org/people/paul-erhart/>`_ at the `Department of
Physics <https://www.chalmers.se/en/departments/physics/Pages/default.aspx>`_
of `Chalmers University of Technology <https://www.chalmers.se/>`_ in
Gothenburg, Sweden with funding from the Knut och Alice Wallenbergs Foundation,
the Swedish Research Council, the Swedish Foundation for Strategic Research,
and the Swedish National Infrastructure for Computing.

When using :program:`hiphive` in your research please cite the following paper:

* *The Hiphive Package for the Extraction of High-Order Force Constants by Machine Learning* |br|
  Fredrik Eriksson, Erik Fransson, and Paul Erhart |br|
  Advanced Theory and Simulations **2**, 1800184 (2019) |br|
  `doi: 10.1002/adts.201800184 <https://doi.org/10.1002/adts.201800184>`_ |br|
  [EriFraErh19]_

You might also find the following paper useful, which discusses in detail the advantages and disadvantages of different regression schemes in various different application scenarios:

* *Efficient construction of linear models in materials modeling and applications to force constant expansions* |br|
  Erik Fransson, Fredrik Eriksson, and Paul Erhart |br|
  npj Computational Materials **6**, 135 (2020) |br|
  `doi: 10.1038/s41524-020-00404-5 <https://doi.org/10.1038/s41524-020-00404-5>`_ |br|
  [FraEriErh20]_

If you want to run large-scale molecular dynamics simulations with force constant potentials constructed via :program:`hiphive`, you should find the GPU implementation in the :program:`GPUMD` code useful, which is described in the following paper:

* *Efficient calculation of the lattice thermal conductivity by atomistic simulations with ab-initio accuracy* |br|
  Joakim Brorsson, Arsalan Hashemi, Zheyong Fan, Erik Fransson, Fredrik Eriksson, Tapio Ala-Nissila, Arkady V. Krasheninnikov, Hannu-Pekka Komsa, and Paul Erhart |br|
  Advanced Theory and Simulations **4**,  2100217 (2021) |br|
  `doi: 10.1002/adts.202100217 <http://doi.org/10.1002/adts.202100217>`_ |br|
  [BroHasFan21]_
  
:program:`hiphive` implements methods that have evolved in the field over many
years including work by, e.g.,

* Parlinski, Li, and Kawazoe [ParLiKaw97]_
* Esfarjani and Stokes [EsfSto08]_
* Hellman, Abrikosov, and Simak [HelAbrSim11]_
* Tadano, Gohda, and Tsuneyuki [TadGohTsu14]_
* Zhou, Nielson, Xia, and Ozolins [ZhoNieXia14]_
* Togo and Tanaka [TogTan15]_

Please cite these original papers as appropriate for your work.

For a general overview of the vibrational properties of materials see e.g., [Ful10]_.
