from argparse import Namespace
import unittest
from unittest.mock import patch
from smap.haplotype import (CervusTable,
                            Stacks,
                            Haplotyper,
                            CountMatrix,
                            FrequencyMatrix,
                            DosageMatrix,
                            filter_bed_loci,
                            main,
                            parse_args)
from smap.plotting import PlotLevel
from tempfile import TemporaryDirectory
from data import merged_clusters, snps_vcf, wt_bam, sample1_bam, sample2_bam
from pathlib import Path
from textwrap import dedent
import pandas as pd
import numpy as np
from io import StringIO
from copy import deepcopy
from math import inf


LOCUS_COLUMN_NAME = 'Locus'
HAPLOTYPES_COLUMN_NAME = 'Haplotypes'
REFERENCE_COLUMN_NAME = 'Reference'
INDEX_COLUMNS = [REFERENCE_COLUMN_NAME, LOCUS_COLUMN_NAME, HAPLOTYPES_COLUMN_NAME]


class TestCommandLine(unittest.TestCase):
    def test_main_without_args(self):
        """
        Fail if passed args are empty.
        Check if usage is printed.
        """
        with self.assertRaises(SystemExit) as cm:
            main([])
        self.assertNotEqual(cm.exception.code, 0)

    def test_main_help(self):
        """
        Test if help is printed if --help is passed.
        """
        with self.assertRaises(SystemExit) as cm:
            main(args=['--help'])
        self.assertEqual(cm.exception.code, 0)

    def test_version(self):
        """Test version printing.
        """
        with self.assertRaises(SystemExit) as cm:
            main(args=['--version'])
        self.assertEqual(cm.exception.code, 0)

    def test_argument_parsing(self):
        arguments = ["-partial", "include",
                     "--plot", "all",
                     "--no_indels",
                     "--max_distinct_haplotypes", "inf",
                     "--min_distinct_haplotypes", "0",
                     "-z", "2",
                     "-r", "merged",
                     "-p", "1",
                     "-m", "2",
                     "--discrete_calls", "dosage",
                     "--frequency_interval_bounds", "0.5", "10", "90", "90",
                     "--undefined_representation", "NA",
                     "--min_haplotype_frequency", "5",
                     "--min_read_count", "1",
                     "--locus_correctness", "100",
                     "-c", "100",
                     "/foo/bar/",
                     "/foo/bar.bed",
                     "/foo/bar.vcf",
                     "--cervus"]
        result = parse_args(arguments)
        expected = Namespace(alignments_dir=Path('/foo/bar'),
                             bed=Path('/foo/bar.bed'),
                             cervus=True,
                             discrete_calls='dosage',
                             dosage_filter=2,
                             frequency_bounds=[0.5, 10.0, 90.0, 90.0],
                             locus_correctness_filter=100,
                             mapping_orientation='stranded',
                             mask_frequency=2.0,
                             max_distinct_haplotypes=inf,
                             max_read_count=inf,
                             min_distinct_haplotypes=0,
                             min_haplotype_frequency=5,
                             min_read_count=100,
                             minimum_mapping_quality=30,
                             no_indels=True,
                             out='',
                             partial='include',
                             plot=PlotLevel('all'),
                             plot_type='png',
                             processes=1,
                             read_type=None,
                             undefined_representation='NA',
                             vcf='/foo/bar.vcf')
        self.assertEqual(result, expected)

    def test_allow_float_for_min_haplotype_frequency(self):
        arguments = ["-partial", "include",
                     "-mapping_orientation", "ignore",
                     "-f", "10.4",
                     "/foo/bar/",
                     "/foo/bar.bed",
                     "/foo/bar.vcf"]
        result = parse_args(arguments)
        expected = Namespace(alignments_dir=Path('/foo/bar'),
                             bed=Path('/foo/bar.bed'),
                             cervus=False,
                             discrete_calls=None,
                             dosage_filter=None,
                             frequency_bounds=None,
                             locus_correctness_filter=None,
                             mapping_orientation='ignore',
                             mask_frequency=0,
                             max_distinct_haplotypes=inf,
                             max_read_count=inf,
                             min_distinct_haplotypes=0,
                             min_haplotype_frequency=10.4,
                             min_read_count=0,
                             minimum_mapping_quality=30,
                             no_indels=False,
                             out='',
                             partial='include',
                             plot=PlotLevel('summary'),
                             plot_type='png',
                             processes=1,
                             read_type=None,
                             undefined_representation=pd.NA,
                             vcf='/foo/bar.vcf')
        self.assertEqual(result, expected)


# TODO: strand-specific tests
# TODO: test generate indels
class TestStacks(unittest.TestCase):
    def setUp(self):
        self.tempdir = TemporaryDirectory()
        self.merged_clusters_bed = Path(self.tempdir.name) / "final_stack_positions.bed"
        with self.merged_clusters_bed.open(mode='w') as test_bed:
            test_bed.write(merged_clusters())
        with self.merged_clusters_bed.open(mode='r') as test_bed:
            self.stacks = Stacks(test_bed)
        self.vcf = Path(self.tempdir.name) / "snps.vcf"
        with self.vcf.open(mode='w') as vcf_file:
            vcf_file.write(snps_vcf())

    def tearDown(self):
        self.tempdir.cleanup()

    def test_init(self):
        result = {
            "1:7-115_+": {'positions': {115, 7},
                          'scaffold': '1',
                          'smaps': {7, 115},
                          'start': 6,
                          'stop': 115,
                          'strand': '+',
                          'variants': {}},
            "1:246-354_+": {'positions': {354, 246, 344},
                            'scaffold': '1',
                            'smaps': {246, 344, 354},
                            'start': 245,
                            'stop': 354,
                            'strand': '+',
                            'variants': {}}
        }
        self.assertDictEqual(self.stacks.stacks, result)

    def test_remove_non_polymorphic_stacks(self):
        result = {
            "1:7-115_+": {'positions': {58, 115, 7},
                          'scaffold': '1',
                          'smaps': {7, 115},
                          'start': 6,
                          'stop': 115,
                          'strand': '+',
                          'variants': {58: {'alt': 'C', 'ref': 'T'}}},
            "1:246-354_+": {'positions': {354, 299, 246, 344},
                            'scaffold': '1',
                            'smaps': {246, 344, 354},
                            'start': 245,
                            'stop': 354,
                            'strand': '+',
                            'variants': {299: {'alt': 'A,C', 'ref': 'G'}}}
        }
        # Add an extra non-polymorphic stack (not in vcf file)
        self.stacks._stacks['1:116-200_+'] = {'positions': {200, 116},
                                              'scaffold': '1',
                                              'smaps': {200, 116},
                                              'start': 116,
                                              'stop': 200,
                                              'strand': '+',
                                              'variants': {}}
        self.stacks.remove_non_polymophic_stacks(self.vcf)
        self.assertDictEqual(self.stacks.stacks, result)

    def test_remove_non_polymorphic_stacks_pass_file_not_exist(self):
        self.stacks._stacks['1:116-200_+'] = {'positions': {199, 115},
                                              'scaffold': '1',
                                              'smaps': ['199', '115'],
                                              'start': 116,
                                              'stop': 200,
                                              'strand': '+',
                                              'variants': {}}
        with self.assertRaises(ValueError):
            self.stacks.remove_non_polymophic_stacks(Path("/tmp/foo"))

    def test_remove_non_polymorphic_stacks_pass_file_not_vcf(self):
        self.stacks._stacks['1:116-200_+'] = {'positions': {199, 115},
                                              'scaffold': '1',
                                              'smaps': ['199', '115'],
                                              'start': 116,
                                              'stop': 200,
                                              'strand': '+',
                                              'variants': {}}
        wrong_format = Path(self.tempdir.name) / "foo.txt"
        with wrong_format.open('w') as fh:
            fh.write('foo')
        with self.assertRaises(ValueError):
            self.stacks.remove_non_polymophic_stacks(wrong_format)

    def test_file_does_not_exist(self):
        with self.assertRaises(FileNotFoundError):
            Stacks(Path("/tmp/foo"))

    def test_pass_empty_file(self):
        empty_file = Path(self.tempdir.name) / "foo.txt"
        empty_file.touch()
        Stacks(empty_file)

    def test_not_a_bed_file(self):
        wrong_format = Path(self.tempdir.name) / "foo.txt"
        with wrong_format.open('w') as fh:
            fh.write('foo')
        with self.assertRaises(ValueError):
            Stacks(wrong_format)

    def test_vcf_add_header(self):
        vcf = Path(self.tempdir.name) / "no_header.vcf"
        with vcf.open('w') as vcf_file:
            vcf_file.write(snps_vcf(header=False))
        self.stacks._check_vcf(vcf)
        with vcf.open('r') as vcf_file:
            vcf_contents = vcf_file.read()
            self.assertMultiLineEqual(vcf_contents.strip(), snps_vcf())

    def test_coordinates(self):
        result = dedent("""
                        Reference	Locus	SNPs	SMAPs	SNPs_and_SMAPs
                        1	1:246-354_+	299	246,344,354	246,299,344,354
                        1	1:7-115_+	58	7,115	7,58,115
                        """)
        coordinate_file = Path(self.tempdir.name) / "coordinates.tsv"
        self.stacks.remove_non_polymophic_stacks(self.vcf)
        self.stacks.write_coordinates(coordinate_file)
        with coordinate_file.open('r') as handler:
            coordinate_contents = handler.read()
            self.assertMultiLineEqual(coordinate_contents.strip(), result.strip())


