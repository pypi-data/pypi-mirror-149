.. raw:: html

    <style> .navy {color:navy} </style>
	
.. role:: navy

.. raw:: html

    <style> .white {color:white} </style>

.. role:: white

############################
Pools
############################

Step 4: Filtering haplotypes and calculating haplotype frequencies
------------------------------------------------------------------

procedure
~~~~~~~~~

After processing all BAM files in the given directory and storing all observed haplotypes in a table for each sample, **SMAP haplotype-sites** loops over all tables to create an integrated genotyping matrix that contains all observed haplotypes across all BAM files and collects their absolute read counts. The next step is to switch from absolute read count per haplotype to relative read depth per haplotype per Locus, *i.e.* to calculate haplotype frequencies. The haplotype frequency is calculated per haplotype per locus per sample (haplotype count per sample/total read count per Locus per sample; range 0-100%).

.. image:: ../../images/sites/SMAP_haplotype_step5_Shotgun.png

filters
~~~~~~~

:navy:`read errors create false positive haplotypes`

Randomly distributed read errors that happen to co-localize with the SMAP/SNP positions erroneously create low frequency haplotypes. Example data are shown in the scheme above, see tables below for the occurence in real GBS data of 8 diploid individuals. 

:navy:`false positive haplotypes are removed from the data set with a minimum frequency threshold (option` ``-f``:navy:`)`

Haplotypes that never reach a user-defined minimum haplotype frequency threshold (default 0%) *in at least one* of the BAM files, are removed entirely from the haplotype count table. After this filter, the haplotype frequency is *recalculated* on the remaining read counts per haplotype per Locus per BAM file. The effect of adjusting this filter is illustrated in real data in the tables below. Please compare the tables below at subsequent steps of filtering: ``-f 0`` filtering is effectively no filter (all haplotype observations > 0% are kept). Most noise from low frequency haplotypes can effectively be removed with ``-f 1`` or ``-f 5`` . We recommend to test the effect of this parameter on your own data, as it depends on if you want to retain low frequency alleles or not. Please inspect the haplotype frequency histograms to estimate relevant values for your data (see Graphical output).

:navy:`low frequency haplotypes may also be masked (per locus/sample) using the frequency_mask (option` ``-m``:navy:`)`

Haplotypes that reach the user defined ``-f`` value in at least one BAM file are retained. However, observations of the same haplotype in other BAM files but with a haplotype frequency lower than the ``-f`` value are also retained, potentially allowing noise. These values may additionaly be masked with option ``-m``.
The option ``-m`` masks all haplotype frequencies lower than set value by substituting them with NaN's or another value defined by ``--undefined_representation``. The other haplotype frequencies are *not recalculated*.


.. tabs::

   .. tab:: info
      
	  The following tabs show real experimental data of two loci. All detected haplotypes are reported using the default ``-f 0``, demonstrating how haplotype frequency filtering removes noise.
  
   .. tab:: *-f 0* filtering
	  
	  .. csv-table:: 	  
	     :file: ../.././tables/sites/2n_ind_GBS_SE_NI_DOSdiplo_FR_R10_F0.csv
	     :header-rows: 1
	  
   .. tab:: *-f 1* filtering
	  
	  .. csv-table:: 	  
	     :file: ../.././tables/sites/2n_ind_GBS_SE_NI_DOSdiplo_FR_R10_F1.csv
	     :header-rows: 1
	  
   .. tab:: *-f 5* filtering
	  
	  .. csv-table:: 	  
	     :file: ../.././tables/sites/2n_ind_GBS_SE_NI_DOSdiplo_FR_R10_F5.csv
	     :header-rows: 1

   .. tab:: *-f 5* and *-m 1* filtering
	  
	  .. csv-table:: 	  
	     :file: ../.././tables/sites/2n_ind_GBS_SE_NI_DOSdiplo_FR_R10_F5_M1.csv
	     :header-rows: 1

   .. tab:: *-f 5* and *-m 5* filtering
	  
	  .. csv-table:: 	  
	     :file: ../.././tables/sites/2n_ind_GBS_SE_NI_DOSdiplo_FR_R10_F5_M5.csv
	     :header-rows: 1

