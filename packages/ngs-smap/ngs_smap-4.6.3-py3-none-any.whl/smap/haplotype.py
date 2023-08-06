from __future__ import annotations
import logging
import operator

from collections import Counter, defaultdict, abc
from functools import partial
from itertools import product
import concurrent.futures
from pathlib import Path
from typing import Dict, Iterable, Union, Tuple, IO, AnyStr, TextIO
from argparse import ArgumentParser, Namespace

from pandas.core.frame import DataFrame
from pandas.api.types import is_integer_dtype
from smap import __version__
from math import inf, log10
import fileinput
import numpy as np
import pandas as pd
from pybedtools import BedTool
from pysam import AlignedSegment, AlignmentFile
from copy import deepcopy
from textwrap import dedent
import re
import csv
import string
import random
from abc import ABC

from .plotting import barplot, histogram, PLOT_SUMMARY, PLOT_NOTHING, PLOT_ALL, PlotLevel

LOGGER = logging.getLogger("Haplotype")

REFERENCE_COLUMN_NAME = 'Reference'
LOCUS_COLUMN_NAME = 'Locus'
HAPLOTYPES_COLUMN_NAME = 'Haplotypes'
INDEX_COLUMNS = [REFERENCE_COLUMN_NAME, LOCUS_COLUMN_NAME, HAPLOTYPES_COLUMN_NAME]


class Stacks():
    def __init__(self, bed_path: Union[TextIO, Path, str]):
        self._bed = BedTool(bed_path)
        try:
            assert self._bed.file_type in ('bed', 'empty')
        except ValueError:  # bed is a stream, not an actual file
            self._bed = self._bed.saveas()
        except (IndexError, AssertionError) as exc:
            raise ValueError('Provided file is not a valid bed file.') from exc
        self._stacks = self._parse_stack_bed()
        LOGGER.debug('Initiated %r', self)

    def __repr__(self):
        return "%s(quality_threshold=%r,stacks={...}). Number of stacks=%s" % \
               ('Stacks', self._bed, len(self._stacks))

    @property
    def stacks(self):
        return self._stacks

    def _parse_stack_bed(self):
        LOGGER.info('Loading stack regions and their SMAP and variant positions.')
        LOGGER.debug('Parsing BED %r', self._bed)

        stacks = {}
        first = True
        for scaffold, start, stop, _, _, strand, smaps, *_ in self._bed:
            start = int(start)
            region = f'{scaffold}:{start+1}-{stop}_{strand}'
            smaps = set(map(int, smaps.split(',')))
            if first:
                first = False
                if min(smaps) == start:
                    raise ValueError(('It seems that the .bed file uses an incorrect '
                                      'SMAP coordinate system (7th column).\n'
                                      'SMAP>=4.2.0 requires the SMAP coordinates to be 1-based, '
                                      'compared to the previously used 0-based system.\n'
                                      'BED files generated using SMAP can be updated by using '
                                      'the latest version of delineate.\n'
                                      'For more information, please consult the manual '
                                      '(https://ngs-smap.readthedocs.io/en/dev/sites/'
                                      'sites_scope_quickstart.html)\n'))
            stacks.setdefault(region, {'scaffold':  scaffold,
                                       'start': start,
                                       'stop': int(stop),
                                       'strand': strand,
                                       'variants': dict(),
                                       'positions': smaps,  # Updated with vcf positions later.
                                       'smaps': set(smaps)})  # Copy because reference otherwise!
        LOGGER.debug('Found %s stacks in BED file %r', len(stacks), self._bed)
        return stacks

    @staticmethod
    def _check_vcf(vcf_file):
        """
        Checks if a VCF file contains the correct header. If not, create it.
        """
        LOGGER.info('Checking the VCF file for a header.')
        # FileInput allows for inplace editing and writing stdout to file
        with fileinput.FileInput(files=(str(vcf_file),), inplace=True) as file_input:
            for line in file_input:
                if file_input.isfirstline() and not line.startswith('##fileformat=VCFv'):
                    print('##fileformat=VCFv4.2\n' + line, end='')
                else:
                    print(line, end='')

    def remove_non_polymophic_stacks(self, vcf_path: Union[str, Path]):
        LOGGER.info('Removing non-polymorphic stacks.')
        vcf_path = Path(vcf_path)
        if not vcf_path.is_file():
            raise ValueError(f"VCF file {vcf_path} does not exist or is not a file.")
        self._check_vcf(vcf_path)
        vcf = BedTool(str(vcf_path))
        try:
            assert vcf.file_type in ('vcf', 'empty')
        except (IndexError, AssertionError):
            raise ValueError(f'{vcf_path!s} is not a valid vcf file or is empty.')

        LOGGER.debug('Intersecting the stacks BED file %r '
                     'with VCF file %s indicating the polymorphisms.', self._bed, str(vcf_path))
        intersect = self._bed.intersect(vcf, loj=True)

        for mapping in intersect:
            if mapping[10] != '.':
                scaffold, start, stop, strand = mapping[0], int(mapping[1]), \
                    int(mapping[2]), mapping[5]
                region = f'{scaffold}:{start+1}-{stop}_{strand}'
                try:
                    selected_region = self._stacks[region]
                except KeyError:
                    raise ValueError('A variant region was defined in the .vcf file' +
                                     'which is not present in the stacks.')
                else:
                    var_position, variants_ref, variants_alt = int(mapping[11]), \
                        mapping[13], mapping[14]
                    selected_region['positions'].add(var_position)
                    selected_region['variants'][var_position] = {'ref': variants_ref,
                                                                 'alt': variants_alt}

        original_stack_count = len(self._stacks)
        self._stacks = {stack_name: stack_info
                        for stack_name, stack_info in self._stacks.items()
                        if len(stack_info['smaps']) > 2
                        or len(stack_info['variants'].keys()) > 0}
        overlap_count = sum(len(stack['smaps']) > 2 or len(stack['variants']) > 0
                            for stack in self._stacks.values())

        LOGGER.info('%s non-polymorphic stacks were ignored.',
                    original_stack_count - len(self._stacks))
        LOGGER.info('Building haplotypes for %s stacks of which %s overlap ' +
                    'with min. 1 variant position.', len(self._stacks), overlap_count)

        # Sort the stacks based on their name
        self._stacks = {stack_name: stack_info
                        for stack_name, stack_info in sorted(self._stacks.items())}

    def write_coordinates(self, target_file: Union[str, Path]):
        with open(target_file, 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter='\t')
            writer.writerow(['Reference', 'Locus', 'SNPs', 'SMAPs', 'SNPs_and_SMAPs'])
            for locus_name, stack_info in self._stacks.items():
                snp_list = ",".join(map(str, sorted(stack_info['variants'])))
                smap_list = ",".join(map(str, sorted(stack_info['smaps'])))
                smaps_and_variants = ",".join(map(str, sorted(list(stack_info['positions']))))
                writer.writerow([stack_info['scaffold'], str(locus_name), snp_list,
                                 smap_list, smaps_and_variants])


