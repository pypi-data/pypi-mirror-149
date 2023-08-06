.. raw:: html

    <style> .navy {color:navy} </style>
	
.. role:: navy

.. raw:: html

    <style> .white {color:white} </style>

.. role:: white

############################
Genotyping-By-Sequencing
############################

.. _SMAPhaploGBSHIW:

Setting the stage
-----------------

.. admonition:: Core

	**Haplotypes are defined by SMAPs and SNPs.**

Type of library determines the shape of Stacks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

While GBS generally creates \`stacks´ \of reads after reference mapping, the exact shape of the Stacks depends on the type of sequencing data (single-end, paired-end, or merged reads).

.. tabs::

   .. tab:: GBS separate reads
	  
	  .. tabs::

		 .. tab:: GBS single-end
	  
			.. image:: ../../images/sites/A_GBS-SE.png
			
			| Single-end GBS reads are derived from individual molecules. If NGS read length is shorter than the PCR-amplified GBS fragment length (distance between two neighboring restriction sites (RE)), then that individual molecule is only partially sequenced (black arrows).
			| **SMAP haplotype-sites** only constructs haplotypes that are backed by actual, individual reads.

			| Without imputation, no information is available about the phase of potential SNPs in the non-sequenced part of the same molecule (grey lines). While single-end GBS reads mapped on opposite strands may cover a common region in the middle of the fragment, such reads can never be derived from the same molecule, and should thus be counted as individual allele observations.
			| **SMAP haplotype-sites** accounts for this by considering strandedness of read mapping for single-end GBS (see also tab :ref:`single-end reads <SMAPdelHIW>`).
			| **SMAP haplotype-sites** applied to single-end reads, therefore, creates two independent stacks; one for each strand, to cover the left-hand side of a fragment and the right-hand side of a fragment, as reads are aligned (anchored) to the RE recognition sites on the outer borders of the fragment.

			| In single-enzyme GBS, single-end sequencing leads to an equal proportion of \+ \ strand and \- \ strand mapped reads.
			| In double-enzyme GBS, single-end sequencing typically leads to exclusive mapping in one orientation, *i.e.* on one of both strands.
			| **SMAP haplotype-sites** works for any (combination of) enzyme, and needs no prior information on the enzyme, nor on the position of restriction enzyme recognition sites in the reference genome.
			| **SMAP haplotype-sites** should be used in ``-mapping_orientation stranded`` mode for analysis of single-end reads.
			
		 .. tab:: GBS paired-end
	  
			.. image:: ../../images/sites/A_GBS-PE.png
			
			| Paired-end GBS reads are derived from two sides of an individual molecule. If NGS read length is longer than half of the PCR-amplified GBS fragment length (distance between two neighboring restriction sites (RE)), then those reads overlap at least partially in the middle of the GBS fragment. If reads are not merged prior to read mapping, it is best to run **SMAP** as if the reads were derived from single-end read data.
			| **SMAP haplotype-sites** strictly considers SNPs in the same read for Read-Backed haplotyping.

			| In single-enzyme GBS, reads map in equal proportions to the \+ \ strand and the \- \ strand.
			| In double-enzyme GBS, sequencing typically leads to exclusive mapping in one orientation, *i.e.* on one of both strands.
			| Because most paired-end reads will overlap in the middle region of the GBS PCR-fragment, and information from both sequencing orientations is available, the choice of enzyme (combination) is not relevant for paired-end read mapping.
			| **SMAP haplotype-sites** works for any (combination of) enzyme, and needs no prior information on the enzyme, nor on the position of restriction enzyme recognition sites in the reference genome.

			| Because most paired-end reads will overlap in the middle region of the GBS PCR-fragment, there is positional overlap between \+ \ strand mapped reads and \- \ strand mapped reads, but the reads themselves do not span the entire GBS-fragment. This means that per read, there is still a non-sequenced portion of the fragment in which SNPs can not be phased using Read-Backed haplotyping.
			| **SMAP haplotype-sites** uses strandedness of mapping for paired-end reads, just like for single-end reads, in order to create haplotypes that match the length of the individual reads.

			| Paired-end mapped GBS reads have the advantage (compared to merged reads) of showing more features causing polymorphic Stack Mapping Anchor Points (SMAPs, see :ref:`Polymorphisms <SMAPdelsepvmerg>` affect the shape of Stacks).
			| Paired-end mapped GBS reads have the disadvantage (compared to merged reads) of shorter haplotype length, and that per locus, two partially overlapping Stacks are created that carry partially redundant genetic information (via SNPs located in the overlap region), thus potentially artificially inflating the number of molecular markers.
			| **SMAP haplotype-sites** should be used in ``-mapping_orientation stranded`` mode for analysis of paired-end reads that are not merged prior to mapping.

   .. tab:: GBS merged reads
	  
	  .. image:: ../../images/sites/A_GBS-PE_merged.png
	  
	  | Paired-end GBS reads are derived from two sides of an individual molecule. If NGS read length is longer than half of the PCR-amplified GBS fragment length (distance between two neighboring restriction sites (RE)), then those reads overlap at least partially in the middle of the GBS fragment. In this case, both reads cover a common sequence of the same molecule and the reads can be merged (by e.g. `PEAR <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3933873/>`_), to reduce redundancy of read count, and to create a long sequence spanning the entire GBS fragment from RE to RE.
	  | **SMAP haplotype-sites** strictly considers SNPs in the same molecule for Read-Backed haplotyping.

	  | In single-enzyme GBS, reads map in equal proportions to the \+ \ strand and the \- \ strand.
	  | In double-enzyme GBS, sequencing typically leads to exclusive mapping in one orientation, *i.e.* on one of both strands.
	  | Merging paired-end read data generates a sequence that spans the entire length of the GBS-fragment (between two neighboring RE’s).
	  | Because the mapped sequence will span from RE to RE, the strandedness of the mapping does not influence which part of the fragment is covered by read information (as is the case for single-end sequencing). This means that single-enzyme or double-enzyme GBS both yield sequence reads that span the entire fragment, and all reads can be considered as a single Stack per genomic locus.
	  | See the documentation on :ref:`SMAP delineate <SMAPdelHIW>` for further explanation on how to define the start and end points per locus before running **SMAP haplotype-sites**.

	  | **SMAP haplotype-sites** works for any (combination of) enzyme, and needs no prior information on the enzyme, nor on the position of restriction enzyme recognition sites in the reference genome.
	  | **SMAP haplotype-sites** should be run in ``-mapping_orientation ignore`` mode for analysis of merged paired-end reads.
	  | **SMAP haplotype-sites** will not consider strandedness of mapping for merged paired-end reads. 
	  | Compared to single-end GBS reads, paired-end merged reads lead to a single non-redundant observation of allele frequency per locus, with the maximum read count across the length of the fragment.
	  | If paired-end reads are merged before mapping, this creates longer haplotypes compared to single-end reads, and does not need imputation or phase extension.


Recognizing haplotypes
~~~~~~~~~~~~~~~~~~~~~~

Tabs below show GBS-SE read alignments of five heterozygous diploid individuals.

A single GBS locus is shown flanked by two *Pst*\I \ sites (grey boxes). Only forward mapping reads of a single :ref:`MergedCluster <SMAPdeldef>` are shown.
Reverse mapping reads aligning to the right hand side of the GBS fragment exist and form a second MergedCluster, but are not shown here for clarity. The haplotype frequencies of the second MergedCluster are shown on the sample type pages in the :ref:`data tables <SMAPhaplofilter>` illustrating the filtering procedures.
As illustrated in :ref:`SMAP delineate <SMAPdeldef>`, InDels and soft clipping potentially cause polymorphisms in the alignment on the \5´ \ or \3´ \ end of mapped reads, thus creating SMAPs (light blue arrows on top of the reference sequence). A MergedCluster is defined by the outermost SMAP positions (15618 \- \15711 bp).

Recognizing **SNPs** by variant calling software typically depends on \`reading´ \ an alignment **from top to bottom** at individual nucleotide positions. For instance, comparing all reads aligned at position 15623 leads to the identification of the C/T SNP. Each SNP is called independently from the neighboring SNPs. A total of 8 SNPs occur across the MergedCluster region (purple arrows on the reference sequence). Some SNPs are located in a region that is only covered by one of the two alleles in these heterozygous diploid individuals (at 15704 and 15705 bp in Sample 4). Classical SNP calling would call these positions as homozygous in sample 4, because there is only one observed type of read at that position.

In sharp contrast, recognizing haplotypes requires to \`read´ \ alignments from left to right, *i.e.* to combine the neighboring SMAPs and SNPs into a string of connected polymorphisms (named the **haplotype**). While all individuals shown here are heterozygous for some SNPs and homozygous for other SNPs, each individual is clearly heterozygous at the locus in the sense that each individual carries two different haplotypes. A total of six distinct haplotypes exist across the sample set. The reconstructed haplotype codes are shown on the right. Light blue arrows and characters indicate SMAPs, purple arrows and characters indicate SNPs. More information on haplotype calling is found below the tabs.


.. tabs::

   .. tab:: GBS single-end reads, Sample 1
	  
	  .. image:: ../../images/sites/scaffold_10030_Sample1_haplo_new.png

   .. tab:: GBS single-end reads, Sample 2
	  
	  .. image:: ../../images/sites/scaffold_10030_Sample2_haplo_new.png
	  
   .. tab:: GBS single-end reads, Sample 3
	  
	  .. image:: ../../images/sites/scaffold_10030_Sample3_haplo_new.png
	  
   .. tab:: GBS single-end reads, Sample 4
	  
	  .. image:: ../../images/sites/scaffold_10030_Sample4_haplo_new.png
	  
   .. tab:: GBS single-end reads, Sample 5
	  
	  .. image:: ../../images/sites/scaffold_10030_Sample5_haplo_new.png
	  
----
	  
Step 1: Combining SMAP and SNP positions into sets of known polymorphic sites
-----------------------------------------------------------------------------

procedure
~~~~~~~~~

:navy:`Defining SNPs in MergedClusters`

The first step of **SMAP haplotype-sites** is to intersect a BED file with MergedClusters obtained from :ref:`SMAP delineate <SMAPdelHIW>`, with a `VCF <https://samtools.github.io/hts-specs/VCFv4.2.pdf>`_ file that lists all SNP positions across the sample set.

