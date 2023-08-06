
.. raw:: html

    <style> .navy {color:navy} </style>

.. role:: navy

.. raw:: html

    <style> .white {color:white} </style>

.. role:: white

############################
How It Works
############################

.. _SMAPdesignHIW:

Workflow of **SMAP design**
+++++++++++++++++++++++++++

| The target genes must be provided as a FASTA and associated GFF file containing at least the *gene*, *CDS* and *exon* features, which can be obtained using **SMAP selector**.
|
| The gRNAs are provided by the user as a list with the standard output of CRISPOR, FlashFry, or any other tab-delimited file with matching format. The list is filtered based on several criteria: gRNAs with a poly-T stretch (≥4T; a Pol III termination signal), and *Bsa*\I and *Bbs*\I restriction sites (for cloning) are removed and only gRNAs targeting the ‘central part’ of the CDS (as defined by the user as a length percentage) are retained. The gRNAs must also have a minimum user-defined MIT score, when available. For each gene, Primer3 designs a maximum of 150 amplicons (by default) of a user-defined size range. The specificity of each primer is tested against all reference sequences, ensuring no cross-amplification is possible. Amplicons are spaced by a minimum of 5 bp to spread the amplicons across the target genes.
|
| Filtered gRNAs are overlapped with the Primer3-generated amplicons. The amplicons are then ranked based on the gRNAs they cover: first on the number of the gRNAs (an amplicon with two gRNAs will rank higher than an amplicon with one gRNA), second whether the gRNAs overlap with each other (amplicons with non-overlapping gRNAs will rank highest), third on the average gRNA specificity scores, and fourth on the average gRNA efficiency scores. If no specificity or efficiency scores are provided in the gRNA file, amplicons are only ranked based on the number of gRNAs and their relative positions. **SMAP design** selects a (user-defined) maximum number of non-overlapping top-ranking amplicons per gene, each covering a (user-defined) maximum number of gRNAs.  
|
| **SMAP design** generates three output files: a tab-separated values (TSV) file with the primer sequences per gene, a TSV file with the gRNA sequences per gene, and a GFF3 file with the primer and gRNA location on the reference sequences (and other annotation features that were included in the GFF file provided by the user). Sequences for which no design was retained are included at the end of the primer and gRNA file with extra information on the reason for design failure. Optionally, **SMAP design** creates a summary file and summary graphs, to facilitate quick evaluation of the set of gRNAs and amplicons. These graphs show the relationship between the number of gRNAs and the number of non-overlapping amplicons per gene that **SMAP design** generated and indicate the reasons for not retaining any gRNA-overlapping amplicons on given genes. This is either because no gRNAs were designed for that gene, none of the gRNAs passed the filters, Primer3 was not capable of designing specific amplicons for the gene, or there was no overlap between the gRNAs and the amplicons.


SMAP selector
+++++++++++++

Amplicon design optimization starts with choosing the set of genes for which primers need to be designed (grouped by homology group, pathway, interpro domain (`domain repository <https://www.ebi.ac.uk/interpro/about/consortium/>`_)).

Recommendations for the selection of genes can be found in the section :ref:`Recommendations & Troubleshooting <SMAPdesignPickAmplicons>`.

**SMAP design** minimally requires as input a FASTA file with target sequences and a GFF file with gene features such as gene, CDS, exon.

Procedure
~~~~~~~~~

Reference gene sets in FASTA and GFF format can be extracted with the python script Get_fasta_and_gff_for_selected_hom_groups_extended_flanking_region.py

| It is mandatory to specify the genome GFF and FASTA file of the species, the gene families data file and the species as positional arguments:

| ``gff3 file`` :white:`######` *(str)* :white:`###` Path to the gff3 file (tab-delimited) of the species containing gene, CDS, and exon features with positions relative to the fasta file [no default].
| Example from PLAZA: `annotation.selected_transcript.all_features.ath.gff3.gz <https://ftp.psb.ugent.be/pub/plaza/plaza_public_monocots_05/GFF/ath/annotation.selected_transcript.all_features.ath.gff3.gz>`_
| ``fasta file`` :white:`#####` *(str)* :white:`###` Path to the FASTA file containing the genomic sequence of the species [no default].
| Example from PLAZA: `ath.fasta.gz <https://ftp.psb.ugent.be/pub/plaza/plaza_public_dicots_05/Genomes/ath.fasta.gz>`_
| ``gene families data file`` :white:`#####` *(str)* :white:`###` Path to the gene family information file (tab-delimited) for the (coding) genes, separated per gene family type [no default].
| Example from PLAZA: `genefamily_data.HOMFAM.csv.gz <https://ftp.psb.ugent.be/pub/plaza/plaza_public_dicots_05/GeneFamilies/genefamily_data.HOMFAM.csv.gz>`_
| ``species`` :white:`#####` *(str)* :white:`###` Species, corresponding with species indicated in the gene family info file. [no default].
| Example: ath.

