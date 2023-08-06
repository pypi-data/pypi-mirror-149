"""
SMAP-delineate analyzes read-mapping distribution for
reduced-representation DNA sequencing libraries. The output
can be filtered to produce high-quality loci ready for
downstream analysis.
"""
import logging
import multiprocessing
import warnings
from argparse import ArgumentParser, Namespace
from collections import namedtuple
from csv import DictWriter
from functools import partial
from itertools import chain
from pathlib import Path
from statistics import median
from typing import Dict, Iterable, Iterator, List, TextIO, Tuple, Union
from math import inf, log10
from textwrap import dedent

import pandas as pd
import pysam
from pybedtools import BedTool

from smap import __version__

from .plotting import (PLOT_ALL,
                       PLOT_NOTHING,
                       PLOT_SUMMARY,
                       barplot,
                       histogram,
                       scatterplot,
                       PlotLevel)

LOGGER = logging.getLogger("Delineate")
StacksDict = Dict[str, Dict[str, Union[List[Union[str, int]], str, int]]]
ClustersDict = Dict[int,  Dict[str, Union[List[Union[str, int]], str, int]]]

StacksFilteringOptions = namedtuple('StacksFilteringOptions',
                                    ['min_mapping_quality', 'min_stack_depth', 'max_stack_depth'])
ClustersFilteringOpstions = namedtuple('ClustersFilteringOpstions',
                                       ['min_cluster_length', 'max_cluster_length',
                                        'max_stack_number', 'min_stacks_depth_fraction',
                                        'min_cluster_read_depth', 'max_cluster_read_depth'])


def to_int(lst: Iterable[str]) -> List[int]:
    "Cast an iterable of strings to integers"
    return list(map(int, lst))


