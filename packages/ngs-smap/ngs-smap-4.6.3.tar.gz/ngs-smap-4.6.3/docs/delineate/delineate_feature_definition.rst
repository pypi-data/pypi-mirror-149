.. raw:: html

    <style> .navy {color:navy} </style>
	
.. role:: navy

.. raw:: html

    <style> .white {color:white} </style>

.. role:: white

###################################
Feature Description
###################################

.. _SMAPdeldef:

Definition of SMAPs, Stacks, StackClusters, and MergedClusters
--------------------------------------------------------------

| Intuitively, GBS may be expected to create perfectly aligned \`Stacks´ \ of reads after reference mapping. However, due to allelic sequence diversity, in reality the start and end points of mapped GBS reads often do not align at a given genomic locus, thus creating \`fuzzy´ \ Stacks.
| To emphasize the occurence of *consistency* in the variation of read mapping, **SMAP delineate** introduces three novel concepts in addition to **Stacks**, namely: **SMAPs**, **StackClusters** and **MergedClusters**. 

**SMAP delineate** first creates **Stacks** by identifying sets of reads with identical read mapping start and end positions per sample.  
The start and end positions of such **Stacks** are called **Stack Mapping Anchor Points** (:ref:`SMAPs <SMAPdeldef>`), so that Stacks capture read mapping consistency.  
Stacks are then incrementally overlapped, so that **StackClusters** capture *within*-sample read mapping variation, and **MergedClusters** capture *between*-sample read mapping variation.
See schemes below for graphical illustration of the concepts.

.. tabs:: 

	.. tab:: Overview
		
		**Schematic overview of SMAPs, Stacks, StackClusters, and MergedClusters.**
		
			.. image:: ../images/delineate/SMAP_delineate_cut.png
	

	.. tab:: Stacks
		
			.. image:: ../images/delineate/features_Stack.png
	
		Stacks capture consistent read mapping positions of reads derived from the same locus.
	
	.. tab:: StackClusters
		
			.. image:: ../images/delineate/features_StackCluster.png
		
		StackClusters capture variation of read mapping positions of reads derived from divergent alleles *within* a sample. SMAPs can be used as a novel type of molecular marker to differentiate between haplotypes.

	
	.. tab:: MergedClusters
	
			.. image:: ../images/delineate/features_MergedCluster.png
		   
		MergedClusters capture variation of read mapping positions derived from divergent alleles from the same genomic locus *across* samples. SMAPs can be used as a novel type of molecular marker to differentiate between haplotypes.
		
	.. tab:: Sneak preview: SNP calling artefacts
	
			.. image:: ../images/delineate/features_StackCluster_SNP.png
		
		| Reads within a StackCluster do not always cover the same genomic positions and this may cause SNP calling artefacts.
		| In this case a 4 bp deletion compared to the reference sequence results in two distinct Stacks. One of the Stacks covers a part of the genome that is not covered by the other Stack. 
		| SNPs in this region are called as homozygous SNPs because the SNP calling algorithm evaluates the alignment from "top to bottom" one nucleotide position at the time, and only takes the observed aligned nucleotides into account and is not aware that read depth is "missing" from the second allele.
		| For more explanation see :ref:`The effect of polymorphisms on Stacks <SMAPdelsepvmerg>`.
		
----

Why polymorphisms (SNPs and InDels) give rise to variation in mapping positions of reads 
----------------------------------------------------------------------------------------

| Above, we illustrate the common observation that sequence polymorphisms affect the final read mapping positions. 
| So, paradoxically, while GBS is used to detect polymorphisms by genome re-sequencing of restriction enzyme site flanking loci, polymorphisms themselves affect each of the three main steps in the GBS procedure:

	  1. GBS library construction (restriction enzyme site ligated adapters)
	  #. sequencing (Illumina short reads with fixed length)
	  #. mapping (`BWA-MEM <http://bio-bwa.sourceforge.net/bwa.shtml>`_; Smith-Waterman seed-extension alignment)
      
| Next, we explain the underlying reasons for each step.

