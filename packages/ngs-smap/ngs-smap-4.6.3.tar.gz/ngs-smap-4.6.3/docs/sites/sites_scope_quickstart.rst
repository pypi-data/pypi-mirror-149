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

:navy:`SMAP haplotype-sites: using polymorphic sites (SNPs, SVs, and/or SMAPs) for read-backed haplotyping`

| **SMAP haplotype-sites** reconstructs multi-allelic haplotypes based on a predefined set of polymorphisms at Single Nucleotide Polymorphisms (SNPs), breakpoints of Structural Variants (SVs) and/or Stack Mapping Anchor Points (:ref:`SMAPs <SMAPdeldef>`) through read-backed haplotyping.
| **SMAP haplotype-sites** can be used for \`stacked´ \ read data such as Genotyping-By-Sequencing (GBS) or highly multiplex amplicon sequencing (HiPlex), and for random fragmented (e.g. Shotgun Sequencing) read data.  

.. image:: ../images/sites/SMAP_sites_introduction_scheme.png

:navy:`SMAP haplotype-sites only requires this input:`
	
	1. a single BED file to define the start and end points of loci (loci created by :ref:`SMAP delineate <SMAPdelHIW>` for GBS, amplicon regions for HiPlex, and Sliding frames for Shotgun sequencing).
	2. a single VCF file containing bi-allelic SNPs obtained with third-party SNP calling software.
	3. a set of indexed BAM files for all samples that need to be compared.

| **SMAP haplotype-sites** performs read-backed haplotyping, per sample, per locus, per read, using positional information of read alignments and creates multi-allelic haplotypes from a short string of polymorphic *sites* (ShortHaps).
| **SMAP haplotype-sites** takes a conservative approach, without any form of imputation or phase extension, and strictly considers SNPs and/or SMAPs within a read for read-backed haplotyping.
| **SMAP haplotype-sites** filters out genotype calls of loci with low read counts, and low frequency haplotypes, to control for noise in the data.
| **SMAP haplotype-sites** creates a multi-allelic genotype call matrix listing haplotype calls, per sample, per locus, across the sample set.
| **SMAP haplotype-sites** always returns quantitative haplotype frequencies, useful for Pool-Seq data.
| **SMAP haplotype-sites** can also create discrete haplotype calls (expressed as either dominant or dosage calls) for individual samples.
| **SMAP haplotype-sites** plots the haplotype frequency distribution per sample.
| **SMAP haplotype-sites** plots a histogram of the number of haplotypes per locus across the sample set to show the haplotype diversity.

:navy:`Loci with sets of polymorphic sites`

| In the SMAP haplotype-sites workflow, the user first selects loci known to be covered by reads across the sample set. For HiPlex data, pairs of primers define locus positions. SNPs identified by third-party software that are located within these loci are combined into haplotypes, all other SNPs and all other non-polymorphic positions are excluded. For Shotgun data, dynamic sliding frames are used that bundle neighboring SNPs, based on a VCF file with known SNPs obtained by third-party software. For GBS data, read mapping polymorphisms (SMAPs, see :ref:`SMAP delineate <SMAPdelsepvmerg>`) define locus positions and may be combined with SNPs as molecular markers for haplotyping. (See for third-party SNP calling software: `SAMtools <http://www.htslib.org/>`_, `BEDtools <https://bedtools.readthedocs.io/en/latest/index.html>`_, `Freebayes <https://github.com/ekg/freebayes>`_, or `GATK <https://gatk.broadinstitute.org/hc/en-us>`_ for individuals, or `SNAPE-pooled <https://github.com/EmanueleRaineri/snape-pooled>`_ for Pool-Seq data. See also `Veeckman et al, 2019 <https://academic.oup.com/dnaresearch/article/26/1/1/5133005>`_ for a comparison of methods).

----
 
.. _SMAPhaploquickstart:

Quick Start
-----------

