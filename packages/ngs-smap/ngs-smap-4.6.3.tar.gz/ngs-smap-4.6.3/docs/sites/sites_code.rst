.. raw:: html

    <style> .navy {color:navy} </style>

.. role:: navy

.. raw:: html

    <style> .white {color:white} </style>

.. role:: white

###########################
Summary of Commands
###########################

This page provides a summary of all command examples and options of **SMAP haplotype-sites**.

Mandatory options
-----------------

:navy:`read mapping orientation`

| The option ``-mapping_orientation`` must always be used to specify if strandedness of read mapping should be considered for haplotyping. ``-mapping_orientation stranded`` means that only reads will be considered that map on the same strand as indicated per locus in the SMAP BED file. ``-mapping_orientation ignore`` should be used to collect all reads per locus independent of the strand that the reads are mapped on (i.e. ignoring their mapping orientation). See the :ref:`section on strandedness <SMAPhaploASpartialShotgun>` for more information.


.. tabs::

   .. tab:: HiPlex

	  | use ``-mapping_orientation ignore`` for PE HiPlex reads that were merged before mapping (by e.g; `PEAR <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3933873/>`_).

   .. tab:: Shotgun

	  | use ``-mapping_orientation ignore`` for single-end, paired-end reads mapped separately, or reads that were merged before mapping (by e.g; `PEAR <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3933873/>`_).

   .. tab:: GBS

	  | use ``-mapping_orientation stranded`` for single-end or paired-end reads mapped separately.
	  | use ``-mapping_orientation ignore`` for reads that were merged before mapping (by e.g; `PEAR <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3933873/>`_).


:navy:`partial`

| The option ``-partial`` must always be used to specify if reads are expected to be aligned at both outer positions of the locus (HiPlex, Shotgun SNPs in sliding frames) or if reads are expected to display read mapping polymorphisms along the locus (GBS, Shotgun SVs). 
| ``-partial exclude`` means that only reads are considered for haplotyping that completely cover the locus including both start and end points. Partially mapped reads are excluded. (see also :ref:`HiPlex <SMAPhaploASpartialHiplex>` and :ref:`Shotgun SNPs <SMAPhaploASpartialShotgun>`)
| ``-partial include`` means that all reads are considered for haplotyping, including reads that only partially cover the locus. (see also :ref:`GBS <SMAPhaploGBSpartial>` and :ref:`Shotgun SVs <SMAPhaploASpartialShotgun>`) 

.. tabs::

   .. tab:: HiPlex

	  | Use ``-partial exclude`` for :ref:`HiPlex <SMAPhaploASpartialHiplex>` because reads amplified with both primers are expected to cover the entire region between the primers. This is scored by being "present" in the read-reference aligned nucleotide pair on the two SMAP positions (just downstream of the forward primer, and just upstream of the reverse primer). Reads with partial alignments are considered amplification, sequencing, or read trimming artefacts, and are excluded from evaluation in the haplotype tables.

   .. tab:: Shotgun

	  | Use ``-partial exclude`` for :ref:`Shotgun <SMAPhaploASpartialShotgun>` if sliding frames are used to haplotype sets of neighboring SNPs.
	  | Use ``-partial include`` for :ref:`Shotgun <SMAPhaploASpartialShotgun>` if sliding frames are used to haplotype the junctions of SVs.

   .. tab:: GBS

	  | Use ``-partial include`` for :ref:`GBS <SMAPhaploGBSpartial>` because you must **include** reads with mapping position polymorphisms in the haplotype table.


General options
---------------