class Stacks():
    """
    Stacks are a set of short sequencing reads from one sample with identical
    read mapping start en stop positions. This class provides the means to
    identify the stacks and to filter them and write them to file. Additionally,
    stacks can be merged into clusters.
    """
    _CHROMOSOME_LABEL = 'chr'
    _START_LABEL = 'start'
    _END_LABEL = 'end'
    _STACK_NAME_LABEL = 'name'
    _DEPTH_LABEL = 'stack_depth'
    _STRAND_LABEL = 'strand'
    _CIGAR_LABEL = 'cigar'
    _STACK_COLUMNS = (_CHROMOSOME_LABEL, _START_LABEL,
                      _END_LABEL, _STACK_NAME_LABEL,
                      _DEPTH_LABEL, _STRAND_LABEL,
                      _CIGAR_LABEL)

    def __init__(self,
                 bam: Union[Path, str],
                 strand_specific: bool,
                 min_mapping_quality: int):
        bam = Path(bam)
        if not bam.is_file:
            raise FileNotFoundError(f'{bam}: No such file or directory.')
        assert strand_specific in (True, False)
        if min_mapping_quality < 0 or min_mapping_quality >= 256:
            raise ValueError("The mapping quality must be an integer between 0 and 255.")
        self._number_of_parsed_reads = 0
        self._strand_specific = strand_specific
        self._min_mapping_quality = int(min_mapping_quality)
        self._bam_file = Path(bam)
        self._stacks: StacksDict = self._bam_to_stacks(bam)

    def write_to_bed(self, write_to: TextIO, label: str) -> None:
        """
        Write the stacks to a tab-delimited file (.bed file).
        """
        if not self._stacks:
            return
        columns_to_write = (self._CHROMOSOME_LABEL, self._START_LABEL,
                            self._END_LABEL, self._STACK_NAME_LABEL,
                            self._DEPTH_LABEL, self._STRAND_LABEL,
                            "label"
                            )
        self._stacks = {id_: {**stack, "label": label} for id_, stack in self._stacks.items()}
        writer = DictWriter(write_to,
                            delimiter="\t",
                            fieldnames=columns_to_write,
                            lineterminator='\n',
                            extrasaction='ignore')
        writer.writerows(self._stacks.values())
        write_to.flush()

    @property
    def bam_file(self) -> Path:
        """
        File which contains the mapping information that was used
        to generate the stacks.
        """
        return self._bam_file

    @bam_file.setter
    def bam_file(self, bam_path: Union[str, Path]):
        bam_path = Path(bam_path)
        if not bam_path.is_file():
            raise ValueError(("The given path does not seem to "
                              f"point to an existing file {bam_path}."))
        self._bam_file = bam_path

    @property
    def number_of_parsed_reads(self) -> int:
        """
        Number of reads (unfiltered) that were used to build
        the stacks.
        """
        return self._number_of_parsed_reads

    def depth_filter(self, min_stack_depth: int, max_stack_depth: int) -> None:
        """
        Filter out stacks below minimal stack depth, used to remove spurious reads.
        Filter out stacks above maximal stack depth, used to remove loci with potential
        homeologous mapping or repetitive sequences.
        """
        self._stacks = {name: stack for name, stack in self._stacks.items()
                        if min_stack_depth <= stack[self._DEPTH_LABEL] <= max_stack_depth}

    def merge(self) -> 'Clusters':
        """
        Merge the stacks into clusters. Stacks are merged using the bedtools merge tool,
        which combines overlapping regions of the genome into a single feature.
        """
        if not self._stacks:
            return Clusters({}, self._strand_specific)
        # Configure the merge. Each tuple in this list represents an output column
        # after the merge. The first element of the tuple is the input for that column,
        # the second element is the operation performed on that column to generate the output.
        # These are 'extra' columns: the first three are always chr, start and stop.
        merge_options = [
            (self._DEPTH_LABEL, 'collapse'),
            (self._STRAND_LABEL, 'distinct'),
            (self._START_LABEL, 'collapse'),
            (self._END_LABEL, 'collapse'),
            (self._CIGAR_LABEL, 'collapse'),
            (self._CIGAR_LABEL, 'count')
        ]

        # Put the stacks into a .bed file
        bed_data_frame = pd.DataFrame.from_dict(self._stacks, orient='index')
        bed_data_frame = bed_data_frame[list(self._STACK_COLUMNS)]
        bed = BedTool.from_dataframe(bed_data_frame)

        # Bedtools uses column positions to define the input, get those positions.
        column_options = [(self._STACK_COLUMNS.index(column_name)+1, column_option)
                          for (column_name, column_option) in merge_options]
        columns, options = list(zip(*column_options))

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            # Merge the stacks. Merge requires a sorted bed as input
            # s: allow stacks on the same strand to overlap or not
            # d: distance between stacks
            # c: the indices of the input columns
            # o: the operations to perform on the input columns
            merged_stacks = bed.sort().merge(s=self._strand_specific, d=-1,
                                             c=columns, o=options)

        # Transform the bed file into a dictionary.
        # to_dataframe passes extra arguments to pandas.read_tables.
        merged_stacks = merged_stacks.to_dataframe(header=None, names=Clusters.fields())
        merged_stacks.reset_index()

        for i, (_, column_option) in enumerate(merge_options):
            # collapse generates a comma separated multivalue string
            # Split into a list, and cast to integer of possible
            if column_option == "collapse":
                try:
                    str_column = merged_stacks.iloc[:, i+3].str
                except AttributeError:
                    # If the column contains only single-values,
                    # it could have been inferred as type int by pandas.
                    # In that case, cast it to string, as split only works on
                    # strings.
                    str_column = merged_stacks.iloc[:, i+3].astype(str).str
                # The first three columns are chr, start, stop
                # The other columns are set by the c= option in merge()
                try:
                    new_column = str_column.split(',').apply(to_int)
                except ValueError:
                    new_column = str_column.split(',')
                merged_stacks.iloc[:, i+3] = new_column
        return Clusters(merged_stacks.to_dict(orient='index'),
                        self._strand_specific)

    def plot_depth(self, name: str, plot_type: str) -> None:
        if not self._stacks:
            return
        stack_depths = [stack[self._DEPTH_LABEL] for stack in self._stacks.values()]
        max_depth = max(stack_depths)
        # Get the closest power of 10 for x-axis ticks
        closest_power = int(round(log10(max_depth), 0))
        xaxisticks = max(1, 10**max(1, closest_power-1))
        histogram(stack_depths,
                  f'{name}.Stack.depth',
                  f'Stack read depth\nsample: {name}',
                  'Stack read depth (counts)',
                  'Number of Stacks',
                  'g',
                  0,
                  max_depth,
                  1,
                  plot_type=plot_type,
                  xaxisticks=xaxisticks,
                  ylog_scale=True)

    def plot_length(self, name: str, plot_type: str) -> None:
        """
        Create a histogram of the stack lengths.
        """
        if not self._stacks:
            return
        lengths = [stack[self._END_LABEL] - stack[self._START_LABEL]
                   for stack in self._stacks.values()]
        max_length = max(lengths)
        closest_power = int(round(log10(max_length), 0))
        xaxisticks = max(1, 10**max(1, closest_power-1))
        histogram(lengths,
                  f'{name}.Stack.length',
                  f'Stack length\nsample: {name}',
                  'Stack length (bp)',
                  'Number of Stacks',
                  'g',
                  0,
                  max_length,
                  1,
                  plot_type=plot_type,
                  xaxisticks=xaxisticks)

    def plot_read_length_depth_correlation(self, name: str, plot_type: str) -> None:
        if not self._stacks:
            return
        lengths = [stack[self._END_LABEL] - stack[self._START_LABEL]
                   for stack in self._stacks.values()]
        stack_depths = [stack[self._DEPTH_LABEL] for stack in self._stacks.values()]
        scatterplot(lengths,
                    stack_depths,
                    f'{name}.Stack.LengthDepthCorrelation',
                    f'Read depth distribution at varying Stack length.\nsample: {name}',
                    'Stack length (bp)',
                    'Stack read depth (counts)',
                    'g',
                    plot_type,
                    marker="$\u00B7$"
                    )

    def plot_cigar_operators(self, name: str, plot_type: str) -> None:
        if not self._stacks:
            return None
        distribution = {'H': 0, 'S': 0, 'I': 0, 'D': 0}
        total = 0
        cigars = [stack[self._CIGAR_LABEL] for stack in self._stacks.values()]
        possible_letters = distribution.keys()
        for cigar in cigars:
            for letter in possible_letters:
                if letter in cigar:
                    distribution[letter] += 1
            total += 1
        plot_labels = {'H': "Hard\nclipping", 'S': "Soft\nclipping",
                       'D': "Deletion", 'I': "Insertion"}
        distribution_renamed = {plot_labels[letter]: count
                                for letter, count in distribution.items()}
        distribution_renamed['Total reads'] = total

        barplot(distribution_renamed.keys(), distribution_renamed.values(),
                name=f'{name}.cigar.counts',
                title=f'Abundance of read mapping features\nsample: {name}',
                xlab='Cigar operator class',
                ylab='Number of mapped reads',
                color='orange',
                plot_type=plot_type)

    def _bam_to_stacks(self, bam_file: Path) -> StacksDict:
        """
        Read the reads in a .bam file and generate the stacks. Filter out reads
        for which the mapping quality was below the defined threshold.
        """
        try:
            bamfile = pysam.AlignmentFile(bam_file, 'rb')
        except ValueError as exc:
            raise ValueError(f"Could not read records from file {bam_file}. "
                             "It could be either malformatted or empty.") from exc
        else:
            stacks = self._reads_to_stacks(self._mapping_quality_filter(bamfile.fetch()))
            if self.number_of_parsed_reads == 0:
                LOGGER.warning("No records passed the mapping quality filter for %s.", bam_file)
            bamfile.close()
            return stacks

    def _reads_to_stacks(self, reads: Iterator[pysam.AlignedSegment]) -> StacksDict:
        """
        Generate stacks by counting the reads that have the same unique read-reference mapping.
        """
        parsed_reads = 0
        stacks = {}
        for read in reads:
            reference_end = read.reference_end
            if reference_end is None:
                # reference_end points to one past the last aligned residue.
                # Returns None if not available (read is unmapped or no cigar alignment present).
                continue

            reference_name = read.reference_name  # Chromosome or scaffold
            reference_start = int(read.reference_start)
            orientation_suffix, strand = self._get_strand_info(read)

            # A string to uniquely identify the stack
            name = f"{reference_name}:{reference_start+1}-{reference_end}{orientation_suffix}"
            try:
                # Check if the stack exists
                stack = stacks[name]
            except KeyError:
                # Create a new stack if it does not exist.
                stacks[name] = {self._STACK_NAME_LABEL: name,
                                self._CHROMOSOME_LABEL: reference_name,
                                self._START_LABEL: reference_start,
                                self._END_LABEL: int(reference_end),
                                self._CIGAR_LABEL: read.cigarstring,
                                self._STRAND_LABEL: strand,
                                self._DEPTH_LABEL: 1
                                }
            else:
                # Add an extra read count to an already existing stack
                stack[self._DEPTH_LABEL] += 1
            parsed_reads += 1
        self._number_of_parsed_reads = parsed_reads
        return stacks

    def _get_strand_info(self, read: pysam.AlignedSegment) -> Tuple[str, str]:
        """
        Get the read strand information. For merged reads the strand is always '+'.
        For separate reads, get the strand information from the alignment. The orientation
        suffix is used as string representation in the stack name.
        """
        strand = "-" if self._strand_specific and read.is_reverse else "+"
        return f"_{strand}", strand

    def _mapping_quality_filter(self, read_iterator: Iterator[pysam.AlignedSegment]) \
            -> Iterator[pysam.AlignedSegment]:
        yield from filter(lambda x: x.mapping_quality >= self._min_mapping_quality, read_iterator)


