.. raw:: html

    <style> .navy {color:navy} </style>
	
.. role:: navy

.. raw:: html

    <style> .white {color:white} </style>

.. role:: white

############################
How It Works
############################

.. _SMAPeffectHIW:

Here, we describe the technical implementation of **SMAP effect-prediction**.

----

Preparing input files with SMAP design and SMAP haplotype-window
----------------------------------------------------------------

SMAP design
~~~~~~~~~~~

During the **SMAP design** workflow, **SMAP target-selection** first selects one or more genes with a short flanking upstream and downstream region, and a GFF file is created with the positional information of the exons that together make up the protein coding sequence (CDS).  
Importantly, **SMAP target-selection** makes sure that all sequences are oriented in the direction of the protein coding gene. Genes encoded on the - strand in the reference genome sequence are reverse complemented, and all coordinates of the CDS are automatically reversed.   
If custom created FASTA and GFF files are provided to **SMAP effect-prediction**, and CDS features are positioned on the - strand in the GFF file with the structural gene annotation, **SMAP effect-prediction** will indicate which genes have errors, and should be reverse completented prior to running **SMAP haplotype-window** and **SMAP effect-prediction**.  
If the CDS of a particular gene does not begin with a START codon (ATG), or end with a STOP codon (TAA, TAG or TGA), **SMAP effect-prediction** will indicate which genes have errors that should be corrected in the reference sequence FASTA file or the structural gene annotation GFF file.  


.. image:: images/HowItWorks/HIW_gene.png  

Then, **SMAP design** identifies amplicons and gRNAs in the CDS of the gene. One or more amplicons may be designed per gene, each containing one or more gRNAs. A minimal spacing between the gRNA(s) and the primer binding sites are respected to allow for editing at some distance from the PAM site without affecting the primer binding sites, thus retaining the capacity to amplify the genomic region containing induced mutations.

The coordinates of gRNAs and primers with respect to the selected reference gene sequence are listed in GFF files for downstream analysis. Border sequences are defined as the last 10 nucleotides at the 3' end of the forward and reverse primers for delineation of haplotype sequences by **SMAP haplotype-window**.  

.. image:: images/HowItWorks/HIW_design.png  

The sequences of the gRNAs are used to synthesize gRNAs and clone into expression vectors to drive CRISPR/Cas in plant materials. The primers are used for HiPlex sequencing of potentially edited lines.  

SMAP haplotype-window
~~~~~~~~~~~~~~~~~~~~~

**SMAP haplotype-window** analyses reads aligned to the target loci and extracts the exact DNA sequence inbetween the upstream and downstream border sequences per locus, thus listing all observed haplotypes per locus across a collection of potential mutants. **SMAP haplotype-window** also calculates relative haplotype frequency per locus per sample. This genotyping table is the input for **SMAP effect-prediction**.  

.. image:: images/HowItWorks/HIW_window.png  

----

The subsequent steps of SMAP effect-prediction
----------------------------------------------

Next, we describe the seven subsequent steps of **SMAP effect-prediction**.  


Step 1. Collect
~~~~~~~~~~~~~~~

:navy:`Collect all positional and sequence information needed to predict the encoded protein for each haplotype`

**SMAP effect-prediction** collects the following information from files prepared by the other modules of SMAP:

