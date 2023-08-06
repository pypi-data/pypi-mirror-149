.. raw:: html

    <style> .navy {color:navy} </style>

.. role:: navy

.. raw:: html

    <style> .white {color:white} </style>

.. role:: white

#####################################
Example Data
#####################################

.. _SMAPdesignex:

Illustration of primer and guide design
---------------------------------------

Below, we present the summary plots output of twelve designs for different species and gene family sizes created with **SMAP design** to illustrate typically expected output. For each data set, the command to run **SMAP design** with settings are displayed for comparison to your own data.

The user is advised to run **SMAP design** first with the mandatory and default settings, and then decide on the most optimal parameter settings for your own design.
The example data shown below are merely meant to illustrate the expected outcome of data sets processed with parameters adjusted to the specific species and reference (gene) sets.
If your data does not look like these examples, please check out the section :ref:`Recommendations and Troubleshooting <SMAPdesignRecommendTrouble>` for examples (and suggested solutions) of suboptimal designs, or sample sets analyzed with inappropriate parameter settings for **SMAP design**.
There, some guidelines for troubleshooting are provided for **SMAP design** :ref:`parameter settings <SMAPdesignSummaryCommand>`.



.. tabs::

   .. tab:: Arabidopsis

       .. tabs::

           .. tab:: Small gene family

                   Command used to run **SMAP design** on a small gene family from Arabidopsis
                   
                     ::
                    
                       python SMAPdesign.py HOM04D000931_ath.fasta HOM04D000931_ath.gff -g HOM04D000931_ath_FlashFry.tsv -o HOM04D000931_ath_SMAPdesign -minl 120 -maxl 150 -smy -v -bo
                    
                   Summary plot
                    
                    .. image:: ../images/design/HOM04D000931_Ath_SMAPdesign_summary_plot.png
                    

           .. tab:: Medium gene family

                   Command used to run **SMAP design** on a medium-sized gene family from Arabidopsis
                   
                     ::

                       python SMAPdesign.py HOM04D000029_ath.fasta HOM04D000029_ath.gff -g HOM04D000029_ath_FlashFry.tsv -o HOM04D000029_ath_SMAPdesign -minl 120 -maxl 150 -smy -v -bo

                   Summary plot
                    
                    .. image:: ../images/design/HOM04D000029_Ath_SMAPdesign_summary_plot.png
                    

           .. tab:: Large gene family

                   Command used to run **SMAP design** on a large gene family from Arabidopsis
                   
                     ::
                    
                       python SMAPdesign.py HOM04D000001_ath.fasta HOM04D000001_ath.gff -g HOM04D000001_ath_FlashFry.tsv -o HOM04D000001_ath_SMAPdesign -minl 120 -maxl 150 -smy -v -bo
                    
                   Summary plot
                    
                    .. image:: ../images/design/HOM04D000001_Ath_SMAPdesign_summary_plot.png
                    

   .. tab:: Chlamydomonas

       .. tabs::

           .. tab:: Small gene family

                   Command used to run **SMAP design** on a small gene family from Chlamydomonas
                   
                     ::
                    
                       python SMAPdesign.py HOM04x5M006964_cre.fasta HOM04x5M006964_cre.gff -g HOM04x5M006964_cre_FlashFry.tsv -o HOM04x5M006964_cre_SMAPdesign -minl 220 -maxl 250 -smy -v -bo
                    
                   Summary plot
                    
                    .. image:: ../images/design/HOM04x5M006964_Cre_SMAPdesign_summary_plot.png
                    

           .. tab:: Medium gene family

                   Command used to run **SMAP design** on a medium-sized gene family from Chlamydomonas
                   
                     ::
                    
                       python SMAPdesign.py HOM04x5M000141_cre.fasta HOM04x5M000141_cre.gff -g HOM04x5M000141_cre_FlashFry.tsv -o HOM04x5M000141_cre_SMAPdesign -minl 220 -maxl 250 -smy -v -bo
                    
                   Summary plot
                    
                    .. image:: ../images/design/HOM04x5M000141_Cre_SMAPdesign_summary_plot.png
                    

           .. tab:: Large gene family

                   Command used to run **SMAP design** on a large gene family from Chlamydomonas
                   
                     ::
                    
                       python SMAPdesign.py HOM04x5M000042_cre.fasta HOM04x5M000042_cre.gff -g HOM04x5M000042_cre_FlashFry.tsv -o HOM04x5M000042_cre_SMAPdesign -minl 220 -maxl 250 -smy -v -bo
                    
                   Summary plot
                    
                    .. image:: ../images/design/HOM04x5M000042_Cre_SMAPdesign_summary_plot.png
                    

   .. tab:: Soybean

       .. tabs::

           .. tab:: Small gene family

                   Command used to run **SMAP design** on a small gene family from Soybean
                   
                     ::
                    
                       python SMAPdesign.py HOM04D000162_gma.fasta HOM04D000162_gma.gff -g HOM04D000162_gma_FlashFry.tsv -o HOM04D000162_gma_SMAPdesign -minl 400 -maxl 800 -d 150 -smy -v -bo
                    
                   Summary plot
                    
                    .. image:: ../images/design/HOM04D000162_Gma_SMAPdesign_summary_plot.png
                    

           .. tab:: Medium gene family

                   Command used to run **SMAP design** on a medium-sized gene family from Soybean
                   
                     ::
                    
                       python SMAPdesign.py HOM04D000015_gma.fasta HOM04D000015_gma.gff -g HOM04D000015_gma_FlashFry.tsv -o HOM04D000015_gma_SMAPdesign -minl 400 -maxl 800 -d 150 -smy -v -bo
                    
                   Summary plot
                    
                    .. image:: ../images/design/HOM04D000015_Gma_SMAPdesign_summary_plot.png
                    

           .. tab:: Large gene family

                   Command used to run **SMAP design** on a large gene family from Soybean
                   
                     ::
                    
                       python SMAPdesign.py HOM04D000001_gma.fasta HOM04D000001_gma.gff -g HOM04D000001_gma_FlashFry.tsv -o HOM04D000001_gma_SMAPdesign -minl 400 -maxl 800 -d 150 -smy -v -bo
                    
                   Summary plot
                    
                    .. image:: ../images/design/HOM04D000001_Gma_SMAPdesign_summary_plot.png
                    

   .. tab:: Human

       .. tabs::

           .. tab:: Small gene family

                   Command used to run **SMAP design** on a small gene family from Human
                   
                     ::
                    
                       python SMAPdesign.py HOM03P000828_hom.fasta HOM03P000828_hom.gff -g HOM03P000828_hom_FlashFry.tsv -o HOM03P000828_hom_SMAPdesign -minl 220 -maxl 250 -d 15 -smy -v -bo
                    
                   Summary plot
                    
                    .. image:: ../images/design/HOM03P000828_Hom_SMAPdesign_summary_plot.png
                    

           .. tab:: Medium gene family

                   Command used to run **SMAP design** on a medium-sized gene family from Human
                   
                     ::
                    
                       python SMAPdesign.py HOM03P000059_hom.fasta HOM03P000059_hom.gff -g HOM03P000059_hom_FlashFry.tsv -o HOM03P000059_hom_SMAPdesign -minl 220 -maxl 250 -d 15 -smy -v -bo
                    
                   Summary plot
                    
                    .. image:: ../images/design/HOM03P000059_Hom_SMAPdesign_summary_plot.png
                    

           .. tab:: Large gene family

                   Command used to run **SMAP design** on a large gene family from Human
                   
                     ::
                    
                       python SMAPdesign.py HOM03P000013_hom.fasta HOM03P000013_hom.gff -g HOM03P000013_hom_FlashFry.tsv -o HOM03P000013_hom_SMAPdesign -minl 220 -maxl 250 -d 15 -smy -v -bo
                    
                   Summary plot
                    
                    .. image:: ../images/design/HOM03P000013_Hom_SMAPdesign_summary_plot.png


