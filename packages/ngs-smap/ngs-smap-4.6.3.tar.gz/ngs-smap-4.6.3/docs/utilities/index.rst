.. SMAP documentation master file, created by
   sphinx-quickstart on Wed Aug  5 13:28:17 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _SMAP_utilities_index:

SMAP utilities
==============

| This is the manual for the complementary **SMAP utilities** tools of the SMAP-package.
| The first step prior to running **SMAP haplotype-sites** is the definition of the locus start and end points.
| The module **SMAP sliding-frame** should be used to define Sliding frames covering SNPs and/or structural variants in Shotgun data (currently run as Python3 scripts provided in the **SMAP utility** tools).

.. image:: ../images/utilities/SMAP_utilities_Sliding_frame_scope_Shotgun.png

| The module **SMAP** :ref:`delineate <SMAPdelindex>` should be run for GBS data to define relevant loci and read mapping polymorphisms in a data-driven manner.
| A module called **SMAP primer-design** will be launched in the near future for integrated design of HiPlex PCR primers and downstream analysis with **SMAP** :ref:`haplotype-sites <SMAPhaploHiPlexHIW>`.

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
   utilities_scope_quickstart

