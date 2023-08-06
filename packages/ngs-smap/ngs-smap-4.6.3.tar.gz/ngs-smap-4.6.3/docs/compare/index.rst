.. SMAP documentation master file, created by
   sphinx-quickstart on Wed Aug  5 13:28:17 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _SMAPcompindex:

SMAP compare
================================

| This is the manual for the SMAP compare component of the SMAP-package.  

| **SMAP compare** identifies the number of common loci across two runs of :ref:`SMAP delineate <SMAPdelindex>`. 
| **SMAP compare** is a useful tool to compare the overlap (or loss thereof) of loci targeted by different NGS methods, in different sample sets, or by specific bioinformatic parameter settings for filtering, etc. This, in turn, helps to optimize NGS library preparation parameters and bioinformatics parameters throughout the entire workflow, for a given set of samples.
| **SMAP compare** can be used to compare loci detected in sets of individuals vs their respective pools (Pool-Seq), in parents versus progeny, or the consistency of NGS library preparation across laboratories. 
| **SMAP compare** can also be used to optimize bioinformatics parameter settings across all steps of read data analysis, including read `preprocessing <https://gbprocess.readthedocs.io/en/latest/gbs_data_processing.html>`_, read mapping (e.g. `BWA-MEM <http://bio-bwa.sourceforge.net/bwa.shtml>`_), and selection of high quality loci by :ref:`SMAP delineate <SMAPdelindex>`.

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
   compare