| Using the GFF file generated by **SMAP design** a graphical view of the amplicons and gRNAs can be obtained with a vector program such as CLC or Geneious.
| In Geneious it would look like this.

.. image:: ../images/design/HOM04D000931_ath_graphicalOutput.png

The yellow arrows show the CDS (multiple transcripts are shown per gene), the blue arrows are the amplicons, the dark and light green arrows are the forward and reverse primer, respectively, the grey arrows are the gRNAs and the white arrows are the borders.

Example usage restricted regions primer design option
-----------------------------------------------------
The ``--restrictedPrimerDesign`` or ``-rpd`` option restricts amplicon design to exonic regions and will ignore large intronic regions. This speeds up the primer design and can increase retention rates, because the 150 amplicons that Primer3 designs by default will no longer be located in intronic regions, and subsequently discared because there is no overlap with a CDS.
Below are some examples comparing the design of three human gene families (with typically very large introns) with and without the ``-rpd`` option. The time needed to run these is given.


.. tabs::

            .. tab:: Small gene family (6 genes)

                  | **Without -rpd**
                  | Runtime: 00:00:26.69

                   .. tabs::

                         .. tab:: command
                                | command
                            ::

                               python SMAPdesign.py HOM03P000828_hom.fasta HOM03P000828_hom.gff -g HOM03P000828_hom_FlashFry.tsv -o HOM03P000828_hom_SMAPdesign -minl 220 -maxl 250 -d 15 -smy -v -bo

                         .. tab:: summary plot
                                | summary plot
                                .. image:: ../images/design/HOM03P000828_Hom_SMAPdesign_summary_plot.png

                  | **With -rpd**
                  | Runtime: 00:00:26.56

                   .. tabs::

                         .. tab:: command
                                | command
                            ::

                               python SMAPdesign.py HOM03P000828_hom.fasta HOM03P000828_hom.gff -g HOM03P000828_hom_FlashFry.tsv -o HOM03P000828_hom_SMAPdesign -rpd -minl 220 -maxl 250 -d 15 -smy -v -bo

                         .. tab:: summary plot
                                | summary plot
                                .. image:: ../images/design/HOM03P000828_Hom_rpd_SMAPdesign_summary_plot.png


            .. tab:: Medium gene family (34 genes)

                  | **Without -rpd**
                  | Runtime: 94:22:08.77

                   .. tabs::

                         .. tab:: command
                                | command
                            ::

                                 python SMAPdesign.py HOM03P000059_hom.fasta HOM03P000059_hom.gff -g HOM03P000059_hom_FlashFry.tsv -o HOM03P000059_hom_SMAPdesign -minl 220 -maxl 250 -d 15 -smy -v -bo

                         .. tab:: summary plot
                                | summary plot
                                .. image:: ../images/design/HOM03P000059_Hom_SMAPdesign_summary_plot.png

                  | **With -rpd**
                  | Runtime: 14:35:23.75

                   .. tabs::

                         .. tab:: command
                                | command
                            ::

                                 python SMAPdesign.py HOM03P000059_hom.fasta HOM03P000059_hom.gff -g HOM03P000059_hom_FlashFry.tsv -o HOM03P000059_hom_SMAPdesign -rpd -minl 220 -maxl 250 -d 15 -smy -v -bo

                         .. tab:: summary plot
                                | summary plot
                                .. image:: ../images/design/HOM03P000059_Hom_rpd_SMAPdesign_summary_plot.png

            .. tab:: Large gene family (98 genes)

                  | **Without -rpd**
                  | Runtime:

                   .. tabs::

                         .. tab:: command
                                | command
                            ::

                                python SMAPdesign.py HOM03P000013_hom.fasta HOM03P000013_hom.gff -g HOM03P000013_hom_FlashFry.tsv -o HOM03P000013_hom_SMAPdesign -minl 220 -maxl 250 -d 15 -smy -v -bo

                         .. tab:: summary plot
                                | summary plot
                                .. image:: ../images/design/HOM03P000013_Hom_SMAPdesign_summary_plot.png

                  | **With -rpd**
                  | Runtime: 08:57:11.93

                   .. tabs::

                         .. tab:: command
                                | command
                            ::

                                python SMAPdesign.py HOM03P000013_hom.fasta HOM03P000013_hom.gff -g HOM03P000013_hom_FlashFry.tsv -o HOM03P000013_hom_SMAPdesign -rpd -minl 220 -maxl 250 -d 15 -smy -v -bo

                         .. tab:: summary plot
                                | summary plot
                                .. image:: ../images/design/HOM03P000013_Hom_rpd_SMAPdesign_summary_plot.png