After filtering out low frequency haplotypes the final haplotype frequency table is created. This is the end point for analysis of Pool-Seq data.

Haplotype frequency distributions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The different tabs below show the typical haplotype frequency distributions of GBS or HiPlex data in pools. The commands to run **SMAP haplotype-sites** on these datatypes are shown below each graph.

.. tabs::

   .. tab:: diploid pool, single-enzyme GBS, single-end reads
	  
	  .. image:: ../../images/sites/2n_pools_GBS_SE_001.haplotype.frequency.histogram.png
	  
	  ::
			
			smap haplotype-sites /path/to/BAM/ /path/to/BED/ /path/to/VCF/ -mapping_orientation stranded -partial include --no_indels --min_read_count 30 -f 2 -p 8 --min_distinct_haplotypes 2 --plot_type png --plot all -o 2n_pool_GBS_SE_NI

   .. tab:: diploid pool, double-enzyme GBS, merged reads
	  
	  .. image:: ../../images/sites/2n_pools_GBS_PE_001.scaff.haplotype.frequency.histogram.png

	  ::
			
			smap haplotype-sites /path/to/BAM/ /path/to/BED/ /path/to/VCF/ -mapping_orientation ignore -partial include --no_indels --min_read_count 30 -f 2 -p 8 --min_distinct_haplotypes 2 --plot_type png --plot all -o 2n_pools_GBS_PE_NI

   .. tab:: tetraploid pool, single-enzyme GBS, merged reads
	  
	  .. image:: ../../images/sites/4n_pools_GBS_PE_001.scaff.haplotype.frequency.histogram.png
	  
	  ::
				
			smap haplotype-sites /path/to/BAM/ /path/to/BED/ /path/to/VCF/ -mapping_orientation ignore -partial include --no_indels --min_read_count 30 -f 2 -p 8 --min_distinct_haplotypes 2 --plot_type png --plot all -o 4n_pools_GBS_PE_NI

   .. tab:: diploid pool, HiPlex, merged reads :white:`###`
	  
	  .. image:: ../../images/sites/2n_pools_HiPlex_PE_001.haplotype.frequency.histogram.png
	  
	  ::
			
			smap haplotype-sites /path/to/BAM/ /path/to/BED/ /path/to/VCF/ -mapping_orientation ignore -partial exclude --no_indels --min_read_count 30 -f 2 -p 8 --min_distinct_haplotypes 2 --plot_type png --plot all -o 2n_pool_HiPlex_NI_NP

Output
------

**Tabular output**

.. tabs::

   .. tab:: General output

      By default, **SMAP haplotype-sites** will return two .tsv files.  
 
      :navy:`haplotype counts`
      
      **Read_counts_cx_fx_mx.tsv** (with x the value per option used in the analysis) contains the read counts (``-c``) and haplotype frequency (``-f``) filtered and/or masked (``-m``) read counts per haplotype per locus as defined in the BED file from **SMAP delineate**.  
      This is the file structure:
      
		============ ========== ======= ======= ========
		Locus        Haplotypes Sample1 Sample2 Sample..
		============ ========== ======= ======= ========
		Chr1:100-200 00010      0       13      34
		Chr1:100-200 01000      19      90      28
		Chr1:100-200 00110      60      0       23	
		Chr1:450-600 0010       70      63      87
		Chr1:450-600 0110       108     22      134
		============ ========== ======= ======= ========

      :navy:`relative haplotype frequency`
      
      **Haplotype_frequencies_cx_fx_mx.tsv** contains the relative frequency per haplotype per locus in sample (based on the corresponding count table: Read_counts_cx_fx_mx.tsv). The transformation to relative frequency per locus-sample combination inherently normalizes for differences in total number of mapped reads across samples, and differences in amplification efficiency across loci.  
      This is the file structure:
      
		============ ========== ======= ======= ========
		Locus        Haplotypes Sample1 Sample2 Sample..
		============ ========== ======= ======= ========
		Chr1:100-200 00010      0       0.13    0.40
		Chr1:100-200 01000      0.24    0.87    0.33
		Chr1:100-200 00110      0.76    0       0.27
		Chr1:450-600 0010       0.39    0.74    0.39
		Chr1:450-600 0110       0.61    0.26    0.61
		============ ========== ======= ======= ========
		
