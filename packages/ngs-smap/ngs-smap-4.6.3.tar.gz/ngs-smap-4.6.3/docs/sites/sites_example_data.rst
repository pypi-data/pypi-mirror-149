.. raw:: html

    <style> .navy {color:navy} </style>
	
.. role:: navy

.. raw:: html

    <style> .white {color:white} </style>

.. role:: white

#####################################
Example Data
#####################################

.. _SMAPexample:

:navy:`Illustration of haplotyping with SMAP haplotype-sites`


Below, we present good quality data sets analysed with **SMAP haplotype-sites** to illustrate typically expected haplotyping results. For each data set, the command to run **SMAP haplotype-sites** with suggested optimal settings, together with graphical results are displayed for comparison to your own data.

Please note that while we *suggest* 'optimal' parameter settings in the command to run SMAP haplotype-sites, the default of SMAP haplotype-sites is to perform as little filtering as possible and to report all loci. The user is adviced to run SMAP haplotype-sites first with the mandatory and default settings (no data filtered out), and then decide on the most optimal parameter settings for your own data. Parameter settings should be iteratively adjusted for each novel data set, after manual inspection of the graphical output. The example data shown below are merely meant to illustrate the expected outcome of data sets processed with parameters adjusted to the specific type of library, reads and samples. If your data does not look like these examples, please check out the section :ref:`Recommendations and Troubleshooting <SMAPRecommendTroubleSites>` for examples (and suggested solutions) of incorrectly generated, preprocessed, or mapped reads, or sample sets analyzed with inappropriate parameter settings for SMAP haplotype-sites. There, some guidelines for troubleshooting are provided, which may help to optimize library preparation, sequencing, read `preprocessing <https://gbprocess.readthedocs.io/en/latest/gbs_data_processing.html>`_ or **SMAP haplotype-sites** :ref:`parameter settings <SMAPSummaryCommand>`.


.. _SMAPexample_HiPlex:

HiPlex 
------

:navy:`Individuals`

.. tabs::

   .. tab:: diploid individual

	  | Tab command shows a typical command to run **SMAP haplotype-sites** for HiPlex data in diploid individuals.
	  | Tabs further show typical graphical output such as haplotype frequency distribution at the individual sample level, as well as summary graphics that show locus and sample completeness and correctness and haplotype diversity, together with explanation about step-specific parameters.

		  .. tabs::

			 .. tab:: command
			 
				:: 
					
					smap haplotype-sites /path/to/BAM/ -mapping_orientation stranded  -p 8 --plot all --plot_type png --name 2n_ind_GBS-SE -f 50 -g 200 --min_stack_depth 3 --max_stack_depth 500 --min_cluster_depth 10 --max_cluster_depth 1500 --max_stack_number 2 --min_stack_depth_fraction 10 --completeness 1 --max_smap_number 10
			 
			 .. tab:: Haplotype frequency per sample
			 
				**SMAP haplotype-sites** run with ``--plot all`` plots the haplotype frequency distribution per sample. If discrete haplotype calling is performed, the frequency interval borders are also shown on the graph to check that individuals indeed show a haplotype frequency distribution according to expectation.   

				.. image:: ../images/haplotype-sites_examples/potato/haplotype_counts_discrete_calls_filtered.barplot_potato.png
				
				In diploid individuals, three peaks are expected: one below around 10% (noise) and one above around 90% (the major homozygous allele, but some data is lost to noise), and an intermediary peak around 50% to show heterozygous loci. See section on :ref:`InDels <SMAPInDelsAffectMappingRange>`.

				\_________________________________________________________________________________________________\

				
			 .. tab:: Sample completeness and correctness  
			 
				**SMAP haplotype-sites** run with ``--discrete_calling`` plots the sample correctness and completeness scores.

				.. image:: ../images/haplotype-sites_examples/potato/sample_call_completeness_potato.histogram.png
				
				Sample completeness scores shows the distribution of the number of loci detected versus the total number of loci screened.

				\_________________________________________________________________________________________________\

				.. image:: ../images/haplotype-sites_examples/potato/sample_call_correctness_potato.histogram.png
				
				Sample correctness scores shows the distribution of the number of loci correctly called versus the total number of loci detected.

			.. tab:: Locus completeness and correctness  
			 
				**SMAP haplotype-sites** run with ``--discrete_calling`` plots the sample correctness and completeness scores.
				\_________________________________________________________________________________________________\
				
				.. image:: ../images/haplotype-sites_examples/potato/sample_call_completeness_potato.histogram.png
				
				Locus completeness scores shows the distribution of the number of samples detected versus the total number of samples screened per locus.

				\_________________________________________________________________________________________________\

				.. image:: ../images/haplotype-sites_examples/potato/sample_call_correctness_potato.histogram.png
				
				Locus correctness scores shows the distribution of the number of samples correctly called versus the total number of samples detected.

				\_________________________________________________________________________________________________\

			 .. tab:: Haplotype diversity
             
				The haplotype diversity plot show the number of haplotypes per locus. Two plots are created, one directly after haplotype calling and one after filtering if discrete haplotype calling is performed.

				Before filtering:  
				
				.. image:: ../images/haplotype-sites_examples/potato/haplotype_counts_discrete_calls_filtered.barplot_potato.png
				
				After filtering:  
				
				.. image:: ../images/haplotype-sites_examples/potato/haplotype_counts_discrete_calls_filtered.barplot_potato.png
				
				The reduction in the number of haplotypes per locus shows how effective the current parameter settings are for removing noise. The user can evaluate whether the parameter settings are too stringent or too permissive, by running **SMAP haplotype-sites** several times with different parameter settings and comparing the haplotype diversity and sample and locus completeness and correctess plots.

				\_________________________________________________________________________________________________\

   .. tab:: tetraploid individual

	  | Tab command shows a typical command to run **SMAP haplotype-sites** for HiPlex data in tetraploid individuals.
	  | Tabs further show typical graphical output such as haplotype frequency distribution at the individual sample level, as well as summary graphics that show locus and sample completeness and correctness and haplotype diversity, together with explanation about step-specific parameters.

		  .. tabs::

			 .. tab:: command
			 
				:: 
					
					smap haplotype-sites /path/to/BAM/ -mapping_orientation stranded  -p 8 --plot all --plot_type png --name 2n_ind_GBS-SE -f 50 -g 200 --min_stack_depth 3 --max_stack_depth 500 --min_cluster_depth 10 --max_cluster_depth 1500 --max_stack_number 2 --min_stack_depth_fraction 10 --completeness 1 --max_smap_number 10
			 
			 .. tab:: Haplotype frequency per sample
			 
				**SMAP haplotype-sites** run with ``--plot all`` plots the haplotype frequency distribution per sample. If discrete haplotype calling is performed, the frequency interval borders are also shown on the graph to check that individuals indeed show a haplotype frequency distribution according to expectation.   

				.. image:: ../images/haplotype-sites_examples/potato/haplotype_counts_discrete_calls_filtered.barplot_potato.png
				
				In diploid individuals, three peaks are expected: one below around 10% (noise) and one above around 90% (the major homozygous allele, but some data is lost to noise), and an intermediary peak around 50% to show heterozygous loci. See section on :ref:`InDels <SMAPInDelsAffectMappingRange>`.

				\_________________________________________________________________________________________________\

				
			 .. tab:: Sample completeness and correctness  
			 
				**SMAP haplotype-sites** run with ``--discrete_calling`` plots the sample correctness and completeness scores.

				.. image:: ../images/haplotype-sites_examples/potato/sample_call_completeness_potato.histogram.png
				
				Sample completeness scores shows the distribution of the number of loci detected versus the total number of loci screened.

				\_________________________________________________________________________________________________\

				.. image:: ../images/haplotype-sites_examples/potato/sample_call_correctness_potato.histogram.png
				
				Sample correctness scores shows the distribution of the number of loci correctly called versus the total number of loci detected.

			.. tab:: Locus completeness and correctness  
			 
				**SMAP haplotype-sites** run with ``--discrete_calling`` plots the sample correctness and completeness scores.
				\_________________________________________________________________________________________________\
				
				.. image:: ../images/haplotype-sites_examples/potato/sample_call_completeness_potato.histogram.png
				
				Locus completeness scores shows the distribution of the number of samples detected versus the total number of samples screened per locus.

				\_________________________________________________________________________________________________\

				.. image:: ../images/haplotype-sites_examples/potato/sample_call_correctness_potato.histogram.png
				
				Locus correctness scores shows the distribution of the number of samples correctly called versus the total number of samples detected.

				\_________________________________________________________________________________________________\

			 .. tab:: Haplotype diversity
             
				The haplotype diversity plot show the number of haplotypes per locus. Two plots are created, one directly after haplotype calling and one after filtering if discrete haplotype calling is performed.

				Before filtering:  
				
				.. image:: ../images/haplotype-sites_examples/potato/haplotype_counts_discrete_calls_filtered.barplot_potato.png
				
				After filtering:  
				
				.. image:: ../images/haplotype-sites_examples/potato/haplotype_counts_discrete_calls_filtered.barplot_potato.png
				
				The reduction in the number of haplotypes per locus shows how effective the current parameter settings are for removing noise. The user can evaluate whether the parameter settings are too stringent or too permissive, by running **SMAP haplotype-sites** several times with different parameter settings and comparing the haplotype diversity and sample and locus completeness and correctess plots.

				\_________________________________________________________________________________________________\

