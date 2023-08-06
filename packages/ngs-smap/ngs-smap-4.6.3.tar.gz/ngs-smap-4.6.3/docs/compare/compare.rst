.. raw:: html

    <style> .navy {color:navy} </style>
	
.. role:: navy

.. raw:: html

    <style> .white {color:white} </style>

.. role:: white

.. raw:: html

    <style> .green {color:green} </style>
    <style> .blue {color:blue} </style>
    <style> .red {color:red} </style>

.. role:: green
.. role:: blue
.. role:: red

##################################################################
Comparisons across data sets, shared and unique loci
##################################################################

General Introduction
--------------------

**SMAP compare** analyzes the overlap (shared and unique loci) between two GBA data sets that have both been processed with :ref:`SMAP delineate <SMAPdelindex>`.
**SMAP compare** can be used to compare:

	1.	parameter settings during read `preprocessing <https://gbprocess.readthedocs.io/en/latest/gbs_data_processing.html>`_. 
	#.  parameter settings during read mapping (e.g. `BWA-MEM <http://bio-bwa.sourceforge.net/bwa.shtml>`_).
	#.  parameter settings during locus delineation (:ref:`SMAP delineate <SMAPdelindex>`).
	#.	sets of progeny derived from independent breeding lines to estimate transferability of marker sets across a breeding program.
	#.	a set of pools against their constituent individuals to estimate sensitivity of detection across the allele frequency spectrum (example shown below).
	#.	GBS experiments performed in different labs, to investigate if similar protocols lead to similar sets of loci, *i.e.* comparability of own data to external data.
	
----
	
Command to run SMAP compare
---------------------------

::

	smap compare <Set1.bed> <Set2.bed> 

----

Input
-----

**SMAP compare** only needs two final BED files containing loci, created with :ref:`SMAP delineate <SMAPdelHIW3>`.

Examples of input BED files are shown below:  

| Set1 contains GBS samples of 48 diploid individuals.  
| Set2 contains 16 replicate Pool-Seq GBS samples of those constituent 48 individuals.

.. tabs::

   .. tab:: Set1 BED (individuals)
   
	  ============= ====== ====== =================================== ================= ======= ================== ============== ========= ==============
	  Reference     Start  End    MergedCluster_name                  Mean_read_depth   Strand  SMAPs              Completeness   nr_SMAPs  Name
	  ============= ====== ====== =================================== ================= ======= ================== ============== ========= ==============
	  scaffold_1    41455  41541  :green:`scaffold_1:41456-41541_+`   :green:`604`      \+      41456,41541        :green:`8`     2         48_individuals
	  scaffold_1    41486  41569  scaffold_1:41487-41569\_\-          579               \-      41487,41569        3              2         48_individuals
	  scaffold_1    42704  42778  scaffold_1:42705-42778_+            61                \+      42705,42778        2              2         48_individuals
	  scaffold_1    42798  42884  scaffold_1:42799-42884\_\-          72                \-      42799,42884        2              2         48_individuals
	  scaffold_1    77857  77943  :red:`scaffold_1:77858-77943_+`     :red:`43`         \+      77858,77943        :red:`3`       2         48_individuals
	  scaffold_1    156606 156692 scaffold_1:156607-156692\_\-        1067              \-      156607,156692      37             2         48_individuals
	  scaffold_12   2530   2596   scaffold_12:2531-2596_+             39                \+      2531,2596          3              2         48_individuals
	  scaffold_12   33659  33725  scaffold_12:33660-33725_+           18                \+      33660,33725        1              2         48_individuals
	  scaffold_12   34732  34806  scaffold_12:34733-34806_+           890               \+      34733,34806        45             2         48_individuals
	  scaffold_12   34732  34806  scaffold_12:34733-34806\_\-         768               \-      34733,34806        47             2         48_individuals
	  scaffold_34   36267  36358  scaffold_34:36268-36358_+           1169              \+      36268,36296,36358  36             3         48_individuals
	  scaffold_34   46267  46334  scaffold_34:46268-46334\_\-         150               \-      46268,46334        48             2         48_individuals
	  scaffold_72   23080  23166  :blue:`scaffold_72:23081-23166\_\-` :blue:`1423`      \-      23081,23156,23166  :blue:`48`     3         48_individuals
	  ============= ====== ====== =================================== ================= ======= ================== ============== ========= ==============
	  

   .. tab:: Set2 BED (pools)
   
	  ============= ====== ====== =================================== ================= ======= ================== ============== ========= =========
	  Reference     Start  End    MergedCluster_name                  Mean_read_depth   Strand  SMAPs              Completeness   nr_SMAPs  Name
	  ============= ====== ====== =================================== ================= ======= ================== ============== ========= =========
	  scaffold_1    41455  41541  :green:`scaffold_1:41456-41541_+`   :green:`42`       \+      41456,41541        :green:`1`     2         16_pools 
	  scaffold_1    41486  41569  scaffold_1:41487-41569\_\-          111               \-      41487,41569        3              2         16_pools 
	  scaffold_1    156606 156692 scaffold_1:156607-156692\_\-        915               \-      156607,156692      16             2         16_pools 
	  scaffold_12   34732  34806  scaffold_12:34733-34806_+           2403              \+      34733,34806        16             2         16_pools 
	  scaffold_12   34732  34806  scaffold_12:34733-34806\_\-         2284              \-      34733,34806        16             2         16_pools 
	  scaffold_34   36267  36358  scaffold_34:36268-36358_+           1242              \+      36268,36296,36358  16             3         16_pools 
	  scaffold_34   46267  46334  scaffold_34:46268-46334\_\-         809               \-      46268,46334        16             2         16_pools 
	  scaffold_72   23080  23166  :blue:`scaffold_72:23081-23166\_\-` :blue:`1882`      \-      23081,23156,23166  :blue:`16`     3         16_pools 
	  ============= ====== ====== =================================== ================= ======= ================== ============== ========= =========
	  