class Clusters():
    """
    Clusters are groupings of unique sets of mapped reads (stacks).
    If regions of two or more stacks overlap, they are merged into a cluster.
    """
    _CLUSTER_NAME_LABEL = 'name'
    _CHROMOSOME_LABEL = 'chr'
    _DEPTH_LABEL = 'stack_depth_collapse'
    _START_LABEL = 'start'
    _START_COLLAPSE_LABEL = 'start_collapse'
    _END_COLLAPSE_LABEL = 'end_collapse'
    _CIGAR_COLLAPSE_LABEL = 'cigar_collapse'
    _STRAND_LABEL = 'strand'
    _END_LABEL = 'end'
    _STACK_COUNT_LABEL = 'stack_number_count'
    _CLUSTER_COLUMNS = (_CHROMOSOME_LABEL,
                        _START_LABEL,
                        _END_LABEL,
                        _DEPTH_LABEL,
                        _STRAND_LABEL,
                        _START_COLLAPSE_LABEL,
                        _END_COLLAPSE_LABEL,
                        _CIGAR_COLLAPSE_LABEL,
                        _STACK_COUNT_LABEL)

    def __init__(self, merged_stacks: dict, strand_specific: bool):
        assert strand_specific in (True, False)
        self._merged_stacks = merged_stacks
        self._strand_specific = strand_specific

    @classmethod
    def fields(cls) -> Tuple[str]:
        """
        Information that needs to be specified for each cluster.
        """
        return cls._CLUSTER_COLUMNS

    @property
    def number_of_clusters(self) -> int:
        """
        The number of clusters.
        """
        return len(self._merged_stacks)

    def __add__(self, other: 'Clusters') -> 'Clusters':
        """
        Add two groups of clusters together, making sure their names (ids)
        are unique.
        """
        return Clusters({i: cluster
                         for i, (_, cluster)
                         in enumerate(chain(self._merged_stacks.items(),
                                            other._merged_stacks.items()))},
                        self._strand_specific)

    def merge(self, strand_specific: bool) -> 'MergedClusters':
        """
        Merge the clusters into MergedClusters. Clusters are merged using the bedtools merge tool,
        which combines overlapping regions of the genome into a single feature. Can be used to
        combine information across samples, by first joining the clusters togther (see __add__).
        """
        assert strand_specific in (True, False)
        if not self._merged_stacks:
            return MergedClusters({})
        # Generate a dataframe to use with pybedtools
        columns = list(self._CLUSTER_COLUMNS)  # Copy
        columns.insert(3, self._CLUSTER_NAME_LABEL)
        to_dataframe_dict = self._add_cluster_name(self._merged_stacks)

        # Flatten lists
        to_dataframe_dict = {
            id_: {field: ",".join(map(str, value_)) if isinstance(value_, list) else value_
                  for field, value_ in cluster.items()}
            for id_, cluster in to_dataframe_dict.items()
        }

        clusters_dataframe = pd.DataFrame.from_dict(to_dataframe_dict,
                                                    orient='index',
                                                    columns=columns)
        bed = BedTool.from_dataframe(clusters_dataframe)

        # Configure the merge. Each tuple in this list represents an output column
        # after the merge. The first element of the tuple is the input for that column,
        # the second element is the operation performed on that column to generate the output.
        # These are 'extra' columns: the first three are always chr, start and stop.
        merge_options = [
            (self._STRAND_LABEL, 'distinct'),
            (self._DEPTH_LABEL, 'collapse'),
            (self._START_COLLAPSE_LABEL, 'collapse'),
            (self._END_COLLAPSE_LABEL, 'collapse'),
            (self._STACK_COUNT_LABEL, 'sum'),
            (self._STACK_COUNT_LABEL, 'count')
        ]

        # Bedtools uses column positions to define the input, get those positions.
        column_options = [(columns.index(column_name)+1, column_option)
                          for (column_name, column_option) in merge_options]
        columns_indices, options = list(zip(*column_options))

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            # Merge the clusters. Merge requires a sorted bed as input
            # s: allow stacks on the same strand to overlap or not
            # d: distance between stacks
            # c: the indices of the input columns
            # o: the operations to perform on the input columns
            merged_clusters = bed.sort().merge(s=strand_specific, d=-1,
                                               c=columns_indices, o=options)

        # Transform the bed file into a dictionary.
        # to_dataframe passes extra arguments to pandas.read_tables.
        merged_clusters = merged_clusters.to_dataframe(header=None, names=MergedClusters.fields())

        # collapse generates a comma separated multivalue string
        # Split into a list, and cast to integer of possible
        for i, (_, column_option) in enumerate(merge_options):
            if column_option == "collapse":
                try:
                    str_column = merged_clusters.iloc[:, i+3].str
                except AttributeError:
                    # If the column contains only single-values,
                    # it could have been inferred as type int by pandas.
                    # In that case, cast it to string.
                    str_column = merged_clusters.iloc[:i+3].astype(str)
                # The first three columns are chr, start, stop
                # The other columns are set by the c= option in merge()
                try:
                    new_column = str_column.split(',').apply(to_int)
                except ValueError:
                    new_column = str_column.split(',')
                merged_clusters.iloc[:, i+3] = new_column
        return MergedClusters(merged_clusters.to_dict(orient='index'))

    def write_to_bed(self, buffer: TextIO, label: str):
        """
        Write the clusters to a tab-delimited file (.bed file).
        """
        if not self._merged_stacks:
            return
        to_write_dict = {}
        for id_, cluster in self._merged_stacks.items():
            # Write sum of the read depth instead of a list
            read_depth = sum(cluster[self._DEPTH_LABEL])

            # Get a sorted unique SMAP list
            # Start and end positions are bed-format: start 0-based, end 1-based (incl.)
            # However, for SMAPS and SNPS, we use 1-based (like in VCF format)
            start_positions = [start+1 for start in cluster[self._START_COLLAPSE_LABEL]]
            unique_positions = set(start_positions +
                                   cluster[self._END_COLLAPSE_LABEL])
            nr_smaps = len(unique_positions)
            all_positions = ",".join(map(str, sorted(list(unique_positions))))
            to_write_dict[id_] = {**cluster,
                                  'label': label,
                                  'all_smaps': all_positions,
                                  'depth_sum': read_depth,
                                  'nr_smaps': nr_smaps}
        to_write_dict = self._add_cluster_name(to_write_dict)

        # Join lists into comma-separated strings.
        to_write_dict = {
            id_: {field: ",".join(map(str, value_)) if isinstance(value_, list) else value_
                  for field, value_ in cluster.items()}
            for id_, cluster in to_write_dict.items()
        }
        fieldnames = (self._CHROMOSOME_LABEL, self._START_LABEL, self._END_LABEL,
                      self._CLUSTER_NAME_LABEL, 'depth_sum', self._STRAND_LABEL,
                      'all_smaps', self._STACK_COUNT_LABEL, 'nr_smaps', 'label')
        writer = DictWriter(buffer, delimiter="\t", fieldnames=fieldnames,
                            lineterminator='\n', extrasaction='ignore')
        writer.writerows(to_write_dict.values())
        buffer.flush()

    def _add_cluster_name(self, merged_stacks: ClustersDict) -> ClustersDict:
        """
        Add a name for a cluster to the info about that cluster.
        This is a helper function for generating .bed files and the MergedClusters.
        The start and stop positions are defined according to the bed format,
        however, in the cluster name, we use 1-based coordinates, so we add 1 to the start.
        """
        return {id_: dict(cluster, **{self._CLUSTER_NAME_LABEL:
                (f"{cluster[self._CHROMOSOME_LABEL]}:"
                 f"{cluster[self._START_LABEL]+1}-"
                 f"{cluster[self._END_LABEL]}_"
                 f"{cluster[self._STRAND_LABEL]}")})
                for id_, cluster in merged_stacks.items()}

    def plot_stack_number_per_cluster(self, name: str, plot_type: str) -> None:
        """
        Plot a histogram of the number of stacks in a cluster.
        """
        if not self._merged_stacks:
            return
        stack_numbers = [cluster[self._STACK_COUNT_LABEL]
                         for cluster in self._merged_stacks.values()]
        histogram(stack_numbers,
                  f'{name}.StackCluster.Stacks',
                  f'Stacks per StackCluster\nsample: {name}',
                  'Stacks per StackCluster',
                  'Number of StackClusters',
                  'b',
                  1,
                  max(stack_numbers),
                  1,
                  plot_type,
                  xaxisticks=1 if max(stack_numbers) < 10 else 5)

    def plot_cluster_read_depth(self, name: str, plot_type: str) -> None:
        """
        Plot a histogram of the total read depth in each cluster.
        """
        if not self._merged_stacks:
            return
        cluster_read_depths = [sum(cluster[self._DEPTH_LABEL])
                               for cluster in self._merged_stacks.values()]
        max_depth = max(cluster_read_depths)
        closest_power = int(round(log10(max_depth), 0))
        xaxisticks = max(1, 10**max(1, closest_power-1))
        histogram(
            cluster_read_depths,
            f'{name}.StackCluster.depth',
            f'StackCluster read depth\nsample: {name}',
            'StackCluster read depth (counts)',
            'Number of StackClusters',
            'b',
            0,
            max_depth,  # responds to user defined thresholds
            1,
            plot_type,
            xaxisticks=xaxisticks,
            ylog_scale=True
        )

    def plot_cluster_stack_depth_ratio(self, name: str, plot_type: str) -> None:
        """
        Plot a histogram of the stack depth fraction for each cluster.
        The stack depth fraction of a cluster is the ratio of the smallest
        read depth of all stacks in a cluster to total read depth of all stacks
        in the cluster.
        """
        if not self._merged_stacks:
            return
        ratios = []
        for cluster in self._merged_stacks.values():
            sd_sum = sum(cluster[self._DEPTH_LABEL])
            sd_min = min(cluster[self._DEPTH_LABEL])
            sd_ratio = int(round((sd_min/sd_sum)*100))
            ratios.append(sd_ratio)
        histogram(ratios,
                  f'{name}.StackCluster.sdf',
                  f'Minimum SDF per StackCluster\nsample: {name}',
                  'Minimum SDF per StackCluster (%)',
                  'Number of StackClusters',
                  'b',
                  1,
                  100,  # ratio, always in the range 0-100.
                  1,
                  plot_type,
                  xaxisticks=10)

    def plot_cluster_lengths(self, name: str, plot_type: str) -> None:
        """
        Plot a histogram of the cluster lengths.
        """
        if not self._merged_stacks:
            return
        cluster_lengths = [cluster[self._END_LABEL] - cluster[self._START_LABEL]
                           for cluster in self._merged_stacks.values()]
        histogram(cluster_lengths,
                  f'{name}.StackCluster.length',
                  f'StackCluster length\nsample: {name}',
                  'StackCluster length (bp)',
                  'Number of StackClusters',
                  'b',
                  0,
                  max(cluster_lengths),
                  2,
                  plot_type,
                  xaxisticks=10)

    def plot_number_of_smaps(self, name: str, plot_type: str) -> None:
        if not self._merged_stacks:
            return
        smap_counts = [len(set(cluster[self._START_COLLAPSE_LABEL] +
                               cluster[self._END_COLLAPSE_LABEL]))
                       for cluster in self._merged_stacks.values()]
        histogram(smap_counts,
                  f'{name}.StackCluster.SMAP',
                  f'Number of SMAPs per StackCluster\nsample: {name}',
                  'SMAPs per StackCluster',
                  'Number of StackClusters',
                  'b',
                  2,
                  max(smap_counts),
                  1,
                  plot_type,
                  xaxisticks=1 if max(smap_counts) < 10 else 5)

    def plot_read_length_depth_correlation(self, name: str, plot_type: str) -> None:
        if not self._merged_stacks:
            return
        lengths = [cluster[self._END_LABEL] - cluster[self._START_LABEL]
                   for cluster in self._merged_stacks.values()]
        cluster_depths = [sum(cluster[self._DEPTH_LABEL])
                          for cluster in self._merged_stacks.values()]
        scatterplot(lengths,
                    cluster_depths,
                    f'{name}.StackCluster.LengthDepthCorrelation',
                    f'Read depth distribution at varying StackCluster length.\nsample: {name}',
                    'StackCluster length (bp)',
                    'StackCluster read depth (counts)',
                    'b',
                    plot_type,
                    marker="$\u00B7$"
                    )

    def max_stack_number_filter(self, max_stack_number: int) -> None:
        """
        Filter clusters to remove those composed of too many stacks.
        """
        self._merged_stacks = {number: stack for number, stack in self._merged_stacks.items()
                               if stack[self._STACK_COUNT_LABEL] <= max_stack_number}

    def read_depth_filter(self,
                          min_cluster_read_depth: int,
                          max_cluster_read_depth: int) -> None:
        """
        Filter cluster to remove those for which the total read depth in the stacks is either
        too low or too high.
        """
        self._merged_stacks = {id_: cluster for id_, cluster in self._merged_stacks.items()
                               if min_cluster_read_depth <= sum(cluster[self._DEPTH_LABEL]) <=
                               max_cluster_read_depth}

    def length_filter(self, min_length: int, max_length: int) -> None:
        """
        Filter clusters to remove those that are either too long or too short.
        """
        self._merged_stacks = {id_: cluster for id_, cluster in self._merged_stacks.items()
                               if min_length <=
                               (cluster[self._END_LABEL] - cluster[self._START_LABEL])
                               <= max_length}

    def stack_depth_fraction_filter(self, minimum_stack_depth_fraction: float) -> None:
        """
        Redefine clusters to remove stacks that contain too few reads compared to
        other stacks in te same cluster. The creterion for removing a stack from
        a cluster is the relative stack depth fraction: the ratio of the read depth
        for a stack and the total read depth in a cluster.
        """
        result = {}
        for id_, cluster in self._merged_stacks.items():
            # Do not change the object while you are iterating!
            # Create a copy
            new_cluster = dict(cluster)

            # Calculate the depth fraction for each stack in the cluster
            total_cluster_depth = sum(cluster[self._DEPTH_LABEL])
            relative_stack_depths = [i/total_cluster_depth * 100
                                     for i in cluster[self._DEPTH_LABEL]]

            # Based on the stack depth, get the stacks we want to keep
            stacks_to_keep = [stack_depth >= minimum_stack_depth_fraction
                              for stack_depth in relative_stack_depths]
            if any(stacks_to_keep):
                # Define the columns we need to filter to remove the stacks
                columns = [self._START_COLLAPSE_LABEL, self._END_COLLAPSE_LABEL,
                           self._DEPTH_LABEL, self._CIGAR_COLLAPSE_LABEL]

                # Filter the columns. Stack information is stored as lists in
                # these columns, where information about the same stack
                # is stored at the same location in each list.
                for column in columns:
                    new_cluster[column] = [entry
                                           for to_keep, entry in
                                           zip(stacks_to_keep, cluster[column])
                                           if to_keep]

                # Update the start and stop position of the cluster
                new_cluster[self._START_LABEL] = min(new_cluster[self._START_COLLAPSE_LABEL])
                new_cluster[self._END_LABEL] = max(new_cluster[self._END_COLLAPSE_LABEL])
                new_cluster[self._STACK_COUNT_LABEL] = sum(stacks_to_keep)
                result[id_] = new_cluster
        self._merged_stacks = result