:navy:`Pools`

.. tabs::

   .. tab:: diploid pool

	  | Tab command shows a typical command to run **SMAP haplotype-sites** for HiPlex data in pools of diploid individuals.
	  | Tabs further show typical graphical output such as haplotype frequency distribution at the individual sample level, as well as summary graphics that show locus and sample completeness and correctness and haplotype diversity, together with explanation about step-specific parameters.

		  .. tabs::

			 .. tab:: command
			 
				:: 
					
					smap haplotype-sites /path/to/BAM/ -mapping_orientation stranded  -p 8 --plot all --plot_type png --name 2n_ind_GBS-SE -f 50 -g 200 --min_stack_depth 3 --max_stack_depth 500 --min_cluster_depth 10 --max_cluster_depth 1500 --max_stack_number 2 --min_stack_depth_fraction 10 --completeness 1 --max_smap_number 10
			 
			 .. tab:: Haplotype frequency per sample
			 
				**SMAP haplotype-sites** run with ``--plot all`` plots the haplotype frequency distribution per sample. If discrete haplotype calling is performed, the frequency interval borders are also shown on the graph to check that individuals indeed show a haplotype frequency distribution according to expectation.   

				.. image:: ../images/haplotype-sites_examples/potato/haplotype_counts_discrete_calls_filtered.barplot_potato.png
				
				In diploid individuals, three peaks are expected: one below around 10% (noise) and one above around 90% (the major homozygous allele, but some data is lost to noise), and an intermediary peak around 50% to show heterozygous loci. See section on :ref:`InDels <SMAPInDelsAffectMappingRange>`.

				\_________________________________________________________________________________________________\

			 .. tab:: Haplotype diversity
             
				The haplotype diversity plot show the number of haplotypes per locus. Two plots are created, one directly after haplotype calling and one after filtering if discrete haplotype calling is performed.

				Before filtering:  
				
				.. image:: ../images/haplotype-sites_examples/potato/haplotype_counts_discrete_calls_filtered.barplot_potato.png
				
				After filtering:  
				
				.. image:: ../images/haplotype-sites_examples/potato/haplotype_counts_discrete_calls_filtered.barplot_potato.png
				
				The reduction in the number of haplotypes per locus shows how effective the current parameter settings are for removing noise. The user can evaluate whether the parameter settings are too stringent or too permissive, by running **SMAP haplotype-sites** several times with different parameter settings and comparing the haplotype diversity and sample and locus completeness and correctess plots.

				\_________________________________________________________________________________________________\


   .. tab:: tetraploid pool

	  | Tab command shows a typical command to run **SMAP haplotype-sites** for HiPlex data in pools of tetraploid individuals.
	  | Tabs further show typical graphical output such as haplotype frequency distribution at the individual sample level, as well as summary graphics that show locus and sample completeness and correctness and haplotype diversity, together with explanation about step-specific parameters.

		  .. tabs::

			 .. tab:: command
			 
				:: 
					
					smap haplotype-sites /path/to/BAM/ -mapping_orientation stranded  -p 8 --plot all --plot_type png --name 2n_ind_GBS-SE -f 50 -g 200 --min_stack_depth 3 --max_stack_depth 500 --min_cluster_depth 10 --max_cluster_depth 1500 --max_stack_number 2 --min_stack_depth_fraction 10 --completeness 1 --max_smap_number 10
			 
			 .. tab:: Haplotype frequency per sample
			 
				**SMAP haplotype-sites** run with ``--plot all`` plots the haplotype frequency distribution per sample. If discrete haplotype calling is performed, the frequency interval borders are also shown on the graph to check that individuals indeed show a haplotype frequency distribution according to expectation.   

				.. image:: ../images/haplotype-sites_examples/potato/haplotype_counts_discrete_calls_filtered.barplot_potato.png
				
				In diploid individuals, three peaks are expected: one below around 10% (noise) and one above around 90% (the major homozygous allele, but some data is lost to noise), and an intermediary peak around 50% to show heterozygous loci. See section on :ref:`InDels <SMAPInDelsAffectMappingRange>`.

				\_________________________________________________________________________________________________\

				
			 .. tab:: Haplotype diversity
             
				The haplotype diversity plot show the number of haplotypes per locus. Two plots are created, one directly after haplotype calling and one after filtering if discrete haplotype calling is performed.

				Before filtering:  
				
				.. image:: ../images/haplotype-sites_examples/potato/haplotype_counts_discrete_calls_filtered.barplot_potato.png
				
				After filtering:  
				
				.. image:: ../images/haplotype-sites_examples/potato/haplotype_counts_discrete_calls_filtered.barplot_potato.png
				
				The reduction in the number of haplotypes per locus shows how effective the current parameter settings are for removing noise. The user can evaluate whether the parameter settings are too stringent or too permissive, by running **SMAP haplotype-sites** several times with different parameter settings and comparing the haplotype diversity and sample and locus completeness and correctess plots.

				\_________________________________________________________________________________________________\