.. tabs::

   .. tab:: general options

	  | ``alignments_dir`` :white:`#############` *(str)* :white:`###` Path to the directory containing BAM and BAI files. All BAM files should be in the same directory. Positional mandatory argument, should be the **first** argument after ``smap haplotype-sites`` [no default].  
	  | ``bed`` :white:`#####################` *(str)* :white:`###` Path to the BED file containing sites for which haplotypes will be reconstructed. For GBS experiments, the BED file should be generated using :ref:`SMAP delineate <SMAPdelHIW>`. For HiPlex data, a BED6 file can be provided, with the 4th and 5th column being blank and the chromosome name, locus start position site, locus end position site and strand information populating the first, second, third and sixth column respectively. Positional mandatory argument, should be the **second** argument after ``smap haplotype-sites``.
	  | ``vcf`` :white:`#####################` *(str)* :white:`###` Path to the VCF file (in VCFv4.2 format) containing variant positions. It should contain at least the first 9 columns listing the SNP positions, sample-specific genotype calls across the sampleset are not required. Positional mandatory argument, should be the **third** argument after ``smap haplotype-sites``.
	  | ``-p``, ``--processes`` :white:`###########` *(int)* :white:`###` Number of parallel processes [1].
	  | ``--plot`` :white:`#########################` Select which plots are to be generated. Choosing "nothing" disables plot generation. Passing "summary" only generates graphs with information for all samples while "all" will also enable generate per-sample plots [default "summary"].
	  | ``-t``, ``--plot_type`` :white:`##################` Use this option to choose plot format, choices are png and pdf [png].  
	  | ``-o``, ``--out`` :white:`###############` *(str)* :white:`###` Basename of the output file without extension [SMAP_haplotype_sites].
	  | ``-u``, ``--undefined_representation`` :white:`#######` Value to use for non-existing or masked data [NaN].
	  | ``-h``, ``--help`` :white:`#####################` Show the full list of options. Disregards all other parameters.
	  | ``-v``, ``--version`` :white:`###################` Show the version. Disregards all other parameters.
	  | ``--debug`` :white:`########################` Enable verbose logging.
	  | 
	  | Options may be given in any order.

Filtering options
-----------------

.. tabs::

   .. tab:: filtering options

	  | ``-q``, ``--min_mapping_quality`` :white:`####` *(int)* :white:`###` Minimum .bam mapping quality to retain reads for analysis [30].
	  | ``--no_indels`` :white:`#####################` Use this option if you want to **exclude** haplotypes that contain an InDel at the given SNP/SMAP positions. These reads are also ignored to evaluate the minimal read count [default off; indels are included in output].
	  | ``-j``, ``--min_distinct_haplotypes`` :white:`#` *(int)* :white:`###` Minimal number of distinct haplotypes per locus across all samples. Loci that do not fit this criterium are removed from the final output [0].
	  | ``-k``, ``--max_distinct_haplotypes`` :white:`#` *(int)* :white:`###` Maximal number of distinct haplotypes per locus across all samples. Loci that do not fit this criterium are removed from the final output [inf].
	  | ``-c``, ``--min_read_count`` :white:`#######` *(int)* :white:`###` Minimal total number of reads per locus per sample [0].
	  | ``-d``, ``--max_read_count`` :white:`#######` *(int)* :white:`###` Maximal number of reads per locus per sample, read count is calculated after filtering out the low frequency haplotypes (``-f``) [inf].
	  | ``-f``, ``--min_haplotype_frequency`` :white:`#` *(float)* :white:`##` Set minimal HF (in %) to retain the haplotype in the genotyping matrix. Haplotypes above this threshold in at least one of the samples are retained. Haplotypes that never reach this threshold in any of the samples are removed [0].
	  | ``-m``, ``--mask_frequency`` :white:`#######` *(float)* :white:`##` Mask haplotype frequency values below this threshold for individual samples to remove noise from the final output. Haplotype frequency values below this threshold are set to ``-u``. Haplotypes are not removed based on this value, use ``--min_haplotype_frequency`` for this purpose instead.
	  | 
	  | Options may be given in any order.

Options for discrete calling in individual samples
--------------------------------------------------

