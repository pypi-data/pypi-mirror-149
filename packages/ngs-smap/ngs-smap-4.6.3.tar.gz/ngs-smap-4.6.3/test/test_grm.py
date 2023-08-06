from argparse import Namespace
from smap.grm import (Jaccard,
                      parse_new_sample_names_file,
                      LocusInformationCoefficient,
                      Ochiai,
                      SorensenDice)
from smap.haplotype import INDEX_COLUMNS
from io import StringIO
from unittest import TestCase
import pandas as pd


class TestInputOutput(TestCase):
    def test_parse_new_file_names(self):
        test = StringIO("a\tb\nd\td\ne\tf")
        expected = {
            "a": "b",
            "d": "d",
            "e": "f",
        }
        result = parse_new_sample_names_file(test, current_names=["a", "d", "e"])
        self.assertDictEqual(result, expected)

    def test_parse_new_file_names_raises(self):
        test = StringIO("a\tb\tc\nd\n\ne\tf\n")
        expected_message = (r"^Error while parsing sample names file. Please check that "
                            r"there are no duplicate samples in the first column of the "
                            r"file, and that all of these samples are also present in the "
                            r"header of the haplotypes table\.")
        with self.assertRaisesRegex(ValueError, expected_message):
            parse_new_sample_names_file(test, current_names=["a", "f"])


class TestSampleSharedUniqueStatistics(TestCase):
    def setUp(self) -> None:
        index = pd.MultiIndex.from_tuples([("1", "1:7-115_+", "000"),
                                           ("1", "1:7-115_+", "00."),
                                           ("1", "1:7-115_+", "0.0"),
                                           ("1", "1:7-115_+", "..0"),
                                           ("2", "1:1-10_+", "000")], names=INDEX_COLUMNS)
        self.ser1 = pd.Series([pd.NA, 0.0, 50.0, 10.0, 40.0],
                              dtype="Float64",
                              index=index)
        self.ser2 = pd.Series([pd.NA, 50.0, 50.0, pd.NA, pd.NA],
                              dtype="Float64",
                              index=index)

    def test_number_of_shared_alleles(self):
        res = self.ser1.smap.number_of_shared_alleles(self.ser2)
        self.assertIs(res, 1)
        res = self.ser2.smap.number_of_shared_alleles(self.ser1)
        self.assertIs(res, 1)

    def test_number_of_unique_alleles(self):
        res = self.ser1.smap.number_of_unique_alleles(self.ser2, include_non_shared_loci=False)
        self.assertIs(res, 1)
        res = self.ser1.smap.number_of_unique_alleles(self.ser2, include_non_shared_loci=True)
        self.assertIs(res, 2)


class TestCoefficient(TestCase):
    def setUp(self) -> None:
        index = pd.MultiIndex.from_tuples([("1", "1:246-354_+", "0000"),
                                           ("1", "1:246-354_+", "010."),
                                           ("1", "1:246-354_+", "0100"),
                                           ("1", "1:7-115_+", "000"),
                                           ("1", "1:7-115_+", "010")], names=INDEX_COLUMNS)
        self.sample2 = pd.Series([pd.NA, 25.0, 75.0, pd.NA, 100.0],
                                 index=index,
                                 dtype="Float64",
                                 name="Sample2.BWA.bam")
        self.wt = pd.Series([100.0, pd.NA, pd.NA, 100.0, pd.NA],
                            index=index,
                            dtype="Float64",
                            name="WT.BWA.bam")
        self.sample1 = pd.Series([pd.NA, pd.NA, pd.NA, 50.0, 50.0],
                                 index=index,
                                 dtype="Float64",
                                 name="Sample1.BWA.bam")