.. tabs::

   .. tab:: required input

	1)	the gene sequence from the reference genome; **SMAP target-selection** extracts the gene sequence and places it with the CDS on the + strand orientation in the reference FASTA file used for SMAP.  
	#)	the position of the CDS regions in the reference sequence; **SMAP target-selection** calculates the correct positions of the CDS with respect to the extracted gene reference sequence of 1).  
	#)	the position of the amplicon(s) in the gene reference sequence; **SMAP design** creates pairs of primers for HiPlex sequencing of genomic DNA, and stores the relative position of the corresponding border regions in a GFF file.  
	#)	the position of gRNA(s) for CRISPR/Cas genome editing within an amplicon; **SMAP design** optionally creates one or more gRNAs per amplicon to induce mutations in a particular position of the reference genome.  
	#)	the collection of haplotypes per locus and their relative frequencies per sample; **SMAP haplotype-window** extracts haplotypes (exact DNA sequences) using the exact same reference gene coordinates as outlined in 1)-4).  

   .. tab:: reference sequence FASTA
	 
	  .. csv-table:: 
	     :delim: ;
	     :file: images/HowItWorks/genome_TR.fasta
	     :header-rows: 0
	  
   .. tab:: gene and CDS positions GFF
	  
	  .. csv-table:: 
	     :delim: , 
	     :file: images/HowItWorks/local_gff_file_TR.gff
	     :header-rows: 0
	  
   .. tab:: border positions GFF
	  
	  .. csv-table:: 
	     :delim: ;
	     :file: images/HowItWorks/borders_TR.gff
	     :header-rows: 0
	  
   .. tab:: gRNA positions GFF
	  
	  .. csv-table:: 
	     :delim: ;
	     :file: images/HowItWorks/guides_TR.gff
	     :header-rows: 0
	  
   .. tab:: SMAP haplotype-window haplotype frequency table
	  
	  .. csv-table:: 
	     :delim: ;
	     :file: images/HowItWorks/haplotype_frequency_TR.tsv
	     :header-rows: 1
	     :widths: 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5
	  

:navy:`Naturally occurring sequence variation`

If **SMAP effect-prediction** is used to analyse naturally occurring sequence variation present in a broad genepool (*e.g.* ecotypes or breeding materials), it derives the following information per gene and amplicon:

	1)	reference protein sequence (including checks for translational START and STOP codons in the reference protein).
	2)	position of intron/exon junctions and splicing donor/acceptor sites.

:navy:`CRISPR/Cas-induced mutations`

If **SMAP effect-prediction** is used to analyse CRISPR/Cas-induced genome editing, positional information of the gRNA is used to also derive:

	3)	gRNA sequence.
	4)	expected cut-site.
	5)	region of interest (ROI).

The information required (and their respective options) are illustrated in the tabs below. 
The difference between analysing these types of sequence variation is defined by the region of interest (ROI) in which sequence variation is expected: 

.. tabs::

   .. tab:: Natural variation

	.. image:: images/HowItWorks/HIW_collect_ROI_Nat_Var.png  

    In case of natural variation, the entire length of the haplotype window is considered. 

   .. tab:: CRISPR/Cas-induced mutations

	.. image:: images/HowItWorks/HIW_collect_ROI_CRISPR.png  

    In case of CRISPR/Cas-induced mutations, a short region surrounding the gRNA binding site, adjacent to the PAM site where Cas acts on the DNA (either by cutting, base-editing, or other modifications) is considered.
    This region of interest (ROI) is defined by the PAM sequence (Cas-enzyme dependent), the distance between the PAM site and the expected cut-site (offset), the region upstream (in the direction of the PAM site) and downstream (away from the PAM site) from the expected cut-site in which mutations are expected. Any sequence variant that overlaps with the ROI by at least one nucleotide, is considered relevant for **SMAP effect-prediction**.
    All other sequence variants outside the ROI (such as neighboring SNPs, read errors, indels far away from the expected cut-site, or extra nucleotides near the borders resulting from poor trimming by **SMAP haplotype-window**) will be considered as reference sequence and ignored for estimating the resulting protein sequence.
    
----

.. _SMAPeffectHIW2:

Step 2. Align
~~~~~~~~~~~~~

