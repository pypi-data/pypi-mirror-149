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

:navy:`SMAP delineate analyzes read mapping positions and read depth distributions in stacked read alignments`

Bioinformatics analyses that compare reads mapped to a common reference to identify sequence variants require that sufficient reads are mapped to the same reference genome locations across sample sets. However, a range of technical and biological aspects affect read mapping positions and read depth. So, it is important to first analyze if read mapping positions and read depth are consistent across the sample set, for the simple reason that if reads are not mapped to a given location, no variants can be identified in that sample. Here, we address the special case of loci with \`Stacked short reads´ \ obtained with reduced representation libraries such as Genotyping-By-Sequencing (GBS). The **SMAP delineate** approach does not apply to random fragmented (e.g. Shotgun Sequencing) read data.

:navy:`Input: SMAP delineate only requires sorted and indexed BAM files with aligned reads`


Given a set of BAM files with GBS reads, **SMAP delineate** is a simple application to address the questions:

	1.  Where are the reads located?
	#.  How many loci with stacked reads are present per sample?
	#.  Are mapping positions consistent across sample sets?
	#.  Do polymorphisms occur in read mapping start and end positions within Stacked loci?
	#.  How to select loci with sufficient read depth and completeness across the sample set for effective downstream variant calling?

:navy:`Stack delineation captures within-sample and between-sample read mapping variation`

| **SMAP delineate** first creates Stacks by identifying sets of reads with identical read mapping start and end positions per sample.
| The start and end positions of such Stacks are called Stack Mapping Anchor Points (:ref:`SMAPs <SMAPdeldef>`).
| **SMAP delineate** then creates StackClusters by merging Stacks with positional overlap **per sample** (via `bedtools merge <https://bedtools.readthedocs.io/en/latest/content/tools/merge.html>`_), thus capturing SMAP polymorphisms per sample per locus.
| **SMAP delineate** finally creates MergedClusters by merging StackClusters **across all samples** by positional overlap (via `bedtools merge <https://bedtools.readthedocs.io/en/latest/content/tools/merge.html>`_), thus capturing the variation of read mapping distribution across the sample set.

:navy:`Output`

| **SMAP delineate** provides custom filters and creates a BED file with MergedCluster positions, *i.e.* high quality loci for downstream analyses (e.g. SNP variant calling).
| **SMAP delineate** lists read mapping position polymorphisms as a unique type of molecular markers for downstream analyses (e.g. haplotype calling).
| **SMAP delineate** plots :ref:`feature distributions <SMAPdelex>` such as length, read depth, and number of SMAPs per :ref:`Stack, StackCluster, and MergedCluster <SMAPdeldef>`.
| **SMAP delineate** plots a :ref:`saturation curve <SMAPdelex>` and other graphs showing locus completeness across the sample set.

----

Guidelines for read preprocessing and mapping
---------------------------------------------

| Read preprocessing requires specific steps for single-digest or double-digest GBS, in combinations with single-end reads, paired-end reads or merged reads.
| See `Read preprocessing <https://gbprocess.readthedocs.io/en/latest/gbs_data_processing.html>`_ for a detailed description of recommended preprocessing and mapping per GBS method.

----

.. _SMAPdelfilter:
   
Quick Start and options
-----------------------


:navy:`Mandatory options for SMAP delineate`

As **SMAP delineate** is entirely data-driven, it does not need any prior information about which or how many different enzymes are used for GBS library construction.
Just specify the directory containing the BAM and BAI alignment files:

``smap delineate alignments_dir`` :white:`###` Path to the directory containing BAM and BAI alignment files. All BAM files should be in the same directory.

Based on whether reads are separately mapped or are merged before mapping, the user must specify the corresponding option ``--mapping_orientation``:

-  ``-mapping_orientation stranded`` :white:`##` Simply use ``-mapping_orientation stranded`` for any BAM file that contains separately mapped reads. Note that this may be single-end or non-merged paired-end read data. In ``-mapping_orientation stranded`` mode, SMAP delineate will use the strand-specific read mapping orientation (also called :ref:`Strandedness <SMAPdelstrand>`) to delineate Stacks, StackClusters, and MergedClusters. Paired-end information is not used to extend Stacks of paired-end read pairs with internal overlap after read mapping.

-  ``-mapping_orientation ignore`` :white:`###` If paired-end reads are available and the insert library size is less than twice the read length, then we recommend to merge these reads before read mapping (e.g. with `PEAR <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3933873/>`_), and only map reads that were merged. By running SMAP delineate in ``-mapping_orientation ignore`` mode, such merged reads are combined into a Stack irrespective of strand-specific read mapping orientation (also called Strandedness), thus reducing redundancy in the number of unique marker loci on the reference genome and maximizing the effective read depth per StackCluster.

