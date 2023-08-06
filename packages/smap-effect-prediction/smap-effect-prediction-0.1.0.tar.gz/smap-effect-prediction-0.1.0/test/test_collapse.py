from unittest import TestCase
from smap_effect_prediction.modifications.collapse import Collapse
import pandas as pd
import logging

LOCUS_COLUMN_NAME: str = "Locus"
HAPLOTYPE_COLUMN_NAME: str = "Haplotypes"
TARGET_COLUMN_NAME: str = "target"
REFERENCE_COLUMN_NAME: str = 'edit'
START_COLUMN_NAME = 'start'
INDEL_COLUMNNAME = 'INDEL'
SNP_COLUMNNAME = 'SNP'
ALIGNMENT_COLUMNNAME = 'Alignment'
GUIDE_FILTER_COLUMNAME = 'FILTER_gRNA'
GUIDE_FILTER_SNP_COLUMNAME = GUIDE_FILTER_COLUMNAME + '_SNP'
GUIDE_FILTER_INDEL_COLUMNAME = GUIDE_FILTER_COLUMNAME + '_INDEL'
HAPLOTYPE_NAME = 'Haplotype_Name'
EXPECTED_CUT_SITE_COLUM_NAME = 'Expected cut site'


class TestCollapse(TestCase):
    def setUp(self) -> None:
        index_data = [("locus1_1", "foo", "locus1_1",
                       pd.NA, ((1158, 'CT', 'C'),), True, pd.NA, True, "0:1D:CT-C", 1158, 1),
                      ("locus1_1", "bar", "locus1_1",
                       ((1158, 'C', 'G'),), pd.NA, pd.NA, True, True,
                       "0:1D:CT-C,-20:S:C-A", 1158, 1),
                      ("locus1_1", "lorem", "locus1_1",
                       pd.NA, ((1138, 'A', 'AT'),), False, pd.NA, False, "-20:1I:A-AT", 1158, 1),
                      ("locus1_1", "lorem2", "locus1_1",
                       pd.NA, ((1138, 'A', 'AT'),), False, pd.NA, False,
                       "-20:1I:A-AT,45:1I:C-CT", 1158, 1),
                      ("locus1_1", "ipsum", "locus1_1",
                       pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, "ref", 1158, 'ref')]
        index = pd.MultiIndex.from_tuples(index_data,
                                          names=[LOCUS_COLUMN_NAME,
                                                 HAPLOTYPE_COLUMN_NAME,
                                                 TARGET_COLUMN_NAME,
                                                 SNP_COLUMNNAME,
                                                 INDEL_COLUMNNAME,
                                                 GUIDE_FILTER_INDEL_COLUMNAME,
                                                 GUIDE_FILTER_SNP_COLUMNAME,
                                                 GUIDE_FILTER_COLUMNAME,
                                                 HAPLOTYPE_NAME,
                                                 EXPECTED_CUT_SITE_COLUM_NAME,
                                                 REFERENCE_COLUMN_NAME])

        self.input_df = pd.DataFrame({"sample1": [85.0, 15.0, 0.0, 0.0, 0.0],
                                      "sample2": [40.0, 10.0, 1.0, 5.0, 44.0],
                                      "sample3": [40.0, 10.0, 0.0, 0.0, 50.0],
                                      "sample4": [20.0, 30.0, 5.0, 1.0, 44.0]},
                                     index=index)

        output_data = [('locus1_1_ref', "locus1_1", "locus1_1",
                        1158, False), ('locus1_1_0:1D:CT-C', "locus1_1", "locus1_1",
                                       1158, True)]

        output_index = pd.MultiIndex.from_tuples(output_data,
                                                 names=['Haplotype',
                                                        LOCUS_COLUMN_NAME,
                                                        TARGET_COLUMN_NAME,
                                                        EXPECTED_CUT_SITE_COLUM_NAME,
                                                        GUIDE_FILTER_COLUMNAME])

        self.output_df = pd.DataFrame({"sample1": [0.0, 100.0],
                                       "sample2": [50.0, 50.0],
                                       "sample3": [50.0, 50.0],
                                       "sample4": [50.0, 50.0]},
                                      index=output_index)

        index_data_false = [("locus1_1", "foo", "locus1_1",
                             pd.NA, ((1158, 'CT', 'C'),), True, pd.NA, False, "0:1D:CT-C", 1158,
                             1),
                            (
                                "locus1_1", "bar", "locus1_1", ((1158, 'C', 'G'),), pd.NA, pd.NA,
                                True,
                                False, "0:1D:CT-C,-20:S:C-A", 1158, 1),
                            ("locus1_1", "lorem", "locus1_1",
                             pd.NA, ((1138, 'A', 'AT'),), False, pd.NA, False, "-20:1I:A-AT", 1158,
                             1),
                            ("locus1_1", "lorem2", "locus1_1",
                             pd.NA, ((1138, 'A', 'AT'),), False, pd.NA, False,
                             "-20:1I:A-AT,45:1I:C-CT", 1158, 1),
                            ("locus1_1", "ipsum", "locus1_1",
                             pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, "ref", 1158, 'ref')]

        index_false = pd.MultiIndex.from_tuples(index_data_false,
                                                names=[LOCUS_COLUMN_NAME,
                                                       HAPLOTYPE_COLUMN_NAME,
                                                       TARGET_COLUMN_NAME,
                                                       SNP_COLUMNNAME,
                                                       INDEL_COLUMNNAME,
                                                       GUIDE_FILTER_INDEL_COLUMNAME,
                                                       GUIDE_FILTER_SNP_COLUMNAME,
                                                       GUIDE_FILTER_COLUMNAME,
                                                       HAPLOTYPE_NAME,
                                                       EXPECTED_CUT_SITE_COLUM_NAME,
                                                       REFERENCE_COLUMN_NAME])

        self.input_df_false = pd.DataFrame({"sample1": [85.0, 15.0, 0.0, 0.0, 0.0],
                                            "sample2": [40.0, 10.0, 1.0, 5.0, 44.0],
                                            "sample3": [40.0, 10.0, 0.0, 0.0, 50.0],
                                            "sample4": [20.0, 30.0, 5.0, 1.0, 44.0]},
                                           index=index_false)

        output_data_false = [('locus1_1_ref', "locus1_1", "locus1_1",
                              1158, False)]

        output_index_false = pd.MultiIndex.from_tuples(output_data_false,
                                                       names=['Haplotype',
                                                              LOCUS_COLUMN_NAME,
                                                              TARGET_COLUMN_NAME,
                                                              EXPECTED_CUT_SITE_COLUM_NAME,
                                                              GUIDE_FILTER_COLUMNAME])

        self.output_df_false = pd.DataFrame({"sample1": [100.0],
                                             "sample2": [100.0],
                                             "sample3": [100.0],
                                             "sample4": [100.0]},
                                            index=output_index_false)

        index_data_non_filter = [("locus1_1", "foo", "locus1_1",
                                  pd.NA, ((1158, 'CT', 'C'),), "0:1D:CT-C", 1),
                                 ("locus1_1", "bar", "locus1_1",
                                  ((1158, 'C', 'G'),), pd.NA,
                                  "0:1D:CT-C,-20:S:C-A", 1),
                                 ("locus1_1", "lorem", "locus1_1",
                                  pd.NA, ((1138, 'A', 'AT'),), "-20:1I:A-AT", 1),
                                 ("locus1_1", "lorem", "locus1_1",
                                  pd.NA, pd.NA, pd.NA, 'ref')
                                 ]

        index_non_filter = pd.MultiIndex.from_tuples(index_data_non_filter,
                                                     names=[LOCUS_COLUMN_NAME,
                                                            HAPLOTYPE_COLUMN_NAME,
                                                            TARGET_COLUMN_NAME,
                                                            SNP_COLUMNNAME,
                                                            INDEL_COLUMNNAME,
                                                            HAPLOTYPE_NAME,
                                                            REFERENCE_COLUMN_NAME])

        self.input_non_filter_df = pd.DataFrame({"sample1": [85.0, 15.0, 0.0, 0.0],
                                                 "sample2": [40.0, 10.0, 1.0, 0.0],
                                                 "sample3": [40.0, 10.0, 0.0, 0.0],
                                                 "sample4": [20.0, 30.0, 5.0, 0.0]},
                                                index=index_non_filter)

        index_data_non_filter = [('locus1_1_0:1D:CT-C', "locus1_1", "locus1_1"),
                                 ('locus1_1_0:1D:CT-C,-20:S:C-A', "locus1_1", "locus1_1"),
                                 ('locus1_1_-20:1I:A-AT', "locus1_1", "locus1_1"),
                                 ('locus1_1_ref', "locus1_1", "locus1_1")]

        index_non_filter = pd.MultiIndex.from_tuples(index_data_non_filter,
                                                     names=['Haplotype',
                                                            LOCUS_COLUMN_NAME,
                                                            TARGET_COLUMN_NAME])

        self.output_non_filter_df = pd.DataFrame({"sample1": [85.0, 15.0, 0.0, 0.0],
                                                  "sample2": [40.0, 10.0, 1.0, 0.0],
                                                  "sample3": [40.0, 10.0, 0.0, 0.0],
                                                  "sample4": [20.0, 30.0, 5.0, 0.0]},
                                                 index=index_non_filter)

    def test_collapse_without_filter(self):
        lower_cut_site_range = 10
        upper_cut_site_range = 10
        modification = Collapse(lower_cut_site_range, upper_cut_site_range)

        result_non_filter = modification.modify(self.input_non_filter_df, logging.getLogger)

        pd.testing.assert_frame_equal(self.output_non_filter_df, result_non_filter.dataframe)

    def test_collapse_with_filter(self):
        lower_cut_site_range = 10
        upper_cut_site_range = 50

        modification = Collapse(lower_cut_site_range, upper_cut_site_range)
        result = modification.modify(self.input_df, logging.getLogger)
        pd.testing.assert_frame_equal(self.output_df, result.dataframe)

    def test_collapse_all_negative(self):
        lower_cut_site_range = 10
        upper_cut_site_range = 50

        modification = Collapse(lower_cut_site_range, upper_cut_site_range)

        result = modification.modify(self.input_df_false, logging.getLogger)
        pd.testing.assert_frame_equal(self.output_df_false, result.dataframe)
