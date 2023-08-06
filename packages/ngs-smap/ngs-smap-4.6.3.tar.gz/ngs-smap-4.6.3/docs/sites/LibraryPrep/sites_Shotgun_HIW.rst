.. raw:: html

    <style> .navy {color:navy} </style>
	
.. role:: navy

.. raw:: html

    <style> .white {color:white} </style>

.. role:: white

########################################
Shotgun sequencing
########################################

.. _SMAPhaploShotgunHIW:

Setting the stage
-----------------

In Shotgun sequencing, two types of analyses can be distinguished:

Haplotypes may be defined by a set of adjacent SNPs in a dynamic Sliding frame (start and end positions of the locus). The Sliding frames are typically defined as a region around known SNPs, polymorphic positions are scored as reference of alternative.

Alternatively, the junctions of large-scale inversions or deletions may be haplotyped by taking the read mapping breakpoint as variable position flanked by two Anchor points immediately upstream and downstream, and scoring absence/presence of read mapping.

Here, we explain the main difference and provide instructions for setting the correct parameter settings for these contrasting scenario's.

Defining the start and end point for haplotyping adjacent SNPs in Sliding frames
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In any situation in which neighboring SNPs are spaced apart within the length of a read, read-backed haplotyping can be used to phase SNPs.

.. image:: ../../images/sites/coordinates_Shotgun_SNP_short.png

Defining Sliding frames in which to group adjacent SNPs is a trade-off between read depth, read length, and the density of SNPs. We recommend to create a set of BED files with varying Sliding frame lengths and test these for locus and sample call completeness and correctness, and haplotype diversity (number of different haplotypes observed per locus across te sample set).
The Python script in the :ref:`SMAP utilities <SMAP_utilities_quickstart>` transforms a simple VCF-formatted list of SNPs into a BED file with Sliding frames for **SMAP haplotype-sites**. The same VCF file is then used as input for the variant sites in **SMAP haplotype-sites**.  As a rule of thumb, frame length at about one-half to two-thirds of the read length provides an optimal balance between read depth and haplotype diversity and is a good starting point for further optimization.

While the insert size of Shotgun libraries sequenced with Illumina instruments is relatively short (300-500 bp for paired-end libraries), paired-end reads (2x150 bp) usually do not overlap in the middle of the fragment and can not be merged during preprocessing. Read mapping should still be performed in paired mode to increase specificity of mapping with `BWA-MEM <https://janis.readthedocs.io/en/latest/tools/bioinformatics/bwa/bwamem.html>`_. Because Shotgun reads may be mapped in any orientation, mandatory argument ``-mapping_orientation ignore`` should be used to consider all reads, independent of their mapping orientation.
In case short regions of adjacent SNPs are haplotyped, it is logical to only consider reads that span the entire locus. Otherwise, reads that only cover a part of the locus would create additional haplotypes marking absence of read coverage at the first or last SMAP position. So, use the option ``-partial exclude`` to exclude all reads that do not completely span the locus. 

Defining the start and end point for haplotyping large structural variants
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: ../../images/sites/coordinates_Shotgun_SV_short.png

Short reads obtained by Shotgun sequencing may partially map onto the region directly flanking the junction of large structural variants. Typically, the MEM that seeds the alignment places the longest half of the read adjacent to the breakpoint, and the other half of the read is softclipped, or not matched to the reference genome. This results in a sudden and clear drop in read depth around the breakpoint. This read mapping profile can be coded as haplotype by SMAP, because read-reference alignments are transformed to haplotypes while considering absence/presence of read mapping. 
The approach to score clean drops in read depth at SV mapping breakpoints is to define 3-bp loci with the breakpoint nucleotide as the central position, immediately flanked by an upstream and a downstream nucleotide position and score absence/presence per position. So, use the option ``-partial include`` to intentionally haplotype reads that do not completely span the three nucleotides around the read mapping breakpoint to score the polymorphism. 

The Python script in the :ref:`SMAP utilities <SMAP_utilities_quickstart>` transforms a simple VCF-formatted list of Structural Variants' junction positions into a BED file with read mapping breakpoint positions for **SMAP haplotype-sites**. The same VCF file is then used as input for the variant sites in **SMAP haplotype-sites**.
Because Shotgun reads may be mapped in any orientation, the mandatory argument ``-mapping_orientation ignore`` should be used to consider all reads, independent of their mapping orientation.


Recognizing haplotypes
~~~~~~~~~~~~~~~~~~~~~~