----
        
Why Stacks exist in GBS data
----------------------------

:navy:`Stacks are defined as sets of short reads with identical read mapping start and end positions (SMAPs)`


	.. image:: ../images/delineate/Separately_mapped_vs_merged.png


| **Single-end GBS reads** are derived from individual molecules (restriction fragments). If Illumina single-end read length is shorter than the PCR-amplified GBS fragment length (distance between two neighboring restriction enzyme sites (RE)), then that individual molecule is only partially sequenced (black arrows).
| **Paired-end GBS reads** are derived from two sides of an individual molecule. If NGS read length is longer than half of the PCR-amplified GBS fragment length (distance between two neighboring REs), then those reads overlap at least partially in the middle of the GBS fragment. In this case, both reads cover a common sequence of the same molecule and the reads should be **merged** (by e.g. `PEAR <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3933873/>`_) in order to improve the base calling quality in the middle of the read, and to reduce redundancy of read depth (*i.e.* redundancy in reference genome coverage), and to create a long sequence spanning the entire GBS fragment from RE to RE.


=========================  =====================================  =======================================	 
Type of reads mapped       Start position                         End position
=========================  =====================================  =======================================	
separate reads (+ strand)  upstream restriction enzyme site (RE)  Start position + fixed read length
separate reads (- strand)  End position - fixed read length       downstream restriction enzyme site (RE)
merged reads               upstream restriction enzyme site (RE)  downstream restriction enzyme site (RE)
=========================  =====================================  =======================================	
	 
	
	 
| In practice, polymorphisms (SNPs and InDels) affect each of the three steps of GBS (restriction enzyme sites, effective alignable read length, and mapping), thus locally shifting the start and end positions of the final read mapping on the reference genome sequence.
| This, in turn, affects which reference positions are effectively covered by a set of alternative alleles at the borders of a given locus (See Sneak preview: SNP calling artefacts :ref:`above <SMAPdeldef>`). We first describe the general principle based on single-end sequencing. Then we further describe how this principle affects :ref:`paired-end merged sequences <SMAPdelsepvmerg>`.

----

Polymorphisms at restriction enzyme sites affect GBS library construction
-------------------------------------------------------------------------

:navy:`Polymorphisms affect the genomic positions at which adapters may be ligated`


