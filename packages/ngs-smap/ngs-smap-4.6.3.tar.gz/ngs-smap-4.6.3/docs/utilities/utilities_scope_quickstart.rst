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

In Shotgun sequencing, haplotypes are defined by a set of SNPs in a dynamic sliding frame. Start and end positions of sliding frames (called Anchor points) are typically defined as the first and last SNP of a string of neighboring SNPs across a given distance.  
A special case is the detection of the junctions of large-scale inversions or deletions, in which the read mapping breakpoint is taken as variable position flanked by two Anchor points: the nucleotides immediately upstream and downstream. See schemes below for graphical illustration of the two concepts.

Setting the stage
-----------------

:navy:`Haplotyping neighboring SNPs in sliding frames`

Schemes show a heterozygous individual with a reference allele and one alternative allele. Only reads spanning the entire locus are used for read-backed haplotyping. The total read depth (RD) is shown below each derived haplotype (string of "0"'s and "1"'s). 
Note that at longer sliding frame length (40bp versus 60bp), the number of loci reduces (locus_1 and locus_2 are joined into the longer locus_1), the number of SNPs grouped per locus increases, and the number of reads spanning the entire locus_1 (shown in bold) is reduced so that effective read depth per haplotype (RD) reduces.
At shorter maximal sliding frame length (*e.g.* 40 bp) some reads span both locus_1 and locus_2. Because loci are haplotyped independently, different parts of the same read may add data to neighboring loci, as long as they span the entire length *per* locus.

.. tabs:: 

	.. tab:: Sliding frames
	
			.. image:: ../images/utilities/utilities_Sliding_frames_SNPs.png
		   
		Neighboring SNPs define sliding frames. Given a set of SNPs in a VCF file, loci are delineated that contain subsets of neighboring SNPs within a given maximal sliding frame length (*e.g.* 40bp or 60bp).

	.. tab:: Sample1 40bp
		
			.. image:: ../images/utilities/utilities_Sample1_40bp_SNPs.png
		
	.. tab:: Sample2 40bp
		
			.. image:: ../images/utilities/utilities_Sample2_40bp_SNPs.png
		
	.. tab:: Sample3 40bp
		
			.. image:: ../images/utilities/utilities_Sample3_40bp_SNPs.png
		
	.. tab:: Sample1 60bp
		
			.. image:: ../images/utilities/utilities_Sample1_60bp_SNPs.png
		
	.. tab:: Sample2 60bp
		
			.. image:: ../images/utilities/utilities_Sample2_60bp_SNPs.png
		
	.. tab:: Sample3 60bp
		
			.. image:: ../images/utilities/utilities_Sample3_60bp_SNPs.png
		

:navy:`Haplotyping junctions of (large-scale) inversions or deletions`

The junctions surrounding inversions or deletions can be recognized at the single read level as a sudden breakpoint in the read-reference alignment. Typically, the maximum exact match (MEM) that seeds the alignment in BWA-MEM places the longest half of the read adjacent to the breakpoint, and the other half of the read is soft-clipped, or not matched to the reference genome. At the locus level, it can be recognized as the consistent sharp drop in read depth on one side of the junction, as each read is expected to display the same read-reference alignment breakpoint. Heterozygous individuals are expected to display a pattern where half the number of reads display the alignment breakpoint at the junction, and the other half of the number of reads display continuous read-reference alignments across the junction.  
This read mapping profile can be coded as haplotype by SMAP, because read-reference alignments are transformed to haplotypes while considering absence/presence of read mapping.  
The approach to score clean drops in read depth at SV mapping breakpoints is to define 3-bp loci with the breakpoint nucleotide as the central position, immediately flanked by an upstream and a downstream nucleotide position and score absence/presence per position. Deletions with respect to the reference are marked as "-" characters and absence of read mapping (due to terminated read alignment) as "." characters in the haplotype string.

Please note that the above description refers to large scale *inversions* (which, in a short read, behave as a 'deletion' of the sequence neighboring a junction), not *insertions*. **SMAP haplotype-sites** currently does not support identifying *insertions* (and coding those as haplotype strings), as we strictly adhere to the reference coordinate system to encode the absence or presence of nucleotides in the alignment. Adding nucleotides into the haplotype string (insertions with respect to the reference haplotype string) is not possible.  

.. tabs:: 

	.. tab:: Short deletion
		
			.. image:: ../images/utilities/utilities_Sample2_short_deletion.png
		
	.. tab:: Upstream junction
		
			.. image:: ../images/utilities/utilities_Sample2_LB_deletion.png
		
	.. tab:: Downstream junction
		
			.. image:: ../images/utilities/utilities_Sample1_RB_deletion.png
		