class MergedClusters():
    """
    Merged clusters are groupings of overlapping clusters.
    If regions of two or more clusters overlap, they are merged into a mergedcluster.
    """
    _CHROMOSOME_LABEL = 'chr'
    _START_LABEL = 'start'
    _END_LABEL = 'end'
    _STRAND_LABEL = 'strand'
    _DEPTH_LABEL = 'cluster_depth_collapse'
    _START_COLLAPSE_LABEL = 'start_collapse'
    _END_COLLAPSE_LABEL = 'end_collapse'
    _CLUSTER_COUNT_LABEL = 'cluster_count'
    _SAMPLE_COUNT_LABEL = 'sample_count'
    _MERGED_CLUSTER_COLUMNS = (_CHROMOSOME_LABEL, _START_LABEL, _END_LABEL,
                               _STRAND_LABEL, _DEPTH_LABEL, _START_COLLAPSE_LABEL,
                               _END_COLLAPSE_LABEL,
                               _CLUSTER_COUNT_LABEL, _SAMPLE_COUNT_LABEL)

    def __init__(self, merged_clusters: dict):
        self._merged_clusters = merged_clusters

    @classmethod
    def fields(cls) -> Tuple[str]:
        """
        Information that needs to be specified for each merged cluster.
        """
        return cls._MERGED_CLUSTER_COLUMNS

    def write_to_bed(self, buffer: TextIO, label: str) -> None:
        """
        Write the merged clusters to a tab-delimited file (.bed file).
        """
        if not self._merged_clusters:
            LOGGER.warning("No merged clusters were generated! "
                           "Either the input files are malfomated "
                           "or the filtering parameters are too strict.")
            return
        to_write = {}
        for id_, cluster in self._merged_clusters.items():
            new_cluster = dict(cluster)
            positions = \
                set(i+1 for i in cluster[self._START_COLLAPSE_LABEL]) | \
                set(cluster[self._END_COLLAPSE_LABEL])
            name = (f"{cluster[self._CHROMOSOME_LABEL]}:"
                    f"{cluster[self._START_LABEL]+1}-"
                    f"{cluster[self._END_LABEL]}_"
                    f"{cluster[self._STRAND_LABEL]}")
            new_cluster['label'] = label
            new_cluster['SMAP_pos'] = sorted(list(positions))
            new_cluster['nr_smaps'] = len(positions)
            new_cluster['SMAP_pos_count'] = len(positions)
            new_cluster['name'] = name
            new_cluster['read_depth'] = median(cluster[self._DEPTH_LABEL])
            to_write[id_] = new_cluster

        # Join lists into comma-separated strings.
        to_write = {
            id_: {field: ",".join(map(str, value_)) if isinstance(value_, list) else value_
                  for field, value_ in merged_cluster.items()}
            for id_, merged_cluster in to_write.items()
        }

        fieldnames = [self._CHROMOSOME_LABEL, self._START_LABEL, self._END_LABEL,
                      'name', 'read_depth', self._STRAND_LABEL, 'SMAP_pos',
                      self._SAMPLE_COUNT_LABEL, 'SMAP_pos_count', 'label']
        writer = DictWriter(buffer, delimiter="\t", fieldnames=fieldnames,
                            extrasaction='ignore', lineterminator='\n')
        writer.writerows(to_write.values())
        buffer.flush()

    def plot_completeness(self, name: str, plot_type: str) -> None:
        """
        Create a histogram of the completeness: in how many samples
        does a mergedcluster occur.
        """
        if not self._merged_clusters:
            return
        sample_counts = [cluster[self._SAMPLE_COUNT_LABEL]
                         for cluster in self._merged_clusters.values()]
        histogram(sample_counts,
                  f'{name}.MergedCluster.Completeness',
                  'MergedCluster completeness\nacross all samples',
                  'MergedCluster completeness (number of samples)',
                  'Number of MergedClusters',
                  'r',
                  1,
                  max(sample_counts),
                  1,
                  plot_type,
                  xaxisticks=1 if max(sample_counts) < 10 else 5)

    def plot_merged_cluster_length(self, name: str, plot_type: str) -> None:
        """
        Create a histogram of the merged cluster lengths.
        """
        if not self._merged_clusters:
            return
        lengths = [cluster[self._END_LABEL] - cluster[self._START_LABEL]
                   for cluster in self._merged_clusters.values()]
        max_length = max(lengths)
        closest_power = int(round(log10(max_length), 0))
        xaxisticks = max(1, 10**max(1, closest_power-1))
        histogram(lengths,
                  f'{name}.MergedCluster.length',
                  'MergedCluster length\nAcross all samples',
                  'MergedCluster length (bp)',
                  'Number of MergedClusters',
                  'r',
                  0,
                  max(lengths),
                  2,
                  plot_type,
                  xaxisticks=xaxisticks)

    def plot_number_of_smaps(self, name: str, plot_type: str) -> None:
        """
        Create a histogram of the number of SMAPs in the merged clusters.
        """
        if not self._merged_clusters:
            return
        smap_counts = [len(set(cluster[self._START_COLLAPSE_LABEL]) |
                           set(cluster[self._END_COLLAPSE_LABEL]))
                       for cluster in self._merged_clusters.values()]
        histogram(smap_counts,
                  f'{name}.MergedCluster.SMAP',
                  'Number of SMAPs per MergedCluster\nacross all samples',
                  'SMAPs per MergedCluster',
                  'Number of MergedClusters',
                  'r',
                  2,
                  max(smap_counts),
                  1,
                  plot_type,
                  xaxisticks=1 if max(smap_counts) < 10 else 5)

    def plot_read_depth(self, name: str, plot_type: str) -> None:
        if not self._merged_clusters:
            return
        read_depths = [median(cluster[self._DEPTH_LABEL])
                       for cluster in self._merged_clusters.values()]
        max_counts = max(read_depths)
        closest_power = int(round(log10(max_counts), 0))
        xaxisticks = max(1, 10**max(1, closest_power-1))
        histogram(read_depths,
                  f'{name}.MergedCluster.MedianRD',
                  'Median read depth per MergedCluster\nacross all samples',
                  'Median read depth (counts)',
                  'Number of MergedClusters',
                  'r',
                  0,
                  max(read_depths),
                  1,
                  plot_type,
                  xaxisticks=xaxisticks,
                  ylog_scale=True)

    def filter_for_completeness(self, minimum_completeness: float, number_of_samples: int) -> None:
        """
        Check that the total number of clusters is a good
        representation of the number of bam files (e.g. 50% - 100% completeness).
        """
        self._merged_clusters = {key_: cluster for key_, cluster in self._merged_clusters.items()
                                 if (number_of_samples*minimum_completeness/100)
                                 <= cluster['sample_count'] <= number_of_samples}

    def wrong_cluster_order_filter(self) -> None:
        """
        Remove merged clusters that were constructed by two clusters
        that don't overlap and another cluster that links the non-overlapping pair.
        In this case, one big mergedcluster was constructed and read depths were overestimated
        in this case.
        """
        self._merged_clusters = {id_: cluster for id_, cluster
                                 in self._merged_clusters.items()
                                 if max(cluster['start_collapse']) <=
                                 min(cluster['end_collapse'])}

    def max_smap_number_filter(self, max_smaps: int) -> None:
        """
        Filter merged cluster to remove those that have too many smaps.
        """
        self._merged_clusters = {id_: cluster for id_, cluster in
                                 self._merged_clusters.items()
                                 if len(set(cluster['start_collapse']) |
                                        set(map(lambda x: x-1, cluster['end_collapse'])))
                                 <= max_smaps}

    def _redundant_position_filter(self, merged_clusters: dict):
        """
        Make the start and end positions unique.
        """
        result = {}
        for key_, cluster in merged_clusters.items():
            start_positions = self._unique_keep_order(cluster['start_collapse'])
            end_positions = self._unique_keep_order(cluster['end_collapse'])
            new_cluster = dict(cluster)
            new_cluster['start'] = min(start_positions)
            new_cluster['end'] = max(end_positions)+1
            result[key_] = new_cluster
        return result

    @staticmethod
    def _unique_keep_order(items_list: List) -> List:
        """
        Create a unique list, while preserving the order
        of elements from the original list.
        """
        # We could use list(set()), but this would change the order
        unique_set = set()
        unique = [item_ for item_ in items_list if not
                  (item_ in unique_set or unique_set.add(item_))]
        return unique