class TestHaplotyper(unittest.TestCase):
    def setUp(self):
        self.tempdir = TemporaryDirectory()
        merged_clusters_bed = Path(self.tempdir.name) / "final_stack_positions.bed"
        merged_clusters_bed.touch()
        self.stacks = Stacks(merged_clusters_bed)
        self.stacks._stacks = {
            "1:7-115_+": {'positions': {115, 7},
                          'scaffold': '1',
                          'smaps': {115, 7},
                          'start': 6,
                          'stop': 115,
                          'strand': '+',
                          'variants': {}},
            "1:246-354_+": {'positions': {354, 246, 344},
                            'scaffold': '1',
                            'smaps': {354, 246, 344},
                            'start': 245,
                            'stop': 354,
                            'strand': '+',
                            'variants': {}}
        }
        self.mapping_directory = Path(self.tempdir.name + "/mapping/")
        self.mapping_directory.mkdir()

        self.wt = self.mapping_directory / "WT.BWA.bam"
        self.wt_bai = self.mapping_directory / "WT.BWA.bam.bai"
        self.sample1 = self.mapping_directory / "Sample1.BWA.bam"
        self.sample1_bai = self.mapping_directory / "Sample1.BWA.bam.bai"
        self.sample2 = self.mapping_directory / "Sample2.BWA.bam"
        self.sample2_bai = self.mapping_directory / "Sample2.BWA.bam.bai"
        wt_bam_data, wt_bam_index = wt_bam()
        sample1_bam_data, sample1_bam_index = sample1_bam()
        sample2_bam_data, sample2_bam_index = sample2_bam()
        with self.wt.open(mode='wb') as wt_file,\
             self.wt_bai.open(mode='wb') as wt_file_bai, \
             self.sample1.open(mode='wb') as sample1_file,\
             self.sample1_bai.open(mode='wb') as sample1_file_bai,\
             self.sample2.open(mode='wb') as sample2_file,\
             self.sample2_bai.open(mode='wb') as sample2_file_bai:
            wt_file.write(wt_bam_data)
            wt_file_bai.write(wt_bam_index)
            sample1_file.write(sample1_bam_data)
            sample1_file_bai.write(sample1_bam_index)
            sample2_file.write(sample2_bam_data)
            sample2_file_bai.write(sample2_bam_index)

    def tearDown(self):
        self.tempdir.cleanup()

    def test_init(self):
        # TODO: test arguments
        Haplotyper(self.stacks, False, 0, 1)

    def test_pass_empty_stacks(self):
        self.stacks._stacks = {}
        haplotyper = Haplotyper(self.stacks, False, 0, 1)
        haplotyper.haplotype_bam_reads([self.wt, self.sample1, self.sample2])

    def test_pass_no_bam_files(self):
        haplotyper = Haplotyper(self.stacks, False, 0, 1)
        with self.assertRaises(ValueError):
            haplotyper.haplotype_bam_reads([])

    def test_pass_empty_bam_file(self):
        haplotyper = Haplotyper(self.stacks, False, 0, 1)
        empty_bam = Path(self.tempdir.name) / "empty.bam"
        empty_bam.touch()
        with self.assertRaises(ValueError):
            haplotyper.haplotype_bam_reads([empty_bam])

    def test_haplotype_bam_reads(self):
        result_index = pd.MultiIndex.from_tuples([('1', '1:246-354_+', '00.'),
                                                  ('1', '1:246-354_+', '000'),
                                                  ('1', '1:7-115_+', '00')],
                                                 names=INDEX_COLUMNS)
        result = pd.DataFrame([[0, 25, 0], [80, 75, 100], [100, 100, 100]],
                              columns=['Sample1.BWA.bam', 'Sample2.BWA.bam',  'WT.BWA.bam'],
                              index=result_index,
                              dtype=pd.UInt32Dtype())

        haplotyper = Haplotyper(self.stacks, False, 0, 1)
        haplotypes = haplotyper.haplotype_bam_reads([self.wt, self.sample1, self.sample2])
        pd.testing.assert_frame_equal(haplotypes, result, check_exact=True)

    def test_quality_threshold_filter_everything(self):
        empty_index = pd.MultiIndex(levels=[[], [], []], codes=[[], [], []], names=INDEX_COLUMNS)
        result = pd.DataFrame(columns=['Sample1.BWA.bam', 'Sample2.BWA.bam',  'WT.BWA.bam'],
                              index=empty_index)
        haplotyper = Haplotyper(self.stacks, False, 1000, 1)
        haplotypes = haplotyper.haplotype_bam_reads([self.wt, self.sample1, self.sample2])
        pd.testing.assert_frame_equal(haplotypes, result, check_exact=True)

    # TODO: strand_specific, quality threshold that is not the same for each read

    def test_haplotype_bam_reads_sep(self):
        result_index = pd.MultiIndex.from_tuples([('1', '1:246-354_+', '00.'),
                                                  ('1', '1:246-354_+', '000'),
                                                  ('1', '1:7-115_+', '00')],
                                                 names=INDEX_COLUMNS)
        result = pd.DataFrame([[0, 25, 0], [80, 75, 100], [100, 100, 100]],
                              columns=['Sample1.BWA.bam', 'Sample2.BWA.bam',  'WT.BWA.bam'],
                              index=result_index,
                              dtype=pd.UInt32Dtype())

        haplotyper = Haplotyper(self.stacks, True, 0, 1)
        haplotypes = haplotyper.haplotype_bam_reads([self.wt, self.sample1, self.sample2])
        pd.testing.assert_frame_equal(haplotypes, result, check_exact=True)