.. _SMAPexample_Shotgun:

Shotgun
-------

:navy:`Sliding frames`

.. tabs::

   .. tab:: diploid individuals

	  | Tab command shows a typical command to run **SMAP haplotype-sites** for Shotgun PE-86 separately mapped reads of diploid individuals.
	  | Tabs further show typical graphical output such as haplotype frequency distribution at the individual sample level, as well as summary graphics that show locus and sample completeness and correctness and haplotype diversity, together with explanation about step-specific parameters.

		  .. tabs::

			 .. tab:: command
			 
				:: 
					
					smap haplotype-sites /path/to/BAM/ -mapping_orientation stranded  -p 8 --plot all --plot_type png --name 2n_ind_GBS-SE -f 50 -g 200 --min_stack_depth 3 --max_stack_depth 500 --min_cluster_depth 10 --max_cluster_depth 1500 --max_stack_number 2 --min_stack_depth_fraction 10 --completeness 1 --max_smap_number 10
			 
			 .. tab:: Haplotype frequency per sample
			 
				**SMAP haplotype-sites** run with ``--plot all`` plots the haplotype frequency distribution per sample. If discrete haplotype calling is performed, the frequency interval borders are also shown on the graph to check that individuals indeed show a haplotype frequency distribution according to expectation.   

				.. image:: ../images/haplotype-sites_examples/potato/haplotype_counts_discrete_calls_filtered.barplot_potato.png
				
				In diploid individuals, three peaks are expected: one below around 10% (noise) and one above around 90% (the major homozygous allele, but some data is lost to noise), and an intermediary peak around 50% to show heterozygous loci. See section on :ref:`InDels <SMAPInDelsAffectMappingRange>`.

				\_________________________________________________________________________________________________\

				
			 .. tab:: Sample completeness and correctness  
			 
				**SMAP haplotype-sites** run with ``--discrete_calling`` plots the sample correctness and completeness scores.

				.. image:: ../images/haplotype-sites_examples/potato/sample_call_completeness_potato.histogram.png
				
				Sample completeness scores shows the distribution of the number of loci detected versus the total number of loci screened.

				\_________________________________________________________________________________________________\

				.. image:: ../images/haplotype-sites_examples/potato/sample_call_correctness_potato.histogram.png
				
				Sample correctness scores shows the distribution of the number of loci correctly called versus the total number of loci detected.

			.. tab:: Locus completeness and correctness  
			 
				**SMAP haplotype-sites** run with ``--discrete_calling`` plots the sample correctness and completeness scores.
				\_________________________________________________________________________________________________\
				
				.. image:: ../images/haplotype-sites_examples/potato/sample_call_completeness_potato.histogram.png
				
				Locus completeness scores shows the distribution of the number of samples detected versus the total number of samples screened per locus.

				\_________________________________________________________________________________________________\

				.. image:: ../images/haplotype-sites_examples/potato/sample_call_correctness_potato.histogram.png
				
				Locus correctness scores shows the distribution of the number of samples correctly called versus the total number of samples detected.

				\_________________________________________________________________________________________________\

			 .. tab:: Haplotype diversity
             
				The haplotype diversity plot show the number of haplotypes per locus. Two plots are created, one directly after haplotype calling and one after filtering if discrete haplotype calling is performed.

				Before filtering:  
				
				.. image:: ../images/haplotype-sites_examples/potato/haplotype_counts_discrete_calls_filtered.barplot_potato.png
				
				After filtering:  
				
				.. image:: ../images/haplotype-sites_examples/potato/haplotype_counts_discrete_calls_filtered.barplot_potato.png
				
				The reduction in the number of haplotypes per locus shows how effective the current parameter settings are for removing noise. The user can evaluate whether the parameter settings are too stringent or too permissive, by running **SMAP haplotype-sites** several times with different parameter settings and comparing the haplotype diversity and sample and locus completeness and correctess plots.

				\_________________________________________________________________________________________________\

:navy:`Structural Variants`