def generate_stacks(bam_files: Iterable[Path], number_of_processes: int,
                    strand_specific: bool, filtering_options: StacksFilteringOptions):
    """
    Create and filter stacks using multiple cores.
    """
    partial_worker = partial(_stack_generation_worker,
                             strand_specific=strand_specific,
                             options=filtering_options)
    with multiprocessing.Pool(number_of_processes) as pool:
        sample_stacks = pool.map(partial_worker, bam_files)
    return sample_stacks


def _stack_generation_worker(bam: Path, strand_specific: bool,
                             options: StacksFilteringOptions):
    """
    A worker function to generate and filter stacks
    for a single sample in a separate process.
    """

    stacks = Stacks(bam, strand_specific, options.min_mapping_quality)
    stacks.depth_filter(options.min_stack_depth, options.max_stack_depth)
    return stacks


def write_stack_output(sample_stacks: Iterable[Stacks], bam_files: Iterable[Path],
                       plot_level: int, plot_type: str, label: str):
    """
    Write the stacks to a .bed file and generate the stacks graphs for each individual sample.
    """
    for bam, stacks in zip(bam_files, sample_stacks):
        bam_basename = Path(bam.stem).stem
        if LOGGER.isEnabledFor(logging.DEBUG):
            with open(f"{bam_basename}.stacks.bed", 'w') as stacks_bed:
                stacks.write_to_bed(stacks_bed, label)
        if plot_level >= PLOT_ALL:
            stacks.plot_depth(bam_basename, plot_type)
            stacks.plot_length(bam_basename, plot_type)
            stacks.plot_cigar_operators(bam_basename, plot_type)
            stacks.plot_read_length_depth_correlation(bam_basename, plot_type)


