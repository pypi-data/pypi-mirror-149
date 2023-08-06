.. raw:: html

    <style> .navy {color:navy} </style>
	
.. role:: navy

.. raw:: html

    <style> .white {color:white} </style>

.. role:: white

############################
Individuals
############################

.. _SMAPhaplostep4:

Step 4: Filtering haplotypes and calculating haplotype frequencies
------------------------------------------------------------------

procedure
~~~~~~~~~

After processing all BAM files in the given directory and storing all observed haplotypes in a table for each sample, **SMAP haplotype-sites** loops over all tables to create an integrated genotyping matrix that contains all observed haplotypes across all BAM files and collects their absolute read counts. The next step is to switch from absolute read count per haplotype to relative read depth per haplotype per locus, *i.e.* to calculate haplotype frequencies. The haplotype frequency is calculated per haplotype per locus per sample (haplotype count per sample/total read count per locus per sample; range 0-100%).

.. image:: ../../images/sites/SMAP_haplotype_step4_Shotgun.png

.. _SMAPhaplofilter:

filters
~~~~~~~

:navy:`read errors create false positive haplotypes`

Randomly distributed read errors that happen to co-localize with the SMAP/SNP positions erroneously create low frequency haplotypes. Example data are shown in the scheme above, see tables below for the occurence in real GBS data of 8 diploid individuals.

:navy:`false positive haplotypes are removed from the data set with a minimum frequency threshold (option` ``-f``:navy:`)`

Haplotypes that never reach a user-defined minimum haplotype frequency threshold (default 0%) *in at least one* of the samples, are removed entirely from the haplotype count table. After this filter, the haplotype frequency is *recalculated* on the remaining read counts per haplotype per locus per sample. The effect of adjusting this filter is illustrated in real data in the tables below. Please compare the tables below at subsequent steps of filtering: ``-f 0`` filtering is effectively no filter (all haplotype observations > 0% are kept). Most noise from low frequency haplotypes can effectively be removed with ``-f 1`` or ``-f 5`` . We recommend to test the effect of this parameter on your own data, and to inspect the haplotype frequency histograms generated (see Graphical output). 

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

.. _SMAPhaplofreq:

Haplotype frequency distributions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The different tabs below show the typical haplotype frequency distributions of diploid or tetraploid individuals for GBS or HiPlex data. Vertical lines in the haplotype frequency distributions show the thresholds by which haplotype frequency is transformed into discrete call classes. The commands to run **SMAP haplotype-sites** on these datatypes are shown below each graph.
	  
