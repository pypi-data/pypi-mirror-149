.. raw:: html

    <style> .navy {color:navy} </style>
	
.. role:: navy

.. raw:: html

    <style> .white {color:white} </style>

.. role:: white


.. _SMAPdesignRecommendTrouble:

####################################
Recommendations & Troubleshooting
####################################


.. _SMAPdesignPickAmplicons:

Picking reference sequences for primer design
---------------------------------------------

:navy:`HiPlex amplicon design optimization starts with choosing the set of genes for which primers need to be designed.`

| Choosing sets of genes as reference. 

|	Group by HOMOLOGY (use homology groups)
|	Group by PATHWAY (use all genes in a given pathway)
|	Group by INTERPRO (use InterPro domains, `domain repository <https://www.ebi.ac.uk/interpro/about/consortium/>`_)

| Specificity of primer design is determined by all sequences included in the reference sequence FASTA file, not the entire genome. 

Here, we first illustrate how to optimize the choice of reference genes using alternative designs in small gene families, in which subsets of genes are included during primer design. 
We also illustrate highly conserved regions within the gene family to show that conserved regions are avoided during primer design, but only if all genes are included in the fasta file used as input. 
Then, we draw your attention to the importance of XXX in amplicon design, and its evaluation using empirical evidence (amplifying the fragments, mapping, and **SMAP haplotype-window** analysis). 
Also, check out the section :ref:`section on optimisation in different species <SMAPdesignex>` across designs.


.. tabs::

   .. tab:: use sets of candidate genes as reference

		.. image:: ../images/design/Slide12.JPG
		
        text.
        
   .. tab:: use homology groups

		.. image:: ../images/design/Slide12.JPG
		
        text.

----

.. _SMAPdesignIncompleteness:

Specificity and coverage of primer designs versus completeness in the reference gene set
----------------------------------------------------------------------------------------

:navy:`specificity and coverage of primer design versus completeness in the reference gene set`

.. tabs::

   .. tab:: single gene

		.. image:: ../images/design/Slide12.JPG
		
		text.

   .. tab:: subsets of genes

		.. image:: ../images/design/Slide12.JPG
		
		text.

   .. tab:: complete homology groups

		.. image:: ../images/design/Slide12.JPG
		
		text.

   .. tab:: sets of complete homology groups

		.. image:: ../images/design/Slide12.JPG
		
		Because domain shuffling creates novel functionality and drives evolutionary innovation, some proteins contain conserved domains that are present across multiple homology groups. Therefore, depending on the domain content of your gene of interest, it may be required to include multiple homology groups as reference sequence for primer design to make sure that the primer specificity check implemented in Primer3, has access to all relevant potential off-target primer binding sites.

Please notice that ....

----

.. _SMAPdesignSeqTechnology:

Primer designs for specific sequencing technologies
---------------------------------------------------

:navy:`Primer design settings may be optimized depending on the downstream PCR-amplification, library preparation, and sequence technology`

:navy:`amplicon length and complexity versus sequencing throughput:`

	1. HiPlex amplicon sequening, Illumina HiSeq/NovaSeq: 80-150 bp, up to hundreds or thousand(s) of targets, and hundreds of samples
	2. multiplex amplicon sequencing, Illumina MiSeq: 300-500 bp, up to tens of hundred(s) of targets, and up to hundred samples
	3. Singleplex amplicon sequencing, Sanger, 500-1000 bp, single target, and tens of samples, analysis by Tide/ICE
	4. LongRange PCR, MinION 1.000-10.000 bp, single target, few or up to ten(s) of samples

**SMAP design** can simply be adjusted to the needs of subsequent steps of PCR amplification, library preparation method, and the sequencing technology.


To illustrate this point, consider ...  

.. tabs::

   .. tab:: HiPlex amplicon sequening 

	  .. image:: ../images/design/Slide12.JPG

	  | text.

   .. tab:: multiplex amplicon sequencing

	  .. image:: ../images/design/Slide12.JPG

	  | text.

   .. tab:: Singleplex amplicon sequencing

	  .. image:: ../images/design/Slide12.JPG

	  | text. 
   .. tab:: LongRange PCR

	  .. image:: ../images/design/Slide12.JPG

	  | text.

----


Troubleshooting
---------------

While recommended parameters are optimized for commonly used Amplicon-Seq protocols, the graphic results of **SMAP design** may show you that you need to adjust the design, while **SMAP haplotype-window** results may suggest that you need to adjust the data processing procedure.

