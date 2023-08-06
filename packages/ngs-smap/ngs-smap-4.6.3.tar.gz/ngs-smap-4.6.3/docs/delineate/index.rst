.. SMAP documentation master file, created by
   sphinx-quickstart on Wed Aug  5 13:28:17 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


.. _SMAPdelindex:

SMAP delineate
==============

| This is the manual for the component **SMAP delineate** of the SMAP-package.  
| **SMAP delineate** was designed specifically to analyze `Stacks` of GBS reads mapped onto a reference sequence. It is not meant for other types of NGS libraries.  
| **SMAP delineate** requires special preprocessing of GBS reads before read mapping. Please use instructions and software for GBS read preprocessing as described in the manual of `GBprocesS <https://gbprocess.readthedocs.io/en/latest/index.html>`_. 
| Conversely, **SMAP delineate** may be used to analyze whether all preprocessing steps have been performed correctly, and to recognize and remove technical artefacts before downstream analysis of BAM files.
| **SMAP delineate** analyzes read mapping distribution, and captures read mapping polymorphisms *within* loci and *across* samples. 


| To exploit read mapping polymorphisms as *novel* type of genetic diversity markers, **SMAP delineate** introduces the new concepts of Stack Mapping Anchor Points (SMAPs), Stacks, StackClusters and MergedClusters. Detailed information on these features can be found in the section :ref:`Feature Description <SMAPdeldef>`.



.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
   delineate_scope_quickstart
   delineate_feature_definition
   delineate_HIW
   delineate_example_data
   delineate_faq
   delineate_code