Feature Description
-------------------

The scheme below defines the features of sliding frames and shows how parameters can be adjusted to customise the length and spacing of sliding frames with respect to SNPs on a given reference genome sequence.
Key features are:

	1.  Locus: name of the region of the reference genome that contains polymorphisms to be haplotyped.
	#.  Anchor points: the start and end positions of the locus. 
	#.  Maximal frame_length: the maximal length of the frame that includes the first and last SNPs to be grouped, as well as the off-set at start and end of the frame.
	#.  Minimal frame_distance: minimal distance between two adjacent loci.
	#.  Off-set: a number of nucleotides before the first SNP, and after the last SNP. Used to create space around the SNPs to ensure consistent read mapping around the SNPs to be haplotyped.

How It Works
------------

Haplotyping sliding frames with adjacent SNPs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:navy:`Step 1. Locate the first sliding frame on a reference sequence using a-priori known SNP coordinates (in a sorted VCF file).`

	.. image:: ../images/utilities/utilities_HIW_SNP_step1.png

	| 
	| (1) The first SNP on the reference sequence *after* the off-set length becomes the first SNP of Locus 1 (grey vertical arrow). The frame_distance is not considered *before* the first locus.
	| (2) The position at distance off-set upstream of the first SNP defines the 5’ start site of Locus 1 (also called the upstream Anchor point, upstream green vertical arrow). If the off-set is set to "0", the SNP position is the upstream Anchor point of Locus 1.
	| (3) Starting from the 5' start site of Locus 1, all downstream neighboring SNPs within the maximal frame_length minus off-set length are grouped for Locus 1. (So that the coordinate of the last SNP plus off-set length still falls within the maximum frame_length).
	| (4) The position of the last (most downstream) SNP within the group is determined (blue vertical arrow).
	| (5) The 3’ end site of Locus 1 (also called the downstream Anchor point, downstream green vertical arrow) is positioned at the off-set distance after the last SNP in Locus 1. If the off-set is set to "0", the last SNP position is the downstream Anchor point of Locus 1.

:navy:`Step 2. Locate the next sliding frame at some distance downstream of Locus 1.`

	.. image:: ../images/utilities/utilities_HIW_SNP_step2.png

	| 
	| (6) The first SNP *after* a distance with length minimum frame_distance plus off-set after the 3’ end site of Locus 1, becomes the first SNP of Locus 2.
	| (7) The position at distance off-set upstream of the first SNP defines the 5’ start site of Locus 2.
	| (8) All downstream neighboring SNPs within the frame length minus off-set length are grouped for Locus 2. (So that that SNP plus off-set length still falls within the maximum frame_length).
	| (9) The position of the last SNP within the selected group is determined.
	| (10) The 3’ end site of Locus 2 is positioned at the off-set distance after the last SNP in Locus 2.
	| (11) Note that the SNP (shaded purple vertical arrow) positioned in the off-set region, inbetween the 'last SNP' (blue vertical arrow) and the 3’ end site of Locus 2 (downstream green vertical arrow), was not considered to define the locus start and end point coordinates but will still be taken along for haplotyping as it is contained within the Locus 2 range.

:navy:`Step 3. Repeat along the length of the reference sequence, while ignoring SNPs that are too close to the previous locus.`

	.. image:: ../images/utilities/utilities_HIW_SNP_step3.png

	| 
	| (12) The first SNP *after* length minimum frame_distance plus off-set after the 3’ end site of Locus 2 becomes the first SNP of Locus 3.
	| (13) SNPs positioned within the frame-distance regions are ignored.
	| (14) The position at distance off-set upstream of the first SNP defines the 5’ start site of Locus 3.
	| (15) All downstream neighboring SNPs within the frame_length minus off-set length are grouped for Locus 3.
	| (16) If only one SNP exists, this also becomes the last SNP.
	| (17) The 3’ end site of Locus 3 is positioned at the off-set distance after the last SNP in Locus 3.

