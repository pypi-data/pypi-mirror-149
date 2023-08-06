.. SMAP documentation master file, created by
   sphinx-quickstart on Wed Aug  5 13:28:17 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


.. _SMAPdesignindex:

SMAP design
===========

| This is the manual for the component **SMAP-design** of the SMAP-package.
| **SMAP design** was created specifically to design primers for amplicon sequencing, in combination with gRNA design from third party software such as CRISPOR or FlashFry.
| **SMAP design** takes one or more reference sequences (FASTA and GFF) as input and designs non-overlapping amplicons per reference taking target specificity into account.
| **SMAP design** can be combined with gRNA sequences for mutation induction of the reference sequences. As such **SMAP design** overlaps these amplicons and gRNAs, and selects n (user-defined) non-overlapping amplicons with gRNAs according several criteria such as number of gRNAs covered by the amplicon, specificity and efficiency scores.
| **SMAP design** creates a primer file, gRNA file, GFF file with all structural features, and optionally a summary file and plot, and input files required for downstream analysis using **SMAP haplotype-window**.


.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
   design_scope_quickstart
   design_feature_definition
   design_HIW
   design_example_data
   design_faq
   design_code