class TestLocusInformationCoefficient(TestCoefficient):
    def setUp(self) -> None:
        self.coefficient = LocusInformationCoefficient(False, 'Shared', False, False)
        super().setUp()

    def test_from_command_line(self):
        namespace = Namespace(include_non_shared_loci=False,
                              locus_information_criterion='Shared',
                              informative_loci_as_proportion=False,
                              partially_informative_loci=False)
        res = LocusInformationCoefficient.from_command_line_args(namespace)
        expected = LocusInformationCoefficient(False, 'Shared', False, False)
        self.assertEqual(expected, res)

    def test_calculate(self):
        combos = (
            ((self.wt, self.wt),
             pd.Index(['1:246-354_+', '1:7-115_+'], name='Locus')),
            ((self.wt, self.sample1), pd.Index([], dtype='object', name='Locus')),
            ((self.wt, self.sample2), pd.Index([], dtype='object', name='Locus')),
            ((self.sample1, self.wt), pd.Index([], dtype='object', name='Locus')),
            ((self.sample1, self.sample1), pd.Index(['1:7-115_+'], name='Locus')),
            ((self.sample1, self.sample2), pd.Index([], dtype='object', name='Locus')),
            ((self.sample2, self.wt), pd.Index([], dtype='object', name='Locus')),
            ((self.sample2, self.sample1), pd.Index([], dtype='object', name='Locus')),
            ((self.sample2, self.sample2), pd.Index(['1:246-354_+', '1:7-115_+'], name='Locus')),
        )
        for (ser1, ser2), expected in combos:
            result = self.coefficient.calculate(ser1, ser2)
            pd.testing.assert_index_equal(result, expected)


class TestJaccard(TestCoefficient):
    def setUp(self) -> None:
        self.coefficient = Jaccard(False, False)
        super().setUp()

    def test_calculate(self):
        combos = (
            ((self.wt, self.wt), 1.0),
            ((self.wt, self.sample1), 0.5),
            ((self.wt, self.sample2), 0.0),
            ((self.sample1, self.wt), 0.5),
            ((self.sample1, self.sample1), 1.0),
            ((self.sample1, self.sample2), 0.5),
            ((self.sample2, self.wt), 0.0),
            ((self.sample2, self.sample1), 0.5),
            ((self.sample2, self.sample2), 1.0),
        )
        for (ser1, ser2), expected in combos:
            result = self.coefficient.calculate(ser1, ser2)
            self.assertEqual(result, expected)


class TestOchiai(TestCoefficient):
    def setUp(self) -> None:
        self.coefficient = Ochiai(False, False)
        super().setUp()

    def test_calculate(self):
        combos = (
            ((self.wt, self.wt), 1.0),
            ((self.wt, self.sample1), 0.7071067811865475),
            ((self.wt, self.sample2), 0.0),
            ((self.sample1, self.wt), 0.7071067811865475),
            ((self.sample1, self.sample1), 1.0),
            ((self.sample1, self.sample2), 0.7071067811865475),
            ((self.sample2, self.wt), 0.0),
            ((self.sample2, self.sample1), 0.7071067811865475),
            ((self.sample2, self.sample2), 1.0),
        )
        for (ser1, ser2), expected in combos:
            result = self.coefficient.calculate(ser1, ser2)
            self.assertEqual(result, expected)


class TestSorensenDice(TestCoefficient):
    def setUp(self) -> None:
        self.coefficient = SorensenDice(False, False)
        super().setUp()

    def test_calculate(self):
        combos = (
            ((self.wt, self.wt), 1.0),
            ((self.wt, self.sample1), 0.6666666666666666),
            ((self.wt, self.sample2), 0.0),
            ((self.sample1, self.wt), 0.6666666666666666),
            ((self.sample1, self.sample1), 1.0),
            ((self.sample1, self.sample2), 0.6666666666666666),
            ((self.sample2, self.wt), 0.0),
            ((self.sample2, self.sample1), 0.6666666666666666),
            ((self.sample2, self.sample2), 1.0),
        )
        for (ser1, ser2), expected in combos:
            result = self.coefficient.calculate(ser1, ser2)
            self.assertEqual(result, expected)