:navy:`Step 4. Locate the last sliding frame on the reference sequence.`

	.. image:: ../images/utilities/utilities_HIW_SNP_step4.png

	| 
	| (18) The first SNP *after* length minimum frame_distance plus off-set after the 3’ end site of Locus 3 becomes the first SNP of Locus 4.
	| (19) The position at distance off-set upstream of the first SNP defines the 5’ start site of Locus 4.
	| (20) If the frame_length exceeds the remaining length of the reference sequence, it is set at the last nucleotide of the reference sequence. All downstream neighboring SNPs within the frame_length minus off-set length are grouped for Locus 4.
	| (21) The position of the last SNP within the group is determined for Locus 4. The last SNP can be positioned at maximal the length of the reference sequence minus the off-set length.
	| (22) The 3’ end site of Locus 4 is positioned at the off-set distance after the last SNP.

:navy:`Step 5. Continue the process for all other reference sequences.`

:navy:`Step 6. Use the sliding frames to delineate loci for read-backed haplotyping with SMAP haplotype-sites.`

	.. image:: ../images/utilities/utilities_HIW_SNP_step6.png

:navy:`Special cases and the optimal use of parameter settings`

	| According to the following rationale, parameter settings can be optimized to cover special cases.
	| Off-set distances are used to ensure that the sequence context around the SNPs are also covered by the same read.
	| In this case, the outer 5’ and 3’ positions delineating the locus are used as ‘Anchor points’ rather than as polymorphic SNPs and are used for evaluation of complete coverage of the read across the locus length.
	| Always use option ``--partial exclude`` for SMAP haplotype-sites.
	| If the off-set is set to "0", the 5’ end site corresponds to the first SNP, and the 3’ end site of the locus corresponds to the last SNP.
	| If only one SNP exists within the maximal frame_length and off-set is set to "0", then the locus is limited to length 1 and only the single SNP is scored as haplotype.
	| If only one SNP exists within the maximal frame_length and off-set is set greater than "0", then the locus is defined by length 1 + 2 x off-set and both the single SNP and the two Anchor points are scored as haplotype.
	| SNPs positioned in the frame-distance regions are ignored.
	| If the frame_distance is set to "0", loci may become directly adjacent, but frames never overlap.
	| The minimal frame_distance is always respected.
	| Frame_length must always be set at a value greater than or equal to 1 + 2 x off-set.
	| Frame_length must always be set at a value shorter than the longest read length (ideally about one-half to two-thirds). Otherwise, reads can never entirely span the longest frame_length and are dropped by SMAP haplotype-sites.
	| Frame_length is a measure for the maximum length per locus, but the effective locus length distribution is likely smaller and depends on SNP density combined with off-set and frame_length.


Haplotyping the junction sites of large structural variants such as deletions and inversions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:navy:`Each junction is considered as its own sliding frame`


Delineating sliding frames for this application is very simple as all parameters should be fixed.

	(1)  Locus: name of the region of the reference genome that contains the junction.
	(2)  Anchor points: the start and end positions of the locus are defined as the nucleotides immediately adjacent to the junction. 
	(3)  maximal frame_length is set to "3". Each junction is considered separately, the central nucleotide is at the junction.
	(4)  minimal frame_distance is set to "0".
	(5)  off-set is set to "1": the nucleotides immediately upstream and downstream of the junction are Anchor points by definition.
	(6)  always use option ``--partial include`` for SMAP haplotype-sites.

Recommendations and troubleshooting
-----------------------------------

:navy:`Haplotyping sliding frames with adjacent SNPs`

In any situation in which neighboring SNPs are spaced apart within the length of a read, read-backed haplotyping can be used to phase SNPs. Here, we provide some recommendations for optimal parameter settings. 

Use option ``-partial exclude`` 

In case short regions of adjacent SNPs are haplotyped, only consider reads that span the entire locus. Otherwise, reads that only cover a part of the locus (by "random" shearing during library preparation and "random" read mapping start and stop positions) would create additional haplotypes marking absence of read coverage. For instance, a read could create a haplotype '000.', if it was a reference allele of which the alignment stopped just before the last nucleotide to be haplotyped, and the "." character denotes absence of read mapping. This haplotype is a technical artefact, not a biological signal. 

Use option ``-mapping_orientation ignore`` 

Because Shotgun reads may be mapped in any orientation (during Shotgun sequencing, genomic fragments are not cloned or sequenced with directionality with respect to the reference genome sequence), mode ``-mapping_orientation ignore`` should be used because then all reads are considered independent of their mapping orientation.

Use pair-aware read mapping

While the insert size of Shotgun libraries sequenced with Illumina instruments is relatively short (300-500 bp for paired-end libraries), paired-end reads (2x150 bp) usually do not overlap in the middle of the fragment and can not be merged during preprocessing. Read mapping should probably best be performed in pair-aware mode to increase specificity of mapping with `BWA-MEM <https://janis.readthedocs.io/en/latest/tools/bioinformatics/bwa/bwamem.html>`_.