.. tabs::

    .. tab:: tetraploid individuals

	  | Tab command shows a typical command to run **SMAP haplotype-sites** for single-enzyme GBS, merged reads in tetraploid individuals.
	  | Tabs further show typical graphical output such as haplotype frequency distribution at the individual sample level, as well as summary graphics that show locus and sample completeness and correctness and haplotype diversity, together with explanation about step-specific parameters.

		  .. tabs::

			 .. tab:: command
			 
				:: 
					
					smap haplotype-sites /path/to/BAM/ -mapping_orientation ignore -p 8 --plot all --plot_type png --name 2n_ind_GBS-SE -f 50 -g 200 --min_stack_depth 3 --max_stack_depth 500 --min_cluster_depth 10 --max_cluster_depth 1500 --max_stack_number 2 --min_stack_depth_fraction 10 --completeness 1 --max_smap_number 10
			 
			 .. tab:: Haplotype frequency per sample
			 
				**SMAP haplotype-sites** run with ``--plot all`` plots the haplotype frequency distribution per sample. If discrete haplotype calling is performed, the frequency interval borders are also shown on the graph to check that individuals indeed show a haplotype frequency distribution according to expectation.   

				.. image:: ../images/haplotype-sites_examples/potato/haplotype_counts_discrete_calls_filtered.barplot_potato.png
				
				In diploid individuals, three peaks are expected: one below around 10% (noise) and one above around 90% (the major homozygous allele, but some data is lost to noise), and an intermediary peak around 50% to show heterozygous loci. See section on :ref:`InDels <SMAPInDelsAffectMappingRange>`.

				\_________________________________________________________________________________________________\

				
			 .. tab:: Sample completeness and correctness  
			 
				**SMAP haplotype-sites** run with ``--discrete_calling`` plots the sample correctness and completeness scores.

				.. image:: ../images/haplotype-sites_examples/potato/sample_call_completeness_potato.histogram.png
				
				Sample completeness scores shows the distribution of the number of loci detected versus the total number of loci screened.

				\_________________________________________________________________________________________________\

				.. image:: ../images/haplotype-sites_examples/potato/sample_call_correctness_potato.histogram.png
				
				Sample correctness scores shows the distribution of the number of loci correctly called versus the total number of loci detected.

			.. tab:: Locus completeness and correctness  
			 
				**SMAP haplotype-sites** run with ``--discrete_calling`` plots the sample correctness and completeness scores.
				\_________________________________________________________________________________________________\
				
				.. image:: ../images/haplotype-sites_examples/potato/sample_call_completeness_potato.histogram.png
				
				Locus completeness scores shows the distribution of the number of samples detected versus the total number of samples screened per locus.

				\_________________________________________________________________________________________________\

				.. image:: ../images/haplotype-sites_examples/potato/sample_call_correctness_potato.histogram.png
				
				Locus correctness scores shows the distribution of the number of samples correctly called versus the total number of samples detected.

				\_________________________________________________________________________________________________\

			 .. tab:: Haplotype diversity
             
				The haplotype diversity plot show the number of haplotypes per locus. Two plots are created, one directly after haplotype calling and one after filtering if discrete haplotype calling is performed.

				Before filtering:  
				
				.. image:: ../images/haplotype-sites_examples/potato/haplotype_counts_discrete_calls_filtered.barplot_potato.png
				
				After filtering:  
				
				.. image:: ../images/haplotype-sites_examples/potato/haplotype_counts_discrete_calls_filtered.barplot_potato.png
				
				The reduction in the number of haplotypes per locus shows how effective the current parameter settings are for removing noise. The user can evaluate whether the parameter settings are too stringent or too permissive, by running **SMAP haplotype-sites** several times with different parameter settings and comparing the haplotype diversity and sample and locus completeness and correctess plots.

				\_________________________________________________________________________________________________\

:navy:`Oxford Nanopore long reads`

.. tabs::

   .. tab:: diploid individual

	  | Tab command shows a typical command to run **SMAP haplotype-sites** for single-enzyme GBS, merged reads in pools.
	  | Tabs further show typical graphical output such as haplotype frequency distribution at the individual sample level, as well as summary graphics that show locus and sample completeness and correctness and haplotype diversity, together with explanation about step-specific parameters.

		  .. tabs::

			 .. tab:: command
			 
				:: 
					
					smap haplotype-sites /path/to/BAM/ -mapping_orientation ignore -p 8 --plot all --plot_type png --name 2n_ind_GBS-SE -f 50 -g 200 --min_stack_depth 3 --max_stack_depth 500 --min_cluster_depth 10 --max_cluster_depth 1500 --max_stack_number 2 --min_stack_depth_fraction 10 --completeness 1 --max_smap_number 10
			 
			 .. tab:: Haplotype frequency per sample
			 
				**SMAP haplotype-sites** run with ``--plot all`` plots the haplotype frequency distribution per sample. If discrete haplotype calling is performed, the frequency interval borders are also shown on the graph to check that individuals indeed show a haplotype frequency distribution according to expectation.   

				.. image:: ../images/haplotype-sites_examples/potato/haplotype_counts_discrete_calls_filtered.barplot_potato.png
				
				In diploid individuals, three peaks are expected: one below around 10% (noise) and one above around 90% (the major homozygous allele, but some data is lost to noise), and an intermediary peak around 50% to show heterozygous loci. See section on :ref:`InDels <SMAPInDelsAffectMappingRange>`.

				\_________________________________________________________________________________________________\

				
			 .. tab:: Sample completeness and correctness  
			 
				**SMAP haplotype-sites** run with ``--discrete_calling`` plots the sample correctness and completeness scores.

				.. image:: ../images/haplotype-sites_examples/potato/sample_call_completeness_potato.histogram.png
				
				Sample completeness scores shows the distribution of the number of loci detected versus the total number of loci screened.

				\_________________________________________________________________________________________________\

				.. image:: ../images/haplotype-sites_examples/potato/sample_call_correctness_potato.histogram.png
				
				Sample correctness scores shows the distribution of the number of loci correctly called versus the total number of loci detected.

			.. tab:: Locus completeness and correctness  
			 
				**SMAP haplotype-sites** run with ``--discrete_calling`` plots the sample correctness and completeness scores.
				\_________________________________________________________________________________________________\
				
				.. image:: ../images/haplotype-sites_examples/potato/sample_call_completeness_potato.histogram.png
				
				Locus completeness scores shows the distribution of the number of samples detected versus the total number of samples screened per locus.

				\_________________________________________________________________________________________________\

				.. image:: ../images/haplotype-sites_examples/potato/sample_call_correctness_potato.histogram.png
				
				Locus correctness scores shows the distribution of the number of samples correctly called versus the total number of samples detected.

				\_________________________________________________________________________________________________\

			 .. tab:: Haplotype diversity
             
				The haplotype diversity plot show the number of haplotypes per locus. Two plots are created, one directly after haplotype calling and one after filtering if discrete haplotype calling is performed.

				Before filtering:  
				
				.. image:: ../images/haplotype-sites_examples/potato/haplotype_counts_discrete_calls_filtered.barplot_potato.png
				
				After filtering:  
				
				.. image:: ../images/haplotype-sites_examples/potato/haplotype_counts_discrete_calls_filtered.barplot_potato.png
				
				The reduction in the number of haplotypes per locus shows how effective the current parameter settings are for removing noise. The user can evaluate whether the parameter settings are too stringent or too permissive, by running **SMAP haplotype-sites** several times with different parameter settings and comparing the haplotype diversity and sample and locus completeness and correctess plots.

				\_________________________________________________________________________________________________\

