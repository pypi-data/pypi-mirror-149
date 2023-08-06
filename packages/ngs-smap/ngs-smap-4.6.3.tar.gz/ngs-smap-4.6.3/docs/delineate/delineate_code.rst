.. raw:: html

    <style> .navy {color:navy} </style>
	
.. role:: navy

.. raw:: html

    <style> .white {color:white} </style>

.. role:: white

.. _SMAPSummaryCommand:

###########################
Summary of Commands
###########################

This page provides a summary of all options of **SMAP delineate** and examples of typical commands.

.. _SMAPMandatoryArgs:

Mandatory arguments
-------------------

| It is mandatory to specify the directory containing the BAM and BAI alignment files:

| ``alignments_dir`` :white:`#########` *(str)* :white:`###` Path to the directory containing BAM and BAI alignment files. All BAM files should be in the same directory [no default].

| It is mandatory to specify the type of read mapping:

| The option ``-mapping_orientation`` must always be used to specify if strandedness of read mapping should be considered for haplotyping. ``-mapping_orientation stranded`` means that only reads will be considered that map on the same strand as indicated per locus in the SMAP BED file. ``-mapping_orientation ignore`` should be used to collect all reads per locus independent of the strand that the reads are mapped on (i.e. ignoring their mapping orientation). See the :ref:`section on strandedness <SMAPhaploASpartialShotgun>` for more information.

----

General Options
---------------

.. tabs:: 

	.. tab:: General options
		
		**General options:**
		
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

		Command to run **SMAP delineate** with specified directory with BAM files, number of parallel processes, min and max StackCluster length, graphical output format and label for the sample set::
	
			smap delineate /path/to/BAM/ -mapping_orientation stranded -p 8 --plot_type png --name 2n_ind_GBS-SE
		
	.. tab:: **Stacks** filter options
		
		Filter criteria for **Stacks** (within loci) are:

		  | ``-x``, ``--min_stack_depth`` :white:`####` *(int)* :white:`###` Minimum number of reads per Stack per sample. Recommended value is 3 [0].
		  | ``-y``, ``--max_stack_depth`` :white:`####` *(int)* :white:`###` Maximum number of reads per Stack per sample. Recommended value is 1500 [inf].

		Options may be given in any order.  

		Command to run **SMAP delineate** with adjusted Mapping Quality, and Stack read depth min and max values::

			smap delineate /path/to/BAM/ -mapping_orientation stranded -p 8 --plot all --plot_type pdf --name 2n_ind_GBS-SE --min_mapping_quality 20 -f 50 -g 200 --min_stack_depth 5 --max_stack_depth 1500
	
	.. tab:: **StackClusters** filter options
	
		Filter criteria for **StackClusters** (within samples) are:

		  | ``-l``, ``--max_stack_number`` :white:`##########` *(int)* :white:`###` Maximum number of Stacks per StackCluster. Recommended value is 2 for diploid individuals, 4 for tetraploid individuals, 20 for Pool-Seq [inf].
		  | ``-b``, ``--min_stack_depth_fraction`` :white:`####` *(float)* :white:`##` Threshold (%) for minimum relative Stack depth per StackCluster. Removes spuriously mapped reads from StackClusters, and controls for noise in the number of SMAPs per locus. The StackCluster total read depth and number of SMAPs is recalculated based on the retained Stacks per StackCluster per sample. Recommended values are 10.0 for individuals and 5.0 for Pool-Seq [0.0].
		  | ``-c``, ``--min_cluster_depth`` :white:`##########` *(int)* :white:`###` Minimum total number of reads per StackCluster per sample. Sum of all Stacks per StackCluster calculated after filtering out the Stacks with Stack Depth Fraction < -b. A good reference value is 10 for individual diploid samples, 20 for tetraploids, and 30 for Pool-Seq [0].
		  | ``-d``, ``--max_cluster_depth`` :white:`##########` *(int)* :white:`###` Maximum total number of reads per StackCluster per sample. Sum of all Stacks per StackCluster calculated after filtering out the Stacks with Stack Depth Fraction < -b. Used to filter out loci with excessively high read depth [inf].
		  | ``-f``, ``--min_cluster_length`` :white:`#########` *(int)* :white:`###` Minimum Stack and StackCluster length. Can be used to remove Stacks and StackClusters that are either too short compared to the original read length. For separately mapped and merged reads, the minimum length may be about one-third of the original read length (trimmed, before merging and mapping) [0].
		  | ``-g``, ``--max_cluster_length`` :white:`#########` *(int)* :white:`###` Maximum Stack and StackCluster length. Can be used to remove Stacks and StackClusters that are either too long compared to the original read length. For separately mapped reads, the maximum mapped length may be about 1.5 times the original read length (trimmed, before mapping). For merged reads, the maximum mapped length may be about 2.2 times the original read length (trimmed, before merging and mapping) [inf].

		Options may be given in any order.

		Command to run **SMAP delineate** with adjusted Stack Number, StackCluster read depth min and max values, and Stack in StackCluster fraction::

			smap delineate /path/to/BAM/ -mapping_orientation stranded -p 8 --plot all --plot_type pdf --name 2n_ind_GBS-SE --min_mapping_quality 20 -f 50 -g 200 --min_stack_depth 5 --max_stack_depth 500 --max_stack_number 2 --min_cluster_depth 10 --max_cluster_depth 1500 --min_stack_depth_fraction 5
	
	.. tab:: **MergedClusters** filter options

		Filter criteria for **MergedClusters** (across samples) are:

		  | ``-s``, ``--max_smap_number`` :white:`#############` *(int)* :white:`###` Maximum number of SMAPs per MergedCluster across the sample set. Can be used to remove loci with excessive MergedCluster complexity before downstream analysis [inf].
		  | ``-w``, ``--completeness`` :white:`###############` *(int)* :white:`###` Completeness (%), minimum percentage of samples in the sample set that contains an overlapping StackCluster for a given MergedCluster. May be used to select loci with enough read mapping data across the sample set for downstream analysis [0].

		Options may be given in any order.

		Command to run **SMAP delineate** with adjusted SMAP Number and Completeness::

			smap delineate /path/to/BAM/ -mapping_orientation stranded -p 8 --plot all --plot_type pdf --name 2n_ind_GBS-SE --min_mapping_quality 20 -f 50 -g 200 --min_stack_depth 5 --max_stack_depth 1500 --max_stack_number 2 --min_cluster_depth 10 --max_cluster_depth 1500 --min_stack_depth_fraction 5 --max_smap_number 10 --completeness 90