.. tabs::

   .. tab:: diploid individual, single-enzyme GBS, single-end reads, **dominant**
	  
	  .. image:: ../../images/sites/2n_ind_GBS_SE_Dom_001.haplotype.frequency.histogram.png
	  
	  ::
		
			smap haplotype-sites /path/to/BAM/ /path/to/BED/ /path/to/VCF/ -mapping_orientation stranded -partial include --no_indels --min_read_count 10 -f 5 -p 8 --min_distinct_haplotypes 2 --plot_type png --plot all -o 2n_ind_GBS_SE_NI_DOMdiplo --discrete_calls dominant --frequency_interval_bounds 10 

   .. tab:: diploid individual, single-enzyme GBS, single-end reads, **dosage**
	  
	  .. image:: ../../images/sites/2n_ind_GBS_SE_Dos_001.haplotype.frequency.histogram.png
	  
	  ::
		
			smap haplotype-sites /path/to/BAM/ /path/to/BED/ /path/to/VCF/ -mapping_orientation stranded -partial include --no_indels --min_read_count 10 -f 5 -p 8 --min_distinct_haplotypes 2 --plot_type png --plot all -o 2n_ind_GBS_SE_NI_DOSdiplo --discrete_calls dosage --frequency_interval_bounds 10 10 90 90 --dosage_filter 2

   .. tab:: diploid individual, double-enzyme GBS, merged reads, **dominant**
	  
	  .. image:: ../../images/sites/2n_ind_GBS_PE_Dom_001.haplotype.frequency.histogram.png
	  
	  ::
		
			smap haplotype-sites /path/to/BAM/ /path/to/BED/ /path/to/VCF/ -mapping_orientation ignore -partial include --no_indels --min_read_count 10 -f 5 -p 8 --min_distinct_haplotypes 2 --plot_type png --plot all -o 2n_ind_GBS_PE_NI_DOMdiplo --discrete_calls dominant --frequency_interval_bounds 10

   .. tab:: diploid individual, double-enzyme GBS, merged reads, **dosage**
	  
	  .. image:: ../../images/sites/2n_ind_GBS_PE_Dos_001.haplotype.frequency.histogram.png
	  
	  ::
		
			smap haplotype-sites /path/to/BAM/ /path/to/BED/ /path/to/VCF/ -mapping_orientation ignore -partial include --no_indels --min_read_count 10 -f 5 -p 8 --min_distinct_haplotypes 2 --plot_type png --plot all -o 2n_ind_GBS_PE_NI_DOSdiplo --discrete_calls dosage --frequency_interval_bounds 10 10 90 90 --dosage_filter 2

   .. tab:: diploid individual, HiPlex, merged reads, **dominant** :white:`#####`
	  
	  .. image:: ../../images/sites/2n_ind_HiPlex_PE_Dom_001.haplotype.frequency.histogram.png
	  
	  ::
			
			smap haplotype-sites /path/to/BAM/ /path/to/BED/ /path/to/VCF/ -mapping_orientation ignore -partial exclude --no_indels --min_read_count 10 -f 1 -p 8 --min_distinct_haplotypes 2 --plot_type png --plot all -o 2n_ind_HiPlex_NI_NP_DOMdiplo --discrete_calls dominant --frequency_interval_bounds 10

   .. tab:: diploid individual, HiPlex, merged reads, **dosage** :white:`#####`
	  
	  .. image:: ../../images/sites/2n_ind_HiPlex_PE_Dos_001.haplotype.frequency.histogram.png
	  
	  ::
			
			smap haplotype-sites /path/to/BAM/ /path/to/BED/ /path/to/VCF/ -mapping_orientation ignore -partial exclude --no_indels --min_read_count 10 -f 1 -p 8 --min_distinct_haplotypes 2 --plot_type png --plot all -o 2n_ind_HiPlex_NI_NP_DOSdiplo --discrete_calls dosage --frequency_interval_bounds 10 10 90 90 --dosage_filter 2

   .. tab:: tetraploid individual, HiPlex, merged reads, **dominant** :white:`#####`
	  
	  .. image:: ../../images/sites/4n_ind_HiPlex_PE_Dom_001.haplotype.frequency.histogram.png
	  
	  ::
	  
			smap haplotype-sites /path/to/BAM/ /path/to/BED/ /path/to/VCF/ -mapping_orientation ignore -partial exclude --no_indels --discrete_calls dominant --frequency_interval_bounds 10 --min_read_count 10 -f 5 -p 8 --min_distinct_haplotypes 2 --plot_type png --plot all -o 4n_ind__NI_NP_DOMtetra

   .. tab:: tetraploid individual, HiPlex, merged reads, **dosage** :white:`#####`
	  
	  .. image:: ../../images/sites/4n_ind_HiPlex_PE_Dos_001.haplotype.frequency.histogram.png
	  
	  ::
	  
			smap haplotype-sites /path/to/BAM/ /path/to/BED/ /path/to/VCF/ -mapping_orientation ignore -partial exclude --no_indels --discrete_calls dosage --frequency_interval_bounds 12.5 12.5 37.5 37.5 62.5 62.5 87.5 87.5 --dosage_filter 4 --min_read_count 10 -f 5 -p 8 --min_distinct_haplotypes 2 --plot_type png --plot all -o 4n_ind__NI_NP_DOStetra
	  
	  
   .. tab:: tetraploid individual, single-enzyme GBS, merged reads, **dominant**
	  
	  .. image:: ../../images/sites/4n_ind_GBS_PE_Dom_001.haplotype.frequency.histogram.png
	  
	  ::
	  
			smap haplotype-sites /path/to/BAM/ /path/to/BED/ /path/to/VCF/ -mapping_orientation ignore -partial include --no_indels --discrete_calls dominant --frequency_interval_bounds 10 --min_read_count 10 -f 5 -p 8 --min_distinct_haplotypes 2 --plot_type png --plot all -o 4n_ind_GBS_PE_NI_DOMtetra

   .. tab:: tetraploid individual, single-enzyme GBS, merged reads, **dosage**
	  
	  .. image:: ../../images/sites/4n_ind_GBS_PE_Dos_001.haplotype.frequency.histogram.png
	  
	  ::
	  
			smap haplotype-sites /path/to/BAM/ /path/to/BED/ /path/to/VCF/ -mapping_orientation ignore -partial include --no_indels --discrete_calls dosage --frequency_interval_bounds 12.5 12.5 37.5 37.5 62.5 62.5 87.5 87.5 --dosage_filter 4 --min_read_count 10 -f 5 -p 8 --min_distinct_haplotypes 2 --plot_type png --plot all -o 4n_ind_GBS_PE_NI_DOStetra
		