:navy:`Align each haplotype to its reference per locus`

  .. tabs::

	 .. tab:: hap_a SNP

		.. image:: images/HowItWorks/align_hap_a.png

	 .. tab:: hap_b SNP

		.. image:: images/HowItWorks/align_hap_b.png

	 .. tab:: hap_c SNP

		.. image:: images/HowItWorks/align_hap_c.png

	 .. tab:: hap_d insert

		.. image:: images/HowItWorks/align_hap_d.png

	 .. tab:: hap_e insert

		.. image:: images/HowItWorks/align_hap_e.png

	 .. tab:: hap_f SNP

		.. image:: images/HowItWorks/align_hap_f.png

	 .. tab:: hap_g deletion 

		.. image:: images/HowItWorks/align_hap_g.png

	 .. tab:: hap_h deletion + neighboring SNP

		.. image:: images/HowItWorks/align_hap_h.png

	 .. tab:: hap_i deletion

		.. image:: images/HowItWorks/align_hap_i.png

	 .. tab:: hap_j deletion

		.. image:: images/HowItWorks/align_hap_j.png

	 .. tab:: hap_k deletion

		.. image:: images/HowItWorks/align_hap_k.png

	 .. tab:: hap_l deletion

		.. image:: images/HowItWorks/align_hap_l.png

	 .. tab:: hap_m deletion

		.. image:: images/HowItWorks/align_hap_m.png

	 .. tab:: hap_n complex deletion

		.. image:: images/HowItWorks/align_hap_n.png
        
Each alternative haplotype is aligned to it's reference haplotype sequence of the corresponding locus. The reference sequence is retrieved from the coordinates of the borders of that locus provided as GFF file, and the reference sequence FASTA file. Here, the alignments of locus gene3_1 of the example data set are shown. Insertions in the alternative haplotype are shown in green, SNPs are shown in red. 

----

.. _SMAPeffectHIW3:

Step 3. Filter and collapse
~~~~~~~~~~~~~~~~~~~~~~~~~~~

:navy:`Filter for haplotypes based on location of sequence variants within the window: region of interest (ROI)`

**SMAP haplotype-window** extracts all observed unique DNA sequences within a user-defined window and calls these haplotypes. 
So, artefactual haplotypes may be created by sequence variation such as read errors, imprecise trimming, etc.  
**SMAP haplotype-window** allows to filter the genotype call table based on haplotype frequency, but not on sequence content.  
To further eliminate artefactual haplotypes and collapse the genotype table into a simpler matrix with less haplotype complexity, **SMAP effect-prediction** implements an optional filter that only retains sequence variants that overlap with a given ROI.  

:navy:`3.1. Definition of the ROI.`

.. tabs::

   .. tab:: Natural variation

	.. image:: images/HowItWorks/HIW_collect_ROI_Nat_Var.png  

    Because there is no prior focus or knowledge on where naturally occurring sequence variants may be located, the ROI typically spans the entire length of the locus.  

   .. tab:: CRISPR/Cas-induced mutations

	  .. tabs::
	
		 .. tab:: single gRNA  
	
			| Single gRNA with + strand orientation:
			
			.. image:: images/HowItWorks/ROI_hap_forward_no_name.png  
			
			| 
			| Single gRNA with - strand orientation:
			
			.. image:: images/HowItWorks/ROI_hap_reverse_no_name.png  

			| 
			| To clean up sequencing data derived from CRISPR/Cas genome editing, the relevant mutations are expected to occur in a short region surrounding the gRNA binding site, adjacent to the PAM site where Cas acts on the DNA (either by cutting, base-editing, or other modifications).  
			| This region of interest (ROI) is defined by the PAM sequence (Cas-enzyme dependent), the distance between the PAM site and the expected cut-site (offset), the region upstream (in the direction of the PAM site) and downstream (away from the PAM site) from the expected cut-site in which mutations are expected. Any sequence variant that overlaps with the ROI by at least one nucleotide, is considered relevant for **SMAP effect-prediction**.
			| All other sequence variation outside the ROI (such as neighboring SNPs, read errors, indels far away from the expected cut-site, or extra nucleotides near the borders resulting from poor trimming by **SMAP haplotype-window**) will be considered as reference sequence and ignored for estimating the resulting protein sequence.

		 .. tab:: multiple gRNAs  

			| In the current release, **SMAP effect-prediction** only works for a single gRNA per window.  
			| In a future release, we plan to implement a new option to process windows with multiple gRNAs.  
			| Two gRNAs with non-overlapping ROIs:
			
			.. image:: images/HowItWorks/HIW_collect_ROI_CRISPR_double_guide_non-overlap.png  
			
			| 
			| Two gRNAs with overlapping ROIs (single nucleotide overlap):
			
			.. image:: images/HowItWorks/HIW_collect_ROI_CRISPR_double_guide_overlap.png  
			
			| 
			| Two gRNAs with overlapping ROIs (multiple nucleotides overlap):
			
			.. image:: images/HowItWorks/HIW_collect_ROI_CRISPR_double_guide_overlap_s12.png  
			
			| 
			| In cases where multiple gRNAs are located within a single amplicon, **SMAP effect-prediction** first determines the ROI per gRNA, and then estimates if the ROIs overlap. One or more non-redundant regions are then created to cover the entire ROI.  