Basic command to run **SMAP delineate** with default parameters::

	smap delineate /path/to/BAM/ -mapping_orientation stranded
	or
	smap delineate /path/to/BAM/ -mapping_orientation ignore

:navy:`Schematic overview of filtering options`

.. image:: ../images/delineate/SMAP_delineate.png

:navy:`Command line options` 

See tabs below for specific filter options for Stacks, StackClusters, and MergedClusters and more detailed examples of command line options.
It is mandatory to specify the directory containing the BAM and BAI alignment files, and the type of reads (separate or merged).

.. tabs:: 

	.. tab:: General options
    
		**General options:**

		  | ``alignments_dir`` :white:`###########` *(str)* :white:`###` Path to the directory containing BAM and BAI alignment files. All BAM files should be in the same directory. Positional argument, should be the first argument after ``smap delineate`` [no default].
		  | ``--mapping_orientation`` :white:`####################` Define the read mapping type. ``-mapping_orientation stranded`` for single-end reads or for paired-end reads that are mapped separately (without merging forward and reverse reads), ``-mapping_orientation ignore`` for paired-end reads that are merged before mapping.
		  | ``-p``, ``--processes`` :white:`#########` *(int)* :white:`###` Number of parallel processes [1]. 
		  | ``--plot`` :white:`#######################` Select which plots are generated. ``--plot nothing`` disables plot generation. ``--plot summary`` only generates graphs with information across all samples, while ``--plot all`` will also generate per-sample plots [summary].
		  | ``-t``, ``--plot_type`` :white:`################` Use this option to choose plot format, choices are png and pdf [png].  
		  | ``-n``, ``--name`` :white:`#############` *(str)* :white:`###` Label to describe the sample set, will be added to the last column in the final SMAP BED file and is used by **SMAP compare** [Sample_Set1].
		  | ``-u``, ``--undefined_representation`` :white:`#####` Value to use for non-existing or masked data [NaN].
		  | ``-h``, ``--help`` :white:`###################` Show the full list of options. Disregards all other parameters.
		  | ``-v``, ``--version`` :white:`#################` Show the version. Disregards all other parameters.
		  | ``--debug`` :white:`######################` Enable verbose logging. Provides additional intermediate output files used for sample-specific QC, including the BED files for Stacks and StackClusters per sample.

		**General filtering options:**

		  | ``-q``, ``--min_mapping_quality`` :white:`##` *(int)* :white:`###` Minimum read mapping quality to include a read in the analysis [30].

		Options may be given in any order.
		
		Command to run **SMAP delineate** with specified directory with BAM files, number of parallel processes, graphical output format, label for the sample set, and adjusted Mapping Quality::
	
			smap delineate /path/to/BAM/ -mapping_orientation stranded -p 8 --plot_type png --name 2n_ind_GBS-SE --min_mapping_quality 20
		
	.. tab:: **Stacks** filter options
		
		Filter criteria for **Stacks** (within loci) are:

		  | ``-x``, ``--min_stack_depth`` :white:`####` *(int)* :white:`###` Minimum number of reads per Stack per sample. Recommended value is 3 [0]. 
		  | ``-y``, ``--max_stack_depth`` :white:`####` *(int)* :white:`###` Maximum number of reads per Stack per sample. Recommended value is 1500 [inf].

		Options may be given in any order.  
          
		Command to run **SMAP delineate** with specific Stack read depth min and max values::

			smap delineate /path/to/BAM/ -mapping_orientation stranded -p 8 --plot all --plot_type pdf --name 2n_ind_GBS-SE --min_mapping_quality 20 --min_stack_depth 5 --max_stack_depth 1500
	
	.. tab:: **StackClusters** filter options
	
		Filter criteria for **StackClusters** (within samples) are:

		  | ``-l``, ``--max_stack_number`` :white:`########` *(int)* :white:`###` Maximum number of Stacks per StackCluster. Recommended value is 2 for diploid individuals, 4 for tetraploid individuals, 20 for Pool-Seq [inf].
		  | ``-b``, ``--min_stack_depth_fraction`` :white:`##` *(float)* :white:`##` Threshold (%) for minimum relative Stack depth per StackCluster. Removes spuriously mapped reads from StackClusters, and controls for noise in the number of SMAPs per locus. The StackCluster total read depth and number of SMAPs is recalculated based on the retained Stacks per StackCluster per sample. Recommended values are 10.0 for individuals and 5.0 for Pool-Seq [0.0].
		  | ``-c``, ``--min_cluster_depth`` :white:`########` *(int)* :white:`###` Minimum total number of reads per StackCluster per sample. Sum of all Stacks per StackCluster calculated after filtering out the Stacks with Stack Depth Fraction < -b. A good reference value is 10 for individual diploid samples, 20 for tetraploids, and 30 for Pool-Seq [0].
		  | ``-d``, ``--max_cluster_depth`` :white:`########` *(int)* :white:`###` Maximum total number of reads per StackCluster per sample. Sum of all Stacks per StackCluster calculated after filtering out the Stacks with Stack Depth Fraction < -b. Used to filter out loci with excessively high read depth [inf].
		  | ``-f``, ``--min_cluster_length`` :white:`#######` *(int)* :white:`###` Minimum Stack and StackCluster length. Can be used to remove Stacks and StackClusters that are too short compared to the original read length. For separately mapped and merged reads, the minimum length may be about one-third of the original read length (trimmed, before merging and before mapping) [0].
		  | ``-g``, ``--max_cluster_length`` :white:`#######` *(int)* :white:`###` Maximum Stack and StackCluster length. Can be used to remove Stacks and StackClusters that are too long compared to the original read length. For separately mapped reads, the maximum length may be about 1.5 times the original read length (trimmed, before mapping). For merged reads, the maximum length may be about 2.2 times the original read length (trimmed, before merging and mapping) [inf].

		Options may be given in any order.  

		Command to run **SMAP delineate** with adjusted StackCluster length values, Stack Number, StackCluster read depth min and max values, and Stack in StackCluster fraction::

			smap delineate /path/to/BAM/ -mapping_orientation stranded -p 8 --plot all --plot_type pdf --name 2n_ind_GBS-SE --min_mapping_quality 20 -f 50 -g 200 --min_stack_depth 5 --max_stack_depth 1500 --max_stack_number 2 --min_cluster_depth 10 --max_cluster_depth 10000 --min_stack_depth_fraction 5
	
	.. tab:: **MergedClusters** filter options

		Filter criteria for **MergedClusters** (across samples) are:

		  | ``-s``, ``--max_smap_number`` :white:`######` *(int)* :white:`###` Maximum number of SMAPs per MergedCluster across the sample set. Can be used to remove loci with excessive MergedCluster complexity before downstream analysis [inf].
		  | ``-w``, ``--completeness`` :white:`########` *(int)* :white:`###` Completeness (%), minimum percentage of samples in the sample set that contains an overlapping StackCluster for a given MergedCluster. May be used to select loci with enough read mapping data across the sample set for downstream analysis [0].

		Options may be given in any order.

		Command to run **SMAP delineate** with adjusted SMAP Number and Completeness::

			smap delineate /path/to/BAM/ -mapping_orientation stranded -p 8 --plot all --plot_type pdf --name 2n_ind_GBS-SE --min_mapping_quality 20 -f 50 -g 200 --min_stack_depth 5 --max_stack_depth 1500 --max_stack_number 2 --min_cluster_depth 10 --max_cluster_depth 10000 --min_stack_depth_fraction 5 --max_smap_number 10 --completeness 90

