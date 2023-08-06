import unittest
from smap.haplotype import Stacks
from smap.delineate import MergedClusters
from io import StringIO


class TestDelineateHaplotypeWindow(unittest.TestCase):
    def setUp(self):
        self.merged_clusters = MergedClusters({
            0: {'chr': 1, 'cluster_count': 3, 'cluster_depth_collapse': [100, 100, 100],
                'end': 115, 'end_collapse': [115, 115, 115], 'sample_count': 2, 'start': 6,
                'start_collapse': [6, 6, 6], 'strand': '+'},
            1: {'chr': 1, 'cluster_count': 4, 'cluster_depth_collapse': [75, 25, 80, 100],
                'end': 354, 'end_collapse': [354, 344, 354, 354], 'sample_count': 3, 'start': 245,
                'start_collapse': [245, 245, 245, 245], 'strand': '+'}})

    def test_read_delineate_output(self):
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
        bed_buffer = StringIO()
        self.merged_clusters.write_to_bed(bed_buffer, 'Set1')
        bed_buffer.seek(0, 0)
        stacks = Stacks(bed_buffer)
        self.assertDictEqual(stacks.stacks, result)

    def test_raise_old_coordinate_system(self):
        bed_buffer = StringIO(('1\t6\t115\t1:7-115_+\t100\t+\t6,114\t3\t2\tSet1\n'
                               '1\t245\t354\t1:246-354_+\t77.5\t+\t246,344,353\t4\t3\tSet1\n'))
        with self.assertRaisesRegex(ValueError,
                                    '^It seems that the \\.bed file uses '
                                    'an incorrect SMAP coordinate system'):
            Stacks(bed_buffer)