class TestCountMatrix(unittest.TestCase):
    def setUp(self):
        count_index = pd.MultiIndex.from_tuples([('1', '1:246-354_+', '00.'),
                                                 ('1', '1:246-354_+', '000'),
                                                 ('1', '1:246-354_+', '0-0'),
                                                 ('1', '1:7-115_+', '00')],
                                                names=INDEX_COLUMNS)
        self.counts = pd.DataFrame([[0, 25, 0], [80, 75, 100], [10, 0, 0], [100, 100, 100]],
                                   columns=['Sample1.BWA.bam', 'Sample2.BWA.bam', 'WT.BWA.bam'],
                                   index=count_index,
                                   dtype=pd.Int16Dtype())

    def test_init(self):
        CountMatrix(self.counts)

    def test_filter_indels(self):
        result_index = pd.MultiIndex.from_tuples([('1', '1:246-354_+', '00.'),
                                                 ('1', '1:246-354_+', '000'),
                                                 ('1', '1:7-115_+', '00')],
                                                 names=INDEX_COLUMNS)
        result = pd.DataFrame([[0, 25, 0], [80, 75, 100], [100, 100, 100]],
                              columns=['Sample1.BWA.bam', 'Sample2.BWA.bam', 'WT.BWA.bam'],
                              index=result_index,
                              dtype=pd.Int16Dtype())
        count_matrix = CountMatrix(self.counts)
        count_matrix.filter_indels()
        pd.testing.assert_frame_equal(result, count_matrix._df, check_exact=True)

    def test_filter_indels_twice(self):
        result_index = pd.MultiIndex.from_tuples([('1', '1:246-354_+', '00.'),
                                                 ('1', '1:246-354_+', '000'),
                                                 ('1', '1:7-115_+', '00')],
                                                 names=INDEX_COLUMNS)
        result = pd.DataFrame([[0, 25, 0], [80, 75, 100], [100, 100, 100]],
                              columns=['Sample1.BWA.bam', 'Sample2.BWA.bam', 'WT.BWA.bam'],
                              index=result_index,
                              dtype=pd.Int16Dtype())
        count_matrix = CountMatrix(self.counts)
        count_matrix.filter_indels()
        count_matrix.filter_indels()
        pd.testing.assert_frame_equal(result, count_matrix._df, check_exact=True)

    def test_filter_partial(self):
        result_index = pd.MultiIndex.from_tuples([('1', '1:246-354_+', '000'),
                                                 ('1', '1:246-354_+', '0-0'),
                                                 ('1', '1:7-115_+', '00')],
                                                 names=INDEX_COLUMNS)
        result = pd.DataFrame([[80, 75, 100], [10, 0, 0], [100, 100, 100]],
                              columns=['Sample1.BWA.bam', 'Sample2.BWA.bam', 'WT.BWA.bam'],
                              index=result_index,
                              dtype=pd.Int16Dtype())

        count_matrix = CountMatrix(self.counts)
        count_matrix.filter_partial()
        pd.testing.assert_frame_equal(result, count_matrix._df, check_exact=True)

    def test_filter_partial_twice(self):
        result_index = pd.MultiIndex.from_tuples([('1', '1:246-354_+', '000'),
                                                 ('1', '1:246-354_+', '0-0'),
                                                 ('1', '1:7-115_+', '00')],
                                                 names=INDEX_COLUMNS)
        result = pd.DataFrame([[80, 75, 100], [10, 0, 0], [100, 100, 100]],
                              columns=['Sample1.BWA.bam', 'Sample2.BWA.bam', 'WT.BWA.bam'],
                              index=result_index,
                              dtype=pd.Int16Dtype())

        count_matrix = CountMatrix(self.counts)
        count_matrix.filter_partial()
        count_matrix.filter_partial()
        pd.testing.assert_frame_equal(result, count_matrix._df, check_exact=True)

    def test_filter_for_minimum_or_maximum_read_count_min(self):
        result_index = pd.MultiIndex.from_tuples([('1', '1:246-354_+', '00.'),
                                                 ('1', '1:246-354_+', '000'),
                                                 ('1', '1:246-354_+', '0-0'),
                                                 ('1', '1:7-115_+', '00')],
                                                 names=INDEX_COLUMNS)
        result = pd.DataFrame([[pd.NA, 25, 0], [pd.NA, 75, 100], [pd.NA, 0, 0], [100, 100, 100]],
                              columns=['Sample1.BWA.bam', 'Sample2.BWA.bam', 'WT.BWA.bam'],
                              index=result_index,
                              dtype=pd.Int16Dtype())
        count_matrix = CountMatrix(self.counts)
        count_matrix.filter_for_minimum_or_maximum_read_count(100, inf)
        pd.testing.assert_frame_equal(result, count_matrix._df, check_exact=True)

    def test_filter_for_minimum_or_maximum_read_count_max(self):
        result_index = pd.MultiIndex.from_tuples([('1', '1:246-354_+', '00.'),
                                                 ('1', '1:246-354_+', '000'),
                                                 ('1', '1:246-354_+', '0-0')],
                                                 names=INDEX_COLUMNS)
        result = pd.DataFrame([[0, pd.NA, pd.NA], [80, pd.NA, pd.NA], [10, pd.NA, pd.NA]],
                              columns=['Sample1.BWA.bam', 'Sample2.BWA.bam', 'WT.BWA.bam'],
                              index=result_index,
                              dtype=pd.Int16Dtype())
        count_matrix = CountMatrix(self.counts)
        count_matrix.filter_for_minimum_or_maximum_read_count(0, 91)
        pd.testing.assert_frame_equal(result, count_matrix._df, check_exact=True)

    def test_filter_for_minimum_or_maximum_read_count_twice(self):
        result_index = pd.MultiIndex.from_tuples([('1', '1:246-354_+', '00.'),
                                                 ('1', '1:246-354_+', '000'),
                                                 ('1', '1:246-354_+', '0-0'),
                                                 ('1', '1:7-115_+', '00')],
                                                 names=INDEX_COLUMNS)
        result = pd.DataFrame([[pd.NA, 25, 0], [pd.NA, 75, 100], [pd.NA, 0, 0], [100, 100, 100]],
                              columns=['Sample1.BWA.bam', 'Sample2.BWA.bam', 'WT.BWA.bam'],
                              index=result_index,
                              dtype=pd.Int16Dtype())
        count_matrix = CountMatrix(self.counts)
        count_matrix.filter_for_minimum_or_maximum_read_count(100, inf)
        count_matrix.filter_for_minimum_or_maximum_read_count(100, inf)
        pd.testing.assert_frame_equal(result, count_matrix._df, check_exact=True)

    def test_filter_for_minimum_or_maximum_read_count_everything(self):
        empty_index = pd.MultiIndex(levels=[[], [], []], codes=[[], [], []], names=INDEX_COLUMNS)
        result = pd.DataFrame(columns=['Sample1.BWA.bam', 'Sample2.BWA.bam',  'WT.BWA.bam'],
                              index=empty_index)
        count_matrix = CountMatrix(self.counts)
        count_matrix.filter_for_minimum_or_maximum_read_count(101, inf)
        pd.testing.assert_frame_equal(result, count_matrix._df,
                                      check_exact=True,
                                      check_index_type=False,
                                      check_dtype=False)

    def test_filter_for_minimum_or_maximum_read_count_nothing(self):
        result_index = pd.MultiIndex.from_tuples([('1', '1:246-354_+', '00.'),
                                                 ('1', '1:246-354_+', '000'),
                                                 ('1', '1:246-354_+', '0-0'),
                                                 ('1', '1:7-115_+', '00')],
                                                 names=INDEX_COLUMNS)
        result = pd.DataFrame([[0, 25, 0], [80, 75, 100], [10, 0, 0], [100, 100, 100]],
                              columns=['Sample1.BWA.bam', 'Sample2.BWA.bam', 'WT.BWA.bam'],
                              index=result_index,
                              dtype=pd.Int16Dtype())
        count_matrix = CountMatrix(self.counts)
        count_matrix.filter_for_minimum_or_maximum_read_count(0, inf)
        pd.testing.assert_frame_equal(result, count_matrix._df, check_exact=True)

    def test_filter_on_minimum_haplotype_frequency(self):
        result_index = pd.MultiIndex.from_tuples([('1', '1:246-354_+', '00.'),
                                                 ('1', '1:246-354_+', '000'),
                                                 ('1', '1:7-115_+', '00')],
                                                 names=INDEX_COLUMNS)
        result = pd.DataFrame([[0, 25, 0], [80, 75, 100], [100, 100, 100]],
                              columns=['Sample1.BWA.bam', 'Sample2.BWA.bam', 'WT.BWA.bam'],
                              index=result_index,
                              dtype=pd.Int16Dtype())
        count_matrix = CountMatrix(self.counts)
        count_matrix.filter_on_minimum_haplotype_frequency(20)
        pd.testing.assert_frame_equal(result, count_matrix._df, check_exact=True)

    def test_filter_on_minimum_haplotype_frequency_with_mask(self):
        result_index = pd.MultiIndex.from_tuples([('1', '1:246-354_+', '00.'),
                                                 ('1', '1:246-354_+', '000'),
                                                 ('1', '1:7-115_+', '00')],
                                                 names=INDEX_COLUMNS)
        result = pd.DataFrame([[pd.NA, 25, pd.NA], [80, 75, 100], [100, 100, 100]],
                              columns=['Sample1.BWA.bam', 'Sample2.BWA.bam', 'WT.BWA.bam'],
                              index=result_index,
                              dtype=pd.Int16Dtype())
        count_matrix = CountMatrix(self.counts)
        count_matrix.filter_on_minimum_haplotype_frequency(20, minimum_read_frequency=2)
        pd.testing.assert_frame_equal(result, count_matrix._df, check_exact=True)

    def test_filter_on_minimum_haplotype_frequency_with_mask_na(self):
        result_index = pd.MultiIndex.from_tuples([('1', '1:246-354_+', '00.'),
                                                 ('1', '1:246-354_+', '000'),
                                                 ('1', '1:7-115_+', '00')],
                                                 names=INDEX_COLUMNS)
        result = pd.DataFrame([[pd.NA, 25, pd.NA], [80, 75, 100], [100, 100, 100]],
                              columns=['Sample1.BWA.bam', 'Sample2.BWA.bam', 'WT.BWA.bam'],
                              index=result_index,
                              dtype=pd.Int16Dtype())
        self.counts.iat[0, 0] = pd.NA
        count_matrix = CountMatrix(self.counts)
        count_matrix.filter_on_minimum_haplotype_frequency(20, minimum_read_frequency=2)
        pd.testing.assert_frame_equal(result, count_matrix._df, check_exact=True)

    def test_filter_on_minimum_haplotype_frequency_filter_everything(self):
        empty_index = pd.MultiIndex(levels=[[], [], []], codes=[[], [], []], names=INDEX_COLUMNS)
        result = pd.DataFrame(columns=['Sample1.BWA.bam', 'Sample2.BWA.bam',  'WT.BWA.bam'],
                              index=empty_index)
        count_matrix = CountMatrix(self.counts)
        count_matrix.filter_on_minimum_haplotype_frequency(100)
        pd.testing.assert_frame_equal(result,
                                      count_matrix._df,
                                      check_exact=True,
                                      check_index_type=False,
                                      check_dtype=False)

    def test_minimum_haplotype_frequency_out_of_bounds(self):
        count_matrix = CountMatrix(self.counts)
        count_matrix.filter_on_minimum_haplotype_frequency(100)
        count_matrix.filter_on_minimum_haplotype_frequency(0)
        with self.assertRaises(ValueError):
            count_matrix.filter_on_minimum_haplotype_frequency(101)
        with self.assertRaises(ValueError):
            count_matrix.filter_on_minimum_haplotype_frequency(-1)

    def test_filter_minumum_read_frequency(self):
        result_index = pd.MultiIndex.from_tuples([('1', '1:246-354_+', '00.'),
                                                 ('1', '1:246-354_+', '000'),
                                                 ('1', '1:246-354_+', '0-0'),
                                                 ('1', '1:7-115_+', '00')],
                                                 names=INDEX_COLUMNS)
        result = pd.DataFrame([[pd.NA, 25, pd.NA],
                               [80, 75, 100],
                               [10, pd.NA, pd.NA],
                               [100, 100, 100]],
                              columns=['Sample1.BWA.bam', 'Sample2.BWA.bam', 'WT.BWA.bam'],
                              index=result_index,
                              dtype=pd.Int16Dtype())
        count_matrix = CountMatrix(self.counts)
        count_matrix.filter_on_minimum_haplotype_frequency(2, minimum_read_frequency=1)
        pd.testing.assert_frame_equal(result, count_matrix._df, check_exact=True)

    def test_filter_minumum_read_frequency_higher_than_minimum_haplotype_frequency(self):
        result_index = pd.MultiIndex.from_tuples([('1', '1:246-354_+', '00.'),
                                                 ('1', '1:246-354_+', '000'),
                                                 ('1', '1:246-354_+', '0-0'),
                                                 ('1', '1:7-115_+', '00')],
                                                 names=INDEX_COLUMNS)
        result = pd.DataFrame([[0, 25, 0], [80, 75, 100], [10, 0, 0], [100, 100, 100]],
                              columns=['Sample1.BWA.bam', 'Sample2.BWA.bam', 'WT.BWA.bam'],
                              index=result_index,
                              dtype=pd.Int16Dtype())
        count_matrix = CountMatrix(self.counts)
        with self.assertLogs("Haplotype", level='WARNING') as cm:
            count_matrix.filter_on_minimum_haplotype_frequency(0, minimum_read_frequency=11)
            pd.testing.assert_frame_equal(result, count_matrix._df, check_exact=True)
        self.assertEqual(cm.output, [('WARNING:Haplotype:The minimum read frequency threshold'
                                      ' is larger than the minimum haplotype frequency. A '
                                      'haplotype is only to be excluded if for none of the '
                                      'samples the frequency for that haplotype is above the '
                                      'minimum haplotype frequency. Setting the minimum read '
                                      'frequency to the minimum haplotype frequency.')])

    def test_filter_minumum_read_frequency_remove_row(self):
        result_index = pd.MultiIndex.from_tuples([('1', '1:246-354_+', '000'),
                                                 ('1', '1:7-115_+', '00')],
                                                 names=INDEX_COLUMNS)
        result = pd.DataFrame([[80, 75, 100], [100, 100, 100]],
                              columns=['Sample1.BWA.bam', 'Sample2.BWA.bam', 'WT.BWA.bam'],
                              index=result_index,
                              dtype=pd.Int16Dtype())
        count_matrix = CountMatrix(self.counts)
        count_matrix.filter_on_minimum_haplotype_frequency(26, minimum_read_frequency=25)
        pd.testing.assert_frame_equal(result, count_matrix._df, check_exact=True)

    def test_filter_minumum_read_frequency_bounds(self):
        count_matrix = CountMatrix(self.counts)
        count_matrix.filter_on_minimum_haplotype_frequency(2, minimum_read_frequency=0)
        with self.assertRaises(ValueError):
            count_matrix.filter_on_minimum_haplotype_frequency(2, minimum_read_frequency=-1)
        with self.assertRaises(ValueError):
            count_matrix.filter_on_minimum_haplotype_frequency(2, minimum_read_frequency=101)
        count_matrix.filter_on_minimum_haplotype_frequency(100, minimum_read_frequency=100)

    def test_calculate_frequencies(self):
        result_index = pd.MultiIndex.from_tuples([('1', '1:246-354_+', '00.'),
                                                 ('1', '1:246-354_+', '000'),
                                                 ('1', '1:246-354_+', '0-0'),
                                                 ('1', '1:7-115_+', '00')],
                                                 names=INDEX_COLUMNS)
        result = pd.DataFrame([[0.00, 25.00, 0.00],
                               [88.89, 75.00, 100.00],
                               [11.11, 0.00, 0.00],
                               [100.00, 100.00, 100.00]],
                              columns=['Sample1.BWA.bam', 'Sample2.BWA.bam', 'WT.BWA.bam'],
                              index=result_index,
                              dtype=np.float16)
        count_matrix = CountMatrix(self.counts)
        frequencies = count_matrix.calculate_frequencies()
        pd.testing.assert_frame_equal(result, frequencies._df, check_exact=True)

    def test_calculate_frequencies_na(self):
        result_index = pd.MultiIndex.from_tuples([('1', '1:246-354_+', '00.'),
                                                 ('1', '1:246-354_+', '000'),
                                                 ('1', '1:246-354_+', '0-0'),
                                                 ('1', '1:7-115_+', '00')],
                                                 names=INDEX_COLUMNS)
        result = pd.DataFrame([[np.NaN, 25.00, 0.00],
                               [88.89, 75.00, 100.00],
                               [11.11, 0.00, 0.00],
                               [100.00, 100.00, 100.00]],
                              columns=['Sample1.BWA.bam', 'Sample2.BWA.bam', 'WT.BWA.bam'],
                              index=result_index,
                              dtype=np.float16)

        count_matrix = CountMatrix(self.counts)
        # Introduce a NA value
        # This should not change the dtype
        count_matrix._df.iat[0, 0] = pd.NA
        frequencies = count_matrix.calculate_frequencies()
        pd.testing.assert_frame_equal(result, frequencies._df, check_exact=True)

    def test_calculate_frequencies_column_sum_zero(self):
        result_index = pd.MultiIndex.from_tuples([('1', '1:246-354_+', '00.'),
                                                 ('1', '1:246-354_+', '000'),
                                                 ('1', '1:246-354_+', '0-0'),
                                                 ('1', '1:7-115_+', '00')],
                                                 names=INDEX_COLUMNS)
        result = pd.DataFrame([[0.00, 25.00, 0.00, np.NaN],
                               [88.89, 75.00, 100.00, np.NaN],
                               [11.11, 0.00, 0.00, np.NaN],
                               [100.00, 100.00, 100.00, np.NaN]],
                              columns=['Sample1.BWA.bam', 'Sample2.BWA.bam', 'WT.BWA.bam', 'Zeros'],
                              index=result_index,
                              dtype=np.float16)
        self.counts['Zeros'] = [0, 0, 0, 0]
        count_matrix = CountMatrix(self.counts)
        frequencies = count_matrix.calculate_frequencies()
        pd.testing.assert_frame_equal(result, frequencies._df, check_exact=True)

    def test_calculate_frequencies_column_sum_zero_mixed_na(self):
        self.counts = self.counts.astype("object")
        self.counts.iloc[:, 1] = [pd.NA, pd.NA, pd.NA, 1.0]
        message = r"The count matrix must have an integer dtype for all columns"
        with self.assertRaisesRegex(ValueError, expected_regex=message):
            CountMatrix(self.counts)

    def test_write_to_csv(self):
        result = dedent(
            """
            Reference	Locus	Haplotypes	Sample1.BWA.bam	Sample2.BWA.bam	WT.BWA.bam
            1	1:246-354_+	00.	0	25	0
            1	1:246-354_+	000	80	75	100
            1	1:246-354_+	0-0	10	0	0
            1	1:7-115_+	00	100	100	100
            """).strip()
        outfile = StringIO()
        count_matrix = CountMatrix(self.counts)
        count_matrix.to_csv(outfile)
        outfile.seek(0)
        content = outfile.read()
        self.assertMultiLineEqual(content.strip(), result)


