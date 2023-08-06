import sys
import unittest
from data import wt_bam, sample1_bam, sample2_bam
from tempfile import TemporaryDirectory
from smap.delineate import Stacks, Clusters, MergedClusters, main
from pathlib import Path
from textwrap import dedent
from io import StringIO


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


# TODO: separate reads, mapping quality, plotting and generating clusters
class TestStacks(unittest.TestCase):
    def setUp(self):
        self.tempdir = TemporaryDirectory()
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

    def test_invalid_bam(self):
        with self.assertRaises(FileNotFoundError):
            Stacks('foo', False, 1)

    def test_empty_bam(self):
        empty = self.mapping_directory / "empty.bam"
        empty.touch()
        error_message = (f"Could not read records from file {empty}. "
                         "It could be either malformatted or empty.")
        with self.assertRaisesRegex(ValueError, error_message):
            Stacks(empty, False, 20)

    def test_plot_cigar_operators_empty(self):
        empty = Stacks(self.wt, False, 255)
        assert not empty._stacks
        empty.plot_cigar_operators('empty', 'png')

    def test_plot_depth_empty(self):
        empty = Stacks(self.wt, False, 255)
        assert not empty._stacks
        empty.plot_depth('empty', 'png')

    def test_plot_read_length_depth_correlation_empty(self):
        empty = Stacks(self.wt, False, 255)
        assert not empty._stacks
        empty.plot_read_length_depth_correlation('empty', 'png')

    def test_plot_length(self):
        empty = Stacks(self.wt, False, 255)
        assert not empty._stacks
        empty.plot_length('empty', 'png')

    def test_write_to_bed_empty(self):
        stacks = Stacks(self.wt, False, 255)
        bed_buffer = StringIO()
        stacks.write_to_bed(bed_buffer, 'Test')
        bed_written_contents = bed_buffer.getvalue()
        self.assertMultiLineEqual(bed_written_contents.strip(), "")

    def test_invalid_mapping_quality(self):
        with self.assertRaises(ValueError):
            Stacks(self.wt, False, 256)
        with self.assertRaises(ValueError):
            Stacks(self.wt, False, -1)

    def test_invalid_read_type(self):
        with self.assertRaises(AssertionError):
            Stacks(self.wt, 'foo', 1)

    def test_init_separate_reads(self):
        Stacks(self.wt, True, 1)

    def test_init_merged_reads(self):
        Stacks(self.wt, False, 1)

    def test_generate_from_wt_bam(self):
        bed_contents = dedent(
            """
            1	6	115	1:7-115_+	100	+	Test
            1	245	354	1:246-354_+	100	+	Test
            """).strip()
        stacks = Stacks(self.wt, False, 1)
        self.assertEqual(stacks.number_of_parsed_reads, 200)
        bed_buffer = StringIO()
        stacks.write_to_bed(bed_buffer, 'Test')
        bed_written_contents = bed_buffer.getvalue()
        self.assertMultiLineEqual(bed_written_contents.strip(), bed_contents)

    def test_generate_from_heteroz_bam(self):
        bed_contents = dedent(
            """
            1	6	115	1:7-115_+	100	+	Test
            1	245	354	1:246-354_+	80	+	Test
            """).strip()
        stacks = Stacks(self.sample1, False, 1)
        self.assertEqual(stacks.number_of_parsed_reads, 180)
        bed_buffer = StringIO()
        stacks.write_to_bed(bed_buffer, 'Test')
        bed_written_contents = bed_buffer.getvalue()
        self.assertMultiLineEqual(bed_written_contents.strip(), bed_contents)

    def test_generate_from_homoz_bam(self):
        bed_contents = dedent(
            """
            1	6	115	1:7-115_+	100	+	Test
            1	245	354	1:246-354_+	75	+	Test
            1	245	344	1:246-344_+	25	+	Test
            """).strip()
        stacks = Stacks(self.sample2, False, 1)
        self.assertEqual(stacks.number_of_parsed_reads, 200)
        bed_buffer = StringIO()
        stacks.write_to_bed(bed_buffer, 'Test')
        bed_written_contents = bed_buffer.getvalue()
        self.assertMultiLineEqual(bed_written_contents.strip(), bed_contents)

    def test_minimum_stack_depth_filter(self):
        bed_contents = dedent(
            """
            1	6	115	1:7-115_+	100	+	Test
            1	245	354	1:246-354_+	75	+	Test
            """).strip()
        stacks = Stacks(self.sample2, False, 1)
        stacks.depth_filter(30, sys.maxsize)
        bed_buffer = StringIO()
        stacks.write_to_bed(bed_buffer, 'Test')
        bed_written_contents = bed_buffer.getvalue()
        self.assertMultiLineEqual(bed_written_contents.strip(), bed_contents)

    def test_generate_with_maximum_stack_depth_filter(self):
        bed_contents = dedent(
            """
            1	245	354	1:246-354_+	75	+	Test
            1	245	344	1:246-344_+	25	+	Test
            """).strip()
        stacks = Stacks(self.sample2, False, 1)
        stacks.depth_filter(0, 80)
        bed_buffer = StringIO()
        stacks.write_to_bed(bed_buffer, 'Test')
        bed_written_contents = bed_buffer.getvalue()
        self.assertMultiLineEqual(bed_written_contents.strip(), bed_contents)

    def test_merge_sample2(self):
        result = {
            0: {'chr': 1, 'cigar_collapse': ['51M5I58M'], 'end': 115,
                'end_collapse': [115], 'stack_depth_collapse': [100],
                'stack_number_count': 1, 'start': 6, 'start_collapse': [6],
                'strand': '+'},
            1: {'chr': 1, 'cigar_collapse': ['109M', '99M'], 'end': 354,
                'end_collapse': [354, 344], 'stack_depth_collapse': [75, 25],
                'stack_number_count': 2, 'start': 245, 'start_collapse': [245, 245],
                'strand': '+'}}

        stacks = Stacks(self.sample2, False, 1)
        clusters = stacks.merge()
        self.assertDictEqual(clusters._merged_stacks, result)