class _HaplotypeCountProducer():
    def __init__(self, quality_threshold, strand_specific):
        self._quality_threshold = quality_threshold
        self._strand_specific = strand_specific
        LOGGER.debug('Initiated %r', self)

    def __repr__(self):
        return "%s(quality_threshold=%r, strand_specific=%r)" % \
               ('_HaplotypeCountProducer', self._quality_threshold, self._strand_specific)

    def run(self, bam, stacks):
        LOGGER.debug('Opening BAM %s', bam.name)
        try:
            sam_file = AlignmentFile(bam, 'rb')
        except ValueError as e:
            LOGGER.error("There was a problem reading file %s", bam)
            raise e
        result = []
        for stack_name, stack_info in stacks.items():
            # LOGGER.debug('Haplotyping %s.', stack_name)
            reverse_should_not_be = stack_info['strand'] == '+' if self._strand_specific else None
            stack_haplotypes = self._haplotype_stack(stack_info, sam_file, reverse_should_not_be)
            if stack_haplotypes:
                result.append(self._stack_to_dataframe(stack_info['scaffold'], stack_name,
                                                       bam.name, stack_haplotypes))
            # LOGGER.debug('Done haplotyping %s.', stack_name)
        LOGGER.debug('Closing BAM %s', bam.name)
        sam_file.close()
        LOGGER.debug('Concatenating %s stacks for BAM %s', len(result), bam.name)
        if result:
            concat_result = pd.concat(result)
        else:
            empty_index = pd.MultiIndex(levels=[[], [], []], codes=[[], [], []],
                                        names=INDEX_COLUMNS)
            concat_result = pd.DataFrame(columns=[bam.name], index=empty_index)
        LOGGER.debug('Done haplotyping %s stacks for BAM %s. '
                     'Number of results: %s', len(stacks), bam.name, len(concat_result))
        return concat_result

    def _stack_to_dataframe(self, scaffold, stack_name, bam_name, stack_haplotypes):
        haplotypes = list(stack_haplotypes.keys())
        index = pd.MultiIndex.from_product([[scaffold], [stack_name], haplotypes],
                                           names=INDEX_COLUMNS)
        return pd.DataFrame({bam_name: [stack_haplotypes[haplotype] for haplotype in haplotypes]},
                            index=index,
                            dtype=pd.UInt32Dtype())

    def _haplotype_stack(self, stack_info: Dict, sam: AlignmentFile, reverse_should_not_be: bool):
        region_haplotypes = defaultdict(int)
        seen_haplpotypes = dict()
        positions = sorted(stack_info["positions"])
        aligned_reads = sam.fetch(stack_info['scaffold'], stack_info['start'], stack_info['stop'])
        for read in aligned_reads:
            if (read.mapping_quality <= self._quality_threshold) or \
               (read.is_reverse is reverse_should_not_be):
                continue
            cigar, start = read.cigartuples, read.reference_start - read.query_alignment_start
            signature = (start, tuple(cigar), read.query_alignment_sequence)
            try:
                haplotype = seen_haplpotypes[signature]
                region_haplotypes[haplotype] += 1
            except KeyError:
                haplotype = self._haplotype_read(read, positions, cigar, start)
                if haplotype.strip('.'):
                    region_haplotypes[haplotype] += 1
                    seen_haplpotypes[signature] = haplotype
        return region_haplotypes

    def _haplotype_read(self,
                        read: AlignedSegment,
                        positions: Iterable,
                        cigar: Iterable[Tuple[int, str]],
                        start: int):
        aln_pairs = read.get_aligned_pairs(with_seq=True)
        # Substract -1: from 1-based coordinates for SMAPs and SNPs to 0-based
        # coordinates in list from get_aligned_pairs.
        indexes = [self._get_index_from_cigar(pos-1, cigar, start) for pos in positions]
        pos_aln_pairs = [aln_pairs[i] if 0 <= i < len(aln_pairs) else (None,)*3 for i in indexes]
        haplotype = self._call_haplotype(pos_aln_pairs)
        return haplotype

    @staticmethod
    def _get_index_from_cigar(position: int, cigar: Iterable[Tuple[int, str]], start: int) -> int:
        result = position - start
        i = 0
        for operation, cigar_position in cigar:
            if operation == 1:  # I (insert)
                if result >= i:
                    result += cigar_position
                i += cigar_position
            elif operation in {0, 2, 3, 4}:  # M, D, N, S
                i += cigar_position
            elif operation == 5:  # H (hard clip)
                pass
            else:
                # other operations than I, M, D, N, S, H exist,
                # but they do not appear in the datasets
                raise NotImplementedError(f"CIGAR Operation {operation}" +
                                          "not implemented in CIGAR {cigar}.")
        return result

    @staticmethod
    def _call_haplotype(pos_aln_pairs):
        ht_seq = ['.' if ref_seq is None else
                  '-' if read_pos is None else
                  '0' if ref_seq.isupper() else
                  '1' if ref_seq.islower() else ""
                  for read_pos, _, ref_seq in pos_aln_pairs]
        return "".join(ht_seq)

    @staticmethod
    def _list_to_string(lst: Iterable, sep=','):
        return sep.join([str(entry) for entry in lst])


