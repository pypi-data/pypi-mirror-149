.. raw:: html

    <style> .navy {color:navy} </style>
	
.. role:: navy

.. raw:: html

    <style> .white {color:white} </style>

.. role:: white

###########################
Scope & Quick Start
###########################

Scope
-----

The module **SMAP effect prediction** is designed to provide biological interpretation of the haplotype call tables created by **SMAP haplotype-window**.  

It's main functions are to:

	  1. Filter for haplotypes with edits in a defined region of interest (ROI; *e.g.* surrounding the PAM site for CRISPR-Cas experiments) to eliminate noise from the genotype table.  
	  #. Substitute the segment of the original reference gene sequence by the observed haplotype, keeping track of all relevant coordinates of intron-exon borders, translational start and stop codons, and the open reading frame (ORF), and predict the resulting (mutated) protein sequence.  
	  #. Compare the novel predicted protein sequence to the original reference protein and estimate the fraction of the protein length that is still encoded by the novel (mutated) allele.  
	  #. Use a threshold for the %protein length required for (partial) loss of function, and classify all haplotypes by effect class (no/minimal effect, intermediate effect, loss-of-function).  
	  #. Aggregate all observed haplotypes and sum their relative frequencies per effect class.  
	  #. Finally, discretize the genotype calls as homozygous or heterozygous for reference versus loss of function at a user defined minimal effect level.  
	  #. Plot summary statistics of editing "fingerprints" across the data set to allow the user to optimize parameter setting accoring to their experimental data.  

----

Integration in the SMAP package
-------------------------------

.. image:: images/SMAP_global_overview_sites_window_design_effect_WGS_transparent.png

Within the SMAP package, the modules **SMAP target-selection**, **SMAP design**, **SMAP haplotype-window** and **SMAP effect-prediction** are designed to provide a seamless workflow from target selection (e.g. candidate genes), integrated primer and gRNA design, 

multiplex resequencing of target loci across large plant collections, followed by identification of all observed haplotypes (naturally occuring or CRISPR-induced sequence variants), the prediction of functional effects of sequence variants at the protein level to identify (partial) loss-of-function (LOF) alleles, 
and finally aggregate and discretize genotype calls in an integrated genotype table with the homozygous/heterozygous presence of LOF alleles per locus per sample.
The overarching goal of this entire workflow is to identify carriers of LOF alleles for functional analysis, or for genotype-phenotype associations.
Specific functionalities of the other modules are given in their online manuals.

Specifically, the underlying concepts of **SMAP effect-prediction** exploit:

	1.  Modularity, compatibility throughout the entire workflow.  
	#.  Flexibility in design (scalability to complex multi-amplicon / multi-gRNA design per gene).  
	#.  Predicted effect of the observed mutation on the encoded protein level.  
	#.  Customized aggregation of effects per haplotype (thresholds).  
	#.  Customized aggregation of alleles per effect class per locus (thresholds).  
	#.  Discretizing the complex haplotype table to a simple homozygous / heterozygous LOF effect per locus per sample.  
	#.  Single command line operation per module.  
	#.  Traceable output (discrete LOF-call genotype table, alignments, VCF-encoded variants, predicted proteins).  
	#.  Biology-driven decisions.  

----

Guidelines for **SMAP effect-prediction**
-----------------------------------------

These tabs provide a decision scheme to guide you to the correct parameter settings.  

