.. raw:: html

    <style> .navy {color:navy} </style>

.. role:: navy

.. raw:: html

    <style> .white {color:white} </style>

.. role:: white

###################################
Feature Description
###################################

.. _SMAPdesigndef:

Definition of reference gene, CDS, amplicons, guides, and overlaps
------------------------------------------------------------------

| **SMAP design** designs amplicons to resequence specific parts of the genome, possibly in combination with gRNA design for CRISPR/Cas genome editing.

**SMAP design** first creates **amplicons** by designing pairs of primers within a given length range. Specificity of primer binding is embedded in the Primer3 algorithm and tested against all other sequences in the same run of primer design.  
The primer binding site locations of such **amplicons** are also used during the downstream analysis pipeline **SMAP haplotype-window** (:ref:`SMAPs <SMAPdeldef>`), so that the entire workflow from design to analysis is integrated.  
See schemes below for graphical illustration of the concepts.
Amplicons are then positionally overlapped with predefined guides (designed by third-party software such as `CRISPOR <http://crispor.tefor.net/>`_ or `FlashFry <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6033233/>`_), to allow targetted resequencing of potential genome editing sites.

**Schematic overview of reference gene, CDS, amplicons, guides, and overlaps.**

.. image:: ../images/design/Design_overview_scope.png

----

Avoiding polymorphic sites (*e.g.* SNPs) during amplicon design
---------------------------------------------------------------

| It is possible to avoid primer design in locations with known polymorphisms by coding SNP sites as N in the reference sequence before running **SMAP design**.
| Scripts to transform the reference sequence using a list of SNP positions are under development.