.. tabs::

   .. tab:: options for discrete calling in individual samples
	  
	   This option is primarily supported for diploids and tetraploids. Users can define their own custom frequency interval bounds for species with a higher ploidy, but this requires optimization based on the observed haplotype frequency distributions.
	  
	  ``-e``, ``–-discrete_calls`` :white:`###` *(str)* :white:`###` Set to "dominant" to transform haplotype frequency values into presence(1)/absence(0) calls per allele, or "dosage" to indicate the allele copy number.
	  
	  ``-i``, ``--frequency_interval_bounds`` :white:`##` Frequency interval bounds for classifying the read frequencies into discrete calls. Custom thresholds can be defined by passing one or more space-separated integers or floats which represent relative frequencies in percentage. For dominant calling, one value should be specified. For dosage calling, an even total number of four or more thresholds should be specified. Defaults are used by passing either "diploid" or "tetraploid". The default value for dominant calling (see discrete_calls argument) is 10, regardless whether or not "diploid" or "tetraploid" is used. For dosage calling, the default for diploids is "10 10 90 90" and for tetraploids "12.5 12.5 37.5 37.5 62.5 62.5 87.5 87.5"
	  
	  ``-z``, ``--dosage_filter`` :white:`###` *(int)* :white:`###` Mask dosage calls in the loci for which the total allele count for a given locus at a given sample differs from the defined value. For example, in diploid organisms the total allele copy number must be 2, and in tetraploids the total allele copy number must be 4. (default no filtering).
	 
	  ``--locus_correctness`` :white:`########` *(int)* :white:`###` Threshold value: % of samples with locus correctness. Create a new .bed file defining only the loci that were correctly dosage called (-z) in at least the defined percentage of samples (default no filtering).
	  
	  ``--frequency_interval_bounds`` in practical examples and additional information on the dosage filter can be found in the section on recommendations.

----


Examples
--------

:navy:`HiPlex`

.. tabs::


   .. tab:: diploid pool, HiPlex, merged reads
	  
	  ::
			
			smap haplotype-sites /path/to/BAM/ /path/to/BED/ /path/to/VCF/ -mapping_orientation ignore -partial exclude --no_indels --min_read_count 30 -f 2 -p 8 --min_distinct_haplotypes 2 --plot_type png --plot all -o 2n_pool_HiPlex_NI_NP
			
   .. tab:: diploid individual, HiPlex, merged reads, dominant :white:`######`
	  
	  ::
			
			smap haplotype-sites /path/to/BAM/ /path/to/BED/ /path/to/VCF/ -mapping_orientation ignore -partial exclude --min_read_count 10 -f 1 -p 8 --min_distinct_haplotypes 2 --plot_type png --plot all -o 2n_ind_HiPlex_NI_NP_DOMdiplo --discrete_calls dominant --frequency_interval_bounds 10

   .. tab:: diploid individual, HiPlex, merged reads, dosage :white:`######`
	  
	  ::
			
			smap haplotype-sites /path/to/BAM/ /path/to/BED/ /path/to/VCF/ -mapping_orientation ignore -partial exclude --no_indels --min_read_count 10 -f 1 -p 8 --min_distinct_haplotypes 2 --plot_type png --plot all -o 2n_ind_HiPlex_NI_NP_DOSdiplo --discrete_calls dosage --frequency_interval_bounds 10 10 90 90 --dosage_filter 2

   .. tab:: tetraploid individual, HiPlex, merged reads, dominant :white:`######`
	  
	  ::
	  
			smap haplotype-sites /path/to/BAM/ /path/to/BED/ /path/to/VCF/ -mapping_orientation ignore -partial exclude --no_indels --discrete_calls dominant --frequency_interval_bounds 10 --min_read_count 10 -f 5 -p 8 --min_distinct_haplotypes 2 --plot_type png --plot all -o 4n_ind__NI_NP_DOMtetra

   .. tab:: tetraploid individual, HiPlex, merged reads, dosage :white:`######`
	  
	  ::
	  
			smap haplotype-sites /path/to/BAM/ /path/to/BED/ /path/to/VCF/ -mapping_orientation ignore -partial exclude --no_indels --discrete_calls dosage --frequency_interval_bounds 12.5 12.5 37.5 37.5 62.5 62.5 87.5 87.5 --dosage_filter 4 --min_read_count 10 -f 5 -p 8 --min_distinct_haplotypes 2 --plot_type png --plot all -o 4n_ind__NI_NP_DOStetra


:navy:`Shotgun`