:navy:`3.2. Filtering on the ROI.`

.. tabs::

   .. tab:: Natural variation

	.. image:: images/HowItWorks/HIW_collect_ROI_Nat_Var.png  

	|  
	| Since there is no prior focus on where naturally occurring sequence variants may be located, the ROI typically spans the entire length of the locus.


   .. tab:: CRISPR/Cas-induced mutations

	  .. tabs::

		 .. tab:: hap_a SNP

			.. image:: images/HowItWorks/ROI_hap_a_new2.png

			| 
			| The SNP is positioned outside the ROI, so it is excluded from the haplotype call.  


		 .. tab:: hap_b SNP

			.. image:: images/HowItWorks/ROI_hap_b_new2.png

			| 
			| The SNP is positioned outside the ROI, so it is excluded from the haplotype call.  


		 .. tab:: hap_c SNP

			.. image:: images/HowItWorks/ROI_hap_c_new2.png

			| 
			| The SNP is positioned outside the ROI, so it is excluded from the haplotype call.  


		 .. tab:: hap_d insert

			.. image:: images/HowItWorks/ROI_hap_d_new2.png

			| 
			| The insertion is positioned within the ROI, so it is included in the haplotype call.  

		 .. tab:: hap_e insert

			.. image:: images/HowItWorks/ROI_hap_e_new2.png

			| 
			| The insertion is positioned within the ROI, so it is included in the haplotype call.  

		 .. tab:: hap_f SNP

			.. image:: images/HowItWorks/ROI_hap_f_new2.png

			| 
			| The SNP is positioned within the ROI, so it is included in the haplotype call.  

		 .. tab:: hap_g deletion 

			.. image:: images/HowItWorks/ROI_hap_g_new2.png

			| 
			| The deletion is positioned within the ROI, so it is included in the haplotype call.  

		 .. tab:: hap_h deletion + neighboring SNP

			.. image:: images/HowItWorks/ROI_hap_h_new2.png

			| 
			| The deletion is positioned within the ROI, so it is included in the haplotype call.  
			| The neighboring SNP is not positioned within the ROI (at r = 15), so it is not included in the haplotype call.  

			.. image:: images/HowItWorks/ROI_hap_h_new2_neighbor_SNP.png

			| 
			| At r = 30 (a more broad definition of the ROI), the neighboring SNP would be still positioned inside the ROI, and it would be included in the haplotype call, creating a more complex haplotype.  

		 .. tab:: hap_i deletion

			.. image:: images/HowItWorks/ROI_hap_i_new2.png

			| 
			| The deletion is positioned within the ROI, so it is included in the haplotype call.  

		 .. tab:: hap_j deletion

			.. image:: images/HowItWorks/ROI_hap_j_new2.png

			| 
			| The deletion is positioned within the ROI, so it is included in the haplotype call.  

		 .. tab:: hap_k deletion

			.. image:: images/HowItWorks/ROI_hap_k_new2.png

			| 
			| The deletion is positioned within the ROI, so it is included in the haplotype call.  

		 .. tab:: hap_l deletion

			.. image:: images/HowItWorks/ROI_hap_l_new2.png

			| 
			| The deletion is positioned within the ROI, so it is included in the haplotype call.  

		 .. tab:: hap_m deletion

			.. image:: images/HowItWorks/ROI_hap_m_new2.png

			| 
			| The deletion is positioned within the ROI, so it is included in the haplotype call.  

		 .. tab:: hap_n complex deletion

			.. image:: images/HowItWorks/ROI_hap_n_new2.png

			| 
			| The first long deletion spans at least part of the ROI, so it is included in the haplotype call.  
			| The second shorter deletion is positioned entirely within the ROI, so it is also included in the haplotype call.  