The gene families data file can be used to group genes by homology group, pathway, interpro domain... by listing the group_id in the first column of the file, species and gene_id in the second and third column, respectively, and together with the list of 'group_id's' given with the option ``-f``, ``--hom_groups``

.. tabs::

   .. tab:: Example: gene families data file

	  .. csv-table::
	     :file: ../tables/design/gene_families_data_file.csv
	     :header-rows: 1

   .. tab:: Example: group_id's file given with option ``-f, --hom_groups``

	  .. csv-table::
	     :file: ../tables/design/hom_groups.csv
	     :header-rows: 0


| It is mandatory to specify a list with homology groups of interest or a list with genes of interest:

| ``-f``, ``--hom_groups`` :white:`######` *(str)* :white:`###` Path to the list with homology groups of interest [no default and given list with genes is used].
| ``-g``, ``--genes`` :white:`#########` *(str)* :white:`###` Path to the list with genes of interest [no default and given list with homology groups is used].

| Optionally, a flanking region can be extracted upstream and downstream of the target gene:

| ``-r``, ``--region`` :white:`#########` *(int)* :white:`###` Region to extend the FASTA sequence of the genes of interest on both sides with the given number of basepairs or with the maximum possible [default: 0 or enter a positive value].

Options may be given in any order.

Command to run the script with specified GFF and FASTA file, gene families data file, species, region and list with genes of interest::

		python3 Get_fasta_and_gff_for_selected_hom_groups_extended_flanking_region.py /path/to/gff /path/to/fasta /path/to/gene_family_info ath --region 500 --genes /path/to/gene_list

Command to run the script with specified GFF and FASTA file, gene families data file, species, region and list with homology groups of interest::

		python3 Get_fasta_and_gff_for_selected_hom_groups_extended_flanking_region.py /path/to/gff /path/to/fasta /path/to/gene_family_info ath --region 500 --hom_groups /path/to/hom_list

.. image:: ../images/design/SMAPdesign_HIW.png

| Once the FASTA and GFF files are obtained, **SMAP design** is run with these files and optionally with a gRNA file. **SMAP design** first filters the gRNAs from the list and generate amplicons on the reference sequences.

----

gRNA filtering
++++++++++++++

| gRNAs are designed by third-party software like :ref:`FlashFry or CRISPOR <SMAPDesigngRNA>`.
| **SMAP design** applies a couple of filters to gRNAs. The first row of the gRNA file should be a header and is skipped.

* First, for each gRNA **SMAP design** checks whether it is indeed present in the FASTA file and to which strand it corresponds.
* Next, gRNAs with poly-T stretches are discarded since they create a termination signal for Pol III.
* gRNAs with *Bsa*\I or *Bbs*\I recognition sites are also discarded since those restriction enzymes are very often used to clone the gRNAs into expression vectors. To find these sites, the gRNA sequence (without PAM) is extended by the last 6 bases of the promoter and first 6 bases of the scaffold as these extension can create additional restriction sites.
* gRNAs with an MIT score (also known as Hsu score) lower than the threshold are discarded. The MIT score gives an indication on the specificity of the gRNA. The higher the MIT score the more specific the gRNA. More info on the MIT score can be found `here <https://pubmed.ncbi.nlm.nih.gov/23873081/>`_
* gRNAs that target the upstream or downstream ends of the CDS are discarded by default. A gRNA targetting the start of the CDS has a chance of creating an alternative translational start site which can result in a slightly truncated, yet functional protein. A gRNA targeting the end of the CDS might not result in a full knock-out. **SMAP design** calculates the length of the CDS and the position of the gRNA in the CDS; if the gRNA targets the first or last 20% of the CDS length (by default), the gRNA is discarded. As such, the length of the introns do not influence the calculation. Users can adjust the length of 5' and 3' excluded regions.

Amplicon generation
+++++++++++++++++++