Examples
--------

.. tabs::

   .. tab:: diploid individuals, single-end GBS

	  Typical command to run SMAP delineate for separately mapped single-end GBS reads in diploid individuals.
	  
	  ::
				
		smap delineate /path/to/BAM/ -mapping_orientation stranded -p 8 --plot all --plot_type png --name 2n_ind_GBS-SE -f 50 -g 200 --min_stack_depth 3 --max_stack_depth 500 --min_cluster_depth 10 --max_stack_number 2 --min_stack_depth_fraction 10 --completeness 1 --max_smap_number 10
		
   .. tab:: diploid individuals, paired-end GBS

	  Typical command to run SMAP delineate for separately mapped paired-end GBS reads in diploid individuals.
	  
	  ::
				
		smap delineate /path/to/BAM/ -mapping_orientation stranded -p 8 --plot all --plot_type png --name 2n_ind_GBS-SE -f 50 -g 200 --min_stack_depth 3 --max_stack_depth 500 --min_cluster_depth 10 --max_stack_number 2 --min_stack_depth_fraction 10 --completeness 1 --max_smap_number 10
		
   .. tab:: diploid individuals, merged GBS

	  Typical command to run SMAP delineate for merged GBS reads in diploid individuals.
	  
	  ::
				
		smap delineate /path/to/BAM/ -mapping_orientation ignore -p 8 --plot all --plot_type png --name 2n_ind_GBS-merged -f 50 -g 300 --min_stack_depth 3 --max_stack_depth 500 --min_cluster_depth 10 --max_stack_number 2 --min_stack_depth_fraction 10 --completeness 1 --max_smap_number 10
		
   .. tab:: diploid pools, single-end GBS

	  Typical command to run SMAP delineate for separately mapped single-end GBS reads in pools.
	  
	  ::
				
		smap delineate /path/to/BAM/ -mapping_orientation stranded -p 8 --plot all --plot_type png --name 2n_pools_GBS-SE -f 50 -g 200 --min_stack_depth 3 --max_stack_depth 500 --min_cluster_depth 30 --max_stack_number 10 --min_stack_depth_fraction 5 --completeness 1 --max_smap_number 20

   .. tab:: diploid pools, merged GBS

	  Typical command to run SMAP delineate for merged GBS reads in pools.
	  
	  ::
				
		smap delineate /path/to/BAM/ -mapping_orientation stranded -p 8 --plot all --plot_type png --name 2n_pools_GBS-merged -f 50 -g 300 --min_stack_depth 3 --max_stack_depth 500 --min_cluster_depth 30 --max_stack_number 10 --min_stack_depth_fraction 5 --completeness 1 --max_smap_number 20
		
   .. tab:: tetraploid individuals, merged GBS

	  Typical command to run SMAP delineate for merged GBS reads in tetraploid individuals.
		  
	  ::
				
		smap delineate /path/to/BAM/ -mapping_orientation ignore -p 8 --plot all --plot_type png --name 4n_ind_GBS-merged -f 50 -g 300 --min_stack_depth 3 --max_stack_depth 500 --min_cluster_depth 20 --max_stack_number 4 --min_stack_depth_fraction 10 --completeness 1 --max_smap_number 20

   .. tab:: tetraploid pools, merged GBS

	  Typical command to run SMAP delineate for merged GBS reads in pools.
		  
	  ::
				
		smap delineate /path/to/BAM/ -mapping_orientation ignore -p 8 --plot all --plot_type png --name 4n_pools_GBS-merged -f 50 -g 300 --min_stack_depth 3 --max_stack_depth 500 --min_cluster_depth 30 --max_stack_number 10 --min_stack_depth_fraction 5 --completeness 1 --max_smap_number 20
	  
