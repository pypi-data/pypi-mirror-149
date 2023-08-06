from textwrap import dedent
from unittest import TestCase, mock
from tempfile import TemporaryDirectory
from pathlib import Path
from argparse import Namespace
from matplotlib.colors import to_rgba
from smap.plotting import format_ticks
from smap.compare import (get_set_information,
                          get_colormap,
                          heatmap,
                          sets_in_correct_orientation,
                          calculate_loci_intersect_statistics,
                          plot_combo,
                          parse_args)
import numpy as np


class TestCompare(TestCase):
    def setUp(self) -> None:
        set1_data = dedent(
            """\
            1	6	115	1:7-115_+	100	+	7,115	3	2	Set1
            1	245	354	1:246-354_+	77.5	+	246,344,354	4	3	Set1
            """)

        set2_data = dedent(
            """\
            1	10	120	1:11-120_+	120	+	11,120	7	2	Set2
            1	10	120	1:11-120_+	120	-	11,120	7	2	Set2
            1	700	1000	1:701-1000_+	50	+	701,702,1000	4	3	Set2
            """)
        self.tempdir = TemporaryDirectory()
        self.tempdir_path = Path(self.tempdir.name)
        self.set1_bed = self.tempdir_path / "set1.bed"
        self.set2_bed = self.tempdir_path / "set2.bed"
        with self.set1_bed.open('w') as open_set1:
            open_set1.write(set1_data)
        with self.set2_bed.open('w') as open_set2:
            open_set2.write(set2_data)
        return super().setUp()

    def tearDown(self) -> None:
        self.tempdir.cleanup()
        return super().tearDown()

    def test_parse_args(self):
        res = parse_args(["/foo", "/bar"])
        self.assertEqual(res, Namespace(smap_set1=Path('/foo'),
                                        smap_set2=Path('/bar')))

    def test_get_set_information(self):
        label, number_of_samples = get_set_information(self.set1_bed)
        self.assertEqual(label, 'Set1')
        self.assertEqual(number_of_samples, 4)

    def test_multiple_set_labels_raises(self):
        set_data = dedent(
            """\
            1	6	115	1:7-115_+	100	+	7,115	3	2	Set1
            1	245	354	1:246-354_+	77.5	+	246,344,354	4	3	Set2
            """)
        bed = self.tempdir_path / "should_fail.bed"

        with bed.open('w') as open_set:
            open_set.write(set_data)
        message = (rf"{bed} contains more then one sample set "
                   r"\(duplicate entries in the label column\)")
        with self.assertRaisesRegex(ValueError, expected_regex=message):
            get_set_information(bed)

    def test_get_colormap(self):
        gray_value = to_rgba('lightgray')
        cmap = get_colormap(25)
        np.testing.assert_equal(cmap.get_bad(), gray_value)
        self.assertEqual(cmap.N, 25)

    def test_get_set_in_correct_orientation(self):
        first_info, second_info = sets_in_correct_orientation(self.set1_bed, self.set2_bed)
        self.assertEqual(first_info, (self.set2_bed, 'Set2', 7))
        self.assertEqual(second_info, (self.set1_bed, 'Set1', 4))
        first_info, second_info = sets_in_correct_orientation(self.set2_bed, self.set1_bed)
        self.assertEqual(first_info, (self.set2_bed, 'Set2', 7))
        self.assertEqual(second_info, (self.set1_bed, 'Set1', 4))

    def test_calculate_loci_intersect_statistics(self):
        result_number_of_loci = np.array([[0, 0, 0, 0, 1, 0, 0, 1],
                                          [0, 0, 0, 0, 0, 0, 0, 0],
                                          [0, 0, 0, 0, 0, 0, 0, 0],
                                          [0, 0, 0, 0, 0, 0, 0, 1],
                                          [1, 0, 0, 0, 0, 0, 0, 0]])
        expected_depth_set2 = np.array([[0, 0, 0, 0, 50, 0, 0, 120],
                                        [0, 0, 0, 0, 0, 0, 0, 0],
                                        [0, 0, 0, 0, 0, 0, 0, 0],
                                        [0, 0, 0, 0, 0, 0, 0, 120],
                                        [0, 0, 0, 0, 0, 0, 0, 0]])
        expected_depth_set1 = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                                        [0, 0, 0, 0, 0, 0, 0, 0],
                                        [0, 0, 0, 0, 0, 0, 0, 0],
                                        [0, 0, 0, 0, 0, 0, 0, 100],
                                        [77.5, 0, 0, 0, 0, 0, 0, 0]])
        res = calculate_loci_intersect_statistics(self.set1_bed, self.set2_bed)
        number_of_loci, relative_stack_depth_set1, \
            relative_stack_depth_set2, label_set1, label_set2 = res
        # Switched because it has the most number of samples
        self.assertEqual(label_set1, 'Set2')
        self.assertEqual(label_set2, 'Set1')
        np.testing.assert_array_equal(result_number_of_loci, number_of_loci)
        np.testing.assert_array_equal(expected_depth_set2, relative_stack_depth_set1)
        np.testing.assert_array_equal(expected_depth_set1, relative_stack_depth_set2)

    def test_loci_statistics_triple_overlap_skipped(self):
        result_number_of_loci = np.array([[0, 0, 0, 0, 1, 0, 0, 1],
                                          [0, 0, 0, 0, 0, 0, 0, 0],
                                          [0, 0, 0, 0, 0, 0, 0, 0],
                                          [0, 0, 0, 0, 0, 0, 0, 0],
                                          [1, 0, 0, 0, 0, 0, 0, 0]])
        expected_depth_set2 = np.array([[0, 0, 0, 0, 50, 0, 0, 120],
                                        [0, 0, 0, 0, 0, 0, 0, 0],
                                        [0, 0, 0, 0, 0, 0, 0, 0],
                                        [0, 0, 0, 0, 0, 0, 0, 0],
                                        [0, 0, 0, 0, 0, 0, 0, 0]],
                                       dtype=float)
        expected_depth_set1 = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                                        [0, 0, 0, 0, 0, 0, 0, 0],
                                        [0, 0, 0, 0, 0, 0, 0, 0],
                                        [0, 0, 0, 0, 0, 0, 0, 0],
                                        [77.5, 0, 0, 0, 0, 0, 0, 0]],
                                       dtype=float)
        set2_with_extra_merged_cluster = dedent(
            """\
            1	10	120	1:11-120_+	120	+	11,120	7	2	Set2
            1	10	120	1:11-120_+	120	-	11,120	7	2	Set2
            1	700	1000	1:701-1000_+	50	+	701,702,1000	4	3	Set2
            1	15	80	1:16-80_+	25.5	+	16,80	3	2	Set2
            """)
        with self.set2_bed.open('w') as open_set2:
            open_set2.write(set2_with_extra_merged_cluster)
        res = calculate_loci_intersect_statistics(self.set1_bed, self.set2_bed)
        number_of_loci, relative_stack_depth_set1, \
            relative_stack_depth_set2, label_set1, label_set2 = res
        # Switched because it has the most number of samples
        self.assertEqual(label_set1, 'Set2')
        self.assertEqual(label_set2, 'Set1')
        np.testing.assert_array_equal(result_number_of_loci, number_of_loci)
        np.testing.assert_array_equal(expected_depth_set2, relative_stack_depth_set1)
        np.testing.assert_array_equal(expected_depth_set1, relative_stack_depth_set2)

    @mock.patch('smap.compare.heatmap')
    @mock.patch('smap.compare.PdfPages')
    def test_plotting(self, _, mocked_heatmap):
        number_of_loci = np.array([[0, 0, 0, 0, 1, 0, 0, 1],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 1],
                                   [1, 0, 0, 0, 0, 0, 0, 0]])
        depth_set2 = np.array([[0, 0, 0, 0, 50, 0, 0, 120],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 120],
                               [0, 0, 0, 0, 0, 0, 0, 0]], dtype=float)
        depth_set1 = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 100],
                               [77.5, 0, 0, 0, 0, 0, 0, 0]])
        row_labels = "Completeness set1\n(occurrence in number of samples)"
        column_labels = "Completeness set2\n(occurrence in number of samples)"
        expected_cmap = get_colormap(25)

        expected_kwags = [
            {
                "title": ("Frequency of loci per the number of samples\n"
                          "from each set in which the loci were observed."),
                "cbarlabel": "Number of loci",
                "row_label": row_labels,
                "col_label": column_labels,
                "vmin": 1,
                "cmap": expected_cmap
            },
            {
                "title": ("Frequency of loci per the number of samples\n"
                          "from each set in which the loci were observed."
                          "\nLoci that occurred at least once in both sets."),
                "cbarlabel": "Number of loci",
                "row_label": row_labels,
                "col_label": column_labels,
                "vmin": 1,
                "xmin": 1,
                "ymin": 1,
                "cmap": expected_cmap

            },
            {
                "title": "Mean read depth of set1 loci\n"
                         "stratified per number of set1 (x) and set2 (y)\n"
                         "samples in which the loci were observed.",
                "cbarlabel": "Mean read depth",
                "row_label": row_labels,
                "col_label": column_labels,
                "vmin": 1,
                "cmap": expected_cmap
            },
            {
                "title": "Mean read depth of set2 loci\n"
                         "stratified per number of set1 (x) and set2 (y)\n"
                         "samples in which the loci were observed.",
                "cbarlabel": "Mean read depth",
                "row_label": row_labels,
                "col_label": "Completeness\n(occurrence in\nnumber of samples\nset2)",
                "vmin": 1,
                "cmap": expected_cmap

            }
        ]
        plot_combo(number_of_loci, depth_set1, depth_set2, 'set1', 'set2')
        self.assertEqual(mocked_heatmap.call_count, 4)
        for expected, data, call in zip(expected_kwags,
                                        (number_of_loci, number_of_loci, depth_set1, depth_set2),
                                        mocked_heatmap.call_args_list):
            args, kwargs = call
            self.assertDictEqual(kwargs, expected)
            self.assertEqual((data,), args)

    @mock.patch('smap.plotting.plt')
    @mock.patch('smap.plotting.format_ticks')
    def test_heatmap(self, mocked_format_ticks, mocked_matplotlib):
        number_of_loci = np.array([[0, 0, 0, 0, 1, 0, 0, 1],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 1],
                                   [1, 0, 0, 0, 0, 0, 0, 0]])
        mocked_format_ticks.side_effect = [[1, 2], [3, 4]]
        cmap = get_colormap(25)
        heatmap(number_of_loci,
                row_label="Completeness set1\n(occurrence in number of samples)",
                col_label="Completeness set2\n(occurrence in number of samples)",
                title="foo",
                ax=None,
                cbarlabel="bar",
                vmin=1,
                xmin=0,
                cmap=cmap,
                ymin=0)
        ax = mocked_matplotlib.gca()
        ax.set_xlim.assert_called_once_with((-0.5, 7.5))
        ax.set_ylim.assert_called_once_with((4.5, -0.5))
        ax.imshow.assert_called_once_with(number_of_loci,
                                          interpolation=None,
                                          vmin=1,
                                          cmap=cmap)
        ax.set_title.assert_called_once_with("foo")
        ax.set_xlabel.assert_called_once_with("Completeness set1\n"
                                              "(occurrence in number of samples)",
                                              multialignment='center',
                                              size='large')
        ax.set_ylabel.assert_called_once_with("Completeness set2\n"
                                              "(occurrence in number of samples)",
                                              multialignment='center',
                                              size='large')

    def test_format_ticks(self):
        ticks = [-2, -1, 0, 4, 5]
        res = format_ticks(ticks, 0, 5)
        np.testing.assert_array_equal(res, np.array([0, 4, 5]))
        res = format_ticks(ticks, -2, 0)
        np.testing.assert_array_equal(res, np.array([-2, -1, 0]))
        res = format_ticks(ticks, 3, 5)
        np.testing.assert_array_equal(res, np.array([3, 4, 5]))