.. image:: ../../images/sites/SMAP_haplotype_step1_GBS.png

| **SMAP haplotype-sites** uses `bedtools intersect <https://bedtools.readthedocs.io/en/latest/content/tools/intersect.html>`_ to select SNPs from the VCF file that are located within the MergedCluster regions.
| Then, a set of putatively polymorphic sites is made per MergedCluster by concatenating all SMAPs and SNPs, ordered by position.
| The user should run :ref:`SMAP delineate <SMAPdelHIW>` and **SMAP haplotype-sites** on the same set of BAM files to make sure that reconstruction of haplotypes is targeted to pre-selected high-quality MergedCluster loci. The outermost start and end positions of a given MergedCluster are listed in the BED file obtained from :ref:`SMAP delineate <SMAPdelHIW>`. These define regions in the reference genome in which reads from multiple samples overlap. Within this region, internal SMAP positions delineate polymorphic read mapping regions. These regions may further contain SNPs.

filters
~~~~~~~

:navy:`MergedClusters determine the loci of interest, other SNPs are excluded from analysis`

Any SNPs identified by third party software but located outside the MergedClusters identified by :ref:`SMAP delineate <SMAPdelHIW>` are excluded from further analysis. The rationale is that such SNPs may be derived from irregular read mapping stuctures or are incompletely covered across the sample set. Because the delineation of MergedClusters is entirely data-driven and does not depend on *in silico* prediction of positions of restriction sites in the reference genome, the selection of informative loci is inherently focussed on the actual location of mapped reads at nucleotide precision.

