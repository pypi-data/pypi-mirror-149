.. _SMAPeffectSummaryCommand:

#####################################
Summary of the command line arguments
#####################################

.. argparse::
	:module: smap_effect_prediction.__main__
	:func: get_arg_parser
	:prog: SMAP-Effect-Prediction

	Input and output information
		It is mandatory to specify the files with the haplotype frequency table,
		the associated reference sequence, the set of gRNA sequences, and a GFF3 with
		structural gene annotation. First, the haplotype frequency table should be generated
		using `SMAP haplotype-window <https://gitlab.com/dschaumont/smap-haplotype-window>`_.
		Second, the same reference sequence that was used to generate the haplotype frequency table with
		**SMAP haplotype-window** must be provided to **SMAP effect-prediction**. Third,
		haplotype calling occurred within a 'window', defined by two borders 
		(typically the 10 nucleotides at the 3' of the HiPlex primers).
		The position of the windows are provided to **SMAP effect-prediction** by a GFF3 file containing the position of these borders.
		A single gff entry corresponds to one border, and two borders must be linked together
		to form a window by using a shared `NAME` attribute value. All borders must be specified
		in the '+' orientation to the reference genome. Finally, a GFF3 file defining the
		gene and CDS information should be provided. 
		For your convenience, all these input files can be prepared with the modules **SMAP target-selection** and **SMAP design**.
	
	gRNA information
		Regarding input files, there is only one file that is considered optional: a GFF3 file
		of the gRNA positions. These gRNA positions allow **SMAP effect-prediction** to filter haplotypes
		to collapse those haplotypes that only contain variations `outside` a user-defined range around
		the cut-site defined by the gRNA where 'true positive' variation should occur.
		Each gRNA should be a single gff entry, with a '+' orientation compared to the reference.
		Additionally, each gRNA should have a unique `NAME` attribute that specifies its target locus.

		The locations of the gRNAs are not enough to specify where the Cas enzyme cuts the DNA for editing.
		The type of Cas protein used for the editing experiment also determines the offset relative
		to the position of the gRNA. Therefore, options are available to specify this offset by
		either using a predefined offset by using the name of the Cas9 protein, or by using a custom offset (i.e. number of nucleotides).
	
	Alignment parameters : @after
		The default settings below have been determined empirically. As **SMAP effect-prediction** relies heavily on the alignment
		of haplotypes to the reference sequence, caution is advised when changing these defaults. For more information on the alignment implementation,
		we refer to the `biopython documentation <https://biopython.org/docs/1.75/api/Bio.Align.html?highlight=pairwisealigner#Bio.Align.PairwiseAligner>`_. 