**Graphical output**

:navy:`haplotype diversity`

.. tabs::

   .. tab:: haplotype diversity across sampleset
	
	 By default, **SMAP haplotype-sites** will generate graphical output summarizing haplotype diversity. haplotype_diversity_across_sampleset.png shows a histogram of the number of distinct haplotypes per locus *across* all samples.  
     
   .. tab:: example graph
	
	  .. image:: ../../images/sites/haplotype_counts.cigar.barplot.png


:navy:`haplotype frequency distribution per sample`

.. tabs::

   .. tab:: haplotype frequency distribution per sample
	 
     Graphical output of the haplotype frequency distribution for each individual sample can be switched **on** using the option ``--plot_all``. sample_haplotype_frequency_distribution.png shows the haplotype frequency distribution across all loci detected per sample. It is the graphical representation of each sample-specific column in **haplotypes_cx_fx_mx.tsv**. Using the option ``--discrete_calls``, this plot will also show the defined discrete calling boundaries.

   .. tab:: example graph
	
	  .. image:: ../../images/sites/2n_ind_GBS_SE_001.bam.haplotype.frequency.histogram.png

:navy:`quality of genotype calls per locus and per sample`

.. tabs::

   .. tab:: QC of loci and samples using discrete dosage calls  
	
	 After discrete genotype calling with option ``--discrete_calls``, **SMAP haplotype-sites** will evaluate the observed sum of discrete dosage calls per locus per sample versus the expected value per locus (set with option ``-z``, recommended use: 2 for diploid, 4 for tetraploid). 
     
     The quality of genotype calls per *sample* is calculated in two ways: the fraction of loci with calls in that sample versus the total number of loci across all samples (sample_call_completeness); the fraction of loci with expected sum of discrete dosage calls (``-z``) versus the total number of observed loci in that sample (sample_call_correctness). These scores are calculated separately per *sample*, and **SMAP haplotype-sites** plots the distribution of those scores across the sample set (sampleset_call_completeness; sampleset_call_correctness).  
      
     Similarly, the quality of genotype calls per *locus* is calculated in two ways: the fraction of samples with calls for that locus versus the total number of samples (locus_call_completeness); the fraction of samples with expected sum of discrete dosage calls (``-z``) versus the total number of observed samples for that locus (locus_call_correctness). These scores are calculated separately per *locus*, and **SMAP haplotype-sites** plots the distribution of those scores across the locus set (locusset_call_completeness; locusset_call_correctness).  
      
     Both graphs and the corresponding tables (one for samples and one for loci) can be evaluated to identify poorly performing samples and/or loci. We recommend to eliminate these from further analysis by removing BAM files from the run directory and/or loci from the SMAP delineate BED file with SMAPs, and iterate through rounds of data analysis combined with sample and locus quality control.

   .. tab:: completeness and correctness per sample
	
	  .. image:: ../../images/sites/sample_call_completeness_correctness_40canephora.png
	  
   .. tab:: completeness and correctness per locus
	
	  .. image:: ../../images/sites/locus_call_completeness_correctness_40canephora.png


----

Summary of Commands
-------------------

:navy:`Mandatory options:`

| **type of reads:** ``-mapping_orientation stranded`` or ``-mapping_orientation ignore`` 
|
| **locus coverage:** ``-partial include`` (for :ref:`GBS <SMAPhaploGBSpartial>`) or ``-partial exclude`` (for :ref:`HiPlex <SMAPhaploASpartialHiplex>` and for :ref:`Shotgun <SMAPhaploASpartialShotgun>`)