----

.. _SMAPhaplostep5:
			
Step 5: Transforming haplotype frequencies to discrete calls in individuals
---------------------------------------------------------------------------

procedure
~~~~~~~~~~

If individual genotypes are analysed in, the final step is to transform observed haplotype frequencies per individual back to discrete haplotype calls using ``--discrete_calls``. **SMAP haplotype-sites** uses simple, user-defined haplotype frequency thresholds to define discrete genotypic classes. The multi-allelic nature of haplotype calling is retained, and the final genotype call table lists the absence/presence (0/1) or dosage (0/1/2 diploids; 0/1/2/3/4 tetraploids) of each haplotype per individual.

Next, the total count of discrete haplotypes per locus per sample is calculated and output as a table. See examples below.

Alternatively, haplotype read depth data generated with **SMAP haplotype-sites** may be used as input for genotype calling in individuals using statistical methods, for instance `Clark et al. 2019 <https://www.g3journal.org/content/9/3/663>`_.

.. image:: ../../images/sites/SMAP_haplotype_step6.png

Haplotype count tables
~~~~~~~~~~~~~~~~~~~~~~

If **SMAP haplotype-sites** is run using ``--discrete_calls`` the analysis continues by creating discrete haplotype calls per individual sample. For each sample and for each locus, haplotype frequencies are transformed to discrete calls using simple user-defined frequency thresholds based on the observed haplotype frequency spectrum.

Next, the total count of discrete haplotypes per locus per sample is calculated and output as table. See examples below.

