.. raw:: html

    <style> .navy {color:navy} </style>
	
.. role:: navy

.. raw:: html

    <style> .white {color:white} </style>

.. role:: white

############################
How It Works
############################

.. _SMAPdelHIW:


| The **SMAP-package** was created to resolve a paradox in genotype calling using \`Stacked´ \ Genotyping-By-Sequencing reads mapped onto a reference genome sequence.  
| The paradox is that GBS reads mapped onto a reference genome sequence are used to identify genetic polymorphisms (SNPs and/or InDels) as molecular markers, yet :ref:`SNPs and InDels themselves define how and where reads map onto the reference genome sequence <SMAPdelsepvmerg>`, and thus influence their own detection and genotype calling.
| Read-backed haplotyping requires the definition of the start and end point of loci to bundle sets of polymorphic \`Sites´ \ into a string of phased markers. Again, SNPs and InDels themselves define which regions on the reference genome sequence are covered by reads, and thus influence the start and end point of their own loci.

The **SMAP-package** resolves this paradox by:

	1)	recognizing that read mapping polymorphisms exist.
	#)	systematically positioning read mapping polymorphisms in a coordinate system of Stack Mapping Anchor Points (SMAPs) that mark the start and end points of loci covered by reads. This step is called *Delineation of loci*, and is performed by **SMAP delineate**. 
	
	#)	using the read mapping polymorphism itself as a novel type of molecular marker for haplotype calling, based on the read-reference alignment and read-backed phasing.

| Here, we will describe the first two steps (recognizing and systematically positioning SMAPs), while the third step (haplotype calling), is performed by the component :ref:`SMAP haplotype-sites <SMAPhaploHIWindex>`.

| The main goal of **SMAP delineate** is to analyze GBS read mapping distributions across sample sets for: 

	1)	fast Quality Control of read preprocessing and mapping procedures before SNP calling.

	#)	to select loci relevant for haplotyping. For this purpose, **SMAP delineate** creates a BED file with SMAP positions per locus that can subsequently be used for :ref:`read-backed haplotyping using SMAP haplotype-sites <SMAPhaploHIWindex>`.


----

Delineating Stacks in different types of GBS libraries
------------------------------------------------------

The procedure to delineate Stack Mapping Anchor Points (SMAPs) in GBS loci depends on the type of sequencing data (separately mapped reads (single-end, paired-end), or merged reads) and the type of GBS library (single-enzyme GBS or double-enzyme GBS).

Below, we explain the principles underlying **SMAP delineate** applied to these different GBS scenarios, and illustrate how to recognize and position read mapping polymorphisms.
The section :ref:`Feature description <SMAPdelsepvmerg>` provides full details on the different reasons why polymorphisms (SNPs and Indels) give rise to alternative mapping positions of merged reads, compared to a reference read allele obtained by GBS.


.. tabs::

   .. tab:: schematic overview

	  .. tabs::

		 .. tab:: Single-enzyme GBS  

			.. image:: ../images/delineate/SD_HIW_overview.png

			| 
			| In single-enzyme GBS, both ends of a given genomic fragment contain the same \`sticky end´ \(restriction digest overhang). As a consequence, the i5 and i7 Illumina adapters have equal chance to ligate to either end of the fragment. This means that individual copies of the same locus may become ligated in the forward or in the reverse orientation with respect to the i5 or i7 adapters and their corresponding reads may map either onto the \+ \strand or the \- \strand of the reference genome sequence. :ref:`This section <SMAPdelstrand>` explains further why the strandedness of the mapping is relevant for delineation of read mapping polymorphisms in separately mapped reads, but not in merged reads.
			| Separately mapped reads usually span the genomic fragment only partially; from one RE to somewhere internal to the GBS fragment (\`open-ended´\). In contrast, merged reads usually span the genomic fragment from RE to RE (\`closed-ended´\).

		 .. tab:: Double-enzyme GBS  

			.. image:: ../images/delineate/DD_HIW_overview.png

			| 
			| In double-enzyme GBS, the two ends of a given genomic fragment contain different \`sticky ends´ \(restriction digest overhang). As a consequence, the i5 and i7 Illumina adapters can only be ligated to specific ends of the fragment and there is directionality in ligating the i5 or i7 adapters to the respective ends. This means that i7 and i5 sequenced reads will consistently map onto one of both strands of the reference genome sequence. :ref:`This section <SMAPdelstrand>` explains further why the strandedness of the mapping is relevant for delineation of mapping polymorphisms in separately mapped reads, but not in merged reads. 
			| Separately mapped reads usually span the genomic fragment only partially; from one RE to somewhere internal to the GBS fragment (\`open-ended´\). In contrast, merged reads usually span the genomic fragment from RE to RE (\`closed-ended´\).

   .. tab:: single-end reads


	  .. tabs::

		 .. tab:: Single-enzyme GBS  
			
			.. image:: ../images/delineate/separately_SE_SD-GBS_SMAP_legend_2.png

			| 
			| If genomic DNA is digested with a single enzyme, both ends of the resulting fragments contain the same sticky ends. As a consequence, the i5 and i7 Illumina adapters have equal chance to ligate to either end of the fragment.
			| So, there is no directionality of the fragment orientation with respect to the GBS adapter orientation.
			| After PCR amplification of GBS libraries, single-end GBS reads are derived from individual molecules.
			| In single-end sequencing, the i5 sequencing primer is used to create the forward read (i5, purple arrows). See also `Single-enzyme GBS library construction and preprocessing <https://gbprocess.readthedocs.io/en/latest/gbs_data_processing.html>`_.  
			| 
			| Because genomic inserts are not directionally ligated to the Illumina adapters, half of the \`forward´ \reads originate from the upstream region of the fragment and the other half originate from the downstream region of the fragment. After `BWA-MEM <http://bio-bwa.sourceforge.net/bwa.shtml>`_ mapping to the reference genome, this manifests as half of the \`forward´ \reads mapping in the \+ \strand orientation, and the other half of the \`forward´ \ reads mapping in the \- \strand orientation.  
			| 
			| If NGS read length is shorter than the PCR-amplified GBS fragment length (distance between two neighboring restriction enzyme sites (RE1)), then that individual molecule is only partially sequenced (region covered by purple arrows). While single-end GBS reads mapped on opposite strands may cover a common region in the middle of the fragment, such reads can never originate from the same molecule, and should thus be counted as individual haplotype observations in **SMAP haplotype-sites**.

			| **SMAP delineate** accounts for this by considering :ref:`strandedness <SMAPdelstrand>` of read mapping for separately mapped single-end GBS reads, thus creating two independent Stacks per locus.  
			| **SMAP delineate** works for any enzyme and needs no prior information on the enzyme, nor on the position of restriction enzyme recognition sites in the reference genome sequence.  
			| **SMAP delineate** should be used in ``-mapping_orientation stranded`` mode for analysis of single-end reads (to create strand-aware Stacks).  

		 .. tab:: Double-enzyme GBS  

			.. image:: ../images/delineate/separately_SE_DD-GBS_SMAP_legend_2.png

			| 
			| If genomic DNA is digested with two enzymes, the two ends of the resulting fragments contain different sticky ends. As a consequence, the i5 and i7 Illumina adapters can only be ligated to specific ends of the fragment.  
			| So, in double-enzyme GBS, fragment-adapter directionality dictates that each fragment is sequenced in the same orientation so that single-end sequencing typically leads to exclusive mapping of all forward (i5) reads on one of both strands per fragment. All reads are inherently anchored to the restriction site associated with the forward (i5) barcoded sequencing adapter. See also `Double-enzyme GBS library construction and preprocessing <https://gbprocess.readthedocs.io/en/latest/gbs_data_processing.html>`_. Although using strandedness is less critical in double-enzyme GBS compared to single-enzyme GBS, it may help to remove spurious reads and avoid irrelevant SMAPs.
			
			| **SMAP delineate** works for any combination of enzymes and needs no prior information on the enzymes, nor on the position of restriction enzyme recognition sites in the reference genome sequence.
			| **SMAP delineate** should be used in ``-mapping_orientation stranded`` mode for analysis of single-end reads (to create strand-aware Stacks).

   .. tab:: separately mapped paired-end reads


	  .. tabs::

		 .. tab:: Single-enzyme GBS
		 
			.. image:: ../images/delineate/separately_PE_SD-GBS_SMAP_legend_2.png

			| 
			| If genomic DNA is digested with a single enzyme, both ends of the resulting fragments contain the same sticky ends. As a consequence, the i5 and i7 Illumina adapters have equal chance to ligate to either end of the fragment. So, there is no directionality of the fragment orientation with respect to the GBS adapter orientation. Paired-end GBS reads (forward reads, purple arrows; reverse reads, orange arrows) are derived from two sides of an individual molecule. 
			| Because genomic inserts are not directionally ligated to the Illumina adapters, half of the \`forward´ \reads originate from the upstream region of the fragment and the other half originate from the downstream region of the fragment. Conversely, half of the \`reverse´ \reads originate from the upstream region of the fragment and the other half originate from the downstream region of the fragment.

			| If NGS read length is longer than half of the PCR-amplified GBS fragment length, then those reads overlap at least partially in the middle of the GBS fragment.
			| So, while there is positional overlap between \+ \strand mapped reads and \- \strand mapped reads, the reads themselves do not span the entire GBS-fragment. This means that *per read*, there is still a non-sequenced portion of the fragment in which SNPs can not be phased using read-backed haplotyping.
			| **SMAP delineate**, therefore, uses :ref:`strandedness <SMAPdelstrand>` of mapping for separately mapped paired-end reads, just like for single-end reads, to create independent Stacks of reads and to ensure that haplotyping matches the length of individual reads.

			| Separately mapped paired-end GBS reads have the advantage (compared to merged reads) of showing more features causing polymorphic Stack Mapping Anchor Points (:ref:`SMAPs <SMAPdeldef>`, see :ref:`Polymorphisms affect the shape of Stacks <SMAPdelsepvmerg>`).
			| Separately mapped paired-end GBS reads have the disadvantage (compared to merged reads) of shorter haplotype length, and that per locus two partially overlapping Stacks are created that carry partially redundant genetic information (via SNPs located in the overlap region), thus potentially artificially inflating the number of molecular markers.
			| 
			| **SMAP delineate** works for any combination of enzymes and needs no prior information on the enzymes, nor on the position of restriction enzyme recognition sites in the reference genome sequence.
			| **SMAP delineate** should be used in ``-mapping_orientation stranded`` mode for analysis of separately mapped paired-end reads that are not merged.
			| The rationale to merge or not to merge is further described in :ref:`this section <SMAPdelmergeornot>` under the Example data analyses.


		 .. tab:: Double-enzyme GBS
		 
			.. image:: ../images/delineate/separately_PE_DD-GBS_SMAP_legend_2.png

			| 
			| If genomic DNA is digested with two enzymes, the two ends of the resulting fragments contain different sticky ends. As a consequence, the i5 and i7 Illumina adapters can only be ligated to specific ends of the fragment. In double-enzyme GBS, sequencing typically leads to exclusive mapping in one orientation, *i.e.* on one of both strands.

			| Because most paired-end reads will overlap in the middle region of the GBS PCR-fragment, there is positional overlap between \+ \strand mapped reads and \- \strand mapped reads, but the reads themselves do not span the entire GBS-fragment. This means that *per read*, there is still a non-sequenced portion of the fragment in which SNPs can not be phased using Read-Backed haplotyping.
			| **SMAP delineate** uses :ref:`strandedness <SMAPdelstrand>` of mapping for separately mapped paired-end reads, just like for single-end reads, in order to create haplotypes that match the length of the individual reads.

			| Paired-end mapped GBS reads have the advantage (compared to merged reads) of showing more features causing polymorphic Stack Mapping Anchor Points (:ref:`SMAPs <SMAPdeldef>`, see :ref:`Polymorphisms affect the shape of Stacks <SMAPdelsepvmerg>`).
			| Paired-end mapped GBS reads have the disadvantage (compared to merged reads) of shorter haplotype length, and that per locus, two partially overlapping Stacks are created that carry partially redundant genetic information (via SNPs located in the overlap region), thus potentially artificially inflating the number of molecular markers.
			| 
			| **SMAP delineate** works for any combination of enzymes and needs no prior information on the enzyme, nor on the position of restriction enzyme recognition sites in the reference genome sequence.
			| **SMAP delineate** should be used in ``-mapping_orientation stranded`` mode for analysis of separately mapped paired-end reads that are not merged.

   .. tab:: merged reads


	  .. tabs::

		 .. tab:: Single-enzyme GBS
		 
			.. image:: ../images/delineate/merged_PE_SD-GBS_SMAP_legend_2.png

			| 
			| Paired-end GBS reads are derived from two sides of an individual molecule. If NGS read length is longer than half of the PCR-amplified GBS fragment length (distance between two neighboring restriction enzyme sites (RE)), then those reads overlap at least partially in the middle of the GBS fragment. In this case, both reads cover sequence of the same molecule and the reads should be merged (by e.g. `PEAR <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3933873/>`_), to reduce redundancy of read depth, and to create a long sequence spanning the entire GBS fragment from RE1 to RE1.

			| In single-enzyme GBS, reads map in equal proportions to the \+ \strand and the \- \strand.
			| **SMAP haplotype-sites** strictly considers SNPs in the same molecule (read) for Read-Backed haplotyping. Because the mapped sequence will span from RE1 to the neighboring RE1, the strandedness of the mapping does not influence which part of the fragment is covered by read information (as is the case for single-end sequencing). This means that all reads can be considered as a single Stack per genomic locus.

			| **SMAP delineate** works for any enzyme and needs no prior information on the enzyme, nor on the position of restriction enzyme recognition sites in the reference genome. 
			| **SMAP delineate** does not need to consider strandedness of mapping for merged paired-end reads. Compared to single-end GBS reads, paired-end merged reads lead to a single non-redundant observation of allele frequency per locus, with the maximum read depth across the length of the fragment.
			| **SMAP delineate** recommends merging of paired-end reads before mapping to create longer haplotypes compared to separately mapped paired-end reads.
			| **SMAP delineate** should be used in ``-mapping_orientation ignore`` mode for analysis of merged paired-end reads.
			| The rationale to merge or not to merge is described further in :ref:`this section <SMAPdelmergeornot>` under the Example data analyses.

		 .. tab:: Double-enzyme GBS

			.. image:: ../images/delineate/merged_PE_DD-GBS_SMAP_legend_2.png

			| 
			| In double-enzyme GBS, sequencing typically leads to exclusive mapping in one orientation, *i.e.* on one of both strands.
			| Merging paired-end read data generates a sequence that spans the entire length of the GBS-fragment (between two neighboring RE’s).
			| Because the mapped sequence will span from RE1 to RE2, the strandedness of the mapping does not influence which part of the fragment is covered by read information (as is the case for single-end sequencing). This means that single-enzyme or double-enzyme GBS both yield sequence data that span the entire fragment, and all reads can be considered as a single Stack per genomic locus.

			| **SMAP delineate** works for any combination of enzymes and needs no prior information on the enzymes, nor on the position of restriction enzyme recognition sites in the reference genome. 
			| **SMAP delineate** does not need to consider strandedness of mapping for merged paired-end reads.
			| **SMAP** recommends merging of paired-end reads before mapping to create longer haplotypes than with single-end reads, and does not apply imputation or phase extension.
			| **SMAP** should be used in ``-mapping_orientation ignore`` mode for analysis of merged paired-end reads.

----


Step 1. Delineating Stacks
--------------------------

:navy:`Stacks are defined by sets of reads with identical read mapping start and end positions`

Procedure
~~~~~~~~~

For each BAM file, reads are filtered on mapping quality (MQ) score, and stacks are delineated by unique start and end positions of each mapped read, here called Stack Mapping Anchor Points (SMAPs). In a BAM file viewed with ``SAMtools view``, these coordinates are listed per read in column 4 and 5.
For each Stack, the number of reads with exact same start and end positions (SMAPs) is counted. Stacks are only retained with Stack read depth between user-defined minimum and maximum values.

.. tabs::

   .. tab:: schematic
	  
	  **Reads to Stacks:**
	  
	  .. image:: ../images/delineate/Reads_to_Stacks.png

   .. tab:: general options

	**General options:**

	  | ``alignments_dir`` :white:`###########` *(str)* :white:`###` Path to the directory containing BAM and BAI alignment files. All BAM files should be in the same directory. Positional argument, should be the first argument after ``smap delineate`` [no default].
	  | ``-p``, ``--processes`` :white:`#########` *(int)* :white:`###` Number of parallel processes [1].
	  | ``--plot`` :white:`#######################` Select which plots are generated. ``--plot nothing`` disables plot generation. ``--plot summary`` only generates graphs with information across all samples, while ``--plot all`` will also generate per-sample plots [summary].
	  | ``-t``, ``--plot_type`` :white:`################` Use this option to choose plot format, choices are png and pdf [png].
	  | ``-n``, ``--name`` :white:`#############` *(str)* :white:`###` Label to describe the sample set, will be added to the last column in the final SMAP BED file and is used by **SMAP compare** [Sample_Set1].
	  | ``-u``, ``--undefined_representation`` :white:`#####` Value to use for non-existing or masked data [NaN].
	  | ``-h``, ``--help`` :white:`###################` Show the full list of options. Disregards all other parameters.
	  | ``-v``, ``--version`` :white:`#################` Show the version. Disregards all other parameters.
	  | ``--debug`` :white:`######################` Enable verbose logging. Provides additional intermediate output-files used for sample-specific QC.

	Options may be given in any order.
	
	**General filtering options:**

	  | ``-q``, ``--min_mapping_quality`` :white:`##` *(int)* :white:`###` Minimum read mapping quality to include a read in the analysis [30].

	Options may be given in any order.

   .. tab:: **Stack** filter options
	
	Filter criteria for **Stacks** (within loci) are:

	  | ``-x``, ``--min_stack_depth`` :white:`####` *(int)* :white:`###` Minimum number of reads per Stack per sample. Recommended value is 3 [0].
	  | ``-y``, ``--max_stack_depth`` :white:`####` *(int)* :white:`###` Maximum number of reads per Stack per sample. Recommended value is 1500 [inf].

	Options may be given in any order.