Primer3 is used to generate amplicons on each target gene with the following parameters::

    'PRIMER_PRODUCT_SIZE_RANGE': [[-minl, -maxl]],
    'PRIMER_NUM_RETURN': --generateAmplicons,
    'PRIMER_MAX_LIBRARY_MISPRIMING': --primerMaxLibraryMispriming,
    'PRIMER_PAIR_MAX_LIBRARY_MISPRIMING': --primerPairMaxLibraryMispriming,
    'PRIMER_MAX_TEMPLATE_MISPRIMING': --primerMaxTemplateMispriming,
    'PRIMER_PAIR_MAX_TEMPALTE_MISPRIMING': --primerPairMaxTemplateMispriming,
    'PRIMER_MIN_LEFT_THREE_PRIME_DISTANCE': 5,
    'PRIMER_MIN_RIGHT_THREE_PRIME_DISTANCE': 5,

* The **PRIMER_PRODUCT_SIZE_RANGE** parameter determines the size range of the amplicons. The default is set to 120 - 150 bp
* The **PRIMER_NUM_RETURN** parameter  determines the maximum number of amplicons that Primer3 should generate per reference sequence. The default is set to 150 amplicons.
* The **PRIMER_MAX_LIBRARY_MISPRIMING** parameter is the maximum score a primer can have to be used. The score is based on the ability of the primer to bind to other reference sequences in the FASTA file. The default is set to 12.
* The **PRIMER_PAIR_MAX_LIBRARY_MISPRIMING** parameter is the maximum score a primer pair can have to be used. The score is based on the ability of the primer to bind to other reference sequences in the FASTA file. The default is set to 24.
* The **PRIMER_MAX_TEMPLATE_MISPRIMING** parameter is the maximum score a primer can have to be used. The score is based on the ability of the primer to bind elsewhere in the reference sequence.
* The **PRIMER_PAIR_MAX_TEMPLATE_MISPRIMING** parameter is the maximum score a primer pair can have to be used. The score is based on the ability of the primer to bind elsewhere in the reference sequence.
* The **PRIMER_MIN_LEFT_THREE_PRIME_DISTANCE** parameter determines the minimum number of bases between the ends of the left primers. This is set to 5 to prevent amplicons to be designed around hotspots and so spread the amplicons across the reference sequence.
* The **PRIMER_MIN_RIGHT_THREE_PRIME_DISTANCE** parameter determines the minimum number of bases between the ends of the right primers. This is set to 5 to prevent amplicons to be designed around hotspots and so spread the amplicons across the reference sequence.

A mispriming library is given to Primer3 consisting of all reference sequences in the FASTA file. This will ensure that no primers can bind to other reference sequences.

Assignment of gRNAs to amplicons
++++++++++++++++++++++++++++++++

If a gRNA is located between the coordinates of the forward and reverse primer and there is a minimum distance (by default 15 bp) between the gRNA and both primers, the gRNA is retained. gRNAs are assigned to the amplicons in order of highest specificity and efficiency scores, until the maximum allowed number of assigned gRNAs per amplicon is reached.

Amplicon ranking
++++++++++++++++

| At this stage, the amplicons are ranked according to the gRNAs that were assigned to the amplicon.

* First the amplicons are ranked based on the number of gRNAs that were assigned. If the user set the ´´--numbergRNAs´´ parameter to 3, amplicons with 3 amplicons will be ranked first, followed by amplicons with 2 gRNAs and then amplicons with 1 gRNA.
* Next, within the groups of amplicons with an equal number of gRNAs, the amplicons for which the gRNAs do not overlap are ranked above the amplicons for which the gRNAs do overlap. This is to spread the gRNA target sites as much as possible within each amplicon.
* Then, the average MIT score (specificity score) and average number of off-targets of the gRNAs per amplicon is calculated. The amplicons with the highest average MIT score and the lowest number of off-targets are ranked highest.
* Finally, the average doench score (efficiency score) and average out-of-frame score of the gRNAs per amplicon is calculated. The amplicons with the highest average doench and out-of-frame score are ranked highest.

Amplicon and gRNA selection
+++++++++++++++++++++++++++

| To pick the best scoring amplicons, the position in the gene of the highest ranking amplicon is compared to the position of the second highest ranking amplicon.
| If the amplicons do not overlap, the two amplicons are retained. If the amplicons overlap, the position of the highest ranking amplicon is compared to the position of the third highest ranking amplicon and checked for overlap and so on until the maximum number of allowed non-overlapping amplicons per gene is reached.
| If the maximum number of non-overlapping amplicons is not reached, the amplicon combination with the most amplicons is selected.
| The information (ID, position, sequences...) of the selected amplicons and gRNAs are output to primer, gRNA, and GFF files.