.. tabs::

	.. tab:: Overview
	  
		| Answer the :navy:`questions in blue` according to your data and analysis objectives. See section Recommendations and guidelines for further details.  

	.. tab:: Start the decision scheme

		| You have: 
		| 👉 a FASTA file with reference sequences.  
		| 👉 A GFF file with border positions in the reference sequence to delineate amplicon positions.  
		| 👉 A master table with relative haplotype frequencies per sample from **SMAP haplotype-window**.  
		|  
		| :navy:`Do you want to filter for mutations in regions of interest (ROI) within haplotype sequences (e.g. based on gRNA position)?`  

		.. tabs::

			.. tab:: YES, use ROI
			
				| Yes, I want to consider mutations only in a specific range around the gRNA cut site.  

				| I must therefore:  
				| 👉 provide a GFF file with the coordinates of the gRNAs ``option -u``.  
				| 👉 define the lower bounds ``option -r`` and upper bounds ``option -s`` around the cutsite, as nucleotide distance.  
				| and  
				|    👉 define an offset for the cut site position ``option -f`` relative to the gRNA 5’ end  
				|    or  
				|    👉 use a predefined offset by selecting a CAS protein ``option -p``.  
				
				| This will define the region of interest (ROI) searched for mutations. Any mutation that overlaps with at least one nucleotide to the ROI is retained. Mutations outside the ROI are considered as reference sequence and ignored for the prediction of the protein sequence (only the sequences corresponding to the ROI are substituted to the reference sequence before ORF translation). Haplotypes with only mutations outside the ROI are collapsed with the reference haplotype during aggregation.
				| Check out the schemes below for the definition of lower ``-r`` and upper bounds ``-s``, offset ``-f or -p``, and ROI for gRNAs located on the forward and/or reverse strand ``-u``.  
				
				.. tabs::
					
					 .. tab:: Single gRNA, forward strand
						
						  .. image:: /images/HowItWorks/HIW_collect_ROI_CRISPR_single_guide_forward.png  
						
					 .. tab:: Single gRNA, reverse strand
						
						  .. image:: /images/HowItWorks/HIW_collect_ROI_CRISPR_single_guide_reverse.png  
						
					 .. tab:: double gRNA, non-overlap s=8
						
						  .. image:: /images/HowItWorks/HIW_collect_ROI_CRISPR_double_guide_non-overlap.png  
						
					 .. tab:: double gRNA, overlap s=10
						
						  .. image:: /images/HowItWorks/HIW_collect_ROI_CRISPR_double_guide_overlap.png  
						
					 .. tab:: double gRNA, overlap s=12
						
						  .. image:: /images/HowItWorks/HIW_collect_ROI_CRISPR_double_guide_overlap_s12.png  

				:navy:`Do you want to predict the effect of mutations in the ROI on the encoded protein?`  
				 
				.. tabs::
				
					.. tab:: YES, predict effect
						  
						| Yes, I want to predict the encoded protein by substitution of the haplotype sequence in the corresponding reference sequence, and translation of the resulting ORF.  
						|  
						| I must therefore:  
						| 👉 provide a GFF file with CDS annotations of the reference sequences ``option -a``. CDS features must be located on the positive strand.  
						

						| :navy:`Do you want to aggregate the haplotype frequencies based on their effect on the encoded protein?`  
						 
						.. tabs::

							.. tab:: YES, aggregate
								  
								| Yes, I want to aggregate the haplotype frequencies by predicted effect class.  
								| e.g. create the sum of frequencies of all haplotypes leading to major effects, and aggregate the frequencies of all other haplotypes with minor or no effect as reference haplotype.  
								|  
								| I must therefore:  
								| 👉 set a threshold for the percentage protein sequence identity between the mutated and reference protein. Haplotypes **below** the threshold are considered having a major effect and their relative frequencies are summed.  
								  

								| :navy:`Do you want to discretize the aggregated frequencies into discrete calls?`  
								 

								.. tabs::

									.. tab:: YES, discretize
										  
										| Yes, I want to discretize the aggregated frequencies into categorical groups (*i.e.* genotype calls).  
										|  
										| I must therefore:  
										| 👉 set the frequency bounds ``option -i`` to transform frequency data of haplotypes into discrete genotype calls (homozygous reference, heterozygous, homozygous mutated at the predicted protein effect class (minor, major effect)).  
										| 👉 set discrete calls ``option -e`` to get binary presence/absence data.  
										|  


									.. tab:: NO, do not discretize
										  
										| No, I use ‘annotate.tsv’ and ‘collapse.tsv’ as main outputs.  
										|  

							.. tab:: NO, do not aggregate
								  
								| No, I use ‘annotate.tsv’ and ‘collapse.tsv’ as main outputs.  
								|  

					.. tab:: NO, do not predict effect
						  
						| No, I do not want to predict the effect of alternative haplotypes on the encoded protein.  
						|  
						| I must therefore:  
						| 👉 disable this function ``--disable_protein_prediction``.  
						| 👉 consider ‘annotate.tsv’ and ‘collapse.tsv’ as main outputs.  
						|  

			.. tab:: NO, use entire haplotype
				  
				| No, I want to consider mutations in the entire haplotype region (corresponding to the reference sequence between the borders).  
				| 

				  .. image:: /images/HowItWorks/HIW_collect_ROI_Nat_Var.png  
				  

				:navy:`Do you want to predict the effect of haplotype mutations on the encoded protein?`  
				 
				.. tabs::
				
					.. tab:: YES, predict effect
						  
						| Yes, I want to predict the encoded protein by substitution of the entire haplotype sequence in the corresponding reference sequence.
						|  
						| I must therefore:  
						| 👉 provide a GFF file with CDS annotations of the reference sequences ``option -a``. CDS features must be located on the positive strand.  
						|  

						:navy:`Do you want to aggregate the haplotype frequencies based on their effect on the encoded protein?`  

						.. tabs::

							.. tab:: YES, aggregate
								  
								| Yes, I want to aggregate the haplotype frequencies by predicted effect class. 
								| e.g. create the sum of frequencies of all haplotypes leading to major effects, and aggregate the frequencies of all other haplotypes with minor or no effect as reference haplotype.  
								|  
								| I must therefore:  
								| 👉 set a threshold for the percentage protein sequence identity between the mutated and reference protein. Haplotypes **below** the threshold are considered having a major effect and their relative frequencies are summed.  
								|  

								:navy:`Do you want to discretize the aggregated frequencies into discrete calls?`  
								 

								.. tabs::
								
									.. tab:: YES, discretize
										  
										| Yes, I want to discretize the aggregated frequencies into categorical groups (*i.e.* genotype calls).
										| 
										| I must therefore:  
										| 👉 set the frequency bounds ``option -i`` to transform frequency data of haplotypes into discrete genotype calls (homozygous reference, heterozygous, homozygous mutated at the predicted protein effect class (minor, major effect)).  
										| 👉 set discrete calls ``option -e`` to get binary presence/absence data.  
										|  

									.. tab:: NO, do not discretize
										  
										| No, I do not want to discretize the genotype calls. I want to keep the aggregated, quantitative haplotype frequencies (and add the positional and functional annotations to the **SMAP haplotype-window** master table).  
										|  
										| I will therefore:  
										| 👉 use ‘annotate.tsv’ and ‘collapse.tsv’ and aggregated.tsv’ as main output.  
										   

							.. tab:: NO, do not aggregate
								  
								| No, I do not want to aggregate the haplotype frequencies. I also want to keep the haplotypes and their associated annotated data separate.  
								|  
								| I will therefore:  
								| 👉 use ‘annotate.tsv’ and ‘collapse.tsv’ as main output.  
								|  

					.. tab:: NO, do not predict effect
						  
						| No, I do not want to predict the effect of alternative haplotypes on the encoded protein.  
						|  
						| I must therefore:  
						| 👉 disable that function using option ``--disable_protein_prediction``.  
						| 👉 consider ‘annotate.tsv’ and ‘collapse.tsv’ as main output.  
						|  