----

Step 2. Delineating StackClusters
---------------------------------

:navy:`StackClusters are defined by the positional overlap between Stacks within a sample`

Procedure
~~~~~~~~~

For each BAM file, StackClusters are created by positional overlap (`BEDtools merge <https://bedtools.readthedocs.io/en/latest/content/tools/merge.html>`_) between Stacks. For each StackCluster, the number of overlapping Stacks is counted, and the corresponding read depths are summed. Based on user-defined criteria, these StackClusters are then filtered.

The user can set a minimum StackCluster read depth to select loci with sufficient reads for SNP/haplotype calling, and a maximum StackCluster read depth to remove loci likely derived from repetitive sequences.  
For each Stack, the relative contribution to the total StackCluster read depth is evaluated (Stack Depth Fraction). Stacks are only included in a StackCluster if they constitute at least a user-defined minimum fraction of the total read count in the StackCluster. This option removes Stacks derived from low frequency reads (and corresponding SMAPs) spuriously overlapping with otherwise correct StackClusters. Different threshold values are used for individuals and pools, as low frequency (<5-10%) observations are likely to be noise in genotyping data of individuals, while low frequency observations are expected in Pool-Seq data of genetically diverse species.
The user can set a maximum number of Stacks per StackCluster to select loci according to an expected level of genetic diversity. If a StackCluster contains more Stacks than the specified value, the entire StackCluster is discarded from that sample. It is recommended to run **SMAP delineate** several times on your data while changing this value, as it might uncover possible technical or biological errors. For example, for a diploid individual the majority of StackClusters are expected to contain only 2 Stacks. If many StackClusters contain 3 or 4 Stacks this may indicate contamination or mislabeling of the sample. The number of Stacks per StackCluster are visualized in **sample.StackCluster.Stacks.histogram.png**, see :ref:`Example data analyses <SMAPdelex>` for examples from actual data.