def generate_clusters(sample_stacks: Iterable[Stacks], number_of_processes: int,
                      filtering_options: ClustersFilteringOpstions):
    """
    Create and filter clusters using multiple cores.
    """
    worker_function_clusters = partial(_cluster_generation_worker, options=filtering_options)
    with multiprocessing.Pool(number_of_processes) as pool:
        sample_clusters = pool.map(worker_function_clusters, sample_stacks)
    return sample_clusters


def _cluster_generation_worker(stacks: Stacks,
                               options: ClustersFilteringOpstions):
    """
    A worker function to generate and filter clusters
    for a single sample in a separate process.
    """
    clusters = stacks.merge()
    clusters.max_stack_number_filter(options.max_stack_number)
    clusters.length_filter(options.min_cluster_length, options.max_cluster_length)
    clusters.stack_depth_fraction_filter(options.min_stacks_depth_fraction)
    clusters.read_depth_filter(options.min_cluster_read_depth, options.max_cluster_read_depth)
    return clusters


def write_cluster_output(sample_clusters: Iterable[Clusters], bam_files: Iterable[Path],
                         plot_level: int, plot_type: str, label: str):
    """
    Write the clusters to a .bed file and generate the cluster graphs for each individual sample.
    """
    for bam, clusters in zip(bam_files, sample_clusters):
        if not clusters.number_of_clusters:
            LOGGER.warning("No clusters found for sample %s."
                           "Please check the input file and filtering options.",
                           bam)
            continue
        if plot_level >= PLOT_ALL:
            clusters.plot_stack_number_per_cluster(Path(bam.stem).stem, plot_type)
            clusters.plot_cluster_read_depth(Path(bam.stem).stem, plot_type)
            clusters.plot_cluster_stack_depth_ratio(Path(bam.stem).stem, plot_type)
            clusters.plot_cluster_lengths(Path(bam.stem).stem, plot_type)
            clusters.plot_number_of_smaps(Path(bam.stem).stem, plot_type)
            clusters.plot_read_length_depth_correlation(Path(bam.stem).stem, plot_type)
        if LOGGER.isEnabledFor(logging.DEBUG):
            with open(f"{Path(bam.stem).stem}.clusters.bed", mode='w', newline='') as cluster_bed:
                clusters.write_to_bed(cluster_bed, label)


def saturation(sample_stacks: Iterable[Stacks],
               sample_clusters: Iterable[Clusters],
               mapping_quality: int, plot_type: str) -> None:
    """
    Create a scatterplot for the number of reads and the number of clusters.
    """
    LOGGER.info('Plotting saturation curve stack clusters.')
    nr_reads = {stacks.bam_file.name: stacks.number_of_parsed_reads/1000000
                for stacks in sample_stacks}
    nr_reads_df = pd.Series(nr_reads,
                            index=pd.Index(nr_reads.keys(), name="Samples"),
                            name="Number of reads (milion)")
    nr_clusters = {sample: clusters.number_of_clusters
                   for (sample, clusters)
                   in zip(nr_reads.keys(), sample_clusters)}
    nr_clusters_df = pd.Series(nr_clusters,
                               index=pd.Index(nr_clusters.keys(), name="Samples"),
                               name="Number of clusters")
    saturation_df = pd.concat([nr_reads_df, nr_clusters_df], axis=1, join='outer')
    saturation_df.to_csv('StackCluster.Saturation.tsv', sep='\t')

    scatterplot(saturation_df["Number of reads (milion)"].values,
                saturation_df["Number of clusters"].values,
                'StackCluster.Saturation',
                'Saturation of StackClusters per sample',
                ('Number of reads mapped per sample\n(in millions of reads, '
                 f'MQ > {mapping_quality})'),
                'Number of StackClusters',
                'b',
                plot_type
                )


def get_bam_files(dir_path: Path) -> List[Path]:
    """
    Get a list of .bam files in a directory.
    """
    if not dir_path.is_dir():
        raise ValueError(f"{dir_path} does not exitst or is not a directory.")
    bam_files = [f for f in dir_path.iterdir() if f.suffix == '.bam']
    if not bam_files:
        raise ValueError("No .bam files found in the input directory.")
    return bam_files


