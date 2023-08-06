import logging
from unittest import TestCase
from smap_effect_prediction.models import CHROMOSOME_COLUMN_NAME
from smap_effect_prediction.modifications.aggregate import LocusAggregation
import pandas as pd

LOCUS_COLUMN_NAME: str = "Locus"
HAPLOTYPE_COLUMN_NAME: str = "Haplotypes"
TARGET_COLUMN_NAME: str = "target"
INDEL_COLUMNNAME: str = 'INDEL'
SNP_COLUMNNAME: str = 'SNP'
HAPLOTYPE_NAME: str = 'Haplotype_Name'


class TestAggregation(TestCase):
    def setUp(self):
        table_columns = [('1', 'locus1', 'hap1', 'tar1', 'foo', ((3, 'A', 'T'),), tuple(), True),
                         (
                            '1', 'locus1', 'hap2', 'tar2', 'bar',
                            ((7, 'C', 'G'),), ((5, 'AC', 'A'),), True
                         ),
                         (
                            '1', 'locus1', 'hap3', 'tar3', 'lorem',
                            ((10, 'C', 'G'),), tuple(), False)]
        self.frequency_table_index = pd.MultiIndex.from_tuples(table_columns,
                                                               names=[CHROMOSOME_COLUMN_NAME,
                                                                      LOCUS_COLUMN_NAME,
                                                                      HAPLOTYPE_COLUMN_NAME,
                                                                      TARGET_COLUMN_NAME,
                                                                      HAPLOTYPE_NAME,
                                                                      SNP_COLUMNNAME,
                                                                      INDEL_COLUMNNAME,
                                                                      'Effect'])
        frequency_table = pd.DataFrame([(50, 0, pd.NA),
                                        (40, pd.NA, pd.NA),
                                        (10, 100, pd.NA)],
                                       columns=['bam1', 'bam2', 'bam3'],
                                       index=self.frequency_table_index)
        self.frequency_table = frequency_table

    def test_aggregation(self):
        expected_index = pd.MultiIndex.from_tuples([("1",
                                                     'locus1',
                                                     "(3, 'A', 'T'),(7, 'C', 'G')",
                                                     "(5, 'AC', 'A')",
                                                     "foo,bar")],
                                                   names=[CHROMOSOME_COLUMN_NAME,
                                                          LOCUS_COLUMN_NAME,
                                                          SNP_COLUMNNAME,
                                                          INDEL_COLUMNNAME,
                                                          HAPLOTYPE_NAME])
        expected_frame = pd.DataFrame([(90, 0, pd.NA)],
                                      columns=['bam1', 'bam2', 'bam3'],
                                      index=expected_index)
        op = LocusAggregation('Effect')
        result = op.modify(self.frequency_table, logging.getLogger)
        pd.testing.assert_frame_equal(expected_frame, result.dataframe)

    def test_no_edited_haplotypes(self):
        table_columns = [('1', 'locus1', 'hap3', 'tar3', 'foo', ((10, 'C', 'G'),), tuple(), False)]
        frequency_table_index = pd.MultiIndex.from_tuples(table_columns,
                                                          names=[CHROMOSOME_COLUMN_NAME,
                                                                 LOCUS_COLUMN_NAME,
                                                                 HAPLOTYPE_COLUMN_NAME,
                                                                 TARGET_COLUMN_NAME,
                                                                 HAPLOTYPE_NAME,
                                                                 SNP_COLUMNNAME,
                                                                 INDEL_COLUMNNAME,
                                                                 'Effect'])
        frequency_table = pd.DataFrame([(100, 100, pd.NA)],
                                       columns=['bam1', 'bam2', 'bam3'],
                                       index=frequency_table_index)
        expected_index = pd.MultiIndex.from_tuples([('1', 'locus1', tuple(), tuple(), pd.NA)],
                                                   names=[CHROMOSOME_COLUMN_NAME,
                                                          LOCUS_COLUMN_NAME,
                                                          SNP_COLUMNNAME,
                                                          INDEL_COLUMNNAME,
                                                          HAPLOTYPE_NAME])
        expected_frame = pd.DataFrame([(0, 0, pd.NA)],
                                      columns=['bam1', 'bam2', 'bam3'],
                                      index=expected_index)
        op = LocusAggregation('Effect')
        result = op.modify(frequency_table, logging.getLogger)
        pd.testing.assert_frame_equal(expected_frame, result.dataframe)