.. tabs::

   .. tab:: *-f 0* filtering
	  
	  Per diploid sample, loci with a total haplotype count different from a set value (``--dosage_filter``) are removed (set to \`NaN´ \). The recommended value for this filter is 2 for diploids and 4 for tetraploids. The haplotype frequency is then calculated across the set of samples (count per haplotype/total haplotype count per locus \* \ 100%). This measure identifies the haplotypes that are supported by sufficient read depth in individual genotypes, but rare across the sample set (*e.g.* population).

   .. tab:: *-f 0* table
	  
	  ===================== ===================== ===================== ===================== ===================== ===================== ===================== ===================== =====================
	  Locus                 2n_ind_GBS-SE_001.bam 2n_ind_GBS-SE_002.bam 2n_ind_GBS-SE_003.bam 2n_ind_GBS-SE_004.bam 2n_ind_GBS-SE_005.bam 2n_ind_GBS-SE_006.bam 2n_ind_GBS-SE_007.bam 2n_ind_GBS-SE_008.bam
	  ===================== ===================== ===================== ===================== ===================== ===================== ===================== ===================== =====================
	  Chrom_1:15617-15711/+ 2                     2                     2                     2                     2                                      2                     2                     1
	  Chrom_1:15712-15798/- 2                     2                     2                     2                     2                                      2                     2                     1
	  ===================== ===================== ===================== ===================== ===================== ===================== ===================== ===================== =====================

   .. tab:: *-f 1* filtering
	  
	  In ``-f 1`` filtering, haplotypes with a frequency lower than 1% across all samples are removed. This is done in order to remove noise. It is recommended to try out different values and decide which value suits your data best. 

   .. tab:: *-f 1* table
	  
	  ===================== ===================== ===================== ===================== ===================== ===================== ===================== ===================== =====================
	  Locus                 2n_ind_GBS-SE_001.bam 2n_ind_GBS-SE_002.bam 2n_ind_GBS-SE_003.bam 2n_ind_GBS-SE_004.bam 2n_ind_GBS-SE_005.bam 2n_ind_GBS-SE_006.bam 2n_ind_GBS-SE_007.bam 2n_ind_GBS-SE_008.bam
	  ===================== ===================== ===================== ===================== ===================== ===================== ===================== ===================== =====================
	  Chrom_1:15617-15711/+ 2                     2                     2                     2                     2                                      2                     2                     1
	  Chrom_1:15712-15798/- 2                     2                     2                     2                     2                                      2                     2                     1
	  ===================== ===================== ===================== ===================== ===================== ===================== ===================== ===================== =====================

   .. tab:: *-f 5* filtering
	  
	  In ``-f 5`` filtering, haplotypes with a frequency lower than 5% across all samples are removed. This is done in order to remove noise. It is recommended to try out different values and decide which value suits your data best. 

   .. tab:: *-f 5* table
	  
	  ===================== ===================== ===================== ===================== ===================== ===================== ===================== ===================== =====================
	  Locus                 2n_ind_GBS-SE_001.bam 2n_ind_GBS-SE_002.bam 2n_ind_GBS-SE_003.bam 2n_ind_GBS-SE_004.bam 2n_ind_GBS-SE_005.bam 2n_ind_GBS-SE_006.bam 2n_ind_GBS-SE_007.bam 2n_ind_GBS-SE_008.bam
	  ===================== ===================== ===================== ===================== ===================== ===================== ===================== ===================== =====================
	  Chrom_1:15617-15711/+ 2                     2                     2                     2                     2                                      2                     2                     1
	  Chrom_1:15712-15798/- 2                     2                     2                     2                     2                                      2                     2                     2
	  ===================== ===================== ===================== ===================== ===================== ===================== ===================== ===================== =====================

Haplotype call tables
~~~~~~~~~~~~~~~~~~~~~

.. tabs::

   .. tab:: *-f 0* filtering
	  
	  Haplotype allele frequencies are calculated as the number of observations of a haplotype divided by the total number of haplotype observations (ploidy (or ``--dosage_filter`` value) x number of samples with observations) on that locus. In ``-f 0`` filtering, all haplotypes are retained. It is recommended to try out different values and decide which value suits your data best. 
	  
   .. tab:: *-f 0* table
	  
	  .. csv-table:: 	  
	     :file: ../.././tables/sites/2n_ind_GBS_SE_haplo_call_f0.csv
	     :header-rows: 1

   .. tab:: *-f 1* filtering
	  
	  Haplotype allele frequencies are calculated as the number of observations of a haplotype divided by the total number of haplotype observations (ploidy (or ``--dosage_filter`` value) x number of samples with observations) on that locus. In ``-f 1`` filtering, haplotypes with a frequency lower than 1% across all samples are removed. This is done in order to remove noise. It is recommended to try out different values and decide which value suits your data best. 

   .. tab:: *-f 1* table
	  
	  .. csv-table:: 	  
	     :file: ../.././tables/sites/2n_ind_GBS_SE_haplo_call_f1.csv
	     :header-rows: 1

   .. tab:: *-f 5* filtering
	  
	  Haplotype allele frequencies are calculated as the number of observations of a haplotype divided by the total number of haplotype observations (ploidy (or ``--dosage_filter`` value) x number of samples with observations) on that locus. In ``-f 5`` filtering, haplotypes with a frequency lower than 5% across all samples are removed. This is done in order to remove noise. It is recommended to try out different values and decide which value suits your data best.

   .. tab:: *-f 5* table
	  
	  .. csv-table:: 	  
	     :file: ../.././tables/sites/2n_ind_GBS_SE_haplo_call_f5.csv
	     :header-rows: 1

.. _SMAPhaplostep6:
			
Step 6: Filtering for high quality dosage calls in individuals
--------------------------------------------------------------

procedure
~~~~~~~~~~

If individual genotypes are analysed in mode for dosage calls, the final step is to check if the total number of alleles equals that expected for the ploidy of the individual (2 in diploids, and 4 in tetraploids). All locus/sample combinations that do not show the expected number of haplotypes are removed from the genotyping table. In addition, two scores are calculated per sample: the completeness of observations across all tested loci, and the proportion of loci with correct genotype call, across all observed loci for that sample. two scores are calculated per locus: the completeness of observations across all tested sample, and the proportion of samples with correct genotype call, across all observed samples for that locus. A list is created with loci that display a minimum correctness across all observations, and only good quality loci are reported in the final genotype table. **SMAP haplotype-sites** uses simple, user-defined correctness filters to select high quality genotyping data, and the final genotype call table lists the dosage (0/1/2 diploids; 0/1/2/3/4 tetraploids) of each haplotype per individual.


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
		
   .. tab:: Additional output for individuals
   
      For individuals, if the option ``--discrete_calls`` is used, the program will return three additional .tsv files. Their content and order of creation is shown in the image :ref:`above <SMAPhaplostep5>`.  
      
	  | :navy:`haplotype total discrete calls`
      
	  | The first file is called **haplotypes_cx_fx_mx_discrete_calls._total.tsv** and this file contains the total dosage calls, obtained after transforming haplotype frequencies into discrete calls, using the defined ``--frequency_interval_bounds``. The total sum of discrete dosage calls is expected to be 2 in diploids and 4 in tetraploids.

		============ ======= ======= ========
		Locus        Sample1 Sample2 Sample..
		============ ======= ======= ========
		Chr1:100-200 2       2       3       
		Chr1:450-600 2       2       2       
		============ ======= ======= ========
		
	  | :navy:`haplotype discrete calls`
	  
	  | The second file is **haplotypes_cx_fx_mx-discrete_calls_filtered.tsv**, which lists the discrete calls per locus per sample after ``--dosage_filter`` has removed loci per sample with an unexpected number of haplotype calls (as listed in haplotypes_cx_fx_mx_discrete_calls_total.tsv). The expected number of calls is set with option ``-z`` [use 2 for diploids, 4 for tetraploids].

		============ ========== ======= ======= ========
		Locus        Haplotypes Sample1 Sample2 Sample..
		============ ========== ======= ======= ========
		Chr1:100-200 00010         0       1       NA   
		Chr1:100-200 01000         1       1       NA   
		Chr1:100-200 00110         1       0       NA   
		Chr1:450-600 0010          1       1       1    
		Chr1:450-600 0110          1       1       1    
		============ ========== ======= ======= ========
		  
	  | :navy:`population haplotype frequencies`
	  
	  | The third file, **haplotypes_cx_fx_mx_Pop_HF.tsv**, lists the population haplotype frequencies (over all individual samples) based on the total number of discrete haplotype calls relative to the total number of calls per locus.

		============ ========== ====== =====
		Locus        Haplotypes Pop_HF count
		============ ========== ====== =====
		Chr1:100-200 00010      25.0   4    
		Chr1:100-200 01000      50.0   4    
		Chr1:100-200 00110      25.0   4    
		Chr1:450-600 0010       50.0   6    
		Chr1:450-600 0110       50.0   6    
		============ ========== ====== =====

	  | For individuals, if the option ``--locus_correctness`` is used in combination with ``--discrete_calls`` and ``--frequency_interval_bounds``, the programm will create a new .bed file **haplotypes_cx_fx_mx_correctness_loci.bed** (loci filtered from the input .bed file) containing only the loci that were correctly dosage called (-z) in at least the defined percentage of samples. :ref:`See above <SMAPhaplostep5>`.
	  
	  | :navy:`Loci with correct calls across the sample set`

		=============== ====== ====== ============================ ==================== ======= ================= ============== ======== =============
		Reference       Start  End    HiPlex_locus_name            Mean_read_depth      Strand  SMAPs             Completeness   nr_SMAPs Name
		=============== ====== ====== ============================ ==================== ======= ================= ============== ======== =============
		Chr1            100    200    Chr1_100-200                 .                    \+ \    100,199           .              2        HiPlex_Set1  
		Chr1            450    600    Chr1_450-600                 .                    \+ \    450,599           .              2        HiPlex_Set1  
		=============== ====== ====== ============================ ==================== ======= ================= ============== ======== =============
		
**Graphical output**

:navy:`haplotype diversity`

.. tabs::

   .. tab:: haplotype diversity across sample set
	
	 By default, **SMAP haplotype-sites** will generate graphical output summarizing haplotype diversity. haplotype_diversity_across_sampleset.png shows a histogram of the number of distinct haplotypes per locus *across* all samples.  
     
   .. tab:: example graph
	
	  .. image:: ../../images/sites/haplotype_counts.cigar.barplot.png


:navy:`haplotype frequency distribution per sample`

.. tabs::

   .. tab:: haplotype frequency distribution per sample
	 
     Graphical output of the haplotype frequency distribution for each individual sample can be switched **on** using the option ``--plot all``. sample_haplotype_frequency_distribution.png shows the haplotype frequency distribution across all loci detected per sample. It is the graphical representation of each sample-specific column in **haplotypes_cx_fx_mx.tsv**. Using the option ``--discrete_calls``, this plot will also show the defined discrete calling boundaries.

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
	  | ``bed`` :white:`#####################` *(str)* :white:`###` Path to the BED file containing sites for which haplotypes will be reconstructed. For GBS experiments, the BED file should be generated using :ref:`SMAP delineate <SMAPdelHIW>`. For HiPlex data, a BED6 file can be provided, with the 4th and 5th column being blank and the chromosome name, locus start position site, locus end position site and strand information populating the first, second, third and sixth column respectively. Positional mandatory argument, should be the **second** argument after ``smap haplotype-sites``.
	  | ``vcf`` :white:`#####################` *(str)* :white:`###` Path to the VCF file (in VCFv4.1 format) containing variant positions. It should contain at least the first 9 columns listing the SNP positions, sample-specific genotype calls across the sampleset are not required. Positional mandatory argument, should be the **third** argument after ``smap haplotype-sites``.
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
	  
   .. tab:: filtering options

	  | ``-q``, ``--min_mapping_quality`` :white:`####` *(int)* :white:`###` Minimum .bam mapping quality to retain reads for analysis [30].
	  | ``--no_indels`` :white:`#####################` Use this option if you want to **exclude** haplotypes that contain an InDel at the given SNP/SMAP positions. These reads are also ignored to evaluate the minimum read count [default off; indels are included in output].
	  | ``-j``, ``--min_distinct_haplotypes`` :white:`#` *(int)* :white:`###` Minimum number of distinct haplotypes per locus across all samples. Loci that do not fit this criterium are removed from the final output [0].
	  | ``-k``, ``--max_distinct_haplotypes`` :white:`#` *(int)* :white:`###` Maximum number of distinct haplotypes per locus across all samples. Loci that do not fit this criterium are removed from the final output [inf].
	  | ``-c``, ``--min_read_count`` :white:`#######` *(int)* :white:`###` Minimum total number of reads per locus per sample [0].
	  | ``-d``, ``--max_read_count`` :white:`#######` *(int)* :white:`###` Maximum number of reads per locus per sample, read count is calculated after filtering out the low frequency haplotypes (``-f``) [inf].
	  | ``-f``, ``--min_haplotype_frequency`` :white:`#` *(float)* :white:`##` Set minimum haplotype frequency (in %) to retain the haplotype in the genotyping matrix. Haplotypes above this threshold in at least one of the samples are retained. Haplotypes that never reach this threshold in any of the samples are removed [0].
	  | ``-m``, ``--mask_frequency`` :white:`#######` *(float)* :white:`##` Mask haplotype frequency values below this threshold for individual samples to remove noise from the final output. Haplotype frequency values below this threshold are set to ``-u``. Haplotypes are not removed based on this value, use ``--min_haplotype_frequency`` for this purpose instead.
	  | 
	  | Options may be given in any order.	  

	  
   .. tab:: options for discrete calling in individual samples
	  
	   This option is primarily supported for diploids and tetraploids. Users can define their own custom frequency bounds for species with a higher ploidy, but this requires optimization based on the observed haplotype frequency distributions.
	  
	  ``-e``, ``--discrete_calls`` :white:`###` *(str)* :white:`###` Set to "dominant" to transform haplotype frequency values into presence(1)/absence(0) calls per allele, or "dosage" to indicate the allele copy number.
	  
	  ``-i``, ``--frequency_interval_bounds`` :white:`##` Frequency interval bounds for classifying the read frequencies into discrete calls. Custom thresholds can be defined by passing one or more space-separated integers which represent relative frequencies in percentage. For dominant calling, one value should be specified. For dosage calling, an even total number of four or more thresholds should be specified. The usage of defaults can be enabled by passing either "diploid" or "tetraploid". The default value for dominant calling (see discrete_calls argument) is 10, regardless whether or not "diploid" or "tetraploid" is used. For dosage calling, the default for diploids is "10 10 90 90" and for tetraploids "12.5 12.5 37.5 37.5 62.5 62.5 87.5 87.5"
	  
	  ``-z``, ``--dosage_filter`` :white:`###` *(int)* :white:`###` Mask dosage calls in the loci for which the total allele count for a given locus at a given sample differs from the defined value. For example, in diploid organisms the total allele copy number must be 2, and in tetraploids the total allele copy number must be 4. (default no filtering).
	 
	  ``--locus_correctness`` :white:`########` *(int)* :white:`###` Threshold value: % of samples with locus correctness. Create a new BED file defining only the loci that were correctly dosage called (-z) in at least the defined percentage of samples (default no filtering).
	 
	  ``--frequency_interval_bounds`` in practical examples and additional information on the dosage filter can be found in the section recommendations.