def parse_args(args) -> Namespace:
    """
    Parse command line arguments
    """
    LOGGER.debug('Parsing arguments: %r', args)
    delineate_parser = ArgumentParser(
        "delineate",
        description=('Create a bed file with clusters of Stacks using a '
                     'set of bam files containing aligned GBS reads. The Stack Mapping '
                     'Anchor Points "SMAP" within clustersof Stacks are listed 0-based. '
                     'The position of the clusters of Stacks themselves are 0-based '
                     'according to BED format.'))

    delineate_parser.add_argument('-v', '--version',
                                  action='version',
                                  version=__version__)

    input_output_group = delineate_parser.add_argument_group(
        title='In- and output information')
    input_output_group.add_argument(
        'alignments_dir',
        type=Path,
        help=('Path to the directory containing BAM and BAI alignment files. '
              'All BAM files should be in the same directory [current directory].'))
    input_output_group.add_argument(
        '-r', '-mapping_orientation',
        required=True,
        dest='mapping_orientation',
        # choices=['stranded', 'ignore', ''],
        help=('Specify strandedness of read mapping should be considered for haplotyping. '
              'When specifying "ignore", reads are collected per locus independent of the strand '
              'that the reads are mapped on (i.e. ignoring their mapping orientation). "stranded" '
              'means that only those reads will be considered that map on the same strand as '
              'indicated per locus in the BED file. For more information on which option '
              'to choose, please consult the manual.'))
    input_output_group.add_argument(
        '-read_type',
        required=False,
        dest='read_type',
        choices=['separate', 'merged'],
        help=('Deprecated option: please use --mapping_orientation. "--read_type merged" should '
              'be replaced by "--mapping_orientation ignore", and "--read_type merged" by '
              '"--mapping_orientation stranded".'))
    input_output_group.add_argument(
        '-n', '--name',
        dest='label',
        default='Set1',
        type=str,
        help=('Label to describe the sample set, will be added '
              'to the last column in the final stack BED file '
              'and is used by SMAP-compare [Set1].'))

    resources_group = delineate_parser.add_argument_group(
        title='System resources.')
    resources_group.add_argument(
        '-p', '--processes',
        dest='processes',
        default=1,
        type=int,
        help='Number of parallel processes [1].')

    plot_group = delineate_parser.add_argument_group(
        title='Graphical output options')
    plot_group.add_argument(
        '--plot',
        dest='plot',
        type=PlotLevel,
        default=PLOT_SUMMARY,
        choices=(PLOT_ALL, PLOT_SUMMARY, PLOT_NOTHING),
        help=('Select which plots are to be generated. Choosing "nothing" '
              'disables plot generation. Passing "summary" only generates '
              'graphs with information for all samples while "all" will also '
              'enable generate per-sample plots [default "summary"].'))
    plot_group.add_argument(
        '-t', '--plot_type',
        dest='plot_type',
        choices=['png', 'pdf'],
        default='png',
        help='Choose the file type for the plots [png].')

    read_filtering_group = delineate_parser.add_argument_group(
        title='Read filtering options')
    read_filtering_group.add_argument(
        '-q', '--minimum_mapping_quality',
        dest='mapping_quality',
        default=30,
        type=int,
        help=('Minimum bam mapping quality to retain reads for analysis [30].')
    )

    stack_filtering_group = delineate_parser.add_argument_group(
        title='Stack filtering options.')
    stack_filtering_group.add_argument(
        # Use None as default because we want to check if this default is used.
        # If the user did not prvovide a value, the value will be set to 0 later.
        '-x', '--min_stack_depth',
        dest='min_stack_depth',
        default=None,
        type=int,
        help=('Minimum number of reads per Stack per sample. '
              'A good reference value could be 3 [0].'))
    stack_filtering_group.add_argument(
        # Use None as default because we want to check if this default is used.
        # If the user did not prvovide a value, the value will be set to inf later.
        '-y', '--max_stack_depth',
        dest='max_stack_depth',
        default=None,
        type=float,
        help=('Maximum total number of reads per Stack per sample [inf].'))

    cluster_filtering_group = delineate_parser.add_argument_group(
        title='Cluster filtering options')
    cluster_filtering_group.add_argument(
        # Use None as default because we want to check if this default is used.
        # If the user did not prvovide a value, the value will be set to 0 later.
        '-f', '--min_cluster_length',
        dest='min_cluster_length',
        default=None,
        type=int,
        help=('Minimum cluster length. Can be used to remove artifacts that '
              'arise from read merging [0].'))
    cluster_filtering_group.add_argument(
        # Use None as default because we want to check if this default is used.
        # If the user did not prvovide a value, the value will be set to inf later.
        '-g', '--max_cluster_length',
        dest='max_cluster_length',
        default=None,
        type=float,
        help=('Maximum cluster length. Can be used to remove artifacts that '
              'arise from read merging [inf].'))
    cluster_filtering_group.add_argument(
        # Use None as default because we want to check if this default is used.
        # If the user did not prvovide a value, the value will be set to inf later.
        '-l', '--max_stack_number',
        dest='max_stack_number',
        type=float,
        default=None,
        help=('Maximum number of Stacks per StackCluster, may be 2 in diploid '
              'individuals, 4 for tetraploid individuals, 20 for Pool-Seq [inf].'))

    cluster_filtering_group.add_argument(
        # Use None as default because we want to check if this default is used.
        # If the user did not prvovide a value, the value will be set to 0 later.
        '-b', '--min_stack_depth_fraction',
        dest='min_stack_depth_fraction',
        default=None,
        type=float,
        help=('Threshold (%%) for minimum relative Stack depth per StackCluster. '
              'Removes spuriously mapped reads from StackClusters, and controls '
              'for noise in the number of SMAPs per locus. The StackCluster '
              'total read depth and number of SMAPs is recalculated based '
              'on the retained Stacks per sample [0].'
              )
    )
    cluster_filtering_group.add_argument(
        # Use None as default because we want to check if this default is used.
        # If the user did not prvovide a value, the value will be set to 0 later.
        '-c', '--min_cluster_depth',
        dest='min_cluster_depth',
        default=None,
        type=int,
        help=('Minimal total number of reads per StackCluster per sample. '
              'The total number of reads in a StackCluster is calculated '
              'after filtering out the Stacks using --min_stack_depth_fraction. '
              'A good reference value is 10 for individual diploid samples, 20 '
              'for tetraploids, and 30 for Pool-Seq [0].'))
    cluster_filtering_group.add_argument(
        # Use None as default because we want to check if this default is used.
        # If the user did not prvovide a value, the value will be set to inf later.
        '-d', '--max_cluster_depth',
        dest='max_cluster_depth',
        default=None,
        type=float,
        help=('Maximal total number of reads per StackCluster per sample. '
              'The total number of reads in a StackCluster is calculated '
              'after filtering out the Stacks using --min_stack_depth_fraction [inf].'))

    merged_cluster_filtering_group = delineate_parser.add_argument_group(
        title='Merging clusters filtering options')
    merged_cluster_filtering_group.add_argument(
        # Use None as default because we want to check if this default is used.
        # If the user did not prvovide a value, the value will be set to inf later.
        '-s', '--max_smap_number',
        dest='max_smap_number',
        default=None,
        type=float,
        help=('Maximum number of SMAPs per MergedCluster across the sample set. '
              'Can be used to remove loci with excessive MergedCluster complexity '
              'before downstream analysis [inf].'))
    merged_cluster_filtering_group.add_argument(
        # Use None as default because we want to check if this default is used.
        # If the user did not prvovide a value, the value will be set to 0 later.
        '-w', '--completeness',
        dest='completeness',
        default=None,
        type=float,
        help=('Completeness, minimal percentage of samples that contains an '
              'overlapping StackCluster for a given MergedCluster. May be used '
              'to select loci with enough read mapping data across the sample '
              'set for downstream analysis [0].'))
    parsed_args = delineate_parser.parse_args(args)
    if parsed_args.read_type and parsed_args.mapping_orientation:
        raise ValueError("Used both -read_type and -mapping_orientation.")
    if parsed_args.read_type or parsed_args.mapping_orientation in ('separate', 'merged'):
        LOGGER.warning("Option -read_type will be removed in favour of "
                       "-mapping_orientation in a future version. See --help for more information.")

        parsed_args.mapping_orientation = 'ignore' \
                                          if parsed_args.read_type == 'merged' \
                                          else 'stranded'

    parsed_args = set_filter_defaults(parsed_args)
    log_args(parsed_args)
    LOGGER.debug('Parsed arguments: %r', vars(parsed_args))
    return parsed_args