:navy:`3.3. Collapse the haplotype table based on identical haplotype calls in the region of interest (ROI).`

After exclusion of sequence variants *outside* the ROI, some haplotypes may contain identical haplotype calls *within* the ROI.  

.. image:: images/HowItWorks/align_haplotype_name_new_v2.png

If the user decides to ignore sequence variation *outside* the ROI, the algorithm 'collapses' corresponding haplotypes by summing their relative frequencies in the haplotype table.
Accordingly, the haplotype frequency table switches to new haplotype identifiers per locus, because the exact DNA sequence that initially identified the unique haplotypes no longer correspond to the 'collapsed' sequences. 

.. image:: images/HowItWorks/haplotype_collapse.png

----

.. _SMAPeffectHIW4:

Step 4. Annotate
~~~~~~~~~~~~~~~~

:navy:`Annotate the haplotype, score effects on gene structure and predicted protein sequence.`

**SMAP effect-prediction** uses the local GFF file provided by the user to extract gene structure annotation and place the haplotype back into its genomic context. For each haplotype, the corresponding **full length mutated protein sequence** is reconstructed and mutations in **strategic sites** (START codon, splicing sites, and STOP codon) are searched. At the end of the process, the master table is extended with more columns further describing the computationally **predicted effect of each haplotype** on the protein. The steps to annotate the master table are as follows:

:navy:`4.1. Delineate the CDS region in the window by creating a reference 'CDS code'.`

Using the local GFF file provided by the user, **SMAP effect-prediction** identifies the genomic areas corresponding to coding sequences (CDS). The CDS regions are encoded as 1 and the non-coding areas as 0. The reference genome sequence is thereby simplified into a string of 0's and 1's, here named the "CDS code". The file with border positions is used to identify the position of the haplotype both in the genome sequence and in the CDS code. The reference and mutated haplotype are extracted from the master table and the haplotype CDS code is extracted from the CDS code using the border positions. Regions outside the borders in the genomic and CDS code sequences are kept for later stages.

.. image:: images/HowItWorks/code_reference_definition.png

:navy:`4.2. Identify indels and modify the 'CDS code'.`

The alignment between the reference and mutated haplotypes (see Step 2 Align) is used to identify indels. The alignment is screened for gaps; insertions are represented by gaps in the aligned reference haplotype whereas deletions are shown by gaps in the aligned mutated haplotype. Indel indices are captured, and the reference haplotype CDS code is modified accordingly, so that its indexing now matches the length of the alignment and fits the mutated haplotype CDS sequence. 

.. image:: images/HowItWorks/INDELS_gaps.png

Insertions and deletions in the haplotype CDS code are treated differently.  


**Insertions**

For instance, if a +5 bp insertion is observed between positions 43 and 44 in the reference sequence, the haplotype CDS code will be extended by 5 characters at the same index. The mutated haplotype has a longer length compared to the reference haplotype, and so the mutated haplotype CDS code must be extended too. The rules to know which character (either 0 or 1) has to be used for extending the haplotype CDS code are as follows:  