.. tabs::

   .. tab:: overview
	  
	  | The scheme below shows how **SMAP haplotype-sites** is integrated with `preprocessing <https://gbprocess.readthedocs.io/en/latest/index.html>`_, read mapping, locus delineation, and SNP calling. For GBS data, loci are positioned with :ref:`SMAP delineate <SMAPdelindex>`.
	  | Read-reference nucleotide pairs are retrieved by `pysam <https://pysam.readthedocs.io/en/latest/api.html>`_ 's ``get_aligned_pairs`` function, in which lower case nucleotides denote \"different from the reference"\.
	  
	  .. image:: ../images/sites/NatMeth_Fig1b.png

   .. tab:: required input

	  .. tabs::

		 .. tab:: BED
		 
			Depending on the type of data (HiPlex, Shotgun, or GBS), a specific BED file must be created to define the start and end positions of loci.
			
			.. tabs::
			
			   .. tab:: HiPlex
				  
				  Typical Primer3 output that needs to be converted to a BED file to delineate the loci for SMAP haplotype-sites.
				  
				  ========= ========== ========= =============== =============== ========= ======= ====== ======= ============= ============ ======================= ============= ============== ================= ================== ================
				  Index     Seq ID     Count     Primer_type     Orientation     Start     Len     tm     GC%     Any compl     3' compl     Seq                     Prod Size     Seq Length     Included Length   Pair any compl     Pair 3' compl   
				  ========= ========== ========= =============== =============== ========= ======= ====== ======= ============= ============ ======================= ============= ============== ================= ================== ================
				  1         Chr1       1         Generic         FORWARD         2         16      58.72  56.25   5.00          0.00         ATTCTCCGGGGTCACT        72            29887145       29887145          6.00               3.00            
				  2         Chr1       1         Generic         REVERSE         73        17      59.69  47.05   4.00          2.00         GTACACCGGTATTCTTC                                                                                         
				  3         Chr1       1         Generic         FORWARD         92        20      59.65  45.00   3.00          3.00         CCCAAAAATCCCAGTGACAT    83            29887145       29887145          3.00               1.00            
				  4         Chr1       1         Generic         REVERSE         174       20      58.88  55.00   3.00          0.00         TGACAGTAGCCCAAGAGGTG                                                                                      
				  5         Chr1       1         Generic         FORWARD         294       20      60.01  60.00   4.00          0.00         GCTAGTGGGAGCTGAAGTGG    81            29887145       29887145          3.00               1.00            
				  6         Chr1       1         Generic         REVERSE         374       20      60.28  50.00   4.00          2.00         TAGTGCTGGCAACGACCATA                                                                                      
				  7         Chr1       1         Generic         FORWARD         463       20      60.79  60.00   6.00          0.00         GCTGCAGGGTAAGGAGAGGT    84            29887145       29887145          5.00               1.00            
				  8         Chr1       1         Generic         REVERSE         546       21      59.00  47.62   8.00          2.00         GGATATCCTTGTCGAACTCCA                                                                                     
				  ========= ========== ========= =============== =============== ========= ======= ====== ======= ============= ============ ======================= ============= ============== ================= ================== ================
				  
				  The scheme below outlines the relative positions of primers and loci on the reference genome sequence.
				  
				  .. image:: ../images/sites/coordinates_HiPlex_manual.png  
				  
				  For HiPlex data, the user needs to create a custom BED file listing the loci based on the primer binding sites. We recommend to keep primer sequences in HiPlex reads for mapping, but to define the region between the primers in the BED file used for **SMAP haplotype-sites**. This region is defined by the first nucleotide downstream of the forward primer binding site to the last nucleotide upstream of the reverse primer binding site.
			
				  The primer binding site coordinates (using GFF coordinate system for primers: start and end both 1-based) need to be transformed as follows:
			
				  ================= =====================================================
				  BED                     INPUT
				  ================= =====================================================
				  Reference         reference sequence ID
				  Start             F-primer end position (F-primer end given as 1-based coordinate)
				  End               R-primer start position - 1 (R-primer start given as 1-based coordinate)
				  HiPlex_locus_name reference_(F-primer end position + 1)_(R-primer start position - 1)
				  Mean_Read_Depth   .
				  Strand            \+ \
				  SMAPs             (F-primer end position + 1), (R-primer start position - 1)
				  Completeness      .
				  nr_SMAPs          2
				  Name              HiPlex_Set1
				  ================= =====================================================
				  
				  The table below corresponds to the four loci defined by the Primer3 output shown above.
				  
				  =============== ====== ====== ==================== ==================== ======= ============ ============== ======== =============
				  Reference       Start  End    HiPlex_locus_name    Mean_read_depth      Strand  SMAPs        Completeness   nr_SMAPs Name
				  =============== ====== ====== ==================== ==================== ======= ============ ============== ======== =============
				  Chr1            17     56     Chr1:18-56_+         .                    \+ \    18,56        .              2        HiPlex_Set1  
				  Chr1            111    164    Chr1:112-164_+       .                    \+ \    112,164      .              2        HiPlex_Set1  
				  Chr1            313    354    Chr1:314-354_+       .                    \+ \    314,354      .              2        HiPlex_Set1  
				  Chr1            482    525    Chr1:483-525_+       .                    \+ \    483,525      .              2        HiPlex_Set1  
				  =============== ====== ====== ==================== ==================== ======= ============ ============== ======== =============

			   .. tab:: Shotgun_SNPs
				   
				  Consider the following read mapping and associated VCF file with several neighboring SNPs.
				   
				  .. image:: ../images/sites/coordinates_Shotgun_SNPs_manual.png  
				   
				  
				  The user needs to create a custom BED file listing the loci based on a VCF file with SNPs. Sliding frames are created starting from the first SNP in the sequence, We recommend to define 3bp Sliding frames with the central nucleotide at the junction and two flanking nucleotides as SMAPs in the BED file used for **SMAP haplotype-sites**. Each junction on both ends of a structural variant may be genotyped independently.  
				  
				  ============ ====== ====== ==================== ================ ======= ========== ============== ======== =============
				  Reference    Start  End    HiPlex_locus_name    Mean_read_depth  Strand  SMAPs      Completeness   nr_SMAPs Name
				  ============ ====== ====== ==================== ================ ======= ========== ============== ======== =============
				  Chr1         16     32     Chr1:17-32_+         .                \+ \    17,32      .              2        HiPlex_Set1  
				  Chr1         39     56     Chr1:40-56_+         .                \+ \    40,56      .              2        HiPlex_Set1  
				  Chr1         107    108    Chr1:108-108_+       .                \+ \    108,108    .              2        HiPlex_Set1  
				  ============ ====== ====== ==================== ================ ======= ========== ============== ======== =============
			
				  The SNP coordinates need to be transformed into sliding frames as follows:
			
				  ================== ============================================================================
				  BED                     INPUT
				  ================== ============================================================================
				  Reference          reference sequence ID
				  Start              first SNP position in frame - offset - 1
				  End                last SNP position in frame + offset
				  Shotgun_locus_name reference_start_end
				  Mean_Read_Depth    .
				  Strand             \+ \
				  SMAPs              First SNP position - offset, last SNP position + Offset
				  Completeness       .
				  nr_SMAPs           2
				  Name               Shotgun_Set1
				  ================== ============================================================================

			   .. tab:: Shotgun_SVs
				  
				  Consider the following read mapping structure and associated VCF file with structural variants.
				  
				  .. image:: ../images/sites/coordinates_Shotgun_SV_manual.png  
				  
				  
				  The user needs to create a custom BED file listing the loci based on a VCF file with known junctions of Stuctural Variants. We recommend to define 3bp Sliding frames with the central nucleotide at the junction and two flanking nucleotides as SMAPs in the BED file used for **SMAP haplotype-sites**. Each junction on both ends of a structural variant may be genotyped independently.  
				  
				  =============== ====== ====== ============================ ==================== ======= ================= ============== ======== =============
				  Reference       Start  End    HiPlex_locus_name            Mean_read_depth      Strand  SMAPs             Completeness   nr_SMAPs Name
				  =============== ====== ====== ============================ ==================== ======= ================= ============== ======== =============
				  Chr1            42     45     Chr1:43-45_+                 .                    \+ \    43,45             .              2        Shotgun_Set2 
				  Chr1            193    196    Chr1:194-196_+               .                    \+ \    194,196           .              2        Shotgun_Set2 
				  Chr1            10038  10041  Chr1:10039-10041_+           .                    \+ \    10039,10041       .              2        Shotgun_Set2 
				  =============== ====== ====== ============================ ==================== ======= ================= ============== ======== =============
				
				  The SV coordinates need to be transformed to short Sliding frames as follows:
				
				  ================== ============================================================================
				  BED                INPUT
				  ================== ============================================================================
				  Reference          reference sequence ID
				  Start              SV position - 2
				  End                SV position + 1
				  Shotgun_locus_name reference_(SV position - 1)_(SV position + 1)
				  Mean_Read_Depth    .
				  Strand             \+ \
				  SMAPs              (SV position - 1), (SV position + 1)
				  Completeness       .
				  nr_SMAPs           2
				  Name               Shotgun_Set2
				  ================== ============================================================================

			   .. tab:: GBS
				   
				  .. image:: ../images/sites/coordinates_GBS_manual.png  
				    
				    
				    
				  For GBS data, the user needs to run :ref:`SMAP delineate <SMAPdelHIW>` on the same set of BAM files as will be used for haplotyping to create a BED file listing the loci with SMAPs. The read mapping profiles determine the locus start and end points and internal SMAPs.

				  =============== ===== ===== ================================= =================== ======= ======================= ============== ======== =============
				  Reference       Start End   MergedCluster_name                Mean_read_depth     Strand  SMAPs                   Completeness   nr_SMAPs Name
				  =============== ===== ===== ================================= =================== ======= ======================= ============== ======== =============
				  scaffold_10030  15617 15711 scaffold_10030:15618-15711_+      1899                \+      15618,15622,15703,15711 13             4        2n_ind_GBS_SE
				  scaffold_10030  15712 15798 "\scaffold_10030:15713-15798\_\-" 1930                \-      15713,15793,15798       9              3        2n_ind_GBS_SE
				  =============== ===== ===== ================================= =================== ======= ======================= ============== ======== =============
				  
				  | BED file entry listing all relevant features of two neighboring loci. On the + strand of the reference sequence, the start (15617) and end (15711) positions of the locus, together with the mean locus read depth (1899), the strand (\+), the internal SMAP positions (15621, 15702), the number of samples with data at that locus (completeness, 13), the number of SMAPs (4), and a custom label that denotes the dataset (2n_ind_GBS_SE). The second entry lists the locus and SMAP positions on the (\-) strand. 


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

		 .. tab:: BAM
		 		 
			.. image:: ../images/sites/scaffold_10030_ref0030940_0070_edit.png
			
			| BAM file containing the alignments of single-end GBS read data of an individual genotype, illustrating the presence of various haplotypes. The GBS fragment is flanked on both sides by a *Pst* I restriction site (grey box) and contains two independent loci. The first locus contains single-end reads mapped on the forward (+) strand. 
			| The second locus contains reads mapped on the reverse (-) strand. Haplotypes are defined by combinations of neighboring SMAPs (light blue arrows) and SNPs (purple arrows). A SMAP at position 15622 is created by an InDel close to the \5' \ of the GBS-fragment combined with a misalignment (see :ref:`SMAP delineate <SMAPdelsepvmerg>` for details), while a SMAP at position 15792 is created by consistent soft clipping in a particular haplotype. Various sequencing read errors are present at positions other than the identified SNP positions, but are ignored as they are not listed in the VCF file. One of the SNPs (15793) is located in the soft clipped region.

   .. tab:: procedure
	  
	  | **SMAP haplotype-sites** reconstructs haplotypes based on SMAP positions and SNPs through read-backed haplotyping on a given set of BAM files.
	  | **SMAP haplotype-sites** first creates sets of polymorphic positions per locus on the reference genome by intersecting locus regions (obtained with :ref:`SMAP delineate <SMAPdelHIW>`) with a VCF file containing selected SNPs (obtained from any third-party SNP calling algorithm applied to the same set of BAM files). 
	  | In each BAM file, **SMAP haplotype-sites** then evaluates each read-reference alignment for the nucleotide aligned at the SMAP/SNP positions and scores as follows:

	  ========= ===================================================================================
	  CALL TYPE CLASSES
	  ========= ===================================================================================
	  .         absence of read mapping
	  0         presence of the reference nucleotide
	  1         presence of an alternative nucleotide (any nucleotide different from the reference)
	  \- \      presence of a gap in the alignment
	  ========= ===================================================================================
	
	  These calls are concatenated into a haplotype string of \'.01-'\s. For each discovered haplotype in the data, the total number of corresponding reads is counted per sample. Next, the haplotype counts of all samples are integrated into one master table, and expressed as relative haplotype frequency per locus per sample. Haplotypes with low frequency across all samples are removed to control for noise. The final table with haplotype frequencies per locus per sample is the end point for analysis of Pool-Seq data. Using the :ref:`option <SMAPhaploquickstartcommands>` ``--discrete_calls``, **SMAP haplotype-sites** transforms the haplotype frequency table into discrete haplotype calls for individuals.

	  Three modes may be chosen for discrete haplotype calling in individuals:
	  
	  ============================= =============
	  CALL TYPE                     CLASSES
	  ============================= =============
	  dosage calls in diploids      0, 1, 2
	  dosage calls in tetraploids   0, 1, 2, 3, 4
	  dominant calls                0, 1
	  ============================= =============

	  In the following sections, identification and quantification of haplotypes is illustrated on single-end GBS read data of a set of 8 diploid individuals at two partially overlapping loci. The content of the three example input files (BED, VCF, BAM) at this locus will be used to demonstrate the subsequent steps of **SMAP haplotype-sites**.
	  