:navy:`PacBio long reads`

.. tabs::

   .. tab:: diploid individual

	  | Tab command shows a typical command to run **SMAP haplotype-sites** for single-enzyme GBS, merged reads in pools.
	  | Tabs further show typical graphical output such as haplotype frequency distribution at the individual sample level, as well as summary graphics that show locus and sample completeness and correctness and haplotype diversity, together with explanation about step-specific parameters.

		  .. tabs::

			 .. tab:: command
			 
				:: 
					
					smap haplotype-sites /path/to/BAM/ -mapping_orientation ignore -p 8 --plot all --plot_type png --name 2n_ind_GBS-SE -f 50 -g 200 --min_stack_depth 3 --max_stack_depth 500 --min_cluster_depth 10 --max_cluster_depth 1500 --max_stack_number 2 --min_stack_depth_fraction 10 --completeness 1 --max_smap_number 10
			 
			 .. tab:: Haplotype frequency per sample
			 
				**SMAP haplotype-sites** run with ``--plot all`` plots the haplotype frequency distribution per sample. If discrete haplotype calling is performed, the frequency interval borders are also shown on the graph to check that individuals indeed show a haplotype frequency distribution according to expectation.   

				.. image:: ../images/haplotype-sites_examples/potato/haplotype_counts_discrete_calls_filtered.barplot_potato.png
				
				In diploid individuals, three peaks are expected: one below around 10% (noise) and one above around 90% (the major homozygous allele, but some data is lost to noise), and an intermediary peak around 50% to show heterozygous loci. See section on :ref:`InDels <SMAPInDelsAffectMappingRange>`.

				\_________________________________________________________________________________________________\

				
			 .. tab:: Sample completeness and correctness  
			 
				**SMAP haplotype-sites** run with ``--discrete_calling`` plots the sample correctness and completeness scores.

				.. image:: ../images/haplotype-sites_examples/potato/sample_call_completeness_potato.histogram.png
				
				Sample completeness scores shows the distribution of the number of loci detected versus the total number of loci screened.

				\_________________________________________________________________________________________________\

				.. image:: ../images/haplotype-sites_examples/potato/sample_call_correctness_potato.histogram.png
				
				Sample correctness scores shows the distribution of the number of loci correctly called versus the total number of loci detected.

			.. tab:: Locus completeness and correctness  
			 
				**SMAP haplotype-sites** run with ``--discrete_calling`` plots the sample correctness and completeness scores.
				\_________________________________________________________________________________________________\
				
				.. image:: ../images/haplotype-sites_examples/potato/sample_call_completeness_potato.histogram.png
				
				Locus completeness scores shows the distribution of the number of samples detected versus the total number of samples screened per locus.

				\_________________________________________________________________________________________________\

				.. image:: ../images/haplotype-sites_examples/potato/sample_call_correctness_potato.histogram.png
				
				Locus correctness scores shows the distribution of the number of samples correctly called versus the total number of samples detected.

				\_________________________________________________________________________________________________\

			 .. tab:: Haplotype diversity
             
				The haplotype diversity plot show the number of haplotypes per locus. Two plots are created, one directly after haplotype calling and one after filtering if discrete haplotype calling is performed.

				Before filtering:  
				
				.. image:: ../images/haplotype-sites_examples/potato/haplotype_counts_discrete_calls_filtered.barplot_potato.png
				
				After filtering:  
				
				.. image:: ../images/haplotype-sites_examples/potato/haplotype_counts_discrete_calls_filtered.barplot_potato.png
				
				The reduction in the number of haplotypes per locus shows how effective the current parameter settings are for removing noise. The user can evaluate whether the parameter settings are too stringent or too permissive, by running **SMAP haplotype-sites** several times with different parameter settings and comparing the haplotype diversity and sample and locus completeness and correctess plots.

				\_________________________________________________________________________________________________\


.. _SMAPexample_GBS:

GBS
---

:navy:`Individuals`