class Haplotyper():
    def __init__(self,
                 polymorphic_stacks: Stacks,
                 strand_specific: bool,
                 quality_threshold: int,
                 cpu: int):
        self._stacks = polymorphic_stacks.stacks
        self._strand_specific = strand_specific
        self._quality_threshold = quality_threshold
        self._cpu = cpu
        LOGGER.debug('Haplotyper initiated with options: '
                     'strand_specific=%s,quality_threshol=%s,cpu=%s,stacks=%r',
                     strand_specific, quality_threshold, cpu, polymorphic_stacks)

    def haplotype_bam_reads(self, bam_files: Iterable[Path]) -> pd.DataFrame:
        if not bam_files:
            raise ValueError("List of .bam files was empty.")
        number_of_bam = len(bam_files)
        LOGGER.info('Started haplotyping %s bam files.', number_of_bam)
        if self._cpu > number_of_bam:
            number_of_parts = self._cpu // number_of_bam
            stacks_per_part = max(len(self._stacks) // number_of_parts, 1000)
            stacks_iter = list(self._parts(self._stacks, stacks_per_part))
        elif len(self._stacks) > 1000:
            stacks_iter = list(self._parts(self._stacks, 1000))
        else:
            stacks_iter = [self._stacks]
        number_of_parts = len(stacks_iter)

        LOGGER.debug('Stacks split into %s parts.', number_of_parts)
        with concurrent.futures.ProcessPoolExecutor(self._cpu) as executor:
            producer = _HaplotypeCountProducer(self._quality_threshold, self._strand_specific)
            future_haplotype_counts = {}
            for bam_file, (i, stack_part) in product(bam_files, enumerate(stacks_iter)):
                LOGGER.debug('Submitting part %s for bam %s', i, bam_file.name)
                future_haplotype_counts[
                    executor.submit(self._producer_worker, producer, bam_file, stack_part)
                ] = i

            LOGGER.info('Started joining columns for stack counts.')
            merged_results = [self._empty_dataframe()] * number_of_parts
            for i, future in enumerate(concurrent.futures.as_completed(future_haplotype_counts)):
                part_index = future_haplotype_counts[future]
                result = future.result()
                merged_results[part_index] = merged_results[part_index].join(result, how='outer')
                percent_done = (i/(number_of_parts * number_of_bam))*100
                LOGGER.debug("Joining part %s for BAM %s, Total percent done: %.2f",
                             part_index,
                             result.columns[0],
                             percent_done)
                print(f"{percent_done:.2f}%", end='\r')

            LOGGER.debug('Started joining rows for all stacks.')
            concat_results = pd.concat(merged_results)

            LOGGER.debug('Filling NA with 0.')
            concat_results.fillna(value=0, inplace=True)

            LOGGER.debug('Sorting output columns.')
            concat_results = concat_results.reindex(sorted(concat_results.columns), axis=1)

            LOGGER.info('Haplotyping done.')
            return concat_results

    @staticmethod
    def _empty_dataframe():
        return pd.DataFrame(index=pd.MultiIndex.from_product([[], [], []], names=INDEX_COLUMNS))

    @staticmethod
    def _producer_worker(producer: _HaplotypeCountProducer,
                         bam_file: Path,
                         stack_part: Iterable[Dict]) -> pd.DataFrame:
        return producer.run(bam_file, stack_part)

    @staticmethod
    def _parts(dct: Dict, size: int = 200) -> Iterable[Dict]:
        dict_keys = list(dct.keys())
        for i in range(0, len(dict_keys), size):
            yield {key_: dct[key_] for key_ in dict_keys[i:i + size]}


class _Table(ABC):
    def __init__(self, df: pd.DataFrame) -> None:
        self._df = df

    def to_csv(self,
               path_or_buffer: Union[str, Path, IO[AnyStr]],
               na_rep: str = 'NaN', float_format=None):
        self._df.to_csv(path_or_buffer, sep='\t', na_rep=na_rep, float_format=float_format)

    @property
    def sample_names(self) -> list[str]:
        return self._df.columns.to_list()

    @property
    def shape(self):
        return self._df.shape

    def __truediv__(self, other: pd.DataFrame):
        return type(self)(self._df.__truediv__(other))

    def __getitem__(self, *args, **kwargs):
        return type(self)(self._df.__getitem__(*args, **kwargs))


class _HaplotypeTable(_Table, ABC):
    def __init__(self, df: pd.DataFrame) -> None:
        super().__init__(df)

    def shuffle_loci(self) -> None:
        groups = [group for _, group in self._df.groupby(LOCUS_COLUMN_NAME, sort=False)]
        random.shuffle(groups)
        self._df = pd.concat(groups)

    def pool_samples(self, samples: abc.Mapping[str, abc.Sequence[str]]) -> None:
        dtypes = set(self._df.dtypes)
        assert len(dtypes) == 1, 'All dataframe columns should have the same dtype.'
        dtype = dtypes.pop()
        for new_name, samples_to_pool in samples.items():
            self._df[new_name] = self._df[samples_to_pool].sum(axis=1,
                                                               numeric_only=True,
                                                               min_count=1).astype(dtype)
            self._df.drop(samples_to_pool, axis=1, inplace=True)
            LOGGER.info('The samples %s were combined into one sample with ID %s.',
                        ", ".join(samples_to_pool), new_name)

    @property
    def loci_names(self) -> list[str]:
        return list(set(self._df.index.get_level_values(LOCUS_COLUMN_NAME)))

    def iter_samples(self) -> Iterable[Tuple[str, pd.Series]]:
        return self._df.iteritems()

    @property
    def number_of_loci(self):
        return len(self._df.groupby(level=[REFERENCE_COLUMN_NAME, LOCUS_COLUMN_NAME]))

    @property
    def number_of_samples(self):
        return len(self._df.columns)

    def _filter_by_row_label(self,
                             query: str,
                             level: str = 'Haplotypes') -> None:
        self._df = self._df.iloc[~self._df.index.get_level_values(level)
                                                .str.contains(query, regex=False)]

    def _filter_sublevel(self, level: str, to_keep: Iterable[str], axis: int = 0) -> None:
        indexer = [slice(None)
                   if not col == level
                   else to_keep for col in INDEX_COLUMNS]
        self._df = self._df.loc(axis=axis)[tuple(indexer)]

    def rename_samples(self, names_mapping: abc.Mapping[str, str]) -> None:
        self._df.rename(columns=names_mapping, inplace=True)

    def filter_loci(self, to_keep: Iterable[str]):
        self._filter_sublevel(LOCUS_COLUMN_NAME, to_keep)

    def filter_for_locus_completeness(self, min_completeness: float) -> None:
        _, number_of_samples = self._df.shape
        number_of_samples_with_locus = self._df.isnull().groupby(LOCUS_COLUMN_NAME)\
                                               .any().sum(axis=1)
        completeness = number_of_samples_with_locus / number_of_samples
        passes = completeness <= 1 - min_completeness
        to_keep = passes[passes.eq(True)]
        deleted = passes[passes.eq(False)]
        loci_to_keep = to_keep.index.to_list()
        deleted = deleted.index.to_list()
        if len(deleted) > 0:
            LOGGER.info('%s region %s ignored due to a completeness lower than %s',
                        len(deleted),
                        's were' if len(deleted) > 1 else ' was',
                        min_completeness)
        self._filter_sublevel(LOCUS_COLUMN_NAME, loci_to_keep)

    def filter_for_sample_completeness(self, min_completeness: float) -> None:
        locus_position_in_index = INDEX_COLUMNS.index(LOCUS_COLUMN_NAME)
        total_number_of_loci = self._df.index.levshape[locus_position_in_index]
        number_of_loci_per_sample = self._df.isnull().groupby(LOCUS_COLUMN_NAME).any().sum()
        completeness = number_of_loci_per_sample / total_number_of_loci
        passes = completeness <= 1 - min_completeness
        to_keep = passes[passes.eq(True)]
        deleted = passes[passes.eq(False)]
        samples_to_keep = to_keep.index.to_list()
        deleted = deleted.index.to_list()
        if len(deleted) > 0:
            LOGGER.info('The following%s sample%s ignored because they had data '
                        'for less than %s region%s: %s',
                        f' {len(deleted)}' if len(deleted) > 1 else '',
                        's were' if len(deleted) > 1 else ' was',
                        min_completeness,
                        's' if min_completeness == 1 else '',
                        ", ".join(deleted))
        return self._df.loc[:, tuple(samples_to_keep)]

    def filter_indels(self) -> None:
        LOGGER.info("Removing haplotypes with indels.")
        self._filter_by_row_label('-')

    def filter_partial(self) -> None:
        LOGGER.info("Removing haplotypes that cover only parts of the regions.")
        self._filter_by_row_label('.')

    def filter_for_number_of_distinct_haplotypes(self,
                                                 min_distinct_haplotypes: int,
                                                 max_distinct_haplotypes: int) -> None:
        if min_distinct_haplotypes < 0:
            raise ValueError("The minimum number of distinct haplotypes threshold "
                             "must be larger than 0. Currently it is set to "
                             f"{min_distinct_haplotypes}.")

        if max_distinct_haplotypes < 0:
            raise ValueError("The minimum number of distinct haplotypes threshold "
                             "must be larger than 0. Currently it is set to "
                             f"{max_distinct_haplotypes}.")

        def filter_function(group: pd.DataFrame) -> bool:
            return (group.shape[0] >= min_distinct_haplotypes) & \
                   (group.shape[0] <= max_distinct_haplotypes)

        grouped = self._df.groupby(level=[LOCUS_COLUMN_NAME])
        self._df = grouped.filter(filter_function)

    def calculate_similarity_matrix(self):
        raise NotImplementedError


class CountMatrix(_HaplotypeTable):
    def __init__(self, counts: pd.DataFrame):
        if not all(counts.apply(is_integer_dtype)):
            raise ValueError("The count matrix must have an integer dtype for all columns.")
        super().__init__(counts)

    def filter_for_minimum_or_maximum_read_count(self,
                                                 minimum_read_count: int,
                                                 maximum_read_count: int) -> None:
        def transform_function(sample_counts):
            sample_counts_sum = sample_counts.sum()
            if sample_counts_sum < minimum_read_count or sample_counts_sum >= maximum_read_count:
                sample_counts[:] = pd.NA
            return sample_counts
        grouped = self._df.groupby(level=[LOCUS_COLUMN_NAME])
        self._df = grouped.transform(transform_function)
        self._df.dropna(axis='index', how='all', inplace=True)

    def filter_on_minimum_haplotype_frequency(self, minimum_haplotype_frequency: int,
                                              minimum_read_frequency=0) -> None:
        if not 0 <= minimum_haplotype_frequency <= 100:
            raise ValueError("The minimum haplotype frequency must be a number"
                             "between 0 and 100 (inclusive). Value was "
                             f"{minimum_haplotype_frequency}.")

        if not 0 <= minimum_read_frequency <= 100:
            raise ValueError("The minimum read frequency must be a number"
                             f"between 0 and 100 (inclusive). Value was {minimum_read_frequency}.")

        LOGGER.info("Filtering to remove haplotypes with low read frequency.")
        column_sums = self._df.groupby(level=[LOCUS_COLUMN_NAME]).sum()
        frequencies = (self._df.truediv(column_sums, fill_value=None)) * 100
        if minimum_read_frequency and minimum_read_frequency > 0:
            if minimum_read_frequency > minimum_haplotype_frequency:
                LOGGER.warning('The minimum read frequency threshold ' +
                               'is larger than the minimum haplotype frequency. ' +
                               'A haplotype is only to be excluded if for none ' +
                               'of the samples the frequency for that haplotype ' +
                               'is above the minimum haplotype frequency. ' +
                               'Setting the minimum read frequency to the minimum ' +
                               'haplotype frequency.')
                minimum_read_frequency = minimum_haplotype_frequency
            mask_values = (frequencies < minimum_read_frequency).fillna(False).astype(bool)
            self._df = self._df.mask(mask_values)

        max_freq_per_haplotype = frequencies.max(axis=1)
        to_keep = (max_freq_per_haplotype > minimum_haplotype_frequency).astype(bool)
        self._df = self._df.loc[to_keep]

    def calculate_frequencies(self):
        column_sums = self._df.groupby(level=[LOCUS_COLUMN_NAME]).sum()
        frequencies = self._df.truediv(column_sums, fill_value=None)
        frequencies = frequencies.astype(np.float16, copy=False)
        return FrequencyMatrix((frequencies * 100).round(2))


class FrequencyMatrix(_HaplotypeTable):
    def __init__(self, relative_frequencies: pd.DataFrame):
        super().__init__(relative_frequencies)

    def calculate_discrete_calls(self, call_type: str, thresholds: Iterable) -> 'DosageMatrix':
        LOGGER.info('Calculating discrete calls.')
        previous_threshold, *other_threshold = thresholds
        for threshold in other_threshold:
            if previous_threshold > threshold:
                raise ValueError("Please make sure the frequency bounds "
                                 "define non-overlapping intervals.")
            previous_threshold = threshold
        discrete_calls = self._discrete_calls_dispatch(call_type)(thresholds).astype(pd.Int8Dtype())

        def has_calls(group: DataFrame) -> bool:
            return group.any(skipna=True).any()

        discrete_calls = discrete_calls.groupby(level=[LOCUS_COLUMN_NAME]).filter(has_calls)
        return DosageMatrix(discrete_calls)

    def plot_frequencies(self,
                         prefix: str,
                         plot_type: str,
                         thresholds: Iterable[int] = None) -> None:
        for (column_name, column_data) in self._df.iteritems():
            y_values = column_data.dropna().to_list()
            column_name = column_name.rstrip(".bam")
            histogram(y_values,
                      f'{prefix}{column_name}.haplotype.frequency',
                      f'Haplotype frequency distribution\nsample: {column_name}',
                      'Haplotype frequency (%)',
                      'Number of haplotypes',
                      'darkslategray',
                      1,
                      100,
                      1,
                      plot_type,
                      thresholds=thresholds,
                      xaxisticks=10)

    def plot_haplotype_counts(self, plot_name: str, plot_type: str) -> None:
        haplotype_counts = self._df.groupby(level=[LOCUS_COLUMN_NAME]).size()
        haplotype_counts = haplotype_counts.to_list()
        haplotype_count_frequencies = Counter(haplotype_counts)
        bar_heights = [haplotype_count_frequencies[number_of_haplotypes]
                       for number_of_haplotypes
                       in range(min(haplotype_counts, default=0),
                                max(haplotype_counts, default=10)+1)]
        max_counts = max(haplotype_counts, default=10)
        bar_x_positions = range(min(haplotype_counts, default=0), max_counts+1)
        closest_power = int(round(log10(max_counts), 0))
        xaxisticks = max(1, 10**max(1, closest_power-1))
        barplot(bar_x_positions,
                bar_heights,
                plot_name,
                'Haplotype diversity distribution across the sample set',
                'Number of distinct haplotypes per locus',
                'Number of loci',
                'darkslategray',
                plot_type,
                xaxisticks=xaxisticks)

    def _discrete_calls_dispatch(self, call_type: str) -> None:
        cases = {
            "dominant": self._calculate_dominant,
            "dosage": self._calculate_dosage,
        }
        return cases[call_type]

    def _calculate_dosage(self, thresholds: Iterable[str]) -> None:
        def pairwise(lst):
            """Yield successive 2-sized chunks from lst."""
            for i in range(0, len(lst), 2):
                yield lst[i:i + 2]
        not_detected, *other_bounds, homozygous_lower_bound = thresholds
        undetected_mask = self._df <= not_detected
        other_masks = [(self._df >= bound1) &
                       (self._df < bound2)
                       for bound1, bound2 in pairwise(other_bounds)]
        homoz_mask = self._df >= homozygous_lower_bound
        dosages = self._df.mask(undetected_mask, other=0)
        for i, other_mask in enumerate(other_masks, start=1):
            dosages = dosages.mask(other_mask, other=i)
        dosages = dosages.mask(homoz_mask, other=i+1)
        return dosages

    def _calculate_dominant(self, thresholds):
        bound, = thresholds
        not_detected = self._df <= bound
        dom_mask = self._df > bound
        dosages = self._df.mask(not_detected, other=0)
        dosages = dosages.mask(dom_mask, other=1)
        return dosages


class DosageMatrix(_HaplotypeTable):
    def __init__(self, dosage_matrix: pd.DataFrame):
        super().__init__(dosage_matrix)

    def to_cervus(self) -> 'CervusTable':
        transposed = self._df.T
        unique_dosage_sums = np.unique(self._df.groupby(LOCUS_COLUMN_NAME).sum().to_numpy())
        ploidy = np.setdiff1d(unique_dosage_sums, np.array([0]))
        if len(ploidy) != 1:
            raise ValueError('Cervus output can only be created from a dosage table that '
                             'has been filtered to remove dosage calls that do not conform to '
                             'the expected sample ploidy.')
        ploidy = ploidy[0]
        letters = list(string.ascii_lowercase)

        def split_alleles(locus):
            locus_name = locus.columns.get_level_values(LOCUS_COLUMN_NAME)[0]
            _, number_of_haplotypes = locus.shape
            assert number_of_haplotypes <= 26
            letter_representation = pd.Series(letters[:number_of_haplotypes])
            repeated = [letter_representation.repeat(row)
                        for row in locus.to_numpy(dtype=np.int64, na_value=0)]
            res_series = [indx.reset_index(drop=True)
                          if not indx.empty
                          else pd.Series(['*'] * ploidy)
                          for indx in repeated]
            new_columns = pd.Index([f"{locus_name}.{i+1}" for i in range(ploidy)])
            res_index = locus.index
            res_index.name = 'Sample'
            res = pd.DataFrame(res_series, index=locus.index)
            res.columns = new_columns
            return res

        res = transposed.groupby(LOCUS_COLUMN_NAME, sort=False, axis=1).apply(split_alleles)
        res.columns = res.columns.droplevel(LOCUS_COLUMN_NAME)
        return CervusTable(res)

    def filter_distinct_haplotyped_per_sample(self, exact_dosages):
        LOGGER.info('Filtering dosage table to remove loci with unexpected total dosage calls.')
        ne_func = partial(operator.ne, exact_dosages)

        def transform_function(sample_dosages):
            if ne_func(sample_dosages.sum()):
                sample_dosages[:] = pd.NA
            return sample_dosages
        grouped = self._df.groupby(level=[LOCUS_COLUMN_NAME])
        self._df = grouped.transform(transform_function)
        self._df = self._df[self._df.sum(axis=1) != 0]

    def write_population_frequencies(self, path_or_buffer: Union[str, Path, IO[AnyStr]],
                                     na_rep: str = "NaN"):
        to_save = pd.DataFrame()
        total_sums = self._df.groupby(level=[LOCUS_COLUMN_NAME]).sum().sum(axis=1)
        repeat_values = self._df.groupby(level=[LOCUS_COLUMN_NAME]).size()
        total_sums = total_sums.reindex(total_sums.index.repeat(repeat_values))
        population_frequencies = (self._df.sum(axis=1) / total_sums.values).round(2)
        to_save = to_save.assign(AF=population_frequencies)
        to_save = to_save.assign(Total_obs=total_sums.values)
        to_save.to_csv(path_or_buffer, sep='\t', na_rep=na_rep)

    def write_total_calls(self, path_or_buffer: Union[str, Path, IO[AnyStr]], na_rep: str = "NaN"):
        total_calls = self._df.groupby(level=[REFERENCE_COLUMN_NAME, LOCUS_COLUMN_NAME]).sum()
        total_calls.to_csv(path_or_buffer, sep='\t', na_rep=na_rep)

    def write_sample_correctness_completeness(self,
                                              other,
                                              path_or_buffer: Union[str, Path, IO[AnyStr]],
                                              na_rep: str = "NaN"):
        correctness = self._calculate_sample_correctness(other)
        completeness = self._calculate_sample_completeness()
        correctness_completeness = pd.concat([correctness, completeness], axis=1, join='outer')
        correctness_completeness.to_csv(path_or_buffer, sep='\t', na_rep=na_rep)

    def write_locus_correctness_completeness(self,
                                             other,
                                             path_or_buffer: Union[str, Path, IO[AnyStr]],
                                             na_rep: str = "NaN"):
        completeness = self._calculate_locus_completeness()
        correctness = self._calculate_locus_correctness(other)
        correctness_completeness = pd.concat([correctness, completeness], axis=1, join='outer')
        correctness_completeness.to_csv(path_or_buffer, sep='\t', na_rep=na_rep)

    def __deepcopy__(self, memo):
        return DosageMatrix(self._df.copy(deep=True))

    def _boolean_df(self) -> pd.DataFrame:
        return self._df.fillna(0).astype(bool)

    @property
    def number_of_loci_with_counts(self):
        return self._boolean_df().groupby(level=[REFERENCE_COLUMN_NAME, LOCUS_COLUMN_NAME])\
                                 .any().sum()

    @property
    def number_of_samples_with_counts(self):
        return self._boolean_df().groupby(level=[REFERENCE_COLUMN_NAME, LOCUS_COLUMN_NAME])\
                                 .any().sum(axis=1)

    def _calculate_sample_completeness(self):
        completeness = (self.number_of_loci_with_counts / self.number_of_loci) * 100
        completeness.name = 'Sample completeness score'
        completeness.index.name = 'Sample'
        return completeness

    def _calculate_sample_correctness(self, other):
        correctness = (other.number_of_loci_with_counts / self.number_of_loci_with_counts) * 100
        # If a sample has no dosage calls, we devide by 0, which will become nan...
        correctness.fillna(0, inplace=True)
        correctness.name = 'Sample correctness score'
        correctness.index.name = 'Sample'
        return correctness

    def _calculate_locus_completeness(self):
        completeness = self.number_of_samples_with_counts.div(self.number_of_samples, fill_value=0)
        completeness *= 100
        completeness.name = 'Locus completeness score'
        completeness.index.name = 'Locus'
        return completeness

    def _calculate_locus_correctness(self, other):
        correctness = other.number_of_samples_with_counts.div(self.number_of_samples_with_counts,
                                                              fill_value=0)
        correctness *= 100
        correctness.name = 'Locus correctness score'
        correctness.index.name = 'Locus'
        return correctness

    def plot_sample_completeness(self, prefix: str, plot_type: str) -> None:
        sample_completeness = self._calculate_sample_completeness().to_dict()
        completeness_int = [round(i) for i in sample_completeness.values()]
        histogram(completeness_int,
                  f"{prefix}sample_call_completeness",
                  "Sample call completeness: Distribution of loci across the sample set",
                  "Fraction of loci with calls versus the total number of loci (%).",
                  "Number of samples",
                  "darkslategray",
                  0,
                  100,
                  1,
                  plot_type,
                  xaxisticks=10)

    def plot_sample_correctness(self, other: 'DosageMatrix', prefix: str, plot_type: str) -> None:
        sample_correctness = self._calculate_sample_correctness(other).to_dict()
        correctness_int = [round(i) for i in sample_correctness.values()]
        histogram(correctness_int,
                  f"{prefix}sample_call_correctness",
                  "Sample call correctness: Fraction of loci that were called according "
                  "to the dosage filter across the sample set",
                  "Fraction of loci with expected sum of discrete calls (-z) versus the "
                  "total number of observed loci (%).",
                  "Number of samples",
                  "darkslategray",
                  0,
                  100,
                  1,
                  plot_type,
                  xaxisticks=10)

    def plot_locus_completeness(self, prefix: str, plot_type: str) -> None:
        locus_completeness = self._calculate_locus_completeness().to_dict()
        completeness_int = [round(i) for i in locus_completeness.values()]
        histogram(completeness_int,
                  f"{prefix}locus_call_completeness",
                  "Locus call completeness: Distribution of samples across the locus set",
                  "Fraction of samples with calls versus the total number of samples (%).",
                  "Number of loci",
                  "darkslategray",
                  0,
                  100,
                  1,
                  plot_type,
                  xaxisticks=10)

    def plot_locus_correctness(self, other: 'DosageMatrix', prefix: str, plot_type: str) -> None:
        locus_correctness = self._calculate_locus_correctness(other).to_dict()
        correctness_int = [round(i) for locus, i in locus_correctness.items()]
        histogram(correctness_int,
                  f"{prefix}locus_call_correctness",
                  "Locus call correctness: Fraction of samples that were called according "
                  "to the dosage filter across the locus set",
                  "Fraction of samples with calls versus the total number of "
                  "observed samples (%).",
                  "Number of loci",
                  "darkslategray",
                  0,
                  100,
                  1,
                  plot_type,
                  xaxisticks=10)

    def plot_haplotype_counts(self, plot_name: str, plot_type: str) -> None:
        haplotype_counts = self._df.groupby(level=[LOCUS_COLUMN_NAME]).size().tolist()
        haplotype_count_frequencies = Counter(haplotype_counts)
        bar_heights = [haplotype_count_frequencies[number_of_haplotypes]
                       for number_of_haplotypes
                       in range(min(haplotype_counts, default=0),
                                max(haplotype_counts, default=10)+1)]
        max_counts = max(haplotype_counts, default=10)
        bar_x_positions = range(min(haplotype_counts, default=0), max_counts+1)
        closest_power = int(round(log10(max_counts), 0))
        xaxisticks = max(1, 10**max(1, closest_power-1))
        barplot(bar_x_positions,
                bar_heights,
                plot_name,
                'Haplotype diversity distribution across the sample set',
                'Number of distinct haplotypes per locus',
                'Number of loci',
                'darkslategray',
                plot_type,
                xaxisticks=xaxisticks)

    def get_correct_loci(self,
                         other: 'DosageMatrix',
                         correctness_threshold: int) -> Iterable[Tuple[str, str, str]]:
        locus_correctness = self._calculate_locus_correctness(other)
        locus_correctness = locus_correctness[locus_correctness > correctness_threshold]
        correct_loci_split = [tuple(re.split(':|-', locus.rstrip('+').rstrip('_')))
                              for locus
                              in locus_correctness.index.get_level_values(LOCUS_COLUMN_NAME)]
        return correct_loci_split


class CervusTable(_Table):
    def __init__(self, df: pd.DataFrame) -> None:
        super().__init__(df)


def filter_bed_loci(bed: TextIO, write_to: str, loci_to_keep: Iterable[Tuple[str, str, str]]):
    LOGGER.info('Creating new BED file with only correctly called loci.')
    input_bed = BedTool(bed)
    output_bed = BedTool(record for record in input_bed
                         if (record.chrom, str(record.start+1), str(record.end))
                         in loci_to_keep)
    output_bed.saveas(write_to)


def set_default_frequency_thresholds(parsed_args: Namespace):
    if parsed_args.discrete_calls:
        default_thresholds_options = {
            'dominant': {
                'diploid': [10],
                'tetraploid': [10]
                },
            'dosage': {
                'diploid': [10, 10, 90, 90],
                'tetraploid': [12.5, 12.5, 37.5, 37.5, 62.5, 62.5, 87.5, 87.5]
            }
        }
        if not parsed_args.frequency_bounds:
            raise ValueError('If discrete calling is enabled, please define ' +
                             'the interval bounds using the frequency_bounds ' +
                             'parameter (see --help for more information)."')
        defaults_for_type = default_thresholds_options[parsed_args.discrete_calls]
        try:
            # Keyword is used to define thresholds
            parsed_args.frequency_bounds = defaults_for_type[parsed_args.frequency_bounds[0]]
        except KeyError:
            # User has chosen to define own thresholds
            manual_threshold_conditions = {
                'dominant': ('1 threshold', lambda x: len(x) == 1),
                'dosage': ('Odd number of thresholds (at least 4)',
                           lambda x: len(x) >= 4 and len(x) % 2 == 0)
            }
            wording, condition = manual_threshold_conditions[parsed_args.discrete_calls]
            if not condition(parsed_args.frequency_bounds):
                raise ValueError('If setting the thresholds manually in ' +
                                 f'{parsed_args.discrete_calls} mode, ' +
                                 'the thresholds must adhere to the ' +
                                 f'following condition: {wording}')
        parsed_args.frequency_bounds = [float(i) for i in parsed_args.frequency_bounds]
        if parsed_args.dosage_filter is None:
            LOGGER.warning(('Discrete calls will be generated in mode '
                            f'{parsed_args.discrete_calls}, but filtered calls '
                            'will not be generated because "dosage_filter" is not '
                            'specified.'))
            if parsed_args.locus_correctness_filter:
                raise ValueError("--locus_correctness_filter is set, "
                                 "but dosage call filtering is disabled (--dosage_filter).")
    else:
        if parsed_args.dosage_filter:
            raise ValueError("--dosage_filter is defined, "
                             "but discrete calling is disabled (--discrete_calls).")
        if parsed_args.locus_correctness_filter:
            raise ValueError("--locus_correctness_filter is defined, "
                             "but discrete calling is disabled (--discrete_calls).")
        LOGGER.warning(('"discrete_calls" option is not set, will not '
                        'transform frequencies into discrete calls.'))
    return parsed_args


def set_filter_defaults(parsed_args: Namespace):
    warnings_dict = {
        # argument: [default_value]
        'min_distinct_haplotypes': 0,
        'max_distinct_haplotypes': inf,
        'min_read_count': 0,
        'max_read_count': inf,
        'min_haplotype_frequency': 0,
    }
    if parsed_args.dosage_filter:
        warnings_dict['locus_correctness_filter'] = 0

    warning_message = ('"--%(argument)s" argument was not given. This means that '
                       'this filter will not be applied. If you are sure about this, '
                       'you can hide this warning by setting "--%(argument)s %(val)s" '
                       'explicitly.')
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
    orig_argument = getattr(parsed_args, argument_name)
    try:
        # The arguments are now float type (as set in add_argument())
        # Try casting them to int and check if the float was truncated.
        setattr(parsed_args, argument_name, int(orig_argument))
        if orig_argument != int(orig_argument):
            LOGGER.warning(f'Argument "{argument_name}": value '
                           f'"{orig_argument}" truncated to '
                           f'"{int(orig_argument)}".')
    except OverflowError:
        # The float was inf, leave it like that
        setattr(parsed_args, argument_name, orig_argument)
    return parsed_args


def parse_args(args):
    haplotype_parser = ArgumentParser(
        "haplotype-sites",
        description=('Create haplotypes using a VCF '
                     'file containing variant positions and a BED '
                     'file containing SMAPs.'))
    haplotype_parser.add_argument('-v', '--version',
                                  action='version',
                                  version=__version__)
    input_output_group = haplotype_parser.add_argument_group(
        title='Input and output information')
    input_output_group.add_argument(
        'alignments_dir',
        type=Path,
        help=('Path to the directory containing BAM and BAI alignment files. '
              'All BAM files should be in the same directory.'))
    input_output_group.add_argument(
        'bed',
        type=Path,
        help=('BED file containing sites for which '
              'haplotypes will be reconstructed. For GBS experiments, '
              'the BED file should be generated using SMAP delineate. '
              'For HiPlex data, a BED6 file can be provided, with the '
              'reference sequence ID in the 1st column, '
              'the locus start and end site in the 2nd and 3rd column, '
              'the HiPlex_locus_name in the 4th column, '
              'the strand orientation ("+") in the 5th column, '
              'the SMAPs listed in the 6th column, '
              'the 7th and 8th columns may be left blank (or ".") and '
              'the 9th column contains the name of the sample set, respectively.'))
    input_output_group.add_argument(
        'vcf',
        help=('VCF file containing variant positions. '
              'It should contain at least the first 9 columns.'))

    input_output_group.add_argument(
        '-o', '--out',
        dest='out',
        default='',
        type=str,
        help='Basename of the output file without extension (default: "").')
    input_output_group.add_argument(
        '-r', '-mapping_orientation',
        required=True,
        dest='mapping_orientation',
        # choices=['stranded', 'ignore'],
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
        '--cervus',
        action='store_true',
        help='Transform discrete calls table to an output that can be used with Cervus.'
    )

    discrete_calls_group = haplotype_parser.add_argument_group(
        title='Discrete calls options',
        description=('Use thresholds to transform '
                     'haplotype frequencies into discrete calls '
                     'using fixed intervals. '
                     'The assigned intervals are indicated '
                     'by a running integer. This is only '
                     'informative for individual samples '
                     'and not for Pool-Seq data.')
        )
    discrete_calls_group.add_argument(
        '-e', '--discrete_calls',
        choices=['dominant', 'dosage'],
        dest='discrete_calls',
        help=('Set to "dominant" to transform haplotype frequency values '
              'into presence(1)/absence(0) calls per allele, or "dosage" '
              'to indicate the allele copy number.'))
    discrete_calls_group.add_argument(
        '-i', '--frequency_interval_bounds',
        nargs='+',
        dest='frequency_bounds',
        help=('Frequency interval bounds for transforming haplotype '
              'frequencies into discrete calls. Custom thresholds can be '
              'defined by passing one or more space-separated values (relative '
              'frequencies in percentage). For dominant calling, one value '
              'should be specified. For dosage calling, an even total number '
              'of four or more thresholds should be specified. Default values '
              'are invoked by passing either "diploid" or "tetraploid". The '
              'default value for dominant calling (see discrete_calls '
              'argument) is 10, both for "diploid" and "tetraploid". For '
              'dosage calling, the default for diploids is "10, 10, 90, 90" '
              'and for tetraploids "12.5, 12.5, 37.5, 37.5, 62.5, 62.5, 87.5, '
              '87.5".'))
    discrete_calls_group.add_argument(
        # Default will be set to a new default later, need None to check
        # A warning needs to be presented to user if option is not set.
        '-z', '--dosage_filter',
        type=int,
        default=None,
        dest='dosage_filter',
        help=('Mask dosage calls in the loci for which the total allele count '
              'for a given locus at a given sample differs from the defined '
              'value. For example, in diploid organisms the total allele copy '
              'number must be 2, and in tetraploids the total allele copy '
              'number must be 4. (default no filtering).'
              )
    )
    discrete_calls_group.add_argument(
        # Default will be set to a new default later, need None to check
        # A warning needs to be presented to user if option is not set.
        '--locus_correctness',
        type=int,
        default=None,
        dest='locus_correctness_filter',
        help=('Create a new .bed file defining only the loci that were '
              'correctly dosage called (-z) in at least the defined percentage of samples.')
    )

    plot_group = haplotype_parser.add_argument_group(
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
              'generate per-sample plots [default "summary"].'))
    plot_group.add_argument(
        '-t', '--plot_type',
        dest='plot_type',
        choices=['png', 'pdf'],
        default='png',
        help='Choose the file type for the plots [png].')

    file_output_group = haplotype_parser.add_argument_group(
        title='File formatting options')
    file_output_group.add_argument(
        '-m', '--mask_frequency',
        dest='mask_frequency',
        type=float,
        default=0,
        help=('Mask haplotype frequency values below MASK_FREQUENCY for '
              'individual samples to remove noise from the final output. '
              'Haplotype frequency values below MASK_FREQUENCY are set to '
              'UNDEFINED_REPRESENTATION (see -u). Haplotypes are not removed based on this '
              'value, use --min_haplotype_frequency for this purpose instead.'))
    file_output_group.add_argument(
        '-u', '--undefined_representation',
        dest='undefined_representation',
        type=str,
        default=pd.NA,
        help='Value to use for non-existing or masked data [NaN].')

    filtering_group = haplotype_parser.add_argument_group(
        title='Filtering options')
    filtering_group.add_argument(
        '--no_indels',
        dest='no_indels',
        action='store_true',
        help=('Use this option if you want to exclude haplotypes '
              'that contain an indel at the given SNP positions.'
              'These reads are then also ignored to evaluate the minimum'
              'read count (default off: haplotypes with indels are included in output).'))
    filtering_group.add_argument(
        '-a', '-partial',
        dest='partial',
        required=True,
        choices={'include', 'exclude'},
        help=('Choose to include or exclude haplotypes that '
              'contain partial alignments. For GBS data, choose '
              '"include", for HiPlex data, choose "exclude".'))
    filtering_group.add_argument(
        '-q', '--min_mapping_quality',
        dest='minimum_mapping_quality',
        default=30,
        type=int,
        help=('Minimum bam mapping quality to retain reads for '
              'analysis [30].'))
    filtering_group.add_argument(
        # Use None as default because we want to check if this default is used.
        # If the user did not provide a value, the value will be set to 0 later.
        '-j', '--min_distinct_haplotypes',
        dest='min_distinct_haplotypes',
        default=None,
        type=int,
        help=('Minimum number of distinct haplotypes per locus across all '
              'samples. Loci that do not fit this criterium are removed '
              'from the final output [0].'))
    filtering_group.add_argument(
        # Use None as default because we want to check if this default is used.
        # If the user did not provide a value, the value will be set to inf later.
        '-k', '--max_distinct_haplotypes',
        dest='max_distinct_haplotypes',
        default=None,
        type=float,  # This needs to be float, the user can pass "inf" and only float("inf") works
        help=('Maximal number of distinct haplotypes per locus across all '
              'samples. Loci that do not fit this criterium are removed from '
              'the final output [inf].'))
    filtering_group.add_argument(
        # Use None as default because we want to check if this default is used.
        # If the user did not provide a value, the value will be set to 0 later.
        '-c', '--min_read_count',
        dest='min_read_count',
        default=None,  # Will be set to inf by default later
        type=int,
        help=('Minimum total number of reads per locus per sample, read depth '
              'is calculated after filtering out the low frequency haplotypes (-f) [0].'))
    filtering_group.add_argument(
        # Use None as default because we want to check if this default is used.
        # If the user did not provide a value, the value will be set to inf later.
        '-d', '--max_read_count',
        dest='max_read_count',
        default=None,  # Will be set to inf by default later
        type=float,
        help=('Maximal total number of reads per locus per sample, read depth '
              'is calculated after filtering out the low frequency haplotypes '
              '(-f) [inf].'))
    filtering_group.add_argument(
        # Use None as default because we want to check if this default is used.
        # If the user did not provide a value, the value will be set to 0 later.
        '-f', '--min_haplotype_frequency',
        dest='min_haplotype_frequency',
        default=None,
        type=float,
        help=('Minimum haplotype frequency (in %%) to retain the haplotype '
              'in the genotyping table. If in at least one sample the '
              'haplotype frequency is above MIN_HAPLOTYPE_FREQUENCY, the haplotype '
              'is retained. Haplotypes for which MIN_HAPLOTYPE_FREQUENCY is never '
              'reached in any of the samples are removed [0].'))

    resources_group = haplotype_parser.add_argument_group(
        title='System resources')
    resources_group.add_argument(
        '-p', '--processes',
        dest='processes',
        default=1,
        type=int,
        help='Number of parallel processes [1].')

    parsed_args = haplotype_parser.parse_args(args)
    if parsed_args.read_type and parsed_args.mapping_orientation:
        raise ValueError("Used both -read_type and -mapping_orientation.")
    if parsed_args.read_type or parsed_args.mapping_orientation in ('separate', 'merged'):
        LOGGER.warning("Option -read_type will be removed in favour of "
                       "-mapping_orientation in a future version. See --help for more information.")

        parsed_args.mapping_orientation = 'ignore' \
                                          if parsed_args.read_type == 'merged' \
                                          else 'stranded'
    if parsed_args.cervus and not parsed_args.locus_correctness_filter:
        raise ValueError("Requested genotype file for Cervus, "
                         "but this requires --locus_correctness_filter.")

    parsed_args = set_default_frequency_thresholds(parsed_args)
    parsed_args = set_filter_defaults(parsed_args)
    log_args(parsed_args)
    return parsed_args


