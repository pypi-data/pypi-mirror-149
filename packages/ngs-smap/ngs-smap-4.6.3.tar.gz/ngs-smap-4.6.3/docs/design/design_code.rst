.. raw:: html

    <style> .navy {color:navy} </style>

.. role:: navy

.. raw:: html

    <style> .white {color:white} </style>

.. role:: white

.. _SMAPdesignSummaryCommand:

###########################
Summary of Commands
###########################

This page provides a summary of all options of **SMAP design** and examples of typical commands.

.. _SMAPdesignMandatoryArgs:

Mandatory arguments
-------------------

| It is mandatory to specify the reference FASTA and GFF file as positional arguments:

| ``fasta file`` :white:`#####` *(str)* :white:`###` Path to the fasta file containing all genes to screen. Genes are ideally all oriented with their coding sequence in forward orientation [no default].
| ``gff3 file`` :white:`######` *(str)* :white:`###` Path to the gff3 file with at least the CDS feature with positions relative to the fasta file [no default].

----

General Options
---------------

.. tabs::

    .. tab:: General options

        **General options:**

          | ``FASTA file`` :white:`##` *(str)* :white:`##` Path to the FASTA file containing all target genes [no default].
          | ``GFF file`` :white:`##` *(str)* :white:`##` Path to the GFF file containing at least the CDS of all target genes. The location of the features should correspond to the FASTA file [no default].
          | ``-o``, ``--output`` :white:`##` *(str)* :white:`##` Basename for the outputfiles [SMAPdesign].
          | ``-sg``, ``--selectGenes`` :white:`##` Path to text file containing one gene name per line. These gene names refer to the names used in the FASTA file. If this option is used, only designs will be done for the genes listed in the text file. The other genes in the FASTA file, not mentioned in the text file, will still be used to check for mispriming by Primer3.
          | ``-d``, ``--distance`` :white:`##` *(int)* :white:`##` Minimum number of bases between the gRNA and primer. [15]
          | ``-b``, ``--border`` :white:`##` *(int)* :white:`##` The length of the borders [10]. The borders are used for downstream analysis by SMAP.
          | ``-v``, ``--verbose`` :white:`##` Verbose.


        Command to run **SMAP-design** with specified FASTA and GFF file, a gRNA file, output name "MAP3K_SMAPdesign_output", a text file with a selection of genes to do the design on, and a minimum distance between primer and gRNA of 20 bases::

            python3 SMAP-design genes.fasta genes.gff -g gRNAs.tsv -o MAP3K_SMAPdesign_output -sg geneSelection.txt -d 20

    .. tab:: **gRNA** options

        **gRNA options**

          | ``-g``, ``--gRNAfile`` :white:`##` *(str)* :white:`##` Path to the gRNA file.
          | ``-gs``, ``--gRNAsource`` :white:`##` *(str)* :white:`##` Program used to generate the gRNAs, either CRISPOR, FlashFry, or other [FlashFry].
          | ``-ng``, ``--numbergRNAs`` :white:`##` *(int)* :white:`##` Maximum number of gRNAs to retain per amplicon [2].
          | ``-go``, ``--gRNAoverlap`` :white:`##` *(int)* :white:`##` Minimum number of bases between the start of two adjacent gRNAs [5].
          | ``-t``, ``--threshold`` :white:`##` *(int)* :white:`##` Minimum gRNA MIT score allowed. gRNAs with a score lower than the threshold are discarded [80].
          | ``-gl``, ``--gRNAlabel`` :white:`##` Label the gRNAs (gRNA1, gRNA2, gRNA3...) from left to right instead of from best to worst (based on specificity scores..).
          | ``-tr5``, ``--targetRegion5`` :white:`##` *(float)* :white:`##` The fraction of the coding sequence that cannot be targeted by the gRNAs at the 5' end as indicated by a float between 0 and 1 [0.2].
          | ``-tr3``, ``--targetRegion3`` :white:`##` *(float)* :white:`##` The fraction of the coding sequence that cannot be targeted by the gRNAs at the 3' end as indicated by a float between 0 and 1 [0.2].
          | ``-tsr``, ``--targetSpecificRegion`` :white:`##` *(str)* :white:`##` Only target a specific region in the gene indicated by the feature name in the GFF file.
          | ``-prom``, ``--promoter`` :white:`##` *(str)* :white:`##` Give the last 6 bases of the promoter that will be used to express the gRNA. This will be taken into account when checking for BsaI or BbsI sites in the gRNA. By default the U6 promoter is used [GTAGTG].
          | ``-scaf``, ``--scaffold`` :white:`##` *(str)* :white:`##` Give the first 6 bases of the scaffold that will be used. This will be taken into account when checking for BsaI or BbsI sites in the gRNA [GTTTTA].

        Command to run **SMAP-design** with a gRNA file from CRISPOR, output name "MAP3K_SMAPdesign_output", verbose, maximum 1 gRNA per amplicon, an MIT threshold of 90, targetting the complete gene::

            python3 SMAP-design genes.fasta genes.gff -g gRNAs.tsv, -gs CRISPOR --output "MAP3K_SMAPdesign_output" -v -ng 1 -t 90 -tr5 0 -tr3 0

    .. tab:: **Amplicon**  options

        **Amplicon options**

          | ``-na``, ``--numberAmplicons`` :white:`##` *(int)* :white:`##` The maximum number of non-overlapping amplicons in the output [2].
          | ``-minl``, ``--minimumAmpliconLength`` :white:`##` *(int)* :white:`##` The minimum length of the amplicons in base pairs [120].
          | ``-maxl``, ``--maximumAmpliconLength`` :white:`##` *(int)* :white:`##` The maximum length of the amplicons in base pairs [150].
          | ``-ga``, ``--generateAmplicons`` :white:`##` *(int)* :white:`##` Number of amplicons to generate per gene by Primer3. The more amplicons are designed by Primer3 the longer the run will be but the more choice there is to select for amplicons. To generate 50 amplicons per 1000 bases per gene enter -1 [150].
          | ``-pmlm``, ``--primerMaxLibraryMispriming`` :white:`##` *(int)* :white:`##` The maximum allowed weighted similarity of a primer with any sequence in the target gene set (Primer3 setting) [12].
          | ``-ppmlm``, ``--primerPairMaxLibraryMispriming`` :white:`##` *(int)* :white:`##` The maximum allowed sum of similarities of a primer pair (one similarity for each primer) with any single sequence in the target gene set (Primer3 setting) [24].
          | ``-pmtm``, ``--primerMaxTemplateMispriming`` :white:`##` *(int)* :white:`##` The maximum allowed similarity of a primer to ectopic sites in the template (Primer3 setting) [12].
          | ``-ppmtm``, ``--primerPairMaxTemplateMispriming`` :white:`##` *(int)* :white:`##` The maximum allowed summed similarity of both primers to ectopic sites in the template (Primer3 setting) [24].
          | ``-al``, ``--ampliconLabel`` :white:`##` Number the amplicons (Amplicon1, Amplicon2, Amplicon3...) from left to right instead of from best to worst (based on specificity scores..).
          | ``-mpa``, ``--misPrimingAllowed`` :white:`##` Do not check for mispriming in the gene set when designing primers. By default Primer3 will not allow primers that can prime at other target genes (i.e. other genes in the FASTA file).
          | ``-rpd``, ``--restrictPrimerDesign`` :white:`##` This option will restrict primer design in large introns, increasing the speed of amplicon design, especially useful for genes with large introns such as human genes.
          | ``-hp``, ``--homopolymer`` :white:`##` The minimum number of repeated identical nucleotides in an amplicon to be discarded. E.g. if this parameter is set to 8, amplicons containing a polymer of 8 As (-...AAAAAAAA...-), Ts, Gs, or Cs or more will not be used [10].


        Command to run **SMAP-design** with a gRNA file from neither CRISPOR or FlashFry, 3 gRNAs per amplicon, 2 amplicons per gene, amplicons of length 400 - 800 bp, a primer-gRNA distance of 150 bp, not checking for mispriming between target genes, targeting only the first half of the genes, labeling amplicons and gRNAs from left to right and a minimum distance of 10 bases between adjacent gRNAs::

            python3 SMAP-design genes.fasta genes.gff -g gRNAs.tsv -gs other -ng 3 -na 2 -minl 400 -maxl 800 -d 150 -mpa -tr5 0 -tr3 0.5 -gl -al -go 10

    .. tab:: **extra output files** options

        **Extra output files options**

          | ``-smy``, ``--summary`` :white:`##` Write summary file and plot of the output.
          | ``-bo``, ``--bordersOnly`` :white:`##` Write additional GFF and BED file with only borders (for downstream analysis with SMAP).
          | ``-aa``, ``--allAmplicons`` :white:`##` Write additional GFF, primer and gRNA file with all amplicons and their respective gRNAs per gene.
          | ``-db``, ``--debug`` :white:`##` Write additional GFF file with all amplicons designed by Primer3 and all gRNAs before filtering.

        Command to run **SMAP-design** with a gRNA file from FlashFry, only targeting the kinase domains, with an adapted promoter, labeling the gRNAs from left to right, giving a summary, borders file, all-amplicons file and debug file::

            python3 SMAP-design genes.fasta genes.gff -g gRNAs.tsv -tsr kinase -prom GTGGCA -gl -smy -bo -aa -db


----

Examples
--------

.. tabs::

   .. tab:: amplicon only

	  Typical command to run SMAP design only for amplicons.

	  ::

		python3 SMAP-design /path/to/fasta /path/to/gff -p 8 --plot all --plot_type pdf --output Design1_amplicons -minl 80 -maxl 100 -a 80 -n 20 -na

   .. tab:: amplicons and guides

	  Typical command to run SMAP design for amplicons and guides.

	  ::

		python3 SMAP-design /path/to/fasta /path/to/gff -g /path/to/FlashFry.out -p 8 --plot all --plot_type pdf --output Design4_amplicons_80-100_guides_20 -minl 80 -maxl 100 -a 80 -n 20 -na -b 12 -go 35 -t 90 -ng -d 20