Restriction enzyme sites (RE) are positions where GBS-adapters are ligated, and mark the beginning (\5' \  end) of a read sequence.
Polymorphisms (both SNPs and InDels) occuring at the restriction enzyme site may lead to loss or gain of REs in the genome of the sample under study, thus affecting the positions where adapters are ligated. The relative distance between two neighboring RE’s is important because only fragments in a narrow size range (typically 100-300 bp) are size-selected and PCR-amplified before sequencing. Depending on the GBS-protocol, size-selection may be performed through band excision after gel-electrophoresis and/or using restrictive elongation times during PCR-amplification. Thus, polymorphisms at REs lead to absence/presence of entire GBS fragments (NULL alleles), or may locally shift the start position of a read to a neighboring RE. The proportion of non-overlapping GBS loci in the sample set is proportional to the density of SNPs and InDels in the genome; species with higher genetic diversity contain less common GBS loci across sample sets. 

----

.. _SMAPInDelsAffectMappingRange:

Polymorphisms affect the effective sequenced region
---------------------------------------------------

:navy:`InDels affect effective range covered in the reference sequence by reads with fixed read length`


InDels affect which part of the reference sequence is effectively covered by a short read, "anchored" by a restriction enzyme site and of fixed length.

**Deletion**

	.. image:: ../images/delineate/deletion_scheme.png

An alternative allele with a deletion compared to the reference will not have to spend sequence length on the deleted region, thus allowing to sequence farther away from the RE.

**Insertion**

	.. image:: ../images/delineate/insertion_scheme.png

An alternative allele with an insertion compared to the reference will have to spend sequence length on that insertion, thus shortening the distance that can be sequenced away from the RE.

**SNPs**

As SNPs are nucleotide substitutions, they do not change the effective distance sequenced away from the RE.

----

Polymorphisms affect read mapping
---------------------------------

:navy:`Mismatches between read and reference affect the alignment itself, and thus the region of the reference that is covered after read mapping`

The `BWA-MEM <http://bio-bwa.sourceforge.net/bwa.shtml>`_ algorithm works by seeding alignments with maximal exact matches (MEMs) and then extending seeds with the affine-gap Smith-Waterman algorithm (SW). Since sequence reads derived from a given allele at a given locus are identical (except from read errors), the BWA-MEM algorithm generates the same seed and performs the same alignment extension, thus creating exactly the same mapping for all reads derived from the same allele, leading to stacked read alignments per allele.
Polymorphisms may affect the MEM - and thus the initial seed sequence - or stop the extension towards the respective ends of the read if SNPs or InDels interrupt further SW sequence alignment. Notwithstanding, the `BWA-MEM <http://bio-bwa.sourceforge.net/bwa.shtml>`_ alignment algorithm will produce the same mapping for all reads derived from a given allele, with alternative start and end positions compared to reference reads depending on the local distribution of SNPs and InDels.

**Polymorphisms in the middle of a read**

Typically, SNPs or InDels in the middle of the read do not strongly affect the start and end positions of the alignment, as long as minimal read-reference sequence similarity is maintained to support alignment extension outwards from the MEM.

**Polymorphisms towards the ends of a read**

Typically, SNPs and InDels closer to the respective ends of the read will result in soft clipping: the premature truncation of the alignment extension.
Close to the end of a read, InDels may generate a too high gap penalty score, and high density of SNPs may generate a too high cumulative mismatch penalty, to be compensated for by positive scores of matching alignment after the gap or stretch of SNPs, thus leading to truncation of the alignment extension just prior to the start of the polymorphic region (see below).

----

.. _SMAPdelsepvmerg:

SMAPs in separately mapped reads versus merged reads
----------------------------------------------------

In the two tabs below, we illustrate in detail how different types of polymorphisms occuring at various locations within a given locus affect the final read mapping positions. The effect on read mapping is different for separately mapped reads (obtained by single-end or paired-end sequencing), and for paired-end reads that are merged before read mapping.

.. tabs::

   .. tab:: GBS separate reads
   
	  These tabs display schematic overviews of the different reasons why polymorphisms (SNPs and Indels) give rise to alternative mapping positions of reads, compared to a reference read obtained by GBS and mapped as **separate reads**. We show the effects according to the three main steps in the GBS procedure:

	  1. library construction: (gain of RE, loss of RE)
	  #. short, fixed read length sequencing: (insertions and deletions)
	  #. mapping: (soft clipping)

	  .. tabs::

		 .. tab:: gain of RE

				.. image:: ../images/delineate/SMAP_scenario's_seq_align_A.png
			
			| Allele A: a gain of restriction enzyme site in the middle of the fragment.

			| This creates two new PCR-fragments that may both be sequenced (only one is indicated in the scheme). 
			|
			| If only one fragment is PCR-amplifiable, sequenced, and mapped, this creates a novel \3' \  read mapping end and no problem occurs. Note that the novel restriction enzyme site (shown as shaded sequence (CTGCAG) on the \3' \  of the read) is removed during read `preprocessing <https://gbprocess.readthedocs.io/en/latest/index.html>`_. The sequence is indicated here to show how a single SNP can create a novel RE.
			|
			| If both fragments are in the selected size range, but they map next to each other without overlap (image below) (the restriction enzyme site remnant is removed during read preprocessing), the reads are analyzed and counted separately, despite originating from the same chromosome molecule. This inflates the total read counts per locus and **wrongfully** alters haplotype frequencies during :ref:`haplotype calling with SMAP haplotype-sites <SMAPhaploindex>`. To exclude this phenomenon from downstream analysis, by default, all StackClusters are removed where the lowest upstream SMAP of one Stack is found at a higher reference position than the highest downstream SMAP of an other Stack in the same StackCluster. In addition, MergedClusters are removed that were constructed by two StackClusters that do not overlap and an other StackCluster that links the non-overlapping pair (see also :ref:`How it works <SMAPdelHIW3>`).

				.. image:: ../images/delineate/SMAP_scenario's_seq_align_A_extra.png
				
		 .. tab:: loss of RE

				.. image:: ../images/delineate/SMAP_scenario's_seq_align_B.png
			
			| Allele B: a loss of restriction enzyme site.

			| A loss of restriction enzyme site usually leads to a NULL-allele (an allele that can not be amplified and thus lost from detection).
			| The length between the remaining restriction enzyme site and the next neighboring restriction enzyme site is commonly too long for efficient size-selective PCR-amplification and the fragment is thus lost from the GBS library and sequence data.
			| Conversely, if two restriction enzyme sites were initially too close to generate an amplifiable fragment but skipping a restriction enzyme site creates a novel size-selectable PCR-fragment, then loss of a restriction enzyme site may create a novel read mapping end point, as shown here on the \5' \  end of the read.
			| As the read length remains fixed, the \3' \  end of the read mapping also moves upstream with the same distance, thus creating a pair of two novel SMAPs.

		 .. tab:: insertion

				.. image:: ../images/delineate/SMAP_scenario's_seq_align_C.png
			
			| Allele C: a 4 bp insertion in the middle of the read.

			| Sequencing a 4 bp insertion (CATT) in the middle of the read takes up sequence space, hus shortening the distance that can be sequenced away from the RE.
			| Because the total read length is still 86 bp, the 4 bp insert sequence length is \'missing\' from the \3' \  end of the read (GCGG).
			| This shifts the \3' \  end of the read mapping with 4 bp upstream and creates a novel SMAP.
			
		 .. tab:: deletion in middle of read
		 
				.. image:: ../images/delineate/SMAP_scenario's_seq_align_D.png

			| Allele D: a 5 bp deletion in the middle of the read.

			| The \5' \  end read mapping starts directly next to the restriction enzyme site.
			| Because the 5 bp deleted region (CCGGC) does not exist in this allele, but the total read length is still 86 bp, the extra 5 bp sequence length is added to the \3' \  end of the read (AGGAC).
			| This shifts the \3' \  end of the read mapping with 5 bp downstream and creates a novel SMAP.

		 .. tab:: deletion at start of read
		 
				.. image:: ../images/delineate/SMAP_scenario's_seq_align_E.png

			| Allele E: a 4 bp deletion at the start of the read. 

			| Two read mapping shifts occur simultaneously: 
			
				| 1. at the \5' \  end, the remaining 3 bp (CTC) are misaligned because a single mismatch is preferred over a 4 bp gap penalty. This creates an (artefactual) SNP and shifts the \5' \  end of the read mapping with 4 bp and creates a novel SMAP. 
				
				| 2. because the 4 bp deleted region does not exist in this allele, but the total read length is still 86 bp, the extra 4 bp sequence length is added to the \3' \  end of the read (AGGA). This shifts the \3' \  end of the read mapping with 4 bp and creates a novel SMAP. Note: if alignment requires too many mismatches, this ultimately results in soft clipping (see allele G), likely truncating the read alignment at the start of the deletion, thus shifting the mapping. This may occur at either end or even at both ends of a read thus creating novel SMAPs.

		 .. tab:: combination of deletions
		 
				.. image:: ../images/delineate/SMAP_scenario's_seq_align_F.png

			| Allele F: a recombination of allele D and allele E brings both deletions into one haplotype.

			| Two read mapping shifts occur simultaneously:
			
				| 1. at the \5' \  end, the remaining 3 bp (CTC) are misaligned because a single mismatch is prefered over a 4 bp gap penalty. This creates a SNP and shifts the \5' \  end of the read mapping with 4 bp and creates a novel SMAP.
				
				| 2. because the total of 9 bp deleted region does not exist in allele D but the total read length is still 86 bp, the extra 9 bp sequence length is added to the \3' \  end of the read (AGGACGTTC). This shifts the \3' \  end of the read mapping with 9 bp and creates a novel SMAP.
		  
		 .. tab:: soft clipping

				.. image:: ../images/delineate/SMAP_scenario's_seq_align_G.png
			
			Allele G: a high local density of SNPs close to the read end causes soft clipping.

			The original read itself is not truncated, but the alignment stops prematurely (soft clipped region indicated in grey).
			Because `BWA-MEM <http://bio-bwa.sourceforge.net/bwa.shtml>`_ starts from the maximal exact match region, which may be in the middle of the read, and extends the alignment outwards, soft clipping may occur at either end or even at both ends of a read, in any case creating novel SMAPs.
			
			Soft clipping is expected to occur equally often in separately mapped reads compared to merged reads.

   .. tab:: GBS merged reads

	  These tabs display schematic overviews of the different reasons why polymorphisms (SNPs and Indels) give rise to alternative mapping positions of reads, compared to a reference read obtained by GBS and mapped as **merged reads**. We show the effects according to the three main steps in the GBS procedure:

	  1. library construction: (gain of RE, loss of RE)
	  #. short, fixed read length sequencing: (insertions and deletions)
	  #. mapping: (soft clipping)

	  .. tabs::

		 .. tab:: gain of RE

				.. image:: ../images/delineate/SMAP_scenario's_seq_align_PE_A.png

			| Allele A: a gain of restriction enzyme site in the middle of the fragment.

			| This creates two new PCR-fragments that may both be sequenced (only one is indicated in the scheme). 
			|
			| If only one fragment is PCR-amplifiable, sequenced, and mapped, this creates a novel \3' \  read mapping end and no problem occurs. Note that the novel restriction enzyme site (shown as shaded sequence (CTGCAG) on the \3' \  of the read) is removed during read `preprocessing <https://gbprocess.readthedocs.io/en/latest/index.html>`_. The sequence is indicated here to show how a single SNP can create a novel RE.
			|
			| If both fragments are in the selected size range, but they map next to each other without overlap (the restriction enzyme site remnant is removed during read preprocessing) (image below), the reads are analyzed and counted separately, despite originating from the same chromosome molecule. This inflates the total read counts per locus and **wrongfully** alters haplotype frequencies during :ref:`haplotype calling with SMAP haplotype-sites <SMAPhaploindex>`. To exclude this phenomenon from downstream analysis, by default, all StackClusters are removed where the lowest upstream SMAP of one Stack is found at a higher reference position than the highest downstream SMAP of an other Stack in the same StackCluster. In addition, MergedClusters are removed that were constructed by two StackClusters that do not overlap and an other StackCluster that links the non-overlapping pair (see also :ref:`How it works <SMAPdelHIW3>`).

				.. image:: ../images/delineate/SMAP_scenario's_seq_align_PE_A_extra.png
				
			In general for scenario A, merged reads yield the same Stack and the same pair of SMAPs compared to separately mapped reads.

		 .. tab:: loss of RE
			
				.. image:: ../images/delineate/SMAP_scenario's_seq_align_PE_B.png

			Allele B: a loss of restriction enzyme site.

			A loss of restriction enzyme site usually leads to a NULL-allele (an allele that can not be amplified and thus lost from detection).
			The length between the remaining restriction enzyme site and the next neighboring restriction enzyme site is commonly too long for efficient size-selective PCR-amplification and the fragment is thus lost from the GBS library and sequence data.
			Conversely, if two restriction enzyme sites were initially too close to generate an amplifiable fragment but skipping a restriction enzyme site creates a novel size-selectable PCR-fragment, then loss of a restriction site may create a novel read mapping end point, as shown here on the \5' \  end of the read.
			As long as the forward and reverse reads still overlap in the middle of the fragment, the merged read is retained by `PEAR <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3933873/>`_, and read mapping continues all the way to the downstream RE.

			So, in contrast to separately mapped reads, only **one**, not two, novel SMAP is created compared to the reference allele.

		 .. tab:: insertion
			
				.. image:: ../images/delineate/SMAP_scenario's_seq_align_PE_C.png
			
			Allele C: a 4 bp insertion in the middle of the fragment.

			Sequencing a 4 bp insertion (CATT) in the middle of the fragment takes up sequence space in one or both reads, which may reduce the length of sequence in the overlap between forward and reverse reads in the middle of the fragment.
			As long as the forward and reverse reads still overlap in the middle of the fragment, the merged read is retained, and read mapping continues all the way from the upstream RE to the downstream RE.

			So, in contrast to separately mapped reads, **no** novel SMAPs are created compared to the reference allele.
			
		 .. tab:: deletion in middle of read

				.. image:: ../images/delineate/SMAP_scenario's_seq_align_PE_D.png
			
			Allele D: a 5 bp deletion in the middle of the read.

			Because the 5 bp deleted region (CCGGC) does not exist in this allele, the reference sequence covered by both forward and reverse reads is relatively longer, adding to more bases in the overlap recognized by `PEAR <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3933873/>`_. As long as the merged read is retained, read mapping continues all the way from the upstream RE to the downstream RE.

			So, in contrast to separately mapped reads, **no** novel SMAPs are created compared to the reference allele.

		 .. tab:: deletion at start of read

				.. image:: ../images/delineate/SMAP_scenario's_seq_align_PE_E.png
			
		    Allele E: a 4 bp deletion at the start of the read. 

		    | In contrast to separately mapped reads, here only **one** read mapping shift occurs: 

				| at the \5' \  end, the remaining 3 bp (CTC) are misaligned because a single mismatch is preferred over a 4 bp gap penalty. This creates an (artefactual) SNP and shifts the \5' \  end of the read mapping with 4 bp and creates a novel SMAP. Because the 4 bp deleted region (GCGC) does not exist in this allele, the reference sequence covered by both forward and reverse reads is relatively longer, adding more bases in the overlap recognized by `PEAR <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3933873/>`_. As long as the merged read is retained, read mapping continues all the way to the downstream RE.  
				| So, in contrast to separately mapped reads, only one, **not two**, novel SMAPs are created compared to the reference allele. Note: if alignment requires too many mismatches, this ultimately results in soft clipping (see allele G), likely truncating the read alignment at the start of the deletion, thus shifting the mapping. 
				| This may occur at either end or even at both ends of a read, thus creating novel SMAPs.

		 .. tab:: combination of deletions

				.. image:: ../images/delineate/SMAP_scenario's_seq_align_PE_F.png
			
			Allele F: a recombination of allele D and allele E brings both deletions into one haplotype.

			In contrast to separately mapped reads, here only **one** read mapping shift occurs:
			
			at the \5' \  end, the remaining 3 bp (CTC) are misaligned because a single mismatch is preferred over a 4 bp gap penalty.
			This creates an (artefactual) SNP and shifts the \5' \  end of the read mapping with 4 bp and creates a novel SMAP.

			Because the total of 9 bp deleted region does not exist in the forward read of this allele, and the 5 bp deleted region does not exist in the reverse read of this allele, the extra sequence length of both reads adds more bases in the overlap recognized by `PEAR <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3933873/>`_.

			As long as the merged read is retained, read mapping continues all the way to the downstream RE.
			So, in contrast to separately mapped reads, only **one**, not two, novel SMAP is created compared to the reference allele.
		  
		 .. tab:: soft clipping

				.. image:: ../images/delineate/SMAP_scenario's_seq_align_PE_G.png
			
			Allele G: a high local density of SNPs close to the read end causes soft clipping.

			The original read itself is not truncated, but the alignment stops prematurely (soft clipped region indicated in grey).
			Because `BWA-MEM <http://bio-bwa.sourceforge.net/bwa.shtml>`_ starts from the maximal exact match region, which may be in the middle of the read, and extends the alignment outwards, soft clipping may occur at either end or even at both ends of a read, in any case creating novel SMAPs.

			Soft clipping is expected to occur equally often in separately mapped reads compared to merged reads.
		