class TestClusters(unittest.TestCase):
    def setUp(self):
        self._wt_cluster = Clusters({
            0: {'chr': 1, 'cigar_collapse': ['109M'], 'end': 115,
                'end_collapse': [115], 'stack_depth_collapse': [100],
                'stack_number_count': 1, 'start': 6, 'start_collapse': [6],
                'strand': '+'},
            1: {'chr': 1, 'cigar_collapse': ['109M'], 'end': 354,
                'end_collapse': [354], 'stack_depth_collapse': [100],
                'stack_number_count': 1, 'start': 245, 'start_collapse': [245],
                'strand': '+'}}, False)
        self._sample2_clusters = Clusters({
            0: {'chr': 1, 'cigar_collapse': ['51M5I58M'], 'end': 115,
                'end_collapse': [115], 'stack_depth_collapse': [100],
                'stack_number_count': 1, 'start': 6, 'start_collapse': [6],
                'strand': '+'},
            1: {'chr': 1, 'cigar_collapse': ['109M', '99M'], 'end': 354,
                'end_collapse': [354, 344], 'stack_depth_collapse': [75, 25],
                'stack_number_count': 2, 'start': 245, 'start_collapse': [245, 245],
                'strand': '+'}}, False)
        self._sample1_clusters = Clusters({
            0: {'chr': 1, 'cigar_collapse': ['109M'], 'end': 115,
                'end_collapse': [115], 'stack_depth_collapse': [100],
                'stack_number_count': 1, 'start': 6, 'start_collapse': [6],
                'strand': '+'},
            1: {'chr': 1, 'cigar_collapse': ['109M'], 'end': 354,
                'end_collapse': [354], 'stack_depth_collapse': [80],
                'stack_number_count': 1, 'start': 245, 'start_collapse': [245],
                'strand': '+'}}, False)

    def test_write_empty(self):
        bed_buffer = StringIO()
        empty_cluster = Clusters({}, False)
        empty_cluster.write_to_bed(bed_buffer, 'empty')
        bed_written_contents = bed_buffer.getvalue()
        self.assertMultiLineEqual(bed_written_contents.strip(), "")

    def test_plot_empty(self):
        empty_cluster = Clusters({}, False)
        empty_cluster.plot_number_of_smaps('test', 'png')
        empty_cluster.plot_cluster_lengths('test', 'png')
        empty_cluster.plot_cluster_read_depth('test', 'png')
        empty_cluster.plot_cluster_stack_depth_ratio('test', 'png')
        empty_cluster.plot_read_length_depth_correlation('test', 'png')
        empty_cluster.plot_stack_number_per_cluster('test', 'png')

    def test_minimum_cluster_read_depth(self):
        bed_contents = dedent(
            """
            1	6	115	1:7-115_+	100	+	7,115	1	2	Test
            1	245	354	1:246-354_+	100	+	246,344,354	2	3	Test
            """).strip()
        self._sample2_clusters.read_depth_filter(80, sys.maxsize)
        bed_buffer = StringIO()
        self._sample2_clusters.write_to_bed(bed_buffer, 'Test')
        bed_written_contents = bed_buffer.getvalue()
        self.assertMultiLineEqual(bed_written_contents.strip(), bed_contents)

    def test_maximum_cluster_read_depth(self):
        bed_contents = dedent(
            """
            1	245	354	1:246-354_+	80	+	246,354	1	2	Test
            """).strip()
        self._sample1_clusters.read_depth_filter(0, 81)
        bed_buffer = StringIO()
        self._sample1_clusters.write_to_bed(bed_buffer, 'Test')
        bed_written_contents = bed_buffer.getvalue()
        self.assertMultiLineEqual(bed_written_contents.strip(), bed_contents)

    def test_max_stack_number(self):
        bed_contents = dedent(
            """
            1	6	115	1:7-115_+	100	+	7,115	1	2	Test
            """).strip()
        self._sample2_clusters.max_stack_number_filter(1)
        bed_buffer = StringIO()
        self._sample2_clusters.write_to_bed(bed_buffer, "Test")
        bed_written_contents = bed_buffer.getvalue()
        self.assertMultiLineEqual(bed_written_contents.strip(), bed_contents)

    def test_min_stack_depth_fraction(self):
        bed_contents = dedent(
            """
            1	6	115	1:7-115_+	100	+	7,115	1	2	Test
            1	245	354	1:246-354_+	75	+	246,354	1	2	Test
            """).strip()
        self._sample2_clusters.stack_depth_fraction_filter(50)
        bed_buffer = StringIO()
        self._sample2_clusters.write_to_bed(bed_buffer, 'Test')
        bed_written_contents = bed_buffer.getvalue()
        self.assertMultiLineEqual(bed_written_contents.strip(), bed_contents)

    def test_min_stack_depth_fraction_remove_full_cluster(self):
        # Issue 8
        bed_contents = dedent(
            """
            1	6	115	1:7-115_+	100	+	7,115	1	2	Test
            """).strip()
        self._sample2_clusters.stack_depth_fraction_filter(100)
        bed_buffer = StringIO()
        self._sample2_clusters.write_to_bed(bed_buffer, 'Test')
        bed_written_contents = bed_buffer.getvalue()
        self.assertMultiLineEqual(bed_written_contents.strip(), bed_contents)

    def test_min_stack_depth_fraction_remove_first_or_last_stack(self):
        bed_contents = dedent(
            """
            1	6	115	1:7-115_+	100	+	7,115	1	2	Test
            1	245	354	1:246-354_+	100	+	246,344,354	2	3	Test
            """).strip()
        clusters = Clusters({
            0: {'chr': 1, 'cigar_collapse': ['51M5I58M'], 'end': 115,
                'end_collapse': [115], 'stack_depth_collapse': [100],
                'stack_number_count': 1, 'start': 6, 'start_collapse': [6],
                'strand': '+'},
            1: {'chr': 1, 'cigar_collapse': ['109M', '99M', '99M'], 'end': 360,
                'end_collapse': [354, 344, 360], 'stack_depth_collapse': [75, 25, 5],
                'stack_number_count': 3, 'start': 230, 'start_collapse': [245, 245, 230],
                'strand': '+'}}, False)
        clusters.stack_depth_fraction_filter(5)
        bed_buffer = StringIO()
        clusters.write_to_bed(bed_buffer, 'Test')
        bed_written_contents = bed_buffer.getvalue()
        self.assertMultiLineEqual(bed_written_contents.strip(), bed_contents)

    def test_merge(self):
        result = {
            0: {'chr': 1, 'cluster_count': 3, 'cluster_depth_collapse': [100, 100, 100],
                'end': 115, 'end_collapse': [115, 115, 115], 'sample_count': 3, 'start': 6,
                'start_collapse': [6, 6, 6], 'strand': '+'},
            1: {'chr': 1, 'cluster_count': 4, 'cluster_depth_collapse': [75, 25, 80, 100],
                'end': 354, 'end_collapse': [354, 344, 354, 354], 'sample_count': 3, 'start': 245,
                'start_collapse': [245, 245, 245, 245], 'strand': '+'}}
        all_clusters = self._sample2_clusters + self._sample1_clusters + self._wt_cluster
        merged_clusters = all_clusters.merge(True)
        self.assertDictEqual(result, merged_clusters._merged_clusters)