def set_filter_defaults(parsed_args: Namespace):
    """
    Set argument default values for several filters.
    Also warn the user if a filter has nog been set.
    """
    warnings_dict = {
        # argument: [default_value]
        'min_stack_depth': 0,
        'max_stack_depth': inf,
        'min_cluster_length': 0,
        'max_cluster_length': inf,
        'max_stack_number': inf,
        'min_stack_depth_fraction': 0,
        'min_cluster_depth': 0,
        'max_cluster_depth': inf,
        'max_smap_number': inf,
        'completeness': 0
    }
    warning_message = ('"--%(argument)s" argument was not given. This means that '
                       'this filter will not be applied. If you are sure about this, '
                       'you can hide this warning by setting "--%(argument)s %(val)s" '
                       'explictly.')
    for argument, default_val in warnings_dict.items():
        if getattr(parsed_args, argument) is None:
            LOGGER.warning(warning_message, {'argument': argument, 'val': default_val})
            setattr(parsed_args, argument, default_val)

    inf_arguments = [argument for argument, default_val in warnings_dict.items()
                     if default_val == inf]
    for argument in inf_arguments:
        parsed_args = handle_filter_inf(argument, parsed_args)
    return parsed_args


def handle_filter_inf(argument_name: str, parsed_args: Namespace):
    """
    Check if casting to int truncates the float.
    If inf is passed, keep inf.
    """
    orig_argument = getattr(parsed_args, argument_name)
    try:
        # The arguments are now float type (as set in add_argument())
        # Try casting them to int and check if the float was truncated.
        setattr(parsed_args, argument_name, int(orig_argument))
        if orig_argument != int(orig_argument):
            LOGGER.warning('Argument "%s": value "%s" truncated to "%s".',
                           argument_name, orig_argument, int(orig_argument))
    except OverflowError:
        # The float was inf, leave it like that
        setattr(parsed_args, argument_name, orig_argument)
    return parsed_args


def log_args(parsed_args):
    log_string = dedent("""
    Running SMAP delineate using the following options:

    Input & output:
        Alignments directory: {alignments_dir}
        Mapping orientation: {mapping_orientation}
        Name: {label}

    Graphical output options:
        Plot mode: {plot}
        Plot type: {plot_type}

    Read filtering options:
        Mapping quality: {mapping_quality}

    Stack filtering options:
        Minimum stack depth: {min_stack_depth}
        Maximum stack depth: {max_stack_depth}

    Cluster filtering options:
        Minimum cluster length: {min_cluster_length}
        Maximum cluster length: {max_cluster_length}
        Minimum stack depth fraction: {min_stack_depth_fraction}
        Minimum cluster depth: {min_cluster_depth}
        Maximum cluster depth: {max_cluster_depth}

    Merged clusters filtering options:
        Maximum number of SMAPs: {max_smap_number}
        Completeness: {completeness}

    System resources:
        Number of processes: {processes}
    """)
    LOGGER.info(log_string.format(**vars(parsed_args)))


def main(args):
    """
    The entrypoint for SMAP-delineate.
    """
    LOGGER.info('SMAP-delineate started.')
    parsed_args = parse_args(args)
    LOGGER.info(('Generating stacks and clusters for each bam file in %s/ '
                 '(mapping quality >= %s and stack depth between %s and %s).'),
                parsed_args.alignments_dir,
                parsed_args.mapping_quality,
                parsed_args.min_stack_depth, parsed_args.max_stack_depth)
    bam_files = get_bam_files(parsed_args.alignments_dir)
    stack_options = StacksFilteringOptions(parsed_args.mapping_quality,
                                           parsed_args.min_stack_depth,
                                           parsed_args.max_stack_depth)
    cluster_options = ClustersFilteringOpstions(parsed_args.min_cluster_length,
                                                parsed_args.max_cluster_length,
                                                parsed_args.max_stack_number,
                                                parsed_args.min_stack_depth_fraction,
                                                parsed_args.min_cluster_depth,
                                                parsed_args.max_cluster_depth)
    strand_specific = parsed_args.mapping_orientation == 'stranded'
    sample_stacks = generate_stacks(bam_files, parsed_args.processes,
                                    strand_specific,
                                    stack_options)
    write_stack_output(sample_stacks, bam_files,
                       parsed_args.plot, parsed_args.plot_type, parsed_args.label)

    sample_clusters = generate_clusters(sample_stacks, parsed_args.processes,
                                        cluster_options)

    write_cluster_output(sample_clusters, bam_files,
                         parsed_args.plot, parsed_args.plot_type, parsed_args.label)

    if parsed_args.plot >= PLOT_SUMMARY:
        saturation(sample_stacks,
                   sample_clusters,
                   mapping_quality=parsed_args.mapping_quality,
                   plot_type=parsed_args.plot_type)

    LOGGER.info('Merging all clustered stacks.')
    all_clusters = Clusters({}, strand_specific)
    for cluster in sample_clusters:
        all_clusters = all_clusters + cluster
    merged_clusters = all_clusters.merge(strand_specific)
    merged_clusters.filter_for_completeness(parsed_args.completeness, len(bam_files))
    merged_clusters.wrong_cluster_order_filter()
    merged_clusters.max_smap_number_filter(parsed_args.max_smap_number)

    final_file_name = Path((f"final_stack_positions_{parsed_args.label}"
                            f"_C{parsed_args.completeness}"
                            f"_SMAP{parsed_args.max_smap_number}"
                            f"_CL{parsed_args.min_cluster_length}"
                            f"_{parsed_args.max_cluster_length}.bed"))
    with final_file_name.open('w') as final_stacks:
        merged_clusters.write_to_bed(final_stacks, parsed_args.label)
    if parsed_args.plot >= PLOT_SUMMARY:
        merged_clusters.plot_completeness("final_stack_positions", parsed_args.plot_type)
        merged_clusters.plot_merged_cluster_length("final_stack_positions", parsed_args.plot_type)
        merged_clusters.plot_number_of_smaps("final_stack_positions", parsed_args.plot_type)
        merged_clusters.plot_read_depth("final_stack_positions", parsed_args.plot_type)
    LOGGER.info('Finished')