.. tabs::

   .. tab:: general options

	  | ``alignments_dir`` :white:`#############` *(str)* :white:`###` Path to the directory containing BAM and BAI files. All BAM files should be in the same directory. Positional mandatory argument, should be the **first** argument after ``smap haplotype-sites`` [no default].  
	  | ``bed`` :white:`#####################` *(str)* :white:`###` Path to the BED file containing sites for which haplotypes will be reconstructed. For GBS data, the BED file should be generated using :ref:`SMAP delineate <SMAPdelHIW>`. For HiPlex data, a BED6 file can be provided, with the 4th and 5th column left blank and the chromosome name, locus start position site, locus end position site and strand information populating the first, second, third and sixth column respectively. Positional mandatory argument, should be the **second** argument after ``smap haplotype-sites``.
	  | ``vcf`` :white:`#####################` *(str)* :white:`###` Path to the VCF file (in VCFv4.1 format) containing variant positions. It should contain at least the first 9 columns listing the SNP positions. Sample-specific genotype calls across the sample set are not required. Positional mandatory argument, should be the **third** argument after ``smap haplotype-sites``.
	  | ``-p``, ``--processes`` :white:`###########` *(int)* :white:`###` Number of parallel processes [1].
	  | ``--plot`` :white:`#########################` Select which plots are to be generated. Choosing "nothing" disables plot generation. Passing "summary" only generates graphs with information for all samples while "all" will also enable generate per-sample plots [default "summary"].
	  | ``-t``, ``--plot_type`` :white:`##################` Use this option to choose plot format, choices are png and pdf [png].  
	  | ``-o``, ``--out`` :white:`###############` *(str)* :white:`###` Basename of the output file without extension [SMAP_haplotype_sites].
	  | ``-u``, ``--undefined_representation`` :white:`#######` Value to use for non-existing or masked data [NaN].
	  | ``-h``, ``--help`` :white:`#####################` Show the full list of options. Disregards all other parameters.
	  | ``-v``, ``--version`` :white:`###################` Show the version. Disregards all other parameters.
	  | ``--debug`` :white:`########################` Enable verbose logging.
	  | ``--cervus`` :white:`########################` As an additional output file, create an output table that can be used with `Cervus <http://www.fieldgenetics.com/pages/aboutCervus_Overview.jsp>`. Only available while also creating a discrete calls table.
	  | 
	  | Options may be given in any order.
	  
   .. tab:: filtering options

	  | ``-q``, ``--min_mapping_quality`` :white:`####` *(int)* :white:`###` Minimum .bam mapping quality for reads to be included in the analysis [30].
	  | ``--no_indels`` :white:`#####################` Use this option if you want to **exclude** haplotypes that contain an InDel at the given SNP/SMAP positions. These reads are also ignored to evaluate the minimum read count [default off; indels are included in output].
	  | ``-j``, ``--min_distinct_haplotypes`` :white:`#` *(int)* :white:`###` Minimum number of distinct haplotypes per locus across all samples. Loci that do not fit this criterium are removed from the final output [0].
	  | ``-k``, ``--max_distinct_haplotypes`` :white:`#` *(int)* :white:`###` Maximum number of distinct haplotypes per locus across all samples. Loci that do not fit this criterium are removed from the final output [inf].
	  | ``-c``, ``--min_read_count`` :white:`#######` *(int)* :white:`###` Minimum total number of reads per locus per sample [0].
	  | ``-d``, ``--max_read_count`` :white:`#######` *(int)* :white:`###` Maximum number of reads per locus per sample, read count is calculated after filtering out the low frequency haplotypes (``-f``) [inf].
	  | ``-f``, ``--min_haplotype_frequency`` :white:`#` *(float)* :white:`##` Set minimum haplotype frequency (in %) to retain the haplotype in the genotyping matrix. Haplotypes above this threshold in at least one of the samples are retained. Haplotypes that never reach this threshold in any of the samples are removed [0].
	  | ``-m``, ``--mask_frequency`` :white:`#######` *(float)* :white:`##` Mask haplotype frequency values below this threshold for individual samples to remove noise from the final output. Haplotype frequency values below this threshold are set to ``-u``. Haplotypes are not removed based on this value, use ``--min_haplotype_frequency`` for this purpose instead.
	  | 
	  | Options may be given in any order.
