.. raw:: html

    <style> .navy {color:navy} </style>

.. role:: navy

.. raw:: html

    <style> .white {color:white} </style>

.. role:: white


.. _SMAPeffectRecommendTrouble:

#################################
Recommendations & Troubleshooting
#################################


Collect (input files)
---------------------

for troubleshooting: the reference genome sequence should be adjusted to the cultivar/line used for the analysis, to make sure that the reference sequence is indeed detected at least once in the sequences materials (or else: for each locus a ref sequence must be present in the haplotype-windows genotype table, perhaps an option can be added to **SMAP haplotype-window** to output this sequence, even if no observations occur in the sample set.

Annotation rules (assumptions on effect prediction, which types of edits are scored per impact class (no, minor, major))
------------------------------------------------------------------------------------------------------------------------

Filtering out noise (frequency, position, type of polymorphism)
---------------------------------------------------------------

Level of aggregation
--------------------

aggregate by haplotype
aggregate by effect


Discretize
----------

discretization rules (switch from cumulative frequency to WT | het KO| hom KO)


.. _SMAPeffect_thresholds:

Setting thresholds for SMAP effect-prediction
---------------------------------------------

:navy:`Optimization starts with choosing the best (combination of) thresholds for the data set`

The choice of thresholds depends on ... 

Here, we first illustrate how to optimize the thresholds using empirical data on a small number of samples as a pilot experiment.


.. tabs::

   .. tab:: test 1

		.. image:: images/SMAP_effect-prediction.png

		Texts.

   .. tab:: test 2

		.. image:: images/SMAP_effect-prediction.png

		Texts.


Troubleshooting
---------------

While recommended parameters are optimized for commonly used CRISPR experiments protocols, the graphic results of **SMAP effect-prediction** may show you that you need to adjust the data processing procedure.

Use the graphs to check that for each ... Finally, **SMAP effect-prediction** creates a ... curve by plotting ... per sample versus the total number of ... per sample.