.. tabs::
   
   .. tab:: schematic
	  
	  **Stacks to StackClusters:**
	  
	  .. image:: ../images/delineate/Stacks_to_StackClusters.png

   .. tab:: **StackCluster** filter options

	Filter criteria for **StackClusters** (within samples) are:

	  | ``-l``, ``--max_stack_number`` :white:`##########` *(int)* :white:`###` Maximum number of Stacks per StackCluster. Recommended value is 2 for diploid individuals, 4 for tetraploid individuals, 20 for Pool-Seq [inf].
	  | ``-b``, ``--min_stack_depth_fraction`` :white:`####` *(float)* :white:`##` Threshold (%) for minimum relative Stack depth per StackCluster. Removes spuriously mapped reads from StackClusters, and controls for noise in the number of SMAPs per locus. The StackCluster total read depth and number of SMAPs is recalculated based on the retained Stacks per StackCluster per sample. Recommended values are 10.0 for individuals and 5.0 for Pool-Seq [0.0].
	  | ``-c``, ``--min_cluster_depth`` :white:`##########` *(int)* :white:`###` Minimum total number of reads per StackCluster per sample. Sum of all Stacks per StackCluster calculated after filtering out the Stacks with Stack Depth Fraction < -b. A good reference value is 10 for individual diploid samples, 20 for tetraploids, and 30 for Pool-Seq [0].
	  | ``-d``, ``--max_cluster_depth`` :white:`##########` *(int)* :white:`###` Maximum total number of reads per StackCluster per sample. Sum of all Stacks per StackCluster calculated after filtering out the Stacks with Stack Depth Fraction < -b. Used to filter out loci with excessively high read depth [inf].
	  | ``-f``, ``--min_cluster_length`` :white:`#########` *(int)* :white:`###` Minimum Stack and StackCluster length. Can be used to remove Stacks and StackClusters that are too short compared to the original read length. For separately mapped and merged reads, the minimum mapped length may be about one-third of the original read length (trimmed, before merging and mapping).
	  | ``-g``, ``--max_cluster_length`` :white:`#########` *(int)* :white:`###` Maximum Stack and StackCluster length. Can be used to remove Stacks and StackClusters that are too long compared to the original read length. For separately mapped reads, the maximum mapped length may be about 1.5 times the original read length (trimmed, before mapping). For merged reads, the maximum mapped length may be about 2.2 times the original read length (trimmed, before merging and mapping).

	Options may be given in any order.

   .. tab:: removal of artefactual **StackClusters**

	  .. image:: ../images/delineate/SMAP_scenario's_seq_align_PE_A_extra.png
	  
	  If both fragments are in the selected size range, but they map next to each other without overlap (the restriction enzyme site remnant is removed during read preprocessing), the reads are analyzed and counted separately, despite originating from the same chromosome molecule. This inflates the total read counts per locus and wrongfully alters haplotype frequencies during haplotype calling with SMAP haplotype-sites. To exclude this phenomenon from downstream analysis, by default, all StackClusters are removed where the lowest upstream SMAP of one Stack is found at a higher reference position than the highest downstream SMAP of an other Stack in the same StackCluster. In addition, MergedClusters are removed that were constructed by two StackClusters that do not overlap and an other StackCluster that links the non-overlapping pair.

	  In the example above (merged single-enzyme GBS), if a diploid sample contains allele A and the reference allele, the frequencies of ref, A1, and A2 are expected to be 33% each; resembling a triploid and therefore false genotype.