The tabs below show the same locus in 3 diploid individuals. A total of 4 SNPs are found among the individuals; 4 haplotypes can clearly be defined (1 is the same as the reference sequence and 3 alternative haplotypes).
In practice, Shotgun reads map at randomly distributed start and end positions. In this sense, Shotgun read mappings do not show Stacked alignments but as long as reads cover the locus start and end Anchor points, then these reads are taken into account and SNPs in the interior sequence of the locus can all be haplotyped by read-backed haplotyping.

The reconstructed haplotype codes are shown on the right. Light blue arrows indicate locus start and end Anchor points, red arrows and characters indicate SNPs.

.. tabs::

   .. tab:: Shotgun reads, Sample 1
	  
	  .. image:: ../../images/sites/Sample1_haplo_Shotgun_SNP_60bp.png
	  
	  Although in this sample a single base deletion is present at reference position 58, it is not called as it does not coincide with a SNP or Anchor position.
	  Out of a total of 20 reads mapped, 10 reads (indicated in black) span the entire locus of 60 bp and are considered for haplotyping. Ten partially mapping reads are excluded (indicated in grey).
	  
   .. tab:: Shotgun reads, Sample 2
	  
	  .. image:: ../../images/sites/Sample2_haplo_Shotgun_SNP_60bp.png
	  
	  Out of a total of 20 reads mapped, 12 reads (indicated in black) span the entire locus of 60 bp and are considered for haplotyping. Eight partially mapping reads are excluded (indicated in grey).
   .. tab:: Shotgun reads, Sample 3
	  
	  .. image:: ../../images/sites/Sample3_haplo_Shotgun_SNP_60bp.png
	  
	  Out of a total of 20 reads mapped, 11 reads (indicated in black) span the entire locus of 60 bp and are considered for haplotyping. Nine partially mapping reads are excluded (indicated in grey).
	  
----
	  
Step 1: Combining SNPs into sets of known polymorphic sites in Sliding frames
-----------------------------------------------------------------------------

procedure
~~~~~~~~~

For Shotgun data, the user should create a custom BED file which contains Sliding frames to delineate loci for haplotyping (see :ref:`instructions here <SMAPhaploquickstart>`).
Reads not spanning these Sliding frames, as well as SNPs positioned outside these regions are not taken into account for haplotype calling.

.. image:: ../../images/sites/SMAP_haplotype_step1_Shotgun.png

| **SMAP haplotype-sites** uses `bedtools intersect <https://bedtools.readthedocs.io/en/latest/content/tools/intersect.html>`_ to select sets of SNPs from the VCF file that are located inbetween the Anchor points per locus.
| Then, a set of putatively polymorphic sites is made per locus (Sliding frame) by concatenating the locus start site, all internal SNPs, and the locus end site, all ordered by position.

:navy:`Non-polymorphic loci are not analyzed`

Shotgun loci defined in the BED file that do not contain overlapping SNPs are uninformative and are excluded from further analysis.
These loci are also not reported in the output.

----

Step 2: Calling and counting haplotypes
---------------------------------------

**Read-backed haplotyping is used to reconstruct haplotypes.**

.. image:: ../../images/sites/SMAP_haplotype_step2_Shotgun.png

procedure
~~~~~~~~~

:navy:`The following procedure is performed per sample:`

| For each locus listed in the BED file, all overlapping reads are retrieved from a BAM file.
| For each read, a haplotype string is created as follows:
| For each putatively polymorphic site (the outer Anchor points are SNPs themselves), the corresponding position in the aligned read is checked and reference/alternative/absence/gap is scored:

	========= ===========================================================================
	CALL TYPE CLASSES
	========= ===========================================================================
	.         absence of read mapping (indicating partially aligned read)
	0         presence of the reference nucleotide
	1         presence of an alternative nucleotide (any nucleotide different from the reference)
	\- \      presence of a gap in the alignment
	========= ===========================================================================
	
Deletions (\-\) are only scored when they overlap with SNP positions, these are not considered as polymorphic positions. Likewise, insertions are not considered polymorphic positions, and moreover these are not called. In Shotgun-data, InDels do not modify the start and end points of read mapping like in :ref:`GBS data <SMAPdelsepvmerg>`, as loci are defined by the SNPs in the VCF file.