class TestFrequencyMatrix(unittest.TestCase):
    def setUp(self):
        frequency_index = pd.MultiIndex.from_tuples([('1', '1:246-354_+', '00.'),
                                                     ('1', '1:246-354_+', '000'),
                                                     ('1', '1:246-354_+', '0-0'),
                                                     ('1', '1:7-115_+', '00')],
                                                    names=INDEX_COLUMNS)
        self.frequencies = pd.DataFrame([[np.NaN, 25.00, 0.00],
                                         [88.89, 75.00, 100.00],
                                         [11.11, 0.00, 0.00],
                                         [100.00, 100.00, 100.00]],
                                        columns=['Sample1.BWA.bam',
                                                 'Sample2.BWA.bam',
                                                 'WT.BWA.bam'],
                                        index=frequency_index,
                                        dtype=np.float16)

    def test_init(self):
        FrequencyMatrix(self.frequencies)

    def test_filter_for_number_of_distinct_haplotypes_min(self):
        result_index = pd.MultiIndex.from_tuples([('1', '1:246-354_+', '00.'),
                                                 ('1', '1:246-354_+', '000'),
                                                 ('1', '1:246-354_+', '0-0')],
                                                 names=INDEX_COLUMNS)
        result = pd.DataFrame([[np.NaN, 25.00, 0.00],
                               [88.89, 75.00, 100.00],
                               [11.11, 0.00, 0.00]],
                              columns=['Sample1.BWA.bam', 'Sample2.BWA.bam', 'WT.BWA.bam'],
                              index=result_index,
                              dtype=np.float16)
        frequency_matrix = FrequencyMatrix(self.frequencies)
        frequency_matrix.filter_for_number_of_distinct_haplotypes(2, 1500)
        pd.testing.assert_frame_equal(frequency_matrix._df, result)

    def test_filter_for_number_of_distinct_haplotypes_max(self):
        result_index = pd.MultiIndex.from_tuples([('1', '1:7-115_+', '00')],
                                                 names=INDEX_COLUMNS)
        result = pd.DataFrame([[100.00, 100.00, 100.00]],
                              columns=['Sample1.BWA.bam', 'Sample2.BWA.bam', 'WT.BWA.bam'],
                              index=result_index,
                              dtype=np.float16)
        frequency_matrix = FrequencyMatrix(self.frequencies)
        frequency_matrix.filter_for_number_of_distinct_haplotypes(0, 1)
        pd.testing.assert_frame_equal(frequency_matrix._df, result)

    def test_filter_for_number_of_distinct_haplotypes_inclusive_bounds(self):
        result_index = pd.MultiIndex.from_tuples([('1', '1:246-354_+', '00.'),
                                                  ('1', '1:246-354_+', '000'),
                                                  ('1', '1:246-354_+', '0-0'),
                                                  ('1', '1:7-115_+', '00')],
                                                 names=INDEX_COLUMNS)
        result = pd.DataFrame([[np.NaN, 25.00, 0.00],
                               [88.89, 75.00, 100.00],
                               [11.11, 0.00, 0.00],
                               [100.00, 100.00, 100.00]],
                              columns=['Sample1.BWA.bam', 'Sample2.BWA.bam', 'WT.BWA.bam'],
                              index=result_index,
                              dtype=np.float16)
        frequency_matrix = FrequencyMatrix(self.frequencies)
        frequency_matrix.filter_for_number_of_distinct_haplotypes(1, 3)
        pd.testing.assert_frame_equal(frequency_matrix._df, result)
        frequency_matrix.filter_for_number_of_distinct_haplotypes(2, 3)
        result_index = pd.MultiIndex.from_tuples([('1', '1:246-354_+', '00.'),
                                                  ('1', '1:246-354_+', '000'),
                                                  ('1', '1:246-354_+', '0-0')],
                                                 names=INDEX_COLUMNS)
        result = pd.DataFrame([[np.NaN, 25.00, 0.00],
                               [88.89, 75.00, 100.00],
                               [11.11, 0.00, 0.00]],
                              columns=['Sample1.BWA.bam', 'Sample2.BWA.bam', 'WT.BWA.bam'],
                              index=result_index,
                              dtype=np.float16)
        pd.testing.assert_frame_equal(frequency_matrix._df, result)

    def test_filter_for_number_of_distinct_haplotypes_args_out_of_bound(self):
        frequency_matrix = FrequencyMatrix(self.frequencies)
        with self.assertRaises(ValueError):
            frequency_matrix.filter_for_number_of_distinct_haplotypes(-1, 1500)
        with self.assertRaises(ValueError):
            frequency_matrix.filter_for_number_of_distinct_haplotypes(0, -1)

    def test_calculate_dosage_threshold_intervals_overlap(self):
        frequency_matrix = FrequencyMatrix(self.frequencies)
        with self.assertRaises(ValueError):
            frequency_matrix.calculate_discrete_calls('dosage', [20, 10, 90, 90])

    def test_calculate_dosage_diploid(self):
        result_index = pd.MultiIndex.from_tuples([('1', '1:246-354_+', '00.'),
                                                 ('1', '1:246-354_+', '000'),
                                                 ('1', '1:246-354_+', '0-0'),
                                                 ('1', '1:7-115_+', '00')],
                                                 names=INDEX_COLUMNS)
        result = pd.DataFrame([[pd.NA, 1, 0],
                               [1, 1, 2],
                               [1, 0, 0],
                               [2, 2, 2]],
                              columns=['Sample1.BWA.bam', 'Sample2.BWA.bam', 'WT.BWA.bam'],
                              index=result_index,
                              dtype=pd.Int8Dtype())
        frequency_matrix = FrequencyMatrix(self.frequencies)
        dosages = frequency_matrix.calculate_discrete_calls('dosage', [10, 10, 90, 90])
        pd.testing.assert_frame_equal(result, dosages._df)

    def test_calculate_dosage_tetraploid(self):
        result_index = pd.MultiIndex.from_tuples([('1', '1:246-354_+', '00.'),
                                                 ('1', '1:246-354_+', '000'),
                                                 ('1', '1:246-354_+', '0-0'),
                                                 ('1', '1:7-115_+', '00')],
                                                 names=INDEX_COLUMNS)
        result = pd.DataFrame([[pd.NA, 1, 0],
                               [4, 3, 4],
                               [0, 0, 0],
                               [4, 4, 4]],
                              columns=['Sample1.BWA.bam', 'Sample2.BWA.bam', 'WT.BWA.bam'],
                              index=result_index,
                              dtype=pd.Int8Dtype())
        frequency_matrix = FrequencyMatrix(self.frequencies)
        dosages = frequency_matrix.calculate_discrete_calls(
            'dosage',
            [12.5, 12.5, 37.5, 37.5, 62.5, 62.5, 87.5, 87.5]
        )
        pd.testing.assert_frame_equal(result, dosages._df)

    def test_calculate_dosage_dominant_tetraploid(self):
        result_index = pd.MultiIndex.from_tuples([('1', '1:246-354_+', '00.'),
                                                 ('1', '1:246-354_+', '000'),
                                                 ('1', '1:246-354_+', '0-0'),
                                                 ('1', '1:7-115_+', '00')],
                                                 names=INDEX_COLUMNS)
        result = pd.DataFrame([[pd.NA, 1, 0],
                               [1, 1, 1],
                               [1, 0, 0],
                               [1, 1, 1]],
                              columns=['Sample1.BWA.bam', 'Sample2.BWA.bam', 'WT.BWA.bam'],
                              index=result_index,
                              dtype=pd.Int8Dtype())
        frequency_matrix = FrequencyMatrix(self.frequencies)
        dosages = frequency_matrix.calculate_discrete_calls('dominant', [10])
        pd.testing.assert_frame_equal(result, dosages._df)

    def test_calculate_dosage_dominant_tetraploid_wrong_number_of_thresholds(self):
        frequency_matrix = FrequencyMatrix(self.frequencies)
        with self.assertRaises(ValueError):
            frequency_matrix.calculate_discrete_calls('dominant', [12.5, 15])

    def test_calculate_dosage_dominant_tetraploid_none_in_thresholds(self):
        frequency_matrix = FrequencyMatrix(self.frequencies)
        with self.assertRaises(ValueError):
            frequency_matrix.calculate_discrete_calls('dosage', [None])

    def test_calculate_dosage_locus_all_na(self):
        frequency_index = pd.MultiIndex.from_tuples([('1', '1:246-354_+', '00.'),
                                                     ('1', '1:246-354_+', '000'),
                                                     ('1', '1:246-354_+', '0-0'),
                                                     ('1', '1:7-115_+', '00')],
                                                    names=INDEX_COLUMNS)
        frequencies = pd.DataFrame([[np.NaN, 5.00, 5.00],
                                    [5.00, 5.00, 5.00],
                                    [5.00, 5.00, 5.00],
                                    [np.NaN, 100.00, 100.00]],
                                   columns=['Sample1.BWA.bam', 'Sample2.BWA.bam', 'WT.BWA.bam'],
                                   index=frequency_index,
                                   dtype=np.float16)
        result_index = pd.MultiIndex.from_tuples([('1', '1:7-115_+', '00')],
                                                 names=INDEX_COLUMNS)
        result = pd.DataFrame([[pd.NA, 4, 4]],
                              columns=['Sample1.BWA.bam', 'Sample2.BWA.bam', 'WT.BWA.bam'],
                              index=result_index,
                              dtype=pd.Int8Dtype())
        frequency_matrix = FrequencyMatrix(frequencies)
        dosages = frequency_matrix.calculate_discrete_calls(
            'dosage',
            [12.5, 12.5, 37.5, 37.5, 62.5, 62.5, 87.5, 87.5]
        )
        pd.testing.assert_frame_equal(result, dosages._df)

    def test_write_to_csv(self):
        result = dedent(
            """
            Reference	Locus	Haplotypes	Sample1.BWA.bam	Sample2.BWA.bam	WT.BWA.bam
            1	1:246-354_+	00.	NaN	25.00	0.00
            1	1:246-354_+	000	88.88	75.00	100.00
            1	1:246-354_+	0-0	11.11	0.00	0.00
            1	1:7-115_+	00	100.00	100.00	100.00
            """).strip()
        outfile = StringIO()
        frequency_matrix = FrequencyMatrix(self.frequencies)
        frequency_matrix.to_csv(outfile, float_format='%.2f')
        outfile.seek(0)
        content = outfile.read()
        self.assertMultiLineEqual(content.strip(), result)

    @patch('smap.haplotype.barplot')
    def test_plot_haplotype_counts_empty(self, mocked_barplot):
        empty_index = pd.MultiIndex.from_tuples([], names=INDEX_COLUMNS)
        empty_df = pd.DataFrame([], index=empty_index)
        fm = FrequencyMatrix(empty_df)
        fm.plot_haplotype_counts('test', 'png')
        mocked_barplot.assert_called_once_with(range(0, 11),
                                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                               'test',
                                               'Haplotype diversity distribution '
                                               'across the sample set',
                                               'Number of distinct haplotypes per locus',
                                               'Number of loci',
                                               'darkslategray',
                                               'png',
                                               xaxisticks=10)