----

.. _SMAPdelHIW3:

Step 3. Delineating MergedClusters
----------------------------------

:navy:`MergedClusters are defined by the positional overlap between StackClusters across sample sets`

Procedure
~~~~~~~~~

After processing all BAM files in the specified folder, SMAP delineate overlaps (`BEDtools merge <https://bedtools.readthedocs.io/en/latest/content/tools/merge.html>`_) all StackClusters across all samples, and defines a MergedCluster for each genomic locus that is covered by a StackCluster in at least one sample. 
For each MergedCluster, the number of overlapping StackClusters is counted and the corresponding read depths are summed.
MergedClusters are only retained if they meet two criteria; the respective StackCluster was detected in a minimum percentage of samples across the sample set (completeness), and less than a maximum number of SMAPs per MergedCluster to remove excessively high polymorphic loci.

.. tabs::
   
   .. tab:: schematic
	  
	  **StackClusters to MergedClusters:**
	  
	  .. image:: ../images/delineate/StackClusters_to_MergedClusters.png

   .. tab:: **MergedCluster** filter options

	Filter criteria for **MergedClusters** (across samples) are:

	  | ``-s``, ``--max_smap_number`` :white:`#############` *(int)* :white:`###` Maximum number fo SMAPs per MergedCluster across the sample set. Can be used to remove loci with excessive MergedCluster complexity before downstream analysis [inf].
	  | ``-w``, ``--completeness`` :white:`###############` *(int)* :white:`###` Completeness (%), minimum percentage of samples in the sample set that contains an overlapping StackCluster for a given MergedCluster. May be used to select loci with enough read mapping data across the sample set for downstream analysis [0].

	Options may be given in any order.

   .. tab:: removal of artefactual **MergedClusters**

	  .. image:: ../images/delineate/StackCluster_MergedCluster_overlapping_Stacks_readcountinflation.png
	  
	  If StackClusters from different samples map next to each other without overlap, but a third StackCluster from an additional sample links the three StackClusters by positional overlap, this creates a long MergedCluster in which all constituent SMAPs are bundled. As a consequence, all reads with overlap to the entire region are analyzed and counted separately, despite originating from the same chromosome molecule. This inflates the total read counts per locus and wrongfully alters haplotype frequencies during haplotype calling with SMAP haplotype-sites. To exclude this phenomenon from downstream analysis, by default, MergedClusters are removed that were constructed by two StackClusters that do not overlap and an other StackCluster that links the non-overlapping pair.
	  
	  In the example above (3 diploid samples with merged single-enzyme GBS), a single SNP in the middle of the reference read results in the gain of an RE in Sample 1 and 2, in addition in Sample 2, another SNP results in a loss of RE.
	  Separately, all of these samples contain legitimate StackClusters. But if combined, Sample 1 contains 4 copies in the MergedCluster, whereas Sample 2 and 3 only contain 2 copies.
