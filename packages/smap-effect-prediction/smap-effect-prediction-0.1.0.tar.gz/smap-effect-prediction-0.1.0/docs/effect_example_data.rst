.. raw:: html

    <style> .navy {color:navy} </style>

.. role:: navy

.. raw:: html

    <style> .white {color:white} </style>

.. role:: white

#####################################
Example Data
#####################################

.. _SMAPeffectex:

Illustration of SMAP effect-prediction
--------------------------------------

| Below, we present examples of **SMAP effect-prediction** with optimal parameter settings to illustrate typical filtering and aggregation steps. For each data set, the command to run **SMAP effect-prediction** with suggested optimal settings, together with graphical results are displayed for comparison to your own data.
| 
| Please note that while we *suggest* 'optimal' parameter settings in the command to run **SMAP effect-prediction**, the default of **SMAP effect-prediction** is to perform as little filtering as possible and to report all loci. The user is adviced to run **SMAP effect-prediction** first with the mandatory and default settings, and then decide on the most optimal parameter settings for your own data set. Parameter settings should be iteratively adjusted for each novel data set, after manual inspection of the graphical output. The example data shown below are merely meant to illustrate the expected outcome of data sets processed with parameters adjusted to the specific species and reference (gene) sets. If your data does not look like these examples, please check out the section :ref:`Recommendations and Troubleshooting <SMAPeffectRecommendTrouble>` for examples (and suggested solutions) of suboptimal parameters, or sample sets analyzed with inappropriate parameter settings for **SMAP effect-prediction**. There, some guidelines for troubleshooting are provided for **SMAP effect-prediction** :ref:`parameter settings <SMAPeffectSummaryCommand>`.

ROI-based filtering of variants
-------------------------------



aggregate effects per haplotype
-------------------------------

:navy:`SMAP effect-prediction first scores different possible effects independently, and then aggregates those to a single effect score per haplotype`

			 .. image:: images/example_data/102.png

| Tab command shows a typical command to run **SMAP effect-prediction** that aggregates effects per haplotype.
| Tabs for subsequent steps of aggregation show how a single score per haplotype is obtained together with explanation about step-specific parameters.

| Aggregate (impact per haplotype)
| 	score initiation of start site : loss of ATG means protein length = 0.
| 	score splicing acceptor or donor site: truncate protein at last splicing donor site.
| 	score translate protein, create a pair-wise alignment, calculate % identity with reference and % coverage of reference (multiply both scores):
| 	score conserved length in % intervals: 100% = no effect, 95-100% = low impact, 75-95% = medium impact, <75% is high impact. Interval borders can be set at command line.



	  .. tabs::

		 .. tab:: command
		 
			:: 
				
				smap effect-prediction options
		 
		 .. tab:: annotate
		 
			 .. image:: images/SMAP_effect-prediction.png
		
		 .. tab:: filter
			
			.. image:: images/SMAP_effect-prediction.png
			
			text.

----

aggregate haplotypes per locus
------------------------------

:navy:`SMAP effect-prediction takes the aggregated effect score per haplotype, and sums the total relative frequency across haplotypes per effect score (classes: no effect, low impact, medium impact, high impact)`

	  | Text.