----

.. _SMAPeffectfilter:
   
Quick Start and options
-----------------------

:navy:`Schematic overview of filtering options`

.. image:: images/example_data/Slide4.PNG  
.. image:: images/example_data/Slide5.PNG  
.. image:: images/example_data/Slide6.PNG  

:navy:`Mandatory options for SMAP effect-prediction`  

It is mandatory to specify the files with the haplotype frequency table, the associated reference sequence, the set of gRNA sequences and GFF with positional information of CDS.

See section Command line options for specific filter options for subsequent steps of the procedure. 

Example command line to run **SMAP effect-prediction** with adjusted aggregation thresholds::

			python3 -m smap_effect_prediction haplotype-window_genotype_table.tsv genome.fasta anchors.gff local_gff_file.gff3 -u gRNAs.gff -p CAS9 -s 10 -r 20 -e dosage -i diploid -t 90 

----

.. _SMAPeffectoutput:
   
Output
------

.. tabs::

   .. tab:: Graphical output

	  | summary stats per aggregation type. **SMAP effect-prediction** creates an aggregated genotype table, *i.e.* high quality loci for downstream analyses (e.g. genotype-phenotype association).
	  | An example of the summary graphical output:
	  | **SMAP effect-prediction** plots :ref:`feature distributions <SMAPeffectHIW>` such as ... per :ref:`CDS, Gene, and amplicon <SMAPeffectHIW>`.

	  .. image:: images/example_data/newplot.png

   .. tab:: Tabular output
	
	  | **SMAP effect-prediction** creates a pre-aggregation table: locusID, haplotype, overlap_edit_window, impact scores (several columns: Start/Splice/alignRef/%conserved), %AF per sample.
	  | **SMAP effect-prediction** creates a post-aggregation table: locus ID, impact, (aggregated haplotypes as comma separated list), %_allele_freq per sample.
	  | The following tabs show real experimental data of two loci. All detected haplotypes are reported using the defaults, demonstrating how annotation and aggregation compresses the genotype call table.
  
   .. tab:: annotate
	 
	  .. csv-table:: 	  
	     :delim: ;
	     :file: images/example_data/annotate.tsv
	     :header-rows: 1
	  
   .. tab:: aggregated
	  
	  .. csv-table:: 	  
	     :delim: ; 
	     :file: images/example_data/aggregated.tsv
	     :header-rows: 1
	  
   .. tab:: discretized
	  
	  .. csv-table:: 	  
	     :delim: ;
	     :file: images/example_data/discretized.tsv
	     :header-rows: 1

   .. tab:: collapsed
	  
	  .. csv-table:: 	  
	     :delim: ;
	     :file: images/example_data/discretized.tsv
	     :header-rows: 1

         