def log_args(parsed_args):
    log_string = dedent("""
    Running SMAP haplotype-sites using the following options:

    Input & output:
        Alignments directory: {alignments_dir}
        Bed file: {bed}
        VCF file: {vcf}
        Mapping Orientation: {mapping_orientation}
        Output file basename: {out}

    Discrete calls options:
        Discrete call mode: {discrete_calls}
        Frequency bounds: {frequency_bounds}
        Dosage filter: {dosage_filter}
        Locus correctness filter: {locus_correctness_filter}

    Graphical output options:
        Plot mode: {plot}
        Plot type: {plot_type}

    File formatting options:
        Mask frequency: {mask_frequency}
        Undefined_representation: {undefined_representation}

    Filtering options:
        Remove haplotypes with indels: {no_indels}
        Include haplotypes with partial alignment: {partial}
        Minimum read mapping quality: {minimum_mapping_quality}
        Minimum number of haplotypes per locus: {min_distinct_haplotypes}
        Maximum number of haplotypes per locus: {max_distinct_haplotypes}
        Minimum read count per locus in each sample: {min_read_count}
        Maximum read count per locus in each sample: {max_read_count}
        Minimum haplotype frequency: {min_haplotype_frequency}

    System resources:
        Number of processes: {processes}
    """)
    LOGGER.info(log_string.format(**vars(parsed_args)))