How It Works
------------

| **SMAP compare** uses `BEDtools intersect <https://bedtools.readthedocs.io/en/latest/content/tools/intersect.html>`_ to identify shared loci by positional overlap between loci of two **SMAP delineate** BED files.
| **SMAP compare** then calculates summary statistics of features of overlapping loci, such as completeness scores and mean read depth per respective sample set.

For instance:

	1.	locus :green:`scaffold_1:41456-41541_+` is shared between the two sample sets.
	#.	in Set1, locus :green:`scaffold_1:41456-41541_+` is observed in 8 (out of 48) individual samples, and with mean read depth of 604.
	#.	in Set2, locus :green:`scaffold_1:41456-41541_+` is observed in 1 (out of 16) pool-Seq samples, and with mean read depth of 42.
	#.	locus :red:`scaffold_1:77858-77943_+` is only found in 1 out of 48 individuals and in none of the 16 pools.
	#.	locus :blue:`scaffold_72:23081-23166\_\-` is found in 48 out of 48 individuals, and also in 16 out of 16 pools.

| Since for each locus in either BED file, **SMAP compare** extracts the completeness scores in Set1 and Set2, respectively, it can create a pivot table with the number of **shared** loci for a given **combination of completeness scores in the two respective sets**.
| For instance, locus :green:`scaffold_1:41456-41541_+` is one example out of 8 shared loci that are found in 8 out of 48 individuals and also in 1 out of 16 pools, while locus :blue:`scaffold_72:23081-23166\_\-` is one example out of 8 shared loci that are found in 48 out of 48 individuals, and also in 16 out of 16 pools.
| For each set of shared loci for a given combination of completeness scores, **SMAP compare** also calculates the mean read depth across all those loci per sample set. This usually shows that loci with low completeness scores in one of both sample sets may be due to low read depth (and thus missed by undersampling during sequencing) in that sample set.  

----

Graphical output
----------------

**SMAP compare** will plot four heatmaps. The top two heatmaps show the number of loci per combination of Completeness scores in the two respective sample sets. The position in this Completeness score matrix defines in how many samples a locus is observed in each of the two sample sets (Set1 on the x-axis, Set2 on the y-axis), the color in the heatmap shows the number of loci with this combination of Completeness scores.  
Two heatmaps show the mean read depth in the same Completeness score matrix (one plot per sample set).

:navy:`Completeness`

| The first two heatmaps allow to evaluate the expected number of common loci across two sample sets.
| For instance, in this example data, Set1 contains the loci observed across 48 individuals, while Set2 contains the loci observed across 16 replicate pools of these constituent individuals.
| The first heatmap shows that most loci are observed in only one of 48 individuals (Completeness \`1´ \, left-hand side of the graph), showing that the vast majority of GBS fragments is unique to a single individual.
| The heatmap further shows that these same loci are never covered by reads in any of the 16 pools (Completeness \`0´ \), despite being created from the same 48 individuals, revealing the bias against low frequency (MAF 1-2%) allele observations in Pool-Seq data.  
| Conversely, the lower-right corner of the completeness matrix shows that the loci that are commonly found across all replicate pools (Completeness near \`16´ \ on the y-axis), are the same loci that were also commonly found in the individuals (Completeness near \`48´ \on the x-axis)

| The first heatmap shows the Completeness score matrix, including the non-overlapping classes (\`0´ \, observed in one set but not the other set).
| Below, the completeness graphs originally obtained with **SMAP delineate** per sample set are shown at the top (Set1, individuals) and right hand side (Set2, pools) of the **SMAP compare** heatmap for comparison.

	.. image:: ../images/compare/SMAP_compare_2022a.png

The second heatmap shows the Completeness score matrix with only the overlapping classes. Note the difference in the (false colour) scale that is adjusted to the total number of *common* loci in the two sample sets.

.. image:: ../images/compare/SMAP_compare_2022a_partb.png

:navy:`Read depth`

The last two graphs show if sufficient reads were mapped per sample set. These data can be compared to the saturation curves (:ref:`saturation curves <SMAPPickEnzymes>`) obtained after running **SMAP delineate**.

The third heatmap shows the mean read depth per locus observed in Set1, across the Completeness score matrix.

.. image:: ../images/compare/SMAP_compare_2022a_partc.png

The fourth heatmap shows the mean read depth per locus observed in Set2, across the Completeness score matrix.

.. image:: ../images/compare/SMAP_compare_2022a_partd.png