.. tabs::

   .. tab:: diploid individuals, single-enzyme GBS, merged reads

	  | Tab command shows a typical command to run **SMAP haplotype-sites** for single-enzyme GBS, merged reads in diploid individuals.
	  | Tabs further show typical graphical output such as haplotype frequency distribution at the individual sample level, as well as summary graphics that show locus and sample completeness and correctness and haplotype diversity, together with explanation about step-specific parameters.

		  .. tabs::

			 .. tab:: command
			 
				:: 
					
					smap haplotype-sites /path/to/BAM/ -mapping_orientation ignore -p 8 --plot all --plot_type png --name 2n_ind_GBS-SE -f 50 -g 200 --min_stack_depth 3 --max_stack_depth 500 --min_cluster_depth 10 --max_cluster_depth 1500 --max_stack_number 2 --min_stack_depth_fraction 10 --completeness 1 --max_smap_number 10
			 
			 .. tab:: Haplotype frequency per sample
			 
				**SMAP haplotype-sites** run with ``--plot all`` plots the haplotype frequency distribution per sample. If discrete haplotype calling is performed, the frequency interval borders are also shown on the graph to check that individuals indeed show a haplotype frequency distribution according to expectation.   

				.. image:: ../images/haplotype-sites_examples/potato/haplotype_counts_discrete_calls_filtered.barplot_potato.png
				
				In diploid individuals, three peaks are expected: one below around 10% (noise) and one above around 90% (the major homozygous allele, but some data is lost to noise), and an intermediary peak around 50% to show heterozygous loci. See section on :ref:`InDels <SMAPInDelsAffectMappingRange>`.

				\_________________________________________________________________________________________________\

				
			 .. tab:: Sample completeness and correctness  
			 
				**SMAP haplotype-sites** run with ``--discrete_calling`` plots the sample correctness and completeness scores.

				.. image:: ../images/haplotype-sites_examples/potato/sample_call_completeness_potato.histogram.png
				
				Sample completeness scores shows the distribution of the number of loci detected versus the total number of loci screened.

				\_________________________________________________________________________________________________\

				.. image:: ../images/haplotype-sites_examples/potato/sample_call_correctness_potato.histogram.png
				
				Sample correctness scores shows the distribution of the number of loci correctly called versus the total number of loci detected.

			.. tab:: Locus completeness and correctness  
			 
				**SMAP haplotype-sites** run with ``--discrete_calling`` plots the sample correctness and completeness scores.
				\_________________________________________________________________________________________________\
				
				.. image:: ../images/haplotype-sites_examples/potato/sample_call_completeness_potato.histogram.png
				
				Locus completeness scores shows the distribution of the number of samples detected versus the total number of samples screened per locus.

				\_________________________________________________________________________________________________\

				.. image:: ../images/haplotype-sites_examples/potato/sample_call_correctness_potato.histogram.png
				
				Locus correctness scores shows the distribution of the number of samples correctly called versus the total number of samples detected.

				\_________________________________________________________________________________________________\

			 .. tab:: Haplotype diversity
             
				The haplotype diversity plot show the number of haplotypes per locus. Two plots are created, one directly after haplotype calling and one after filtering if discrete haplotype calling is performed.

				Before filtering:  
				
				.. image:: ../images/haplotype-sites_examples/potato/haplotype_counts_discrete_calls_filtered.barplot_potato.png
				
				After filtering:  
				
				.. image:: ../images/haplotype-sites_examples/potato/haplotype_counts_discrete_calls_filtered.barplot_potato.png
				
				The reduction in the number of haplotypes per locus shows how effective the current parameter settings are for removing noise. The user can evaluate whether the parameter settings are too stringent or too permissive, by running **SMAP haplotype-sites** several times with different parameter settings and comparing the haplotype diversity and sample and locus completeness and correctess plots.

				\_________________________________________________________________________________________________\


   .. tab:: diploid individuals, double-enzyme GBS, single-end reads

	  | Tab command shows a typical command to run **SMAP haplotype-sites** for double-enzyme GBS, single-end reads in diploid individuals.
	  | Tabs further show typical graphical output such as haplotype frequency distribution at the individual sample level, as well as summary graphics that show locus and sample completeness and correctness and haplotype diversity, together with explanation about step-specific parameters.

		  .. tabs::

			 .. tab:: command
			 
				:: 
					
					smap haplotype-sites /path/to/BAM/ -mapping_orientation stranded  -p 8 --plot all --plot_type png --name 2n_ind_GBS-SE -f 50 -g 200 --min_stack_depth 3 --max_stack_depth 500 --min_cluster_depth 10 --max_cluster_depth 1500 --max_stack_number 2 --min_stack_depth_fraction 10 --completeness 1 --max_smap_number 10
			 
			 .. tab:: Haplotype frequency per sample
			 
				**SMAP haplotype-sites** run with ``--plot all`` plots the haplotype frequency distribution per sample. If discrete haplotype calling is performed, the frequency interval borders are also shown on the graph to check that individuals indeed show a haplotype frequency distribution according to expectation.   

				.. image:: ../images/haplotype-sites_examples/potato/haplotype_counts_discrete_calls_filtered.barplot_potato.png
				
				In diploid individuals, three peaks are expected: one below around 10% (noise) and one above around 90% (the major homozygous allele, but some data is lost to noise), and an intermediary peak around 50% to show heterozygous loci. See section on :ref:`InDels <SMAPInDelsAffectMappingRange>`.

				\_________________________________________________________________________________________________\

				
			 .. tab:: Sample completeness and correctness  
			 
				**SMAP haplotype-sites** run with ``--discrete_calling`` plots the sample correctness and completeness scores.

				.. image:: ../images/haplotype-sites_examples/potato/sample_call_completeness_potato.histogram.png
				
				Sample completeness scores shows the distribution of the number of loci detected versus the total number of loci screened.

				\_________________________________________________________________________________________________\

				.. image:: ../images/haplotype-sites_examples/potato/sample_call_correctness_potato.histogram.png
				
				Sample correctness scores shows the distribution of the number of loci correctly called versus the total number of loci detected.

			.. tab:: Locus completeness and correctness  
			 
				**SMAP haplotype-sites** run with ``--discrete_calling`` plots the sample correctness and completeness scores.
				\_________________________________________________________________________________________________\
				
				.. image:: ../images/haplotype-sites_examples/potato/sample_call_completeness_potato.histogram.png
				
				Locus completeness scores shows the distribution of the number of samples detected versus the total number of samples screened per locus.

				\_________________________________________________________________________________________________\

				.. image:: ../images/haplotype-sites_examples/potato/sample_call_correctness_potato.histogram.png
				
				Locus correctness scores shows the distribution of the number of samples correctly called versus the total number of samples detected.

				\_________________________________________________________________________________________________\

			 .. tab:: Haplotype diversity

				The haplotype diversity plot show the number of haplotypes per locus. Two plots are created, one directly after haplotype calling and one after filtering if discrete haplotype calling is performed.

				Before filtering:  
				
				.. image:: ../images/haplotype-sites_examples/potato/haplotype_counts_discrete_calls_filtered.barplot_potato.png
				
				After filtering:  
				
				.. image:: ../images/haplotype-sites_examples/potato/haplotype_counts_discrete_calls_filtered.barplot_potato.png
				
				The reduction in the number of haplotypes per locus shows how effective the current parameter settings are for removing noise. The user can evaluate whether the parameter settings are too stringent or too permissive, by running **SMAP haplotype-sites** several times with different parameter settings and comparing the haplotype diversity and sample and locus completeness and correctess plots.

				\_________________________________________________________________________________________________\


   .. tab:: diploid individuals, double-enzyme GBS, merged reads

	  | Tab command shows a typical command to run **SMAP haplotype-sites** for double-enzyme GBS, merged reads in diploid individuals.
	  | Tabs further show typical graphical output such as haplotype frequency distribution at the individual sample level, as well as summary graphics that show locus and sample completeness and correctness and haplotype diversity, together with explanation about step-specific parameters.

		  .. tabs::

			 .. tab:: command
			 
				:: 
					
					smap haplotype-sites /path/to/BAM/ -mapping_orientation ignore -p 8 --plot all --plot_type png --name 2n_ind_GBS-SE -f 50 -g 200 --min_stack_depth 3 --max_stack_depth 500 --min_cluster_depth 10 --max_cluster_depth 1500 --max_stack_number 2 --min_stack_depth_fraction 10 --completeness 1 --max_smap_number 10
			 
			 .. tab:: Haplotype frequency per sample
			 
				**SMAP haplotype-sites** run with ``--plot all`` plots the haplotype frequency distribution per sample. If discrete haplotype calling is performed, the frequency interval borders are also shown on the graph to check that individuals indeed show a haplotype frequency distribution according to expectation.   

				.. image:: ../images/haplotype-sites_examples/potato/haplotype_counts_discrete_calls_filtered.barplot_potato.png
				
				In diploid individuals, three peaks are expected: one below around 10% (noise) and one above around 90% (the major homozygous allele, but some data is lost to noise), and an intermediary peak around 50% to show heterozygous loci. See section on :ref:`InDels <SMAPInDelsAffectMappingRange>`.

				\_________________________________________________________________________________________________\

				
			 .. tab:: Sample completeness and correctness  
			 
				**SMAP haplotype-sites** run with ``--discrete_calling`` plots the sample correctness and completeness scores.

				.. image:: ../images/haplotype-sites_examples/potato/sample_call_completeness_potato.histogram.png
				
				Sample completeness scores shows the distribution of the number of loci detected versus the total number of loci screened.

				\_________________________________________________________________________________________________\

				.. image:: ../images/haplotype-sites_examples/potato/sample_call_correctness_potato.histogram.png
				
				Sample correctness scores shows the distribution of the number of loci correctly called versus the total number of loci detected.

			.. tab:: Locus completeness and correctness  
			 
				**SMAP haplotype-sites** run with ``--discrete_calling`` plots the sample correctness and completeness scores.
				\_________________________________________________________________________________________________\
				
				.. image:: ../images/haplotype-sites_examples/potato/sample_call_completeness_potato.histogram.png
				
				Locus completeness scores shows the distribution of the number of samples detected versus the total number of samples screened per locus.

				\_________________________________________________________________________________________________\

				.. image:: ../images/haplotype-sites_examples/potato/sample_call_correctness_potato.histogram.png
				
				Locus correctness scores shows the distribution of the number of samples correctly called versus the total number of samples detected.

				\_________________________________________________________________________________________________\

			 .. tab:: Haplotype diversity
             
				The haplotype diversity plot show the number of haplotypes per locus. Two plots are created, one directly after haplotype calling and one after filtering if discrete haplotype calling is performed.

				Before filtering:  
				
				.. image:: ../images/haplotype-sites_examples/potato/haplotype_counts_discrete_calls_filtered.barplot_potato.png
				
				After filtering:  
				
				.. image:: ../images/haplotype-sites_examples/potato/haplotype_counts_discrete_calls_filtered.barplot_potato.png
				
				The reduction in the number of haplotypes per locus shows how effective the current parameter settings are for removing noise. The user can evaluate whether the parameter settings are too stringent or too permissive, by running **SMAP haplotype-sites** several times with different parameter settings and comparing the haplotype diversity and sample and locus completeness and correctess plots.

				\_________________________________________________________________________________________________\

   .. tab:: tetraploid individual, single-enzyme GBS, single-end reads

	  | Tab command shows a typical command to run **SMAP haplotype-sites** for single-enzyme GBS, single-end reads in tetraploid individuals.
	  | Tabs further show typical graphical output such as haplotype frequency distribution at the individual sample level, as well as summary graphics that show locus and sample completeness and correctness and haplotype diversity, together with explanation about step-specific parameters.


		  .. tabs::

			 .. tab:: command
			 
				:: 
					
					smap haplotype-sites /path/to/BAM/ -mapping_orientation stranded  -p 8 --plot all --plot_type png --name 2n_ind_GBS-SE -f 50 -g 200 --min_stack_depth 3 --max_stack_depth 500 --min_cluster_depth 10 --max_cluster_depth 1500 --max_stack_number 2 --min_stack_depth_fraction 10 --completeness 1 --max_smap_number 10
			 
			 .. tab:: Haplotype frequency per sample
			 
				**SMAP haplotype-sites** run with ``--plot all`` plots the haplotype frequency distribution per sample. If discrete haplotype calling is performed, the frequency interval borders are also shown on the graph to check that individuals indeed show a haplotype frequency distribution according to expectation.   

				.. image:: ../images/haplotype-sites_examples/potato/haplotype_counts_discrete_calls_filtered.barplot_potato.png
				
				In diploid individuals, three peaks are expected: one below around 10% (noise) and one above around 90% (the major homozygous allele, but some data is lost to noise), and an intermediary peak around 50% to show heterozygous loci. See section on :ref:`InDels <SMAPInDelsAffectMappingRange>`.

				\_________________________________________________________________________________________________\

				
			 .. tab:: Sample completeness and correctness  
			 
				**SMAP haplotype-sites** run with ``--discrete_calling`` plots the sample correctness and completeness scores.

				.. image:: ../images/haplotype-sites_examples/potato/sample_call_completeness_potato.histogram.png
				
				Sample completeness scores shows the distribution of the number of loci detected versus the total number of loci screened.

				\_________________________________________________________________________________________________\

				.. image:: ../images/haplotype-sites_examples/potato/sample_call_correctness_potato.histogram.png
				
				Sample correctness scores shows the distribution of the number of loci correctly called versus the total number of loci detected.

			.. tab:: Locus completeness and correctness  
			 
				**SMAP haplotype-sites** run with ``--discrete_calling`` plots the sample correctness and completeness scores.
				\_________________________________________________________________________________________________\
				
				.. image:: ../images/haplotype-sites_examples/potato/sample_call_completeness_potato.histogram.png
				
				Locus completeness scores shows the distribution of the number of samples detected versus the total number of samples screened per locus.

				\_________________________________________________________________________________________________\

				.. image:: ../images/haplotype-sites_examples/potato/sample_call_correctness_potato.histogram.png
				
				Locus correctness scores shows the distribution of the number of samples correctly called versus the total number of samples detected.

				\_________________________________________________________________________________________________\

			 .. tab:: Haplotype diversity
             
				The haplotype diversity plot show the number of haplotypes per locus. Two plots are created, one directly after haplotype calling and one after filtering if discrete haplotype calling is performed.

				Before filtering:  
				
				.. image:: ../images/haplotype-sites_examples/potato/haplotype_counts_discrete_calls_filtered.barplot_potato.png
				
				After filtering:  
				
				.. image:: ../images/haplotype-sites_examples/potato/haplotype_counts_discrete_calls_filtered.barplot_potato.png
				
				The reduction in the number of haplotypes per locus shows how effective the current parameter settings are for removing noise. The user can evaluate whether the parameter settings are too stringent or too permissive, by running **SMAP haplotype-sites** several times with different parameter settings and comparing the haplotype diversity and sample and locus completeness and correctess plots.

				\_________________________________________________________________________________________________\

   .. tab:: tetraploid individual, single-enzyme GBS, merged reads

	  | Tab command shows a typical command to run **SMAP haplotype-sites** for single-enzyme GBS, merged reads in tetraploid individuals.
	  | Tabs further show typical graphical output such as haplotype frequency distribution at the individual sample level, as well as summary graphics that show locus and sample completeness and correctness and haplotype diversity, together with explanation about step-specific parameters.


		  .. tabs::

			 .. tab:: command
			 
				:: 
					
					smap haplotype-sites /path/to/BAM/ -mapping_orientation ignore -p 8 --plot all --plot_type png --name 2n_ind_GBS-SE -f 50 -g 200 --min_stack_depth 3 --max_stack_depth 500 --min_cluster_depth 10 --max_cluster_depth 1500 --max_stack_number 2 --min_stack_depth_fraction 10 --completeness 1 --max_smap_number 10
			 
			 .. tab:: Haplotype frequency per sample
			 
				**SMAP haplotype-sites** run with ``--plot all`` plots the haplotype frequency distribution per sample. If discrete haplotype calling is performed, the frequency interval borders are also shown on the graph to check that individuals indeed show a haplotype frequency distribution according to expectation.   

				.. image:: ../images/haplotype-sites_examples/potato/haplotype_counts_discrete_calls_filtered.barplot_potato.png
				
				In diploid individuals, three peaks are expected: one below around 10% (noise) and one above around 90% (the major homozygous allele, but some data is lost to noise), and an intermediary peak around 50% to show heterozygous loci. See section on :ref:`InDels <SMAPInDelsAffectMappingRange>`.

				\_________________________________________________________________________________________________\

				
			 .. tab:: Sample completeness and correctness  
			 
				**SMAP haplotype-sites** run with ``--discrete_calling`` plots the sample correctness and completeness scores.

				.. image:: ../images/haplotype-sites_examples/potato/sample_call_completeness_potato.histogram.png
				
				Sample completeness scores shows the distribution of the number of loci detected versus the total number of loci screened.

				\_________________________________________________________________________________________________\

				.. image:: ../images/haplotype-sites_examples/potato/sample_call_correctness_potato.histogram.png
				
				Sample correctness scores shows the distribution of the number of loci correctly called versus the total number of loci detected.

			.. tab:: Locus completeness and correctness  
			 
				**SMAP haplotype-sites** run with ``--discrete_calling`` plots the sample correctness and completeness scores.
				\_________________________________________________________________________________________________\
				
				.. image:: ../images/haplotype-sites_examples/potato/sample_call_completeness_potato.histogram.png
				
				Locus completeness scores shows the distribution of the number of samples detected versus the total number of samples screened per locus.

				\_________________________________________________________________________________________________\

				.. image:: ../images/haplotype-sites_examples/potato/sample_call_correctness_potato.histogram.png
				
				Locus correctness scores shows the distribution of the number of samples correctly called versus the total number of samples detected.

				\_________________________________________________________________________________________________\

			 .. tab:: Haplotype diversity
             
				The haplotype diversity plot show the number of haplotypes per locus. Two plots are created, one directly after haplotype calling and one after filtering if discrete haplotype calling is performed.

				Before filtering:  
				
				.. image:: ../images/haplotype-sites_examples/potato/haplotype_counts_discrete_calls_filtered.barplot_potato.png
				
				After filtering:  
				
				.. image:: ../images/haplotype-sites_examples/potato/haplotype_counts_discrete_calls_filtered.barplot_potato.png
				
				The reduction in the number of haplotypes per locus shows how effective the current parameter settings are for removing noise. The user can evaluate whether the parameter settings are too stringent or too permissive, by running **SMAP haplotype-sites** several times with different parameter settings and comparing the haplotype diversity and sample and locus completeness and correctess plots.

				\_________________________________________________________________________________________________\