:navy:`Non-polymorphic loci are not analyzed`

Any MergedCluster that contains at least 3 SMAP sites contains polymorphisms that can be used as genetic markers. In addition, any MergedCluster that contains 2 SMAPs (identical start and end of read mapping across all samples) and overlaps with at least one SNP can also be converted into polymorphic haplotypes. MergedClusters with maximum 2 SMAPs and no overlapping SNPs, will contain read data but no polymorphism. Hence, the latter class is uninformative and excluded from further analysis.

----

.. _SMAPhaploGBSHIW2:

Step 2: Calling and counting haplotypes
---------------------------------------

**Read-backed haplotyping is used to reconstruct haplotypes at SMAP and SNP sites.**

.. image:: ../../images/sites/SMAP_haplotype_step2.png

procedure
~~~~~~~~~

Recall that **SMAP delineate** was used to define which regions of the genome contain a minimum number of reads in enough samples (see :ref:`filter criteria in SMAP delineate <SMAPdelfilter>`). This positional information is summarized in the **SMAP delineate** BED file as MergedClusters. **SMAP haplotype-sites**, therefore, simply needs to call haplotypes for all reads overlapping with each MergedCluster from each BAM file.

:navy:`The following procedure is performed per sample:`

| For each MergedCluster, all overlapping reads are retrieved from a BAM file.
| For each read, a haplotype string is created as follows:
| For each polymorphic site, the corresponding position in the aligned read is checked for absence/presence and reference/alternative/gap is scored:

	========= ===========================================================================
	CALL TYPE CLASSES
	========= ===========================================================================
	.         absence of read mapping
	0         presence of the reference nucleotide
	1         presence of an alternative nucleotide (any nucleotide different from the reference)
	\- \      presence of a gap in the alignment
	========= ===========================================================================
	