def main(args):
    LOGGER.info('SMAP haplotype-sites started.')
    LOGGER.debug('Parsing arguments: %r', args)
    parsed_args = parse_args(args)
    LOGGER.debug('Parsed arguments: %r' % vars(parsed_args))
    prefix = f"{parsed_args.out}_" if parsed_args.out else ''
    if not parsed_args.bed.is_file():
        raise ValueError(f"Bed file {parsed_args.bed} does not exist or is not a file.")
    with parsed_args.bed.open('r') as bed_file:
        stacks = Stacks(bed_file)
    stacks.remove_non_polymophic_stacks(parsed_args.vcf)
    stacks.write_coordinates(f'{prefix}coordinates.tsv')
    if not parsed_args.alignments_dir.is_dir():
        raise ValueError(f'{parsed_args.alignments_dir!s} does not exist or is not a directory.')
    bam_files = [f for f in parsed_args.alignments_dir.iterdir() if f.suffix == '.bam']
    LOGGER.info('Found %s bam files.', len(bam_files))
    if not bam_files:
        raise ValueError(f"Could not find any .bam files in {parsed_args.alignments_dir!s}")
    haplotyper = Haplotyper(stacks,
                            parsed_args.mapping_orientation == 'stranded',
                            parsed_args.minimum_mapping_quality,
                            parsed_args.processes)
    hapolytype_counts = haplotyper.haplotype_bam_reads(bam_files)

    count_matrix = CountMatrix(hapolytype_counts)
    if parsed_args.no_indels:
        count_matrix.filter_indels()
    if parsed_args.partial == 'exclude':
        count_matrix.filter_partial()
    count_matrix.filter_for_minimum_or_maximum_read_count(parsed_args.min_read_count,
                                                          parsed_args.max_read_count)
    count_matrix.filter_on_minimum_haplotype_frequency(
        parsed_args.min_haplotype_frequency,
        minimum_read_frequency=parsed_args.mask_frequency
    )
    filename_parameters = (f'c{parsed_args.min_read_count}_'
                           f'f{parsed_args.min_haplotype_frequency}_'
                           f'm{parsed_args.mask_frequency}')
    count_matrix.to_csv(f'{prefix}read_counts_{filename_parameters}.tsv',
                        na_rep=parsed_args.undefined_representation)
    frequency_matrix = count_matrix.calculate_frequencies()
    frequency_matrix.to_csv(f'{prefix}haplotype_frequencies_{filename_parameters}.tsv',
                            na_rep=parsed_args.undefined_representation)
    frequency_matrix.filter_for_number_of_distinct_haplotypes(
        parsed_args.min_distinct_haplotypes,
        parsed_args.max_distinct_haplotypes
    )
    if parsed_args.plot >= PLOT_ALL:
        frequency_matrix.plot_frequencies(prefix,
                                          parsed_args.plot_type,
                                          parsed_args.frequency_bounds)
    if parsed_args.plot >= PLOT_SUMMARY:
        frequency_matrix.plot_haplotype_counts(f"{prefix}haplotype_counts_frequencies",
                                               parsed_args.plot_type)
    if parsed_args.discrete_calls:
        dosage_matrix = frequency_matrix.calculate_discrete_calls(
            parsed_args.discrete_calls,
            parsed_args.frequency_bounds
        )
        dosage_matrix.to_csv(f'{prefix}haplotypes_{filename_parameters}_discrete_calls.tsv',
                             na_rep=parsed_args.undefined_representation)
        dosage_matrix.write_total_calls(
            f'{prefix}haplotypes_{filename_parameters}_discrete_calls_total.tsv',
            na_rep=parsed_args.undefined_representation
        )
        if parsed_args.plot >= PLOT_SUMMARY:
            dosage_matrix.plot_haplotype_counts(f"{prefix}haplotype_counts_discrete_calls",
                                                parsed_args.plot_type)
        if parsed_args.dosage_filter:
            orig_dosage_matrix = deepcopy(dosage_matrix)
            dosage_matrix.filter_distinct_haplotyped_per_sample(parsed_args.dosage_filter)
            dosage_matrix.filter_for_number_of_distinct_haplotypes(
                parsed_args.min_distinct_haplotypes,
                parsed_args.max_distinct_haplotypes
            )
            if parsed_args.plot >= PLOT_SUMMARY:
                orig_dosage_matrix.plot_sample_completeness(prefix, parsed_args.plot_type)
                orig_dosage_matrix.plot_sample_correctness(dosage_matrix,
                                                           prefix,
                                                           parsed_args.plot_type)
                orig_dosage_matrix.plot_locus_completeness(prefix, parsed_args.plot_type)
                orig_dosage_matrix.plot_locus_correctness(dosage_matrix,
                                                          prefix,
                                                          parsed_args.plot_type)
                orig_dosage_matrix.write_locus_correctness_completeness(
                    dosage_matrix,
                    f'{prefix}locus_completeness_correctness.tsv',
                    na_rep=parsed_args.undefined_representation
                )
                orig_dosage_matrix.write_sample_correctness_completeness(
                    dosage_matrix,
                    f'{prefix}sample_completeness_correctness.tsv',
                    na_rep=parsed_args.undefined_representation
                )
                dosage_matrix.plot_haplotype_counts(
                    f"{prefix}haplotype_counts_discrete_calls_filtered",
                    parsed_args.plot_type
                )
                if parsed_args.locus_correctness_filter:
                    correct_loci = orig_dosage_matrix.get_correct_loci(
                        orig_dosage_matrix,
                        parsed_args.locus_correctness_filter
                    )
                    new_bed = (f"{prefix}{filename_parameters}_"
                               f"correctness{parsed_args.locus_correctness_filter}"
                               f"_loci.bed")
                    with parsed_args.bed.open('r') as open_bed:
                        filter_bed_loci(open_bed, new_bed, correct_loci)
                    if parsed_args.cervus:
                        cervus_table = dosage_matrix.to_cervus()
                        cervus_table.to_csv(f'{prefix}cervus.tsv', float_format='%.2f')
        dosage_matrix.to_csv(
            f'{prefix}haplotypes_{filename_parameters}_discrete_calls_filtered.tsv',
            na_rep=parsed_args.undefined_representation)
        dosage_matrix.write_population_frequencies(
            f'{prefix}haplotypes_{filename_parameters}_pop_hf.tsv',
            na_rep=parsed_args.undefined_representation)
    LOGGER.info('Finished')