- If positions surrounding the insertion are coding in the haplotype CDS code (*i.e.* 1), then the insertion is considered as coding (*i.e.* made of extra 1's).  

- If positions surrounding the insertion are non-coding in the haplotype CDS code (*i.e.* 0), then the insertion is considered as non-coding as well (*i.e.* made of extra 0's)  

.. image:: images/HowItWorks/code_insertion_intron.png
.. image:: images/HowItWorks/code_insertion_exon.png


- If one of the positions surrounding the insertion is coding (1), and the other is non-coding (0), this means that the mutation occurs right after or right before a splicing site. In both cases, the insertion is considered as coding.  

.. image:: images/HowItWorks/code_insertion_up.png
.. image:: images/HowItWorks/code_insertion_down.png

**Deletions**

.. image:: images/HowItWorks/code_deletion_exon.png
.. image:: images/HowItWorks/code_deletion_across.png

In the case of a deletion, the indices of the deletion in the reference haplotype are simply removed from the haplotype CDS code. The mutated haplotype has a shorter length compared to the reference haplotype, and so does the mutated haplotype CDS code.

**SNPs**

.. image:: images/HowItWorks/code_SNP.png

In case of SNPs, no gaps are observed in the alignment (only mismatches). The indexing is the same between the non-aligned and aligned reference and mutated sequences so the haplotype CDS code is not modified. SNPs in coding areas are assumed to be coding and SNPs in non-coding areas are assumed to be non-coding.


:navy:`4.3. Place CDS codes of reference and mutated haplotypes back into their genome context.`

The mutated haplotype sequence and the mutated CDS code are placed back into their respective context. Both sequences are stitched back with the reference regions outside the borders that were kept at step 1 of the annotation process. This results in a full genome sequence with mutation in the haplotype area and a full CDS code of the **same length** with altered sequence in the haplotype area.

:navy:`4.4. Search for mutations at translational START and STOP codons and splicing sites.`

Before translating the mutated genomic sequence using the mutated CDS code, **strategic sites** are searched for mutations. **SMAP effect-prediction** will consider that any modifications at the translational START codon is a major effect. Because **SMAP effect-prediction** can not reliably predict translation re-initiation that might occur at a downstream alternative translational START codon, it is not possible to compute an alternative protein sequence. The resulting identity score between the reference and the mutated protein is by definition 0. Likewise, modifications at splicing sites are considered major effects. Because **SMAP effect-prediction** cannot reliably predict which downstream splicing donor or acceptor site will be used, the algorithm simply truncates protein translation right at the position of the mutated splicing donor or acceptor site. Finally, mutations at the translational STOP codon lead to an extended open reading frame (ORF) at the 3' end, and the translation continues until it reaches the following STOP codon in the ORF.  

:navy:`4.5. Extract and stitch all CDS sequences to create a full length CDS.`

The mutated protein is obtained using the mutated genomic sequence and the mutated CDS code. Coding areas are extracted and stitched together to form the full CDS. The mutated CDS is then translated, considering possible mutations at strategic sites (see step 4 of the annotation process).  

	 .. image:: images/HowItWorks/Adjusted_ORF_haplotype_name_V4_zoom_exon4_translation.png

*In-silico* translation of the haplotypes of gene3. Amplicons (gene3_1) were projected into their respective gene context and translated in the corresponding ORF. 

:navy:`4.6. Align reference and mutated protein and calculate %identity score.`

The reference and mutated protein are aligned. The number of identical amino acids in the alignment is computed and divided by the total length of the alignment and expressed as percentage to obtain the identity score (see also `Grant lab <http://thegrantlab.org/bio3d/reference/seqidentity.html>`_, `Girgis et al., 2021 <https://doi.org/10.1093/nargab/lqab001>`_, `EBI <https://www.ebi.ac.uk/seqdb/confluence/display/JDSAT/Bioinformatics+Tools+FAQ#BioinformaticsToolsFAQ-Whatdoespercentageidentityreferto?>`_).  

::

	ref ML--IIFGLA
	    ||  ||| ||
	mut MLDKIIF-LA


| Number of identical aligned residues: 7  
| Total length of the alignment: 10  
| %identity score: 7/10 = 0.70 = 70%  

In case the original protein is much longer than the mutated protein, the two proteins are aligned globally so the length of the alignment is 16, but only 7 amino acids are identical in the *alignment*.

::

	ref ML--IIFGLATLGHWS*
	    ||  ||| ||  
	mut MLDKIIF-LA*  


| Number of identical aligned residues: 7  
| Total length of the original protein: 16  
| %identity score: 7/16 = 0.438 = 43.8%  

.. image:: images/HowItWorks/Adjusted_ORF_haplotype_name_V4_translations_alignment.png

Alignment of the predicted proteins encoded by haplotypes of gene3.  

:navy:`4.7. Add the novel annotation columns to the haplotype frequency table.`

The master table is annotated and extended with **five more columns**:  

	1) atgCheck: whether the ROI in the haplotype contains a mutation affecting the START codon: True/False  
	#) splicingSiteCheck: whether the ROI in the haplotype contains a mutation affecting a splicing site: True/False  
	#) stopCodonCheck: whether the ROI in the haplotype contains a mutation affecting the STOP codon: True/False  
	#) protein_sequence: the full length mutated protein sequence  
	#) pairwiseProteinIdentity: the %identity score between the reference and mutated proteins as explained at 6.  

----

.. _SMAPeffectHIW5:

Step 5. Classify loss-of-function effect of mutation on protein per haplotype: LOF effect classes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:navy:`quantify the effect on gene function or activity based on the %identity score`

The user can define the %identity cutoff to declare that a mutation has an effect on the protein function or activity, based on the protein identity score computed in the previous step (see step 4.6. of the annotation process). The degree of loss-of-function (LOF) can be discretized in three discrete effect classes: no or minimal effect, intermediate effect, strong effect (knockout, KO).
Haplotypes leading to substantial loss of the protein sequence are expected to cause major protein disruptions and are therefore considered as loss-of-function (LOF) or knockout (KO) haplotypes. For instance, at a cutoff of 70%, haplotypes with %identity score below 70 are considered major effect mutations, whereas haplotypes with %identity score greater than 70%, are considered to *not* have a major effect on the protein (*i.e* considered as functional as reference).

.. image:: images/HowItWorks/haplotype_LOF_class.png


----

.. _SMAPeffectHIW6:

Step 6. Aggregate haplotype frequencies per locus by LOF effect class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:navy:`Aggregate the frequency values of haplotypes that have at least a minimal degree of LOF: per locus, per sample`


.. image:: images/HowItWorks/haplotype_LOF_frequency_table.png

The frequencies of LOF haplotypes are summed per locus per sample to display the relative fraction of proteins with at least a minimal degree of LOF. The resulting aggregated genotype call table contains the cumulative frequency of all haplotypes encoding a **LOF protein** (one value per locus per sample on a scale of 0-1; where 0 indicates all reference protein, and 1 indicates all LOF protein).  

----

.. _SMAPeffectHIW7:

Step 7. Discretize
~~~~~~~~~~~~~~~~~~

:navy:`Transform cumulative LOF frequency to discrete genotype calls: WT, heterozygous KO, homozygous KO`

.. image:: images/HowItWorks/Discretize_LOF_frequencies_all9genes_newFreq.png


Aggregation of KO haplotype frequencies leads to a quantitative LOF frequency distribution that is difficult to interpret in genetic analysis. The aggregated KO haplotype frequency has a W-shape distributions in diploid samples. Local maxima are located around values of aggregated KO haplotype frequency of 0, 50%, and 100% which corresponds to homozygous reference, heterozygous KO, and homozygous KO, respectively. Indeed situations where half of the reads are KO haplotypes and half are not highlight heterozygosity in a diploid organism. **SMAP effect-prediction** can transform the quantitative KO haplotype frequency into discrete genotype calls, homozygous reference, heterozygous, homozygous mutant, coded as 0, 1, and 2, respectively. The frequency intervals to call such genotypes can be user-defined. As a rule of thumb, we generally consider that <15% is homozygous reference, between 40% and 60% is heterozygous, and >90% is homozygous mutant. These cutoffs can be adjusted after inspection of the graphical output after a first analysis. The discretization further eases the interpretation of the table, especially in the case of Mendelian segregation in progeny, or downstream statistical analyses to associate phenotypes to genotypes. Discretization may also be performed before aggregation of haplotypes per locus so that one can associate phenotype per haplotype rather than per locus.

.. image:: images/frequency_distribution.png