Less is more

Defining sliding frames in which to group adjacent SNPs is a trade-off between read depth, read length, and the density of SNPs. 
We recommend to create a set of BED files with varying sliding frame length and test these for locus and sample call completeness and correctness, and haplotype diversity (number of different haplotypes observed per locus across the sample set).
As a rule of thumb, sliding frame length at about one-half to two-third of the read length provides an optimal balance between read depth and haplotype diversity and is a good starting point for further optimisation.

.. tabs::

   .. tab:: sliding frame length
	  
	  .. image:: ../images/utilities/sliding_frames_probe_capture_graph1.png
	  
	  | The distance between the first and the last SNP within a maximal sliding frame length determine the effective sliding frame length. So, maximal sliding frame length may be optimised per sample set in function of the SNP density. 
	  |
	  

   .. tab:: SNP density
	  
	  .. image:: ../images/utilities/sliding_frames_probe_capture_graph2.png
	  
	  | Increasing sliding frame length increases the number of neighboring SNPs included in the haplotype call.
	  |
	  
   .. tab:: completeness
	  
	  .. image:: ../images/utilities/sliding_frames_probe_capture_graph3.png
	  
	  | Increasing sliding frame length increases the number of neighboring SNPs included in the haplotype call, but it is limited by maximal read length. Maximal sliding frame length may be optimised per sample set in function of locus call completeness, which is determined by library size of the sampleset (total number of reads mapped per sample).
	  |

   .. tab:: haplotype diversity
	  
	  .. image:: ../images/utilities/sliding_frames_probe_capture_graph4.png
	  
	  | Increasing sliding frame length increases the number of neighboring SNPs included in the haplotype call, increases the number of unique haplotypes that can be created, and increases the number of different haplotypes per locus observed across a sample set.
	  
:navy:`Haplotyping the junction sites of large structural variants such as deletions and inversions`

Use option ``-partial include`` 

The basic signal that is being detected is the localised and consistent lack of continued read alignment at a junction flanking a structural variant such as a (large-scale) deletion or inversion. So, reads are expected to show partial alignment in the three nucleotides that are covered in the sliding frame. In fact, only three haplotypes classes are commonly expected: 000 (reference); 00. ; 00- ; 0.. or 0-- (upstream junctions) ..0 ; --0 ; .00 or -00 (downstream junctions). 

Use option ``-mapping_orientation ignore`` 

Because Shotgun reads may be mapped in any orientation (during Shotgun sequencing, genomic fragments are not cloned or sequenced directionally with respect to the reference genome sequence), mode ``-mapping_orientation ignore`` should be used because then all reads are considered independent of their mapping orientation.

Use single-end read mapping

While the insert size of Shotgun libraries sequenced with Illumina instruments is relatively short (300-500 bp for paired-end libraries), paired-end reads (2x150 bp) usually do not overlap in the middle of the fragment and can not be merged during preprocessing. Read mapping should probably best be performed as separate reads as large-scale rearrangements may cause large differences between the order of sequences in the reference and in the pair of reads. Thus, a larger number of reads may map onto the junctions, if each read can be placed independently of its paired read.

----
 
.. _SMAP_utilities_quickstart:
 
Quick Start
-----------