class TestDosageMatrix(unittest.TestCase):
    def setUp(self):
        dosage_index = pd.MultiIndex.from_tuples([('1', '1:246-354_+', '00.'),
                                                  ('1', '1:246-354_+', '000'),
                                                  ('1', '1:246-354_+', '0-0'),
                                                  ('1', '1:7-115_+', '00')],
                                                 names=INDEX_COLUMNS)
        self.dosages = pd.DataFrame([[1, 1, 3],
                                     [1, 1, 2],
                                     [1, 0, 0],
                                     [2, 2, 2]],
                                    columns=['Sample1.BWA.bam', 'Sample2.BWA.bam', 'WT.BWA.bam'],
                                    index=dosage_index,
                                    dtype=pd.Int8Dtype())

    def test_init(self):
        DosageMatrix(self.dosages)

    def test_filter_for_number_of_distinct_haplotypes_min(self):
        result_index = pd.MultiIndex.from_tuples([('1', '1:246-354_+', '00.'),
                                                  ('1', '1:246-354_+', '000'),
                                                  ('1', '1:246-354_+', '0-0')],
                                                 names=INDEX_COLUMNS)
        result = pd.DataFrame([[1, 1, 3],
                               [1, 1, 2],
                               [1, 0, 0]],
                              columns=['Sample1.BWA.bam', 'Sample2.BWA.bam', 'WT.BWA.bam'],
                              index=result_index,
                              dtype=pd.Int8Dtype())
        dosage_matrix = DosageMatrix(self.dosages)
        dosage_matrix.filter_for_number_of_distinct_haplotypes(2, 1500)
        pd.testing.assert_frame_equal(dosage_matrix._df, result)

    def test_filter_for_number_of_distinct_haplotypes_max(self):
        result_index = pd.MultiIndex.from_tuples([('1', '1:7-115_+', '00')],
                                                 names=INDEX_COLUMNS)
        result = pd.DataFrame([[2, 2, 2]],
                              columns=['Sample1.BWA.bam', 'Sample2.BWA.bam', 'WT.BWA.bam'],
                              index=result_index,
                              dtype=pd.Int8Dtype())
        dosage_matrix = DosageMatrix(self.dosages)
        dosage_matrix.filter_for_number_of_distinct_haplotypes(0, 1)
        pd.testing.assert_frame_equal(dosage_matrix._df, result)

    def test_filter_for_number_of_distinct_haplotypes_inclusive_bounds(self):
        result_index = pd.MultiIndex.from_tuples([('1', '1:246-354_+', '00.'),
                                                  ('1', '1:246-354_+', '000'),
                                                  ('1', '1:246-354_+', '0-0'),
                                                  ('1', '1:7-115_+', '00')],
                                                 names=INDEX_COLUMNS)
        result = pd.DataFrame([[1, 1, 3],
                               [1, 1, 2],
                               [1, 0, 0],
                               [2, 2, 2]],
                              columns=['Sample1.BWA.bam', 'Sample2.BWA.bam', 'WT.BWA.bam'],
                              index=result_index,
                              dtype=pd.Int8Dtype())
        dosage_matrix = DosageMatrix(self.dosages)
        dosage_matrix.filter_for_number_of_distinct_haplotypes(1, 3)
        pd.testing.assert_frame_equal(dosage_matrix._df, result)
        dosage_matrix.filter_for_number_of_distinct_haplotypes(2, 3)
        result_index = pd.MultiIndex.from_tuples([('1', '1:246-354_+', '00.'),
                                                  ('1', '1:246-354_+', '000'),
                                                  ('1', '1:246-354_+', '0-0')],
                                                 names=INDEX_COLUMNS)
        result = pd.DataFrame([[1, 1, 3],
                               [1, 1, 2],
                               [1, 0, 0]],
                              columns=['Sample1.BWA.bam', 'Sample2.BWA.bam', 'WT.BWA.bam'],
                              index=result_index,
                              dtype=pd.Int8Dtype())
        pd.testing.assert_frame_equal(dosage_matrix._df, result)

    def test_filter_for_number_of_distinct_haplotypes_args_out_of_bound(self):
        frequency_matrix = DosageMatrix(self.dosages)
        with self.assertRaises(ValueError):
            frequency_matrix.filter_for_number_of_distinct_haplotypes(-1, 1500)
        with self.assertRaises(ValueError):
            frequency_matrix.filter_for_number_of_distinct_haplotypes(0, -1)

    def test_filter_distinct_haplotyped_per_sample_filter_diploid(self):
        result_index = pd.MultiIndex.from_tuples([('1', '1:246-354_+', '00.'),
                                                  ('1', '1:246-354_+', '000'),
                                                  ('1', '1:7-115_+', '00')],
                                                 names=INDEX_COLUMNS)
        result = pd.DataFrame([[pd.NA, 1, pd.NA],
                               [pd.NA, 1, pd.NA],
                               [2, 2, 2]],
                              columns=['Sample1.BWA.bam', 'Sample2.BWA.bam', 'WT.BWA.bam'],
                              index=result_index,
                              dtype=pd.Int8Dtype())
        dosage_matrix = DosageMatrix(self.dosages)
        dosage_matrix.filter_distinct_haplotyped_per_sample(2)
        pd.testing.assert_frame_equal(result, dosage_matrix._df)

    def test_filter_distinct_haplotyped_per_sample_filter_tetraploid(self):
        result_index = pd.MultiIndex.from_tuples([('1', '1:246-354_+', '00.'),
                                                  ('1', '1:246-354_+', '000'),
                                                  ('1', '1:246-354_+', '0-0')],
                                                 names=INDEX_COLUMNS)
        result = pd.DataFrame([[pd.NA, 1, pd.NA],
                               [pd.NA, 1, pd.NA],
                               [pd.NA, 2, pd.NA]],
                              columns=['Sample1.BWA.bam', 'Sample2.BWA.bam', 'WT.BWA.bam'],
                              index=result_index,
                              dtype=pd.Int8Dtype())
        self.dosages.iat[2, 1] = 2
        dosage_matrix = DosageMatrix(self.dosages)
        dosage_matrix.filter_distinct_haplotyped_per_sample(4)
        pd.testing.assert_frame_equal(result, dosage_matrix._df)

    def test_write_to_csv(self):
        result = dedent(
            """
            Reference	Locus	Haplotypes	Sample1.BWA.bam	Sample2.BWA.bam	WT.BWA.bam
            1	1:246-354_+	00.	1	1	3
            1	1:246-354_+	000	1	1	2
            1	1:246-354_+	0-0	1	0	0
            1	1:7-115_+	00	2	2	2
            """).strip()
        outfile = StringIO()
        count_matrix = DosageMatrix(self.dosages)
        count_matrix.to_csv(outfile)
        outfile.seek(0)
        content = outfile.read()
        self.assertMultiLineEqual(content.strip(), result)

    def test_write_population_frequencies(self):
        result = dedent(
            """
            Reference	Locus	Haplotypes	AF	Total_obs
            1	1:246-354_+	00.	0.5	10.0
            1	1:246-354_+	000	0.4	10.0
            1	1:246-354_+	0-0	0.1	10.0
            1	1:7-115_+	00	1.0	6.0
            """).strip()
        outfile = StringIO()
        count_matrix = DosageMatrix(self.dosages)
        count_matrix.write_population_frequencies(outfile)
        outfile.seek(0)
        content = outfile.read()
        self.assertMultiLineEqual(content.strip(), result)

    def test_write_total_df(self):
        result = dedent(
            """
            Reference	Locus	Sample1.BWA.bam	Sample2.BWA.bam	WT.BWA.bam
            1	1:246-354_+	3	2	5
            1	1:7-115_+	2	2	2
            """).strip()
        outfile = StringIO()
        count_matrix = DosageMatrix(self.dosages)
        count_matrix.write_total_calls(outfile)
        outfile.seek(0)
        content = outfile.read()
        self.assertMultiLineEqual(content.strip(), result)

    def test_get_correct_loci(self):
        dosage_matrix = DosageMatrix(self.dosages)
        orig_dosage_matrix = deepcopy(dosage_matrix)
        dosage_matrix.filter_distinct_haplotyped_per_sample(2)
        correct_loci = orig_dosage_matrix.get_correct_loci(dosage_matrix, 50)
        self.assertEqual(correct_loci, [('1', '7', '115')])

    def test_calculate_sample_correctness(self):
        dosage_matrix = DosageMatrix(self.dosages)
        filtered_df_index = pd.MultiIndex.from_tuples([("1", "1:246-354_+", "00."),
                                                       ("1", "1:246-354_+", "000"),
                                                       ("1", "1:7-115_+", "00")],
                                                      names=INDEX_COLUMNS)
        filtered_df = DosageMatrix(pd.DataFrame({"Sample1.BWA.bam": [pd.NA, pd.NA, 2],
                                                 "Sample2.BWA.bam": [1, 1, 2],
                                                 "WT.BWA.bam": [pd.NA, pd.NA, 2]},
                                                index=filtered_df_index))
        correctness = dosage_matrix._calculate_sample_correctness(filtered_df)
        expected_index = pd.Index(["Sample1.BWA.bam", "Sample2.BWA.bam", "WT.BWA.bam"],
                                  name="Sample")
        expected_correctness = pd.Series([50.0, 100.0, 50.0],
                                         name="Sample correctness score",
                                         index=expected_index,
                                         dtype="float64")
        pd.testing.assert_series_equal(expected_correctness, correctness)

    def test_calculate_sample_correctness_all_ba(self):
        dosage_matrix = DosageMatrix(self.dosages)
        filtered_df_index = pd.MultiIndex.from_tuples([("1", "1:246-354_+", "00."),
                                                       ("1", "1:246-354_+", "000"),
                                                       ("1", "1:7-115_+", "00")],
                                                      names=INDEX_COLUMNS)
        filtered_df = DosageMatrix(pd.DataFrame({"Sample1.BWA.bam": [pd.NA, pd.NA, pd.NA],
                                                 "Sample2.BWA.bam": [1, 1, 2],
                                                 "WT.BWA.bam": [pd.NA, pd.NA, 2]},
                                                index=filtered_df_index))
        correctness = dosage_matrix._calculate_sample_correctness(filtered_df)
        expected_index = pd.Index(["Sample1.BWA.bam", "Sample2.BWA.bam", "WT.BWA.bam"],
                                  name="Sample")
        expected_correctness = pd.Series([0, 100.0, 50.0],
                                         name="Sample correctness score",
                                         index=expected_index,
                                         dtype="float64")
        pd.testing.assert_series_equal(expected_correctness, correctness)

    def test_create_cervus_table(self):
        dosage_matrix = DosageMatrix(self.dosages)
        dosage_matrix.filter_distinct_haplotyped_per_sample(2)
        cervus_table = dosage_matrix.to_cervus()
        res_index = pd.Index(['Sample1.BWA.bam',
                              'Sample2.BWA.bam',
                              'WT.BWA.bam'],
                             name="Sample")
        exp = pd.DataFrame([['*', '*', 'a', 'a'],
                            ['a', 'b', 'a', 'a'],
                            ['*', '*', 'a', 'a']],
                           index=res_index,
                           columns=['1:246-354_+.1', '1:246-354_+.2',
                                    '1:7-115_+.1', '1:7-115_+.2'])
        pd.testing.assert_frame_equal(cervus_table._df, exp)

    def test_crete_cervus_table_unfiltered_df(self):
        dosage_matrix = DosageMatrix(self.dosages)
        message = ('Cervus output can only be created from a dosage table that '
                   'has been filtered to remove dosage calls that do not conform to '
                   'the expected sample ploidy.')
        with self.assertRaises(ValueError, msg=message):
            dosage_matrix.to_cervus()

    @patch('smap.haplotype.barplot')
    def test_plot_haplotype_counts_empty(self, mocked_barplot):
        empty_index = pd.MultiIndex.from_tuples([], names=INDEX_COLUMNS)
        empty_df = pd.DataFrame([], index=empty_index)
        fm = DosageMatrix(empty_df)
        fm.plot_haplotype_counts('test', 'png')
        mocked_barplot.assert_called_once_with(range(0, 11),
                                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                               'test',
                                               'Haplotype diversity distribution '
                                               'across the sample set',
                                               'Number of distinct haplotypes per locus',
                                               'Number of loci',
                                               'darkslategray',
                                               'png',
                                               xaxisticks=10)


