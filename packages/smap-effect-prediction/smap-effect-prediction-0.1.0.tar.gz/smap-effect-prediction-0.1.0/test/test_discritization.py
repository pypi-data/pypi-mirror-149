import logging
from unittest import TestCase
from smap_effect_prediction.modifications.discretize import Discretize
import pandas as pd
from smap_effect_prediction.modifications.modification import ModificationType

LOCUS_COLUMN_NAME: str = "Locus"
HAPLOTYPE_COLUMN_NAME: str = "Haplotypes"
TARGET_COLUMN_NAME: str = "target"


class TestDiscritization(TestCase):
    def setUp(self) -> None:
        self.frequency_table_index = pd.MultiIndex.from_tuples([('locus1', 'hap1', 'tar1'),
                                                                ('locus1', 'hap2', 'tar2'),
                                                                ('locus1', 'hap3', 'tar3'),
                                                                ('locus2', 'hap4', 'tar4'),
                                                                ('locus2', 'hap5', 'tar5'),
                                                                ('locus3', 'hap6', 'tar6')],
                                                               names=[LOCUS_COLUMN_NAME,
                                                                      HAPLOTYPE_COLUMN_NAME,
                                                                      TARGET_COLUMN_NAME])
        frequency_table = pd.DataFrame([(50, 0, 20),
                                        (40, 0, 20),
                                        (10, 100, 60),
                                        (100, pd.NA, 50),
                                        (0, 0.5, 50),
                                        (100, pd.NA, 1)],
                                       columns=['bam1', 'bam2', 'bam3'],
                                       index=self.frequency_table_index)
        self.frequency_table = frequency_table

    def test_nothing_detected(self):
        frequency_table = pd.DataFrame([(0, 0, 0),
                                        (0, 0, 0),
                                        (0, 0, 0),
                                        (0, 0, 0),
                                        (0, 0, 0),
                                        (0, 0, 0)],
                                       columns=['bam1', 'bam2', 'bam3'],
                                       index=self.frequency_table_index)
        discritization_op = Discretize('dominant', [10])
        result = discritization_op.modify(frequency_table, logging.getLogger)
        self.assertEqual((result.dataframe == 0).all().sum(), 3)

    def test_discritize_dominant(self):
        discritization_op = Discretize('dominant', [10])
        result = discritization_op.modify(self.frequency_table, logging.getLogger)
        expected_result = pd.DataFrame([(1, 0, 1),
                                        (1, 0, 1),
                                        (0, 1, 1),
                                        (1, pd.NA, 1),
                                        (0, 0, 1),
                                        (1, pd.NA, 0)],
                                       columns=['bam1', 'bam2', 'bam3'],
                                       index=self.frequency_table_index,
                                       dtype=pd.Int8Dtype())
        pd.testing.assert_frame_equal(result.dataframe, expected_result, check_exact=True)

    def test_discritize_dosage(self):
        discritization_op = Discretize('dosage', [10, 10, 90, 90])
        result = discritization_op.modify(self.frequency_table, logging.getLogger)
        expected_result = pd.DataFrame([(1, 0, 1),
                                        (1, 0, 1),
                                        (1, 2, 1),
                                        (2, pd.NA, 1),
                                        (0, 0, 1),
                                        (2, pd.NA, 0)],
                                       columns=['bam1', 'bam2', 'bam3'],
                                       index=self.frequency_table_index,
                                       dtype=pd.Int8Dtype())
        pd.testing.assert_frame_equal(result.dataframe, expected_result, check_exact=True)

    def test_overlapping_intervals_raises(self):
        discritization_op = Discretize('dosage', [11, 10, 90, 90])
        err_msg = r"Please make sure the frequency bounds define non-overlapping intervals\."
        with self.assertRaisesRegex(ValueError, err_msg):
            discritization_op.modify(self.frequency_table, logging.getLogger)

    def test_operates_on(self):
        result = Discretize.operates_on()
        self.assertEqual(result, ModificationType.LOCI)
