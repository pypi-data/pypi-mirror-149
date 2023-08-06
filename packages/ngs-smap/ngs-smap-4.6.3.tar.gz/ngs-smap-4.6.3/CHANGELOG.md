# 4.6.3
* Moved docker container to ILVO organization account ([#81](https://gitlab.com/truttink/smap/-/issues/81)).
* Fixed an issue where the grm line curves always output the same data from each sample pair ([#83](https://gitlab.com/truttink/smap/-/issues/83)).
* Fix an issue where using --locus_information_criterion Unique causes incorrect output in the CompletelyUniqueLoci file (grm) ([#82](https://gitlab.com/truttink/smap/-/issues/82))

# 4.6.2
* Fixed using --informative_loci_as_proportion in grm module ([#79](https://gitlab.com/truttink/smap/-/issues/79))
* Added an option to turn off heatmap annotations in grm module ([#78](https://gitlab.com/truttink/smap/-/issues/78))
* Fixed an issue where line curves could not formatted as a PDF (grm) ([#77](https://gitlab.com/truttink/smap/-/issues/77))
* Resolved an issue where using --locus_information_criterion Unique caused NotImplementedError (grm) ([#76](https://gitlab.com/truttink/smap/-/issues/76))
* Grm module now maintains the order of the samples specified in the second column of the --names file ([#80](https://gitlab.com/truttink/smap/-/issues/80))

# 4.6.1
* Fixed an issue where using the --names option in the grm module caused ValueError ([#74](https://gitlab.com/truttink/smap/-/issues/73))
* Line curves will now be generated for each sample pair in --curves, regardless of their order in the columns ([#75](https://gitlab.com/truttink/smap/-/issues/73))

# 4.6.0
* Added SMAP grm module for calculating the relatedness between samples ([#73](https://gitlab.com/truttink/smap/-/issues/73)).

# 4.5.1
* Fixed an issue creating a barplot of the number of haplotypes with no data ([#72](https://gitlab.com/truttink/smap/-/issues/72)).

# 4.5.0
* Fixed an issue in haplotype where calculating frequencies failed when the counts were not represented in an integer dtype ([#70](https://gitlab.com/truttink/smap/-/issues/70))

# 4.4.0
* Fixed an issue where not all tables would output the reference column name ([#65](https://gitlab.com/truttink/smap/-/issues/65))

# 4.3.0
* Dropped python3.7 support ([#64](https://gitlab.com/truttink/smap/-/issues/64))
* Fix compare component to work with latest bed output from delineate ([#61](https://gitlab.com/truttink/smap/-/issues/61))
* The reference sequence ID is now added as a separate column in haplotype ([#60](https://gitlab.com/truttink/smap/-/issues/60))
* Fix --out option not doing anything ([#58](https://gitlab.com/truttink/smap/-/issues/58))
* Add the ability to create an haplotype table that can be used with Cervus ([#55](https://gitlab.com/truttink/smap/-/issues/55))
* Fix an issue where --min_haplotype_frequency values were rounded to the nearest integer ([#57](https://gitlab.com/truttink/smap/-/issues/57))

# 4.2.2
* Fix an issue where the delineate output .bed file included the number of stacks instead of the number of samples (completeness) ([#54](https://gitlab.com/truttink/smap/-/issues/54))

# 4.2.1
* Add support for python 3.10 ([#51](https://gitlab.com/truttink/smap/-/issues/51))
* Fix an issue where the locus correctness graph is displaying the sample correctness data ([#52](https://gitlab.com/truttink/smap/-/issues/52))
* Fix an aesthetic issue where the correctness and completeness graph labels showed double percentage signs ([#53](https://gitlab.com/truttink/smap/-/issues/51))

# 4.2.0
* Published SMAP on pypi ([#32](https://gitlab.com/truttink/smap/-/issues/32))
* An extra output table has now been made available that provides a list of SMAP and SNP positions for each locus ([#42](https://gitlab.com/truttink/smap/-/issues/42))
* All SMAP and SNP coordinates now use a 1-based coordinate system. Only BED start and stop positions are 0-based, 1-based respectively ([#44](https://gitlab.com/truttink/smap/-/issues/44)).
* Renamed `-read_type` command-line option to `-mapping_orientation`, with possible values `ignore` and `stranded` ([#45](https://gitlab.com/truttink/smap/-/issues/45))
* Fixes an issue where the `--min_number_haplotypes` bound was not inclusive ([#46](https://gitlab.com/truttink/smap/-/issues/46))
* Naming of loci is now systematic in both SMAP delineate and SMAP haplotype ([#47](https://gitlab.com/truttink/smap/-/issues/47))

# 4.1.3
* Fixed an issue where using `--mask_frequency` could not be used when haplotype frequencies drop below the detection threshold (minimum_read_frequency), causing `ValueError` ([#41](https://gitlab.com/truttink/smap/-/issues/41))

# 4.1.2
* Fix an issue where using `--help` causes `ValueError` ([#39](https://gitlab.com/truttink/smap/-/issues/39))
* Fixed an issue where `ValueError` is raised when trying to calculate the correctness for a sample that has no calls ([#40](https://gitlab.com/truttink/smap/-/issues/40))

# 4.1.1
* Fix an issue where `--max_smap_number` defaults to 0, filtering all data ([#38](https://gitlab.com/truttink/smap/-/issues/38))

# 4.1.0
* Enabled Docker support
* Added correctness and completeness plots ([#13](https://gitlab.com/truttink/smap/-/issues/13))
* Output coordinates of saturation plot in seperate output table ([#14](https://gitlab.com/truttink/smap/-/issues/14))
* Print command-line parameters to terminal ([#16](https://gitlab.com/truttink/smap/-/issues/16))
* Added `--locus_correctness` option to haplotype in order to create a new .bed file defining only the loci that were that were correctly dosage called (-z) in the defined percentage of samples ([#21](https://gitlab.com/truttink/smap/-/issues/21))


# 4.0.3
* Bump pandas version to 1.2.2 ([#27](https://gitlab.com/truttink/smap/-/issues/27))
* Dropped support for python3.6 ([#27](https://gitlab.com/truttink/smap/-/issues/27))
* Fix an issue where installation using tarballs from gitlab fails ([#34](https://gitlab.com/truttink/smap/-/issues/34))

# 4.0.2
* Enable support for python 3.9 ([#33](https://gitlab.com/truttink/smap/-/issues/33))

# 4.0.1
* Fix an issue where barplot x-axis labels were always integers ([#30](https://gitlab.com/truttink/smap/-/issues/30))
* After removing loci from the Dosage matrices, the filter for the number of haplotypes is applied again because the number of haplotypes could have decreased ([#29](https://gitlab.com/truttink/smap/-/issues/29))
* The haplotype count barplots had wrong x-axis labels ([#28](https://gitlab.com/truttink/smap/-/issues/28))
* The distinct haplotypes filters are now applied before plotting the haplotype frequencies and the haplotype counts barplot for the frequency matrix ([#26](https://gitlab.com/truttink/smap/-/issues/26))
* Fix an issue where using `--plot summary` option would cause SMAP to generate no graphical output ([#25](https://gitlab.com/truttink/smap/-/issues/25))
* Solve an issue where a cluster is not renames correctly when filtering out stacks ([#24](https://gitlab.com/truttink/smap/-/issues/24))
* Fix an issue with displaying tabs in documentation ([#23](https://gitlab.com/truttink/smap/-/issues/23))
* Added haplotype count barplots for the dosage and filtered dosage matrices ([#22](https://gitlab.com/truttink/smap/-/issues/22))

# 4.0
* Add documentation to readthedocs
* Refactor delineate
* Refactor haplotype
* Completely rework command-line options
* Better scaling of plots
* Enable color in logging
* Rework output
* Add new filtering options
* Add correctness and completeness plots (haplotype)
* Add plot for number of SMAPS per StackCluster and the median read depth per MergedCluster
* Add plots for the correlation between read depth and read length
* Change scatterplot marker size and log scale mergedcluster read depth plot
* Remove cluster if all stacks are removed by the stack depth fraction filter
* Removing stacks from clusters based on relative stack depth is now persitent
* Remove loci with remove loci with no calls from dosage matrices
* Add warning when parsing an empty bam file
# 3.1.1
* Fix incorrect argument type in smap-delineate for maximum number of stacks

# 3.1
* Refactor command-line interface

# 3.0
* Rename haplotype module to haplotype-sites
* Use entrypoints to register different SMAP modules

# 2.3.2
* Fix an issue where pandas NA values could not be interpreted as floating point numbers by numpy.

# 2.3.1
* Replace 'MergedCluster' column name by 'Locus'

# 2.3
* Don't use system calls for checking .vcf file validity
* Added more user input checking
* More efficient usage of memory
* Fix an issue with the calling of dosages for tetraploids and dominant tetraploid use case
* Add automatic testing of SMAP-haplotype

# 2.2.3
* Fixed an issue where the minimum haplotype frequency filtered for maximum haplotype frequency instead

# 2.2.2
*  Fix issue while running delineate where clusters bed files would not be selected for merging if the file names contained a dot

# 2.2.1
* Added tests
* Enable automatic deployment and testing
* Fix delineate help message
* Fix an issue with strandedness while haplotyping
* Fix an issue where finding no haplotypes would result in an error
* Smaller memory footprint

# 2.2
* Add unittests for delineate
* Fix a bug where merged clusters would not be written (delineate)
* Fix: the minimum read depth filter for merged clusters used the stack number count instead of the read depth for filtering
* Fix: apply the correct plot type (png or pdf) for all graphs
* Fix: Fix ValueError if only a few stacks are parsed
* Fix an issue where cigars were written in random order into the output
* Add option to replace NA values in the output
* Add minimum read frequency filter

# 2.1.5
* Speed improvements
* Fix strandedness while delineating stacks from merged reads.
* Fix stack depth
* Sort columns alphabetically for SMAP-haplotype output.

# 2.1.4
* Add haplotype counts to output

# 2.1.3
* Allow plugins to add arguments to subparsers  

# 2.1.2
* Prepare code to allow for plugins (SMAP haplotype-window)

# 2.1.1
* Fix versioning.

# 2.1
* Major refactoring of code.
* Remove the creation of .shelve files.
* Improved logging.
* Improved installation procedure.

# 2.0
* Installation instructions added
* PEP8 formatting
* Remove pysam version checking because now specified in requirements file.
* Algorithmic speed improvements
* More multiprocessing
* Logging is performed using Logger module
* Fix plotting in SMAP-compare

# 1.0
* Initial release