----
	  
Output
------

**Tabular output**

.. tabs::

   .. tab:: General output

      By default, **SMAP haplotype-sites** will return two .tsv files.  
 
      :navy:`haplotype counts`
      
      **Read_counts_cx_fx_mx.tsv** (with x the value per option used in the analysis) contains the read counts (``-c``) and haplotype frequency (``-f``) filtered and/or masked (``-m``) read counts per haplotype per locus as defined in the BED file from **SMAP delineate**.  
      This is the file structure:
      
		============== ========== ======= ======= ========
		Locus          Haplotypes Sample1 Sample2 Sample..
		============== ========== ======= ======= ========
		Chr1:100-200_+ 00010      0       13      34      
		Chr1:100-200_+ 01000      19      90      28      
		Chr1:100-200_+ 00110      60      0       23      
		Chr1:450-600_+ 0010       70      63      87      
		Chr1:450-600_+ 0110       108     22      134     
		============== ========== ======= ======= ========

      :navy:`relative haplotype frequency`
      
      **Haplotype_frequencies_cx_fx_mx.tsv** contains the relative frequency per haplotype per locus in sample (based on the corresponding count table: Read_counts_cx_fx_mx.tsv). The transformation to relative frequency per locus-sample combination inherently normalizes for differences in total number of mapped reads across samples, and differences in amplification efficiency across loci.  
      This is the file structure:
      
		============== ========== ======= ======= ========
		Locus          Haplotypes Sample1 Sample2 Sample..
		============== ========== ======= ======= ========
		Chr1:100-200_+ 00010      0       0.13    0.40    
		Chr1:100-200_+ 01000      0.24    0.87    0.33    
		Chr1:100-200_+ 00110      0.76    0       0.27    
		Chr1:450-600_+ 0010       0.39    0.74    0.39    
		Chr1:450-600_+ 0110       0.61    0.26    0.61    
		============== ========== ======= ======= ========
		
   .. tab:: Additional output for individuals
   
      For individuals, if the option ``--discrete_calls`` is used, the program will return three additional .tsv files. Their content and order of creation is shown in :ref:`this scheme <SMAPhaplostep5>`.  
      
	  | :navy:`haplotype total discrete calls`
      
	  | The first file is called **haplotypes_cx_fx_mx_discrete_calls._total.tsv** and this file contains the total dosage calls, obtained after transforming haplotype frequencies into discrete calls, using the defined ``--frequency_interval_bounds``. The total sum of discrete dosage calls is expected to be 2 in diploids and 4 in tetraploids.

		============== ======= ======= ========
		Locus          Sample1 Sample2 Sample..
		============== ======= ======= ========
		Chr1:100-200_+ 2       2       3       
		Chr1:450-600_+ 2       2       2       
		============== ======= ======= ========
		
	  | :navy:`haplotype discrete calls`
	  
	  | The second file is **haplotypes_cx_fx_mx-discrete_calls_filtered.tsv**, which lists the discrete calls per locus per sample after ``--dosage_filter`` has removed loci per sample with an unexpected number of haplotype calls (as listed in haplotypes_cx_fx_mx_discrete_calls_total.tsv). The expected number of calls is set with option ``-z`` [use 2 for diploids, 4 for tetraploids].

		============== ========== ======= ======= ========
		Locus          Haplotypes Sample1 Sample2 Sample..
		============== ========== ======= ======= ========
		Chr1:100-200_+ 00010         0       1       NA   
		Chr1:100-200_+ 01000         1       1       NA   
		Chr1:100-200_+ 00110         1       0       NA   
		Chr1:450-600_+ 0010          1       1       1    
		Chr1:450-600_+ 0110          1       1       1    
		============== ========== ======= ======= ========
		  
	  | :navy:`population haplotype frequencies`

	  | The third file, **haplotypes_cx_fx_mx_Pop_HF.tsv**, lists the population haplotype frequencies (over all individual samples) based on the total number of discrete haplotype calls relative to the total number of calls per locus.

		============== ========== ====== =====
		Locus          Haplotypes Pop_HF count
		============== ========== ====== =====
		Chr1:100-200_+ 00010      25.0   4    
		Chr1:100-200_+ 01000      50.0   4    
		Chr1:100-200_+ 00110      25.0   4    
		Chr1:450-600_+ 0010       50.0   6    
		Chr1:450-600_+ 0110       50.0   6    
		============== ========== ====== =====

	  | For individuals, if the option ``--locus_correctness`` is used in combination with ``--discrete_calls`` and ``--frequency_interval_bounds``, the programm will create a new .bed file **haplotypes_cx_fx_mx_correctnessx_loci.bed** (loci filtered from the input .bed file) containing only the loci that were correctly dosage called (-z) in at least the defined percentage of samples. :ref:`See above <SMAPhaplostep5>`.

	  | :navy:`Loci with correct calls across the sample set`

		=============== ====== ====== ============================ ==================== ======= ================= ============== ======== =============
		Reference       Start  End    HiPlex_locus_name            Mean_read_depth      Strand  SMAPs             Completeness   nr_SMAPs Name
		=============== ====== ====== ============================ ==================== ======= ================= ============== ======== =============
		Chr1            99     200    Chr1:100-200_+               .                    \+ \    100,200           .              2        HiPlex_Set1  
		Chr1            449    600    Chr1:450-600_+               .                    \+ \    450,600           .              2        HiPlex_Set1  
		=============== ====== ====== ============================ ==================== ======= ================= ============== ======== =============
		