class TestCervus(unittest.TestCase):
    def setUp(self) -> None:
        table_indx = pd.Index(['Sample1.BWA.bam',
                               'Sample2.BWA.bam',
                               'WT.BWA.bam'],
                              name="Sample")
        table = pd.DataFrame([['*', '*', 'a', 'a'],
                              ['a', 'b', 'a', 'a'],
                              ['*', '*', 'a', 'a']],
                             index=table_indx,
                             columns=['1:246-354_+.1', '1:246-354_+.2',
                                      '1:7-115_+.1', '1:7-115_+.2'])
        self.cervus_table = CervusTable(table)

    def test_to_csv(self):
        exp = dedent(
            """
            Sample	1:246-354_+.1	1:246-354_+.2	1:7-115_+.1	1:7-115_+.2
            Sample1.BWA.bam	*	*	a	a
            Sample2.BWA.bam	a	b	a	a
            WT.BWA.bam	*	*	a	a
            """).strip()
        to_write = StringIO()
        self.cervus_table.to_csv(to_write)
        res = to_write.getvalue()
        self.assertMultiLineEqual(exp, res.strip())


class TestFilterBed(unittest.TestCase):
    def setUp(self):
        self.tempdir = TemporaryDirectory()
        self.merged_clusters_bed = Path(self.tempdir.name) / "final_stack_positions.bed"
        with self.merged_clusters_bed.open(mode='w') as test_bed:
            test_bed.write(merged_clusters())

    def tearDown(self):
        self.tempdir.cleanup()

    def test_filter_bed(self):
        result = dedent(
            """
            1	6	115	1:7-115_+	100	+	7,115	3	2	Set1
            """).strip()
        outfile = Path(self.tempdir.name) / 'output_bed.bed'
        with self.merged_clusters_bed.open(mode='r') as test_bed:
            filter_bed_loci(test_bed, outfile, [('1', '7', '115')])
        with outfile.open('r') as open_outfile:
            filter_result = open_outfile.read()
        self.assertMultiLineEqual(filter_result.strip(), result)