.. tabs::

   .. tab:: overview
	  
	  | The scheme below shows how **SMAP sliding frames** works downstream from variant calling and needs the VCF file with SNPs or SVs and the reference FASTA sequence as input.
	  
	  .. image:: ../images/SMAP_global_overview_sites_frames_WGS_phylo_transparent.png

   .. tab:: required input

	  .. tabs::

		 .. tab:: VCF
		 
			==================== ===== == === === ======== ====== ==== ======
			##fileformat=VCFv4.2
			-----------------------------------------------------------------
			#CHROM               POS   ID REF ALT QUAL     FILTER INFO FORMAT
			==================== ===== == === === ======== ====== ==== ======
			scaffold_10030       15623 .  G   T   68888.7  .      .    GT
			scaffold_10030       15650 .  C   T   1097.13  .      .    GT
			scaffold_10030       15655 .  A   T   1097.13  .      .    GT
			scaffold_10030       15682 .  C   G   1097.13  .      .    GT
			scaffold_10030       15689 .  T   C   1097.13  .      .    GT
			scaffold_10030       15700 .  A   C   1097.13  .      .    GT
			scaffold_10030       15704 .  G   T   1097.13  .      .    GT
			scaffold_10030       15705 .  A   C   1097.13  .      .    GT
			scaffold_10030       15733 .  C   T   45538.80 .      .    GT
			scaffold_10030       15753 .  G   C   44581.50 .      .    GT
			scaffold_10030       15769 .  C   A   64858.50 .      .    GT
			scaffold_10030       15787 .  A   C   67454.00 .      .    GT
			scaffold_10030       15796 .  A   C   45281.60 .      .    GT
			==================== ===== == === === ======== ====== ==== ======
			
			VCF file listing the 13 SNPs identified at these two loci using third-party software (see also `Veeckman et al, 2018 <https://academic.oup.com/dnaresearch/article/26/1/1/5133005>`_). In order to comply with bedtools, which generates the locus \- \ SNP overlap, a 9-column VCF format with VCFv4.2-style header is required. However, only the first 2 columns contain essential information for **SMAP haplotype-sites**, the other columns may contain data, or can be filled with \"."\.

		 .. tab:: BED file of reference sequence
		 		 
			.. image:: ../images/utilities/utilities_HIW_SNP_step4.png
			
			| A BED file with the total length per sequence in the reference genome fasta, to make sure that the maximal SMAP positions projected by frame_length and off-set parameter values are not out of range (higher coordinate positions than the maximal number of nucleotides per sequence).

----
	  
Output
------

**Tabular output**

.. tabs::

   .. tab:: BED file with sliding frames

		 By default, **SMAP utilities** will return a BED file with the coordinates of sliding frames, used for SMAP haplotype-sites. The header below is only shown here for easy reference, it is not included in the actual output BED file. 

		============= ====== ====== =================== ================== ======= =========== ============== ======== =============
		Reference     Start  End    Locus_name          Mean_read_depth    Strand  SMAPs       Completeness   nr_SMAPs Name
		============= ====== ====== =================== ================== ======= =========== ============== ======== =============
		Chr1          99     200    Chr1:100-200_+      .                  \+ \    100,200     .              2        Frame_Set1   
		Chr1          449    600    Chr1:450-600_+      .                  \+ \    450,600     .              2        Frame_Set1   
		============= ====== ====== =================== ================== ======= =========== ============== ======== =============
		


----

.. _SMAP_utilities_quickstartcommands:

  
Summary of Commands
-------------------

:navy:`Haplotyping sliding frames with adjacent SNPs`

The Python script in the **SMAP utilities** folder transforms a simple VCF-formatted list of SNPs into a BED file with sliding frames for **SMAP haplotype-sites**.

::

	python3 SMAPutil_SlidingFrames.py --bed reference_genome_Lp.bed --vcf 503TargetGenes_391Genotypes_SNPs.vcf --frame_length 10 --frame_distance 0 --offset 0 -s Set_FL10_FD0_OS0

The same VCF file is then used as input for the variant sites in **SMAP haplotype-sites**
Command examples and options of **SMAP haplotype-sites** for a range of specific sample types are given under :ref:`haplotype frequency profiles <SMAPhaplofreq>`.  

::

    smap haplotype-sites /path/to/BAM/ /path/to/BED/ /path/to/VCF/ -mapping_orientation ignore --no_indels -c 30 -f 5 -p 8 --plot_type png -partial exclude --min_distinct_haplotypes 1 -o haplotypes_FL10_FD0_OS0 --plot all --discrete_calls dosage -i diploid -z 2 --locus_correctness 80


:navy:`Haplotyping the junction sites of large structural variants such as deletions and inversions`

The Python script in the Utilities folder transforms a simple VCF-formatted list of breakpoints into a BED file for SMAP haplotype-sites with the following settings:

::

	python3 SMAPutil_SlidingFrames.py --bed reference_genome_Os.bed --vcf StructuralVar_272Genotypes_Dels.vcf --frame_length 3 --frame_distance 0 --offset 1 -s Set_FL3_FD0_OS1

The same VCF file is then used as input for the variant sites in **SMAP haplotype-sites**
Command examples and options of **SMAP haplotype-sites** for a range of specific sample types are given under :ref:`haplotype frequency profiles <SMAPhaplofreq>`.  

::

    smap haplotype-sites /path/to/BAM/ /path/to/BED/ /path/to/VCF/ -mapping_orientation ignore -partial include -c 30 -f 5 -p 8 --plot_type png --min_distinct_haplotypes 1 -o haplotypes_3bp_regions --plot all --discrete_calls dosage -i diploid -z 2 --locus_correctness 80

Options may be given in any order.