class TestMergedCluster(unittest.TestCase):
    def setUp(self):
        self.merged_clusters = MergedClusters({
            0: {'chr': 1, 'cluster_count': 3, 'cluster_depth_collapse': [100, 100, 100],
                'end': 115, 'end_collapse': [115, 115, 115], 'sample_count': 2, 'start': 6,
                'start_collapse': [6, 6, 6], 'strand': '+'},
            1: {'chr': 1, 'cluster_count': 4, 'cluster_depth_collapse': [75, 25, 80, 100],
                'end': 354, 'end_collapse': [354, 344, 354, 354], 'sample_count': 3, 'start': 245,
                'start_collapse': [245, 245, 245, 245], 'strand': '+'}})

    def test_write_empty(self):
        empty = MergedClusters({})
        bed_buffer = StringIO()
        empty.write_to_bed(bed_buffer, 'empty')
        bed_written_contents = bed_buffer.getvalue()
        self.assertMultiLineEqual(bed_written_contents.strip(), "")

    def test_plot_empty(self):
        empty = MergedClusters({})
        empty.plot_completeness('empty', 'png')
        empty.plot_merged_cluster_length('empty', 'png')
        empty.plot_number_of_smaps('empty', 'png')
        empty.plot_read_depth('empty', 'png')

    def test_filter_for_completeness(self):
        bed_contents = dedent(
            """
            1	245	354	1:246-354_+	77.5	+	246,344,354	3	3	Set1
            """).strip()
        self.merged_clusters.filter_for_completeness(75, 3)
        bed_buffer = StringIO()
        self.merged_clusters.write_to_bed(bed_buffer, 'Set1')
        bed_written_contents = bed_buffer.getvalue()
        self.assertMultiLineEqual(bed_written_contents.strip(), bed_contents)

    def test_max_smap_number_filter(self):
        bed_contents = dedent(
            """
            1	6	115	1:7-115_+	100	+	7,115	2	2	Set1
            """).strip()
        self.merged_clusters.max_smap_number_filter(2)
        bed_buffer = StringIO()
        self.merged_clusters.write_to_bed(bed_buffer, 'Set1')
        bed_written_contents = bed_buffer.getvalue()
        self.assertMultiLineEqual(bed_written_contents.strip(), bed_contents)