**The concatenated string of \`.01-´ \ scores then defines the haplotype per read.** Any haplotype that contains a "." character is removed, as these are derived from partially aligned reads.

| In principle, this procedure allows to detect any linear combination of SNPs (*i.e.* haplotype) per locus, but only experimentally observed haplotypes are recorded. 
| **SMAP haplotype-sites** reconstructs this haplotype string for each read, and counts the number of reads per haplotype per sample. Next, the sum of all read counts per retained haplotype per locus is calculated (total locus read count per sample), filtered for minimal read count per locus (option ``-c``), and all information is stored in a table per sample.

.. image:: ../../images/sites/SMAP_haplotype_step3_Shotgun.png

.. _SMAPhaploASpartialShotgun:

filters
~~~~~~~

:navy:`loci with low read count are removed from the dataset with a read count threshold (option` ``-c``:navy:`)`

Accurate haplotype frequency estimation requires a minimum read count which is different between sample type (individuals and Pool-Seq) and ploidy levels.

The user is advised to use the read count threshold to ensure that the reported haplotype frequencies per locus are indeed based on sufficient read data. If a locus has a total haplotype count below the user-defined minimal read count threshold (option ``-c``; default 0, recommended 10 for diploid individuals, 20 for tetraploid individuals, and 30 for pools) then all haplotype observations are removed for that sample. For more information, see :ref:`recommendations on minimal read depth <SMAPRecommendTroubleSites_RD_filter>`.

:navy:`Haplotypes with gaps on one of the polymorphic sites can be removed from the dataset (option` ``--no_indels``:navy:`)`

In some cases, gaps in the alignment (putatively caused by InDels) may overlap with SNP sites in individual reads. The option ``--no_indels`` filters out any haplotypes that contain \`-´ \ characters in their haplotype string, and recalculates the total read count per locus.

:navy:`Using the option` ``-partial exclude`` :navy:`for Shotgun data`

| Haplotypes are extracted from HiPlex, Shotgun, and GBS data using the same principles of read-backed haplotyping. This means that the same algorithm for haplotype calling and haplotype frequency counting can be used, but with specific options and BED files per library preparation method. Because for haplotyping in Sliding frames, mapped Shotgun reads are expected to span the entire length of the locus, we recommend to remove reads that are partially aligned by using the option ``-partial exclude``.


:navy:`Partially overlapping Sliding frames for Shotgun data`

| Shotgun data may be analysed with partially overlapping Sliding frames, although the haplotypes created in this way also contain partially redundant genetic diversity information, because SNP positions are evaluated several times, and reads may also be used multiple times for haplotyping neighboring regions.

.. image:: ../../images/sites/Sample1_haplo_Shotgun_SNP_overlappingFrames.png

**SMAP haplotype-sites** evaluates all reads that overlap with at least a single nucleotide at a given locus. For Shotgun data analysis in Sliding frame mode, where option ``-partial exclude`` should be used, **SMAP haplotype-sites** first evaluates if a read spans the *entire* length of the locus to which it is mapped. See scheme above. For locus_1, only the reads that align entirely across the Sliding frame are scored for SNPs 39, 71, and 76, while reads with only partial alignment to the Sliding frame of locus_1, are ignored. Conversely, only the reads that align entirely to the Sliding frame of locus_2 are scored for SNPs 71, 76, and 98, while reads with partial alignment to locus_2 are ignored. The option ``-partial exclude`` thus evaluates each read per locus but does not attempt to extend the sets of neighboring SNP sites beyond the reach of reads.


:navy:`Non-overlapping Sliding frames for Shotgun data`

| Shotgun data may also be analysed with non-overlapping Sliding frames, to avoid creating haplotypes with redundant genetic diversity information. Reads may still be used multiple times for haplotyping neighboring regions, as long as they span the *entire* locus of interest.

.. image:: ../../images/sites/Sample1_haplo_Shotgun_SNP_non-overlappingFrames_40bp.png

Loci are defined by starting at the first SNP (39) of a reference sequence and looking for neighboring SNPs within a frame of maximal length (40bp in this scheme). The locus ends at the last SNP observed within that maximum frame (locus_1, SNP 76)), and a new frame starts at the next downstream SNP (98). If no neighboring SNP is located within the maximum frame length, the frame is limited to a single SNP and the locus has length of 1bp (locus_2, SNP 98). **SMAP haplotype-sites** overlaps the loci with the VCF file, recognises that SNP 71 overlaps with locus_1 and cobines that position together with 39 and 76 for haplotyping. **SMAP haplotype-sites** then evaluates all reads that overlap with at least a single nucleotide at a given locus. For Shotgun data analysis in Sliding frame mode, where option ``-partial exclude`` should be used, **SMAP haplotype-sites** first evaluates if a read spans the *entire* length of the locus to which it is mapped. See scheme above. For locus_1, only the reads that align entirely across the Sliding frame are scored for SNPs 39, 71, and 76, while reads with only partial alignment to the Sliding frame of locus_1, are ignored. Conversely, any read that aligns to the single SNP in the Sliding frame of locus_2 (SNP 98) are scored. The option ``-partial exclude`` thus evaluates each read per locus but does not attempt to extend the sets of neighboring SNP sites beyond the reach of reads by setting a maximum Sliding frame length during locus delineation.