**Graphical output**

:navy:`haplotype diversity`

.. tabs::

   .. tab:: haplotype diversity across sampleset
	
	 By default, **SMAP haplotype-sites** will generate graphical output summarizing haplotype diversity. haplotype_diversity_across_sampleset.png shows a histogram of the number of distinct haplotypes per locus *across* all samples.  
     
   .. tab:: example graph
	
	  .. image:: ../images/sites/haplotype_counts.cigar.barplot.png


:navy:`haplotype frequency distribution per sample`

.. tabs::

   .. tab:: haplotype frequency distribution per sample
	 
     Graphical output of the haplotype frequency distribution for each individual sample can be switched **on** using the option ``--plot_all``. sample_haplotype_frequency_distribution.png shows the haplotype frequency distribution across all loci detected per sample. It is the graphical representation of each sample-specific column in **haplotypes_cx_fx_mx.tsv**. Using the option ``--discrete_calls``, this plot will also show the defined discrete calling boundaries.

   .. tab:: example graph
	
	  .. image:: ../images/sites/2n_ind_GBS_SE_001.bam.haplotype.frequency.histogram.png

:navy:`quality of genotype calls per locus and per sample (only for individuals)`

.. tabs::

   .. tab:: QC of loci and samples using discrete dosage calls  
	
     After discrete genotype calling with option ``--discrete_calls``, **SMAP haplotype-sites** will evaluate the observed sum of discrete dosage calls per locus per sample versus the expected value per locus (set with option ``-z``, recommended use: 2 for diploid, 4 for tetraploid). 
     
     The quality of genotype calls per *sample* is calculated in two ways: the fraction of loci with calls in that sample versus the total number of loci across all samples (sample_call_completeness); the fraction of loci with expected sum of discrete dosage calls (``-z``) versus the total number of observed loci in that sample (sample_call_correctness.tsv). These scores are calculated separately per *sample*, and **SMAP haplotype-sites** plots the distribution of those scores across the sample set (sample_call_completeness.png; sample_call_correctness.png).  
      
     Similarly, the quality of genotype calls per *locus* is calculated in two ways: the fraction of samples with calls for that locus versus the total number of samples (locus_call_completeness); the fraction of samples with expected sum of discrete dosage calls (``-z``) versus the total number of observed samples for that locus (locus_call_correctness.tsv). These scores are calculated separately per *locus*, and **SMAP haplotype-sites** plots the distribution of those scores across the locus set (locus_call_completeness.png; locus_call_correctness.png).  
      
     Both graphs and the corresponding tables (one for samples and one for loci) can be evaluated to identify poorly performing samples and/or loci. We recommend to eliminate these from further analysis by removing BAM files from the run directory and/or loci from the SMAP delineate BED file with SMAPs, and iterate through rounds of data analysis combined with sample and locus quality control.

   .. tab:: completeness and correctness across the sample set
	
	  .. image:: ../images/sites/sample_call_completeness_correctness_40canephora.png
	  
	  The sample call completeness plot shows the percentage of loci that have data across the samples after all filters. In read depth-saturated, low diversity datasets, the majority of samples should have high locus completeness and there should not be much variation in completeness between samples. In a high diversity or read depth-unsaturated sample set, locus completeness per sample will be lower and more spread out.
	  
	  The sample call correctness plot displays the percentage of correctly dosage called (``-z``) loci across the sampleset. Loci are only masked in samples with a dosage value different from ``-z`` but remain in the data set for all other samples with the expected dosage value.
	  
   .. tab:: completeness and correctness across the locus set
	
	  .. image:: ../images/sites/locus_call_completeness_correctness_40canephora.png

	  The locus call completeness plot displays the percentage of samples that have data (after every filter) on a locus for every locus. In read depth-saturated, low diversity sample sets, the majority of samples should have many high completeness loci and few low completeness loci. In a high diversity or read depth-unsaturated sample set, many loci will have a low completeness.
	  
	  The locus call correctness plot shows the percentage of samples that were correctly dosage called (``-z``) across the locus set. Loci with low correctness values indicate potential genotype calling artefacts and should be removed from the data set.

----

.. _SMAPhaploquickstartcommands:

  
Summary of Commands
-------------------

A detailed overview of the command line options can be found in section :ref:`Summary of Commands <SMAPhaplofreq>`
A typical command line example looks like this:

::

	smap haplotype-sites /path/to/BAM/ /path/to/BED/ /path/to/VCF/ -mapping_orientation stranded --no_indels -c 10 -f 5 -p 8 --plot_type png -partial include --min_distinct_haplotypes 2 -o haplotypes_SampleSet1

Command examples and options of **SMAP haplotype-sites** for a range of specific sample types are given under :ref:`haplotype frequency profiles <SMAPhaplofreq>`.  
Options may be given in any order.