----

.. _SMAPdeloutput:
   
Output
------

.. tabs::

   .. tab:: Graphical output

	  | By default, five plots are created to summarize locus features across the sample set; a locus saturation curve in function of total reads mapped per sample, a graph plotting the completeness of loci across the sample set, a graph of the read mapping polymorphisms (number of SMAPs) per locus, a graph containing the lengths of loci across the sample set, and a graph with the median read lengths per locus across the sample set. 
	  | Optionally, separate graphs of locus features can be plotted *per sample* and are strongly recommended for Quality Control of each new sample set and trouble-shooting. A graphical summary can be generated for each sample for the two incremental levels of read merging (**Stacks** and **StackClusters**), such as the distribution of read depth, length, and number of Stacks per locus.  
	  |
	  | An extensive collection of examples and explanations for different types of GBS libraries can be found in the section :ref:`Example data analyses <SMAPdelex>`.
	  | A sneak preview of the most important summary graphical output:

	  .. image:: ../images/delineate/Graphical_summary.png  
	  
   .. tab:: Tabular output
	
	  | For each incremental level of read merging (Stacks, StackClusters, and MergedClusters), a BED file listing the SMAP positions, read depth, orientation, numbers of SMAPs, locus length, etc, per locus may be generated.
	  | By default, a single BED file describing the SMAP positions in MergedClusters across the sample set is created for downstream analyses in **SMAP compare** and **SMAP haplotype-sites** (final_SMAP_positions_*filtering-options*.bed).
	  | The BED files for Stacks and StackClusters for each sample can be created using the option ``--debug``.
   
   