:navy:`Pools`

.. tabs::

   .. tab:: tetraploid pool, single-enzyme GBS, merged reads

	  | Tab command shows a typical command to run **SMAP haplotype-sites** for single-enzyme GBS, merged reads in pools.
	  | Tabs further show typical graphical output such as haplotype frequency distribution at the individual sample level, as well as summary graphics that show locus and sample completeness and correctness and haplotype diversity, together with explanation about step-specific parameters.


		  .. tabs::

			 .. tab:: command
			 
				:: 
					
					smap haplotype-sites /path/to/BAM/ -mapping_orientation ignore -p 8 --plot all --plot_type png --name 2n_ind_GBS-SE -f 50 -g 200 --min_stack_depth 3 --max_stack_depth 500 --min_cluster_depth 10 --max_cluster_depth 1500 --max_stack_number 2 --min_stack_depth_fraction 10 --completeness 1 --max_smap_number 10
			 
			 .. tab:: Haplotype frequency per sample
			 
				**SMAP haplotype-sites** run with ``--plot all`` plots the haplotype frequency distribution per sample. If discrete haplotype calling is performed, the frequency interval borders are also shown on the graph to check that individuals indeed show a haplotype frequency distribution according to expectation.   

				.. image:: ../images/haplotype-sites_examples/potato/haplotype_counts_discrete_calls_filtered.barplot_potato.png
				
				In diploid individuals, three peaks are expected: one below around 10% (noise) and one above around 90% (the major homozygous allele, but some data is lost to noise), and an intermediary peak around 50% to show heterozygous loci. See section on :ref:`InDels <SMAPInDelsAffectMappingRange>`.

				\_________________________________________________________________________________________________\

				

			 .. tab:: Haplotype diversity
             
				The haplotype diversity plot show the number of haplotypes per locus. Two plots are created, one directly after haplotype calling and one after filtering if discrete haplotype calling is performed.

				Before filtering:  
				
				.. image:: ../images/haplotype-sites_examples/potato/haplotype_counts_discrete_calls_filtered.barplot_potato.png
				
				After filtering:  
				
				.. image:: ../images/haplotype-sites_examples/potato/haplotype_counts_discrete_calls_filtered.barplot_potato.png
				
				The reduction in the number of haplotypes per locus shows how effective the current parameter settings are for removing noise. The user can evaluate whether the parameter settings are too stringent or too permissive, by running **SMAP haplotype-sites** several times with different parameter settings and comparing the haplotype diversity and sample and locus completeness and correctess plots.

				\_________________________________________________________________________________________________\