Because the algorithm only considers SMAP positions captured in the BEDfile and SNP positions captured in the VCF file, by default deletions (\-\) are only scored when they overlap with SMAP or SNP-positions, these are not considered as polymorphic positions. Likewise insertions are not considered polymorphic positions, and moreover these are not called. However InDels are indirectly called as SMAP-positions captured by :ref:`SMAP-delineate <SMAPdelsepvmerg>`, except in the rare case where a combination of InDels results in a 0 net read length difference and no deletion occurs on a SNP/SMAP position. 

**The concatenated string of \`.01-´ \ scores then defines the haplotype per read.**

| In principle, this procedure allows to detect any linear combination of SMAPs and SNPs (*i.e.* haplotype) per MergedCluster, but only experimentally observed haplotypes are recorded. 
| **SMAP haplotype-sites** reconstructs this haplotype string for each read, and counts the number of reads per haplotype per sample. Next, the sum of all read counts per haplotype per MergedCluster is calculated (total MergedCluster read count per sample) filtered for minimal read count per locus (option ``-c``), and all information is stored in a table per sample.

.. image:: ../../images/sites/SMAP_haplotype_step3.png

.. _SMAPhaploGBSpartial:

filters
~~~~~~~

:navy:`loci with low read count are removed from the dataset with a read count threshold (option` ``-c``:navy:`)`

Accurate haplotype frequency estimation requires a minimum read count which is different between sample type (individuals and Pool-Seq) and ploidy levels.

The user is advised to use the read count threshold to ensure that the reported haplotype frequencies per locus are indeed based on sufficient read data. If a locus has a total haplotype count below the user-defined minimal read count threshold (option ``-c``; default 0, recommended 10 for diploid individuals, 20 for tetraploid individuals, and 30 for pools) then all haplotype observations are removed for that sample. For more information see section on recommendations.

:navy:`haplotypes with gaps on one of the polymorphic positions can be removed from the dataset (option` ``--no_indels``:navy:`)`

In some cases, gaps in the alignment (putatively caused by InDels) may overlap with SMAP or SNP sites in individual reads. The option ``--no_indels`` filters out any haplotypes that contain \`-´ \ characters in their haplotype string, and recalculates the total read count per locus.

:navy:`Why you must use the option` ``-partial include`` :navy:`for GBS data`

| Haplotypes are extracted from GBS and HiPlex data using the same principles of read-backed haplotyping. This means that the same algorithm for haplotype calling and haplotype frequency counting are used. However, specific options and BED files should be used to account for differences in library preparation and read mapping in GBS and HiPlex data.
| :ref:`SMAP delineate <SMAPdeldef>` explains why alternative Read Mapping Anchor Points exist specifically in GBS data, and consequently why reads are expected to display only partial alignment to a given MergedCluster with more than 2 SMAPs. The actual presence/absence of a read at any of the SMAP positions in the BAM alignment, captures this read mapping polymorphism and turns it into a molecular marker (namely the **.** symbol) as part of the '.01-' character string in the haplotype. It is therefore mandatory to use the option ``-partial include`` in order to capture alternative read mappings as molecular markers in GBS data. A reminder of how read mapping polymorphisms are formed can be found :ref:`here <SMAPdelsepvmerg>`.