.. tabs::

   .. tab:: diploid individual, Shotgun-SE, SVs, dosage

	  ::
		
			smap haplotype-sites /path/to/BAM/ /path/to/BED/ /path/to/VCF/ -mapping_orientation stranded -partial include --min_read_count 10 -f 5 -p 8 --min_distinct_haplotypes 2 --plot_type png --plot all -o 2n_ind_GBS_SE_NI_DOMdiplo --discrete_calls dosage --frequency_interval_bounds diploid

:navy:`GBS`

.. tabs::

   .. tab:: diploid pool, single-enzyme GBS, single-end reads
	  
	  ::
			
			smap haplotype-sites /path/to/BAM/ /path/to/BED/ /path/to/VCF/ -mapping_orientation stranded -partial include --no_indels --min_read_count 30 -f 2 -p 8 --min_distinct_haplotypes 2 --plot_type png --plot all -o 2n_pool_GBS_SE_NI

   .. tab:: diploid pool, double-enzyme GBS, merged reads

	  ::
			
			smap haplotype-sites /path/to/BAM/ /path/to/BED/ /path/to/VCF/ -mapping_orientation ignore -partial include --no_indels --min_read_count 30 -f 2 -p 8 --min_distinct_haplotypes 2 --plot_type png --plot all -o 2n_pools_GBS_PE_NI

   .. tab:: tetraploid pool, single-enzyme GBS, merged reads
	  
	  ::
			
			smap haplotype-sites /path/to/BAM/ /path/to/BED/ /path/to/VCF/ -mapping_orientation ignore -partial include --no_indels --min_read_count 30 -f 2 -p 8 --min_distinct_haplotypes 2 --plot_type png --plot all -o 4n_pools_GBS_PE_NI

   .. tab:: diploid individual, single-enzyme GBS, single-end reads, dosage

	  ::
		
			smap haplotype-sites /path/to/BAM/ /path/to/BED/ /path/to/VCF/ -mapping_orientation stranded -partial include --no_indels --min_read_count 10 -f 5 -p 8 --min_distinct_haplotypes 2 --plot_type png --plot all -o 2n_ind_GBS_SE_NI_DOSdiplo --discrete_calls dosage --frequency_interval_bounds 10 10 90 90 --dosage_filter 2

   .. tab:: diploid individual, double-enzyme GBS, merged reads, dominant
	  
	  ::
		
			smap haplotype-sites /path/to/BAM/ /path/to/BED/ /path/to/VCF/ -mapping_orientation ignore -partial include --no_indels --min_read_count 10 -f 5 -p 8 --min_distinct_haplotypes 2 --plot_type png --plot all -o 2n_ind_GBS_PE_NI_DOMdiplo --discrete_calls dominant --frequency_interval_bounds 10

   .. tab:: diploid individual, double-enzyme GBS, merged reads, dosage

	  ::

			smap haplotype-sites /path/to/BAM/ /path/to/BED/ /path/to/VCF/ -mapping_orientation ignore -partial include --no_indels --min_read_count 10 -f 5 -p 8 --min_distinct_haplotypes 2 --plot_type png --plot all -o 2n_ind_GBS_PE_NI_DOSdiplo --discrete_calls dosage --frequency_interval_bounds 10 10 90 90 --dosage_filter 2

   .. tab:: tetraploid individual, single-enzyme GBS, merged reads, dominant
	  
	  ::
	  
			smap haplotype-sites /path/to/BAM/ /path/to/BED/ /path/to/VCF/ -mapping_orientation ignore -partial include --no_indels --discrete_calls dominant --frequency_interval_bounds 10 --min_read_count 10 -f 5 -p 8 --min_distinct_haplotypes 2 --plot_type png --plot all -o 4n_ind_GBS_PE_NI_DOMtetra

   .. tab:: tetraploid individual, single-enzyme GBS, merged reads, dosage
	  
	  ::

			smap haplotype-sites /path/to/BAM/ /path/to/BED/ /path/to/VCF/ -mapping_orientation ignore -partial include --no_indels --discrete_calls dosage --frequency_interval_bounds 12.5 12.5 37.5 37.5 62.5 62.5 87.5 87.5 --dosage_filter 4 --min_read_count 10 -f 5 -p 8 --min_distinct_haplotypes 2 --plot_type png --plot all -o 4n_ind_GBS_PE_NI_DOStetra

