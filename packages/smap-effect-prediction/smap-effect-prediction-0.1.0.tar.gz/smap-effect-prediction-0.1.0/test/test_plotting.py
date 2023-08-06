from unittest import TestCase, mock
from smap_effect_prediction.plotting import PlottingOperation, VariationRangePlot
from smap_effect_prediction.modifications.modification import ModificationType
import pandas as pd
import numpy as np
import logging

LOCUS_COLUMN_NAME: str = "Locus"
HAPLOTYPE_COLUMN_NAME: str = "Haplotypes"
TARGET_COLUMN_NAME: str = "target"
EXPECTED_CUT_SITE_COLUM_NAME = 'Expected cut site'
INDEL_COLUMNNAME = 'INDEL'
SNP_COLUMNNAME = 'SNP'


class TestPlotting(TestCase):
    def test_operates_on(self):
        result = PlottingOperation.operates_on()
        self.assertEqual(result, ModificationType.DATAFRAME)


class TestVariationRangePlot(TestCase):
    def setUp(self) -> None:
        table_tuples = [("locus1_1", "foo", "locus1_1", pd.NA, ((1161, 'CT', 'C'),), 1158),
                        ("locus1_1", "bar", "locus1_1", ((1160, 'C', 'G'),), pd.NA, 1158),
                        ("locus1_1", "lorem", "locus1_1", pd.NA, ((1138, 'A', 'AT'),), 1158),
                        ("locus1_1", "ipsum", "locus1_1", pd.NA, pd.NA, 1158)]
        self.frequency_table_index = pd.MultiIndex.from_tuples(table_tuples,
                                                               names=[LOCUS_COLUMN_NAME,
                                                                      HAPLOTYPE_COLUMN_NAME,
                                                                      TARGET_COLUMN_NAME,
                                                                      SNP_COLUMNNAME,
                                                                      INDEL_COLUMNNAME,
                                                                      EXPECTED_CUT_SITE_COLUM_NAME])
        table_data = {"bam1": [100.0, 15.0, 100.0, 10.0], "bam2": [80.0, 20.0, 100.0, 100.0]}
        self._frequency_table = pd.DataFrame(data=table_data,
                                             index=self.frequency_table_index)

    @mock.patch('smap_effect_prediction.plotting.px')
    def test_variation_plot(self, mocked_plotly):
        call_data = pd.DataFrame({'SNP': [np.nan, 2.0, np.nan], 'INDEL': [3.0, np.nan, -20.0]})
        op = VariationRangePlot()
        op.modify(self._frequency_table, logging.getLogger)
        mocked_plotly.histogram.assert_called_once()
        (args, kwargs) = mocked_plotly.histogram.call_args
        # '==' cannot be used with pandas dfs, so cannot use called_once_with()
        pd.testing.assert_frame_equal(args[0], call_data)
        self.assertEqual(kwargs['marginal'], 'rug')
        self.assertEqual(kwargs['nbins'], 23)
        mocked_plotly.write_html.called_once_with('variable_sites_histogram.html')
