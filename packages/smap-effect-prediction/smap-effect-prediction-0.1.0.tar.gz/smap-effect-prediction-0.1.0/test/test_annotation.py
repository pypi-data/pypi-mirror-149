import logging
from unittest import TestCase
import pandas as pd
from smap_effect_prediction.models import HaplotypeTable, Gff
from smap_effect_prediction.modifications.annotate import (HaplotypePosition,
                                                           DNAPairwiseAlignment,
                                                           EffectAnnotation,
                                                           PairwiseAlignmentAnnotation,
                                                           AddGuideFilter,
                                                           ProteinPrediction,
                                                           AddHaploTypeName)
from smap_effect_prediction.modifications.collapse import Collapse
from textwrap import dedent
from io import StringIO
from Bio.Align import PairwiseAlignment
import numpy as np

from smap_effect_prediction.modifications.modification import ModificationType
import tempfile

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
REFERENCE_COLUMN_NAME = 'edit'
EXPECTED_CUT_SITE_COLUM_NAME = 'Expected cut site'
CHROMOSOME_COLUMN_NAME = "Reference"


class TestHaplotypePosition(TestCase):
    def setUp(self) -> None:
        self.borders = dedent("""\
                                 AT1G06840	SMAP	CRISPR_F_border	1	10	.	+	.	NAME=AT1G06840_1
                                 AT1G06840	SMAP	CRISPR_R_border	16	21	.	+	.	NAME=AT1G06840_1
                                 """)
        self.reference = dedent("""\
                                   >AT1G06840
                                   AAACAAAGGAAGAAAAATAGCAAGTAGAATGGTTTTGACGGAAGAAGGTGGTGAAGTTATGGCGGCGGCGCAACGGAAAC
                                   TTATGATGACGCTCTTCCGTCGGTCTCATCCATTACCTGAAATAGTCAAACTTAGAAAATGTCGTATTATCACTCTTCAA
                                   TGCTCCCACCCAATACCAACTACTTTCCTCTTTCTTTGTCTTGTGTTTCTTACTTGGTCATGGCCTTTTCCTTCTAAACT
                                   CTCTCTCTCTCGAGATTTCGTTTTTTCCTTGGGTCTCCTCTGTTTCCTCCTCTCTCGATATGTTTTCGACCCATCATGTC
                                   """)

        row_index = pd.MultiIndex.from_tuples([("1", "AT1G06840_1", "AGAAA", "AT1G06840_1"),
                                               ("1", "AT1G06840_1", "AGAA", "AT1G06840_1"),
                                               ("1", "AT1G06840_1", "AGAAT", "AT1G06840_1"),
                                               ("1", "AT1G06840_1", "AGAGAT", "AT1G06840_1")],
                                              names=[CHROMOSOME_COLUMN_NAME,
                                                     LOCUS_COLUMN_NAME,
                                                     HAPLOTYPE_COLUMN_NAME,
                                                     TARGET_COLUMN_NAME])

        table_data = {"sample1": [100.0, 15.0, 100.0, 10.0], "sample2": [80.0, 20.0, 100.0, 100.0]}
        self.table_data = table_data
        table = pd.DataFrame(data=table_data,
                             index=row_index)

        self.haplotype_table = HaplotypeTable(table)

    def test_haplotype_annotation(self):
        row_index_result = pd.MultiIndex.from_tuples(
            [("1", "AT1G06840_1", "AGAAA", "AT1G06840_1", "ref", 10, 15),
             ("1", "AT1G06840_1", "AGAA", "AT1G06840_1", 1, 10, 15),
             ("1", "AT1G06840_1", "AGAAT", "AT1G06840_1", 0, 10, 15),
             ("1", "AT1G06840_1", "AGAGAT", "AT1G06840_1", -1, 10, 15)],
            names=["Reference", "Locus", "Haplotypes", "target", 'edit', 'start', 'end'])

        result_table = pd.DataFrame(data={"sample1": [100.0, 15.0, 100.0, 10.0],
                                          "sample2": [80.0, 20.0, 100.0, 100.0]},
                                    index=row_index_result)

        gff = Gff.read_file(StringIO(self.borders))
        modification = HaplotypePosition(gff, StringIO(self.reference))
        locus = modification.modify(self.haplotype_table.dataframe, logging.getLogger)
        self.assertIsInstance(locus, HaplotypeTable)
        pd.testing.assert_frame_equal(locus.dataframe, result_table)

    def test_missing_reference_from_input(self):
        row_index = pd.MultiIndex.from_tuples([("1", "AT1G06840_1", "AGAAC", "AT1G06840_1"),
                                               ("1", "AT1G06840_1", "AGAA", "AT1G06840_1"),
                                               ("1", "AT1G06840_1", "AGAAT", "AT1G06840_1"),
                                               ("1", "AT1G06840_1", "AGAGAT", "AT1G06840_1")],
                                              names=[CHROMOSOME_COLUMN_NAME,
                                                     LOCUS_COLUMN_NAME,
                                                     HAPLOTYPE_COLUMN_NAME,
                                                     TARGET_COLUMN_NAME])
        row_index_result = pd.MultiIndex.from_tuples(
            [("1", "AT1G06840_1", "AGAAA", "AT1G06840_1", "ref", 10, 15),
             ("1", "AT1G06840_1", "AGAAC", "AT1G06840_1", 0, 10, 15),
             ("1", "AT1G06840_1", "AGAA", "AT1G06840_1", 1, 10, 15),
             ("1", "AT1G06840_1", "AGAAT", "AT1G06840_1", 0, 10, 15),
             ("1", "AT1G06840_1", "AGAGAT", "AT1G06840_1", -1, 10, 15)],
            names=["Reference", "Locus", "Haplotypes", "target", 'edit', 'start', 'end'])

        result_table = pd.DataFrame(data={"sample1": [np.nan, 100.0, 15.0, 100.0, 10.0],
                                          "sample2": [np.nan, 80.0, 20.0, 100.0, 100.0]},
                                    index=row_index_result)
        table = pd.DataFrame(data=self.table_data,
                             index=row_index)
        self.haplotype_table = HaplotypeTable(table)
        gff = Gff.read_file(StringIO(self.borders))
        modification = HaplotypePosition(gff, StringIO(self.reference))
        locus = modification.modify(self.haplotype_table.dataframe, logging.getLogger)
        pd.testing.assert_frame_equal(locus.dataframe, result_table)

    def test_locus_missing_border_raises(self):
        self.borders = dedent("""\
                                 foo	SMAP	CRISPR_F_border	1	10	.	+	.	NAME=foo_1
                                 foo	SMAP	CRISPR_R_border	16	21	.	+	.	NAME=foo_1
                                 """)
        gff = Gff.read_file(StringIO(self.borders))
        modification = HaplotypePosition(gff, StringIO(self.reference))
        error_message = r"No borders were found for locus AT1G06840_1\."
        with self.assertRaisesRegex(ValueError, error_message):
            modification.modify(self.haplotype_table.dataframe, logging.getLogger)

    def test_wrong_number_of_borders_raises(self):
        self.borders = dedent("""\
                                 AT1G06840	SMAP	CRISPR_F_border	1	10	.	+	.	NAME=AT1G06840_1
                                 AT1G06840	SMAP	CRISPR_R_border	16	21	.	+	.	NAME=AT1G06840_1
                                 AT1G06840	SMAP	CRISPR_R_border	16	21	.	+	.	NAME=AT1G06840_1
                                 """)
        gff = Gff.read_file(StringIO(self.borders))
        modification = HaplotypePosition(gff, StringIO(self.reference))
        error_message = r"Found 3 borders for locus AT1G06840_1, expected 2\."
        with self.assertRaisesRegex(ValueError, error_message):
            modification.modify(self.haplotype_table.dataframe, logging.getLogger)

    def test_borders_do_not_share_chromosome_raises(self):
        self.borders = dedent("""\
                                 bar	SMAP	CRISPR_F_border	1	10	.	+	.	NAME=AT1G06840_1
                                 foo	SMAP	CRISPR_R_border	16	21	.	+	.	NAME=AT1G06840_1
                                 """)
        gff = Gff.read_file(StringIO(self.borders))
        modification = HaplotypePosition(gff, StringIO(self.reference))
        error_message = r"The borders for AT1G06840_1 do not share the same chromosome"
        with self.assertRaisesRegex(ValueError, error_message):
            modification.modify(self.haplotype_table.dataframe, logging.getLogger)

    def test_borders_start_after_stop_raises(self):
        self.borders = dedent("""\
                                 AT1G06840	SMAP	CRISPR_F_border	10	1	.	+	.	NAME=AT1G06840_1
                                 AT1G06840	SMAP	CRISPR_R_border	16	21	.	+	.	NAME=AT1G06840_1
                                 """)
        gff = Gff.read_file(StringIO(self.borders))
        modification = HaplotypePosition(gff, StringIO(self.reference))
        error_message = r"Malformatted \.gff"
        with self.assertRaisesRegex(ValueError, error_message):
            modification.modify(self.haplotype_table.dataframe, logging.getLogger)

        with tempfile.NamedTemporaryFile() as temp_file:
            with open(temp_file.name, 'w') as open_tf:
                open_tf.write(self.borders)
            with open(temp_file.name, 'r') as open_tf:
                gff = Gff.read_file(open_tf)
                modification = HaplotypePosition(gff, StringIO(self.reference))
                error_message = fr"Gff file {temp_file.name} has an incorrect format\."
                with self.assertRaisesRegex(ValueError, error_message):
                    modification.modify(self.haplotype_table.dataframe, logging.getLogger)

    def test_missing_reference_sequence_raises(self):
        reference = dedent("""\
                           >foo
                           ACGT
                           """)
        gff = Gff.read_file(StringIO(self.borders))
        modification = HaplotypePosition(gff, StringIO(reference))
        with self.assertRaisesRegex(ValueError, (r"Could not find genomic sequence with "
                                                 r"ID AT1G06840 in input \.fasta file\.")):
            modification.modify(self.haplotype_table.dataframe, logging.getLogger)


class TestGuideAnnotation(TestCase):
    def setUp(self) -> None:
        self.gRNAs = dedent("""\
                                locus1	SMAP	Guide	1138	1161	\
                                .	+	.	NAME=locus1_1	POOL=pool108_3	SEQ=dolor
                                locus1	SMAP	Guide	3251	3274	.	+	\
                                .	NAME=locus1_2	POOL=pool108_3	SEQ=sit
                                locus1	SMAP	Guide	4371	4394	.	+	\
                                .	NAME=locus1_3	POOL=pool108_3	SEQ=amet
                                """)
        index_data = [("1", "locus1_1", "foo", "locus1_1", pd.NA, ((1158, 'CT', 'C'),)),
                      ("1", "locus1_1", "bar", "locus1_1", ((1158, 'C', 'G'),), pd.NA),
                      ("1", "locus1_1", "lorem", "locus1_1", pd.NA, ((1138, 'A', 'AT'),)),
                      ("1", "locus1_1", "ipsum", "locus1_1", pd.NA, pd.NA)]
        row_index = pd.MultiIndex.from_tuples(index_data,
                                              names=[CHROMOSOME_COLUMN_NAME,
                                                     LOCUS_COLUMN_NAME,
                                                     HAPLOTYPE_COLUMN_NAME,
                                                     TARGET_COLUMN_NAME,
                                                     SNP_COLUMNNAME,
                                                     INDEL_COLUMNNAME])

        table_data = {"sample1": [100.0, 15.0, 100.0, 10.0], "sample2": [80.0, 20.0, 100.0, 100.0]}
        self.table_data = table_data
        table = pd.DataFrame(data=table_data,
                             index=row_index)
        self.haplotype_table = HaplotypeTable(table)

    def test_reverse_guide(self):
        gRNAs_data = dedent("""\
                                        locus1	SMAP	Guide	1138	1161	\
                                        .	-	.	NAME=locus1_1	POOL=pool108_3	SEQ=dolor""")

        index_data = [("1", "locus1_1", "foo", "locus1_1", pd.NA, ((1156, 'CT', 'C'),)),
                      ("1", "locus1_1", "bar", "locus1_1", ((1161, 'C', 'G'),), pd.NA),
                      ("1", "locus2_1", "lorem", "locus2_1", pd.NA, ((1148, 'A', 'AT'),)),
                      ("1", "locus2_1", "ipsum", "locus2_1", pd.NA, pd.NA)]
        row_index = pd.MultiIndex.from_tuples(index_data,
                                              names=[CHROMOSOME_COLUMN_NAME,
                                                     LOCUS_COLUMN_NAME,
                                                     HAPLOTYPE_COLUMN_NAME,
                                                     TARGET_COLUMN_NAME,
                                                     SNP_COLUMNNAME,
                                                     INDEL_COLUMNNAME])

        table_data = {"sample1": [100.0, 15.0, 100.0, 10.0], "sample2": [80.0, 20.0, 100.0, 100.0]}
        table = pd.DataFrame(data=table_data,
                             index=row_index)

        haplotype_table = HaplotypeTable(table)
        gRNAs_strio = StringIO(gRNAs_data)
        gRNAs = Gff.read_file(gRNAs_strio)
        mod = AddGuideFilter(gRNAs, 3, 7, 7, True)
        result = mod.modify(haplotype_table.dataframe, logging.getLogger).dataframe.reset_index()
        self.assertEqual(result['Expected cut site'].tolist()[0], 1158)
        self.assertEqual(result['Haplotype_Name'].tolist()[0], '0:1D:CT-C')

    def test_reverse_guide_reference_based(self):
        gRNAs_data = dedent("""\
                                           locus1	SMAP	Guide	1138	1161	\
                                           .	-	.	NAME=locus1_1	POOL=pool108_3	SEQ=dolor""")

        index_data = [("1", "locus1_1", "foo", "locus1_1", pd.NA, ((1156, 'CT', 'C'),)),
                      ("1", "locus1_1", "bar", "locus1_1", ((1161, 'C', 'G'),), pd.NA),
                      ("1", "locus2_1", "lorem", "locus2_1", pd.NA, ((1148, 'A', 'AT'),)),
                      ("1", "locus2_1", "ipsum", "locus2_1", pd.NA, pd.NA)]
        row_index = pd.MultiIndex.from_tuples(index_data,
                                              names=[CHROMOSOME_COLUMN_NAME,
                                                     LOCUS_COLUMN_NAME,
                                                     HAPLOTYPE_COLUMN_NAME,
                                                     TARGET_COLUMN_NAME,
                                                     SNP_COLUMNNAME,
                                                     INDEL_COLUMNNAME])

        table_data = {"sample1": [100.0, 15.0, 100.0, 10.0], "sample2": [80.0, 20.0, 100.0, 100.0]}
        table = pd.DataFrame(data=table_data,
                             index=row_index)

        haplotype_table = HaplotypeTable(table)
        gRNAs_strio = StringIO(gRNAs_data)
        gRNAs = Gff.read_file(gRNAs_strio)
        mod = AddGuideFilter(gRNAs, 3, 7, 7, False)
        result = mod.modify(haplotype_table.dataframe, logging.getLogger).dataframe.reset_index()
        self.assertEqual(result['Expected cut site'].tolist()[0], 1158)
        self.assertEqual(result['Haplotype_Name'].tolist()[0], '0:1D:CT-C')

    def test_guide_error_strand(self):
        gRNAs_data = dedent("""locus1	SMAP	Guide	1138	1161	\
                                .	.	.	NAME=locus1_1	POOL=pool108_3	SEQ=dolor""")

        gRNAs_strio = StringIO(gRNAs_data)
        gRNAs = Gff.read_file(gRNAs_strio)
        mod = AddGuideFilter(gRNAs, 3, 7, 7, True)
        msg = (r'gRNA for locus1_1 did not have a strand defined\. '
               r'Please define the strandedness of your gRNA')
        with self.assertRaisesRegex(ValueError, expected_regex=msg):
            mod.modify(self.haplotype_table.dataframe, logging.getLogger)

    def test_guide_error_multiple(self):
        gRNAs_data = dedent("""locus1	SMAP	Guide	1138	1161	\
                                .	-	.	NAME=locus1_1	POOL=pool108_3	SEQ=dolor
                                locus1	SMAP	Guide	1111	2222	\
                                .	-	.	NAME=locus1_1	POOL=pool108_3	SEQ=dolor""")

        gRNAs_strio = StringIO(gRNAs_data)
        gRNAs = Gff.read_file(gRNAs_strio)
        mod = AddGuideFilter(gRNAs, 3, 7, 7, True)
        msg = r'You have provided 2 gRNAs for locus1_1\. Please provide exactly one gRNA per locus'
        with self.assertRaisesRegex(ValueError, expected_regex=msg):
            mod.modify(self.haplotype_table.dataframe, logging.getLogger)

    def test_add_guide_annotation_positive_offset(self):
        index_data = [("1", "locus1_1", "foo", "locus1_1",
                       pd.NA, ((1158, 'CT', 'C'),), False, pd.NA, False, "20:1D:CT-C", 1140),
                      ("1", "locus1_1", "bar", "locus1_1",
                       ((1158, 'C', 'G'),), pd.NA, pd.NA, False, False, "20:S:C-G", 1140),
                      ("1", "locus1_1", "lorem", "locus1_1",
                       pd.NA, ((1138, 'A', 'AT'),), True, pd.NA, True, "0:1I:A-AT", 1140),
                      ("1", "locus1_1", "ipsum", "locus1_1",
                       pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, "ref", 1140)]
        expected_index = pd.MultiIndex.from_tuples(index_data,
                                                   names=[CHROMOSOME_COLUMN_NAME,
                                                          LOCUS_COLUMN_NAME,
                                                          HAPLOTYPE_COLUMN_NAME,
                                                          TARGET_COLUMN_NAME,
                                                          SNP_COLUMNNAME,
                                                          INDEL_COLUMNNAME,
                                                          GUIDE_FILTER_INDEL_COLUMNAME,
                                                          GUIDE_FILTER_SNP_COLUMNAME,
                                                          GUIDE_FILTER_COLUMNAME,
                                                          HAPLOTYPE_NAME,
                                                          EXPECTED_CUT_SITE_COLUM_NAME])

        expected_df = pd.DataFrame({"sample1": [100.0, 15.0, 100.0, 10.0],
                                    "sample2": [80.0, 20.0, 100.0, 100.0]},
                                   index=expected_index)
        gRNAs_strio = StringIO(self.gRNAs)
        gRNAs = Gff.read_file(gRNAs_strio)
        mod = AddGuideFilter(gRNAs, 3, 7, 7, True)
        result = mod.modify(self.haplotype_table.dataframe, logging.getLogger)
        pd.testing.assert_frame_equal(result.dataframe, expected_df)

    def test_operates_on(self):
        result = AddGuideFilter.operates_on()
        self.assertEqual(result, ModificationType.LOCI)


class TestHaplotypeName(TestCase):
    def setUp(self) -> None:
        index_data = [("locus1_1", "foo", "locus1_1", pd.NA, ((1158, 'CT', 'C'),)),
                      ("locus1_1", "bar", "locus1_1", ((1158, 'C', 'G'),), ((1148, 'CGG', 'G'),)),
                      ("locus1_1", "lorem", "locus1_1", pd.NA, ((1138, 'A', 'AT'),)),
                      ("locus1_1", "ipsum", "locus1_1", pd.NA, pd.NA)]
        row_index = pd.MultiIndex.from_tuples(index_data,
                                              names=[LOCUS_COLUMN_NAME,
                                                     HAPLOTYPE_COLUMN_NAME,
                                                     TARGET_COLUMN_NAME,
                                                     SNP_COLUMNNAME,
                                                     INDEL_COLUMNNAME])

        table_data = {"sample1": [100.0, 15.0, 100.0, 10.0], "sample2": [80.0, 20.0, 100.0, 100.0]}
        self.table_data = table_data
        table = pd.DataFrame(data=table_data,
                             index=row_index)
        self.haplotype_table = HaplotypeTable(table)

    def test_haplotype_name(self):
        haplotype_table = self.haplotype_table
        mod = AddHaploTypeName()
        result = mod.modify(haplotype_table.dataframe, logging.getLogger)

        mod_2 = Collapse(7, 7)
        coll = mod_2.modify(result.dataframe, logging.getLogger)
        expected_names = ['locus1_1_1158:1D:CT-C', 'locus1_1_1148:2D:CGG-G,1158:S:C-G',
                          'locus1_1_1138:1I:A-AT', 'locus1_1_ref']
        self.assertEqual(coll.dataframe.reset_index()['Haplotype'].tolist(), expected_names)


class TestEffectAnnotation(TestCase):
    def setUp(self) -> None:
        self.frequency_table_index = pd.MultiIndex.from_tuples([('locus1', 'hap1', 'tar1', 100),
                                                                ('locus1', 'hap2', 'tar2', 80),
                                                                ('locus1', 'hap3', 'tar3', 0),
                                                                ('locus2', 'hap4', 'tar4', 100),
                                                                ('locus2', 'hap5', 'tar5', 99),
                                                                ('locus3', 'hap6', 'tar6', 100)],
                                                               names=[LOCUS_COLUMN_NAME,
                                                                      HAPLOTYPE_COLUMN_NAME,
                                                                      TARGET_COLUMN_NAME,
                                                                      'pairwiseProteinIdentity (%)'
                                                                      ])

        self.frequency_table = pd.DataFrame([(50, 0, 20),
                                             (40, 0, 20),
                                             (10, 100, 60),
                                             (100, pd.NA, 50),
                                             (0, 0.5, 50),
                                             (100, pd.NA, 1)],
                                            columns=['bam1', 'bam2', 'bam3'],
                                            index=self.frequency_table_index)

    def test_effect_annotation(self):
        expected_index = pd.MultiIndex.from_tuples([('locus1', 'hap1', 'tar1', 100, False),
                                                    ('locus1', 'hap2', 'tar2', 80, True),
                                                    ('locus1', 'hap3', 'tar3', 0, True),
                                                    ('locus2', 'hap4', 'tar4', 100, False),
                                                    ('locus2', 'hap5', 'tar5', 99, False),
                                                    ('locus3', 'hap6', 'tar6', 100, False)],
                                                   names=[LOCUS_COLUMN_NAME,
                                                          HAPLOTYPE_COLUMN_NAME,
                                                          TARGET_COLUMN_NAME,
                                                          'pairwiseProteinIdentity (%)',
                                                          'Effect'])
        effect_annotation = EffectAnnotation('pairwiseProteinIdentity (%)', 80)
        result = effect_annotation.modify(self.frequency_table, logging.getLogger)
        expected = self.frequency_table.set_index(expected_index, inplace=False)
        pd.testing.assert_frame_equal(result.dataframe, expected)

    def test_effect_annotation_without_protein_prediction(self):
        self.frequency_table_index = pd.MultiIndex.from_tuples([('locus1', 'hap1', 'tar1', False),
                                                                ('locus1', 'hap2', 'tar2', True),
                                                                ('locus1', 'hap3', 'tar3', True),
                                                                ('locus2', 'hap4', 'tar4', False),
                                                                ('locus2', 'hap5', 'tar5', False),
                                                                ('locus3', 'hap6', 'tar6', False)],
                                                               names=[LOCUS_COLUMN_NAME,
                                                                      HAPLOTYPE_COLUMN_NAME,
                                                                      TARGET_COLUMN_NAME,
                                                                      GUIDE_FILTER_COLUMNAME
                                                                      ])
        self.frequency_table.index = self.frequency_table_index
        expected_index = pd.MultiIndex.from_tuples([('locus1', 'hap1', 'tar1', False, False),
                                                    ('locus1', 'hap2', 'tar2', True, True),
                                                    ('locus1', 'hap3', 'tar3', True, True),
                                                    ('locus2', 'hap4', 'tar4', False, False),
                                                    ('locus2', 'hap5', 'tar5', False, False),
                                                    ('locus3', 'hap6', 'tar6', False, False)],
                                                   names=[LOCUS_COLUMN_NAME,
                                                          HAPLOTYPE_COLUMN_NAME,
                                                          TARGET_COLUMN_NAME,
                                                          GUIDE_FILTER_COLUMNAME,
                                                          'Effect'])
        effect_annotation = EffectAnnotation('pairwiseProteinIdentity (%)', 80)
        result = effect_annotation.modify(self.frequency_table, logging.getLogger)
        expected = self.frequency_table.set_index(expected_index, inplace=False)
        pd.testing.assert_frame_equal(result.dataframe, expected)

    def test_operates_on(self):
        result = EffectAnnotation.operates_on()
        self.assertEqual(result, ModificationType.LOCI)


class TestDNAPairwiseAlignment(TestCase):
    def test_equality(self):
        alignment = DNAPairwiseAlignment('CACTTGCC', 'CACTGCC',
                                         ((0, 0), (3, 3), (4, 3), (8, 7)), 0, 0)
        alignment2 = DNAPairwiseAlignment('CACTTGCC', 'CACTGCC',
                                          ((0, 0), (3, 3), (4, 3), (8, 7)), 0, 0)
        self.assertEqual(alignment, alignment2)

    def test_inequality(self):
        alignment = DNAPairwiseAlignment('CACTTGCC', 'CACTGCC',
                                         ((0, 0), (3, 3), (4, 3), (8, 7)), 0, 0)
        alignment2 = DNAPairwiseAlignment('CACTTGCC', 'CACTGCC',
                                          ((0, 0), (3, 3), (4, 3), (8, 7)), 0, 1)
        self.assertNotEqual(alignment, alignment2)

    def test_inequality_not_an_dna_alignment(self):
        alignment = DNAPairwiseAlignment('CACTTGCC', 'CACTGCC',
                                         ((0, 0), (3, 3), (4, 3), (8, 7)), 0, 0)
        second_object = PairwiseAlignment('CACTTGCC', 'CACTGCC',
                                          ((0, 0), (3, 3), (4, 3), (8, 7)), 0)
        self.assertNotEqual(alignment, second_object)

    def test_hashing(self):
        alignment = DNAPairwiseAlignment('CACTTGCC', 'CACTGCC',
                                         ((0, 0), (3, 3), (4, 3), (8, 7)), 0, 0)
        alignment2 = DNAPairwiseAlignment('CACTTGCC', 'CACTGCC',
                                          ((0, 0), (3, 3), (4, 3), (8, 7)), 0, 1)
        result = set((alignment, alignment2))
        self.assertEqual(len(result), 2)

    def test_from_biopython_object(self):
        biopython_obj = PairwiseAlignment('CACTTGCC', 'CACTGCC',
                                          ((0, 0), (3, 3), (4, 3), (8, 7)), 0)
        DNAPairwiseAlignment.from_alignment(biopython_obj, 3)

    def test_indel_target(self):
        repr_result = dedent("""\
                             CACTTGCC
                             |||-||||
                             CAC-TGCC
                             """)
        alignment = DNAPairwiseAlignment('CACTTGCC', 'CACTGCC',
                                         ((0, 0), (3, 3), (4, 3), (8, 7)), 0, 0)
        indels = alignment.indels()
        self.assertEqual(f"{alignment}", repr_result)
        self.assertEqual(((3, 'CT', 'C'), ), indels)

    def test_indel_query(self):
        repr_result = dedent("""\
                             CAC-TGCC
                             |||-||||
                             CACTTGCC
                             """)
        alignment = DNAPairwiseAlignment('CACTGCC', 'CACTTGCC',
                                         ((0, 0), (3, 3), (3, 4), (7, 8)), 0, 0)
        indels = alignment.indels()
        self.assertEqual(f"{alignment}", repr_result)
        self.assertEqual(((3, 'C', 'CT'), ), indels)

    def test_snp(self):
        repr_result = dedent("""\
                             CACATGCC
                             |||.||||
                             CACTTGCC
                             """)
        alignment = DNAPairwiseAlignment('CACATGCC', 'CACTTGCC',
                                         ((0, 0), (8, 8)), 0, 0)
        self.assertEqual(f"{alignment}", repr_result)
        snps = alignment.snps()
        self.assertEqual(((3, 'A', 'T'), ), snps)

    def test_indel_at_start(self):
        repr_result = dedent("""\
                             -ACTTGCC
                             -|||||||
                             CACTTGCC
                             """)
        alignment = DNAPairwiseAlignment('ACTTGCC', 'CACTTGCC',
                                         ((0, 0), (0, 1), (7, 8)), 0, 0)
        self.assertEqual(f"{alignment}", repr_result)
        indels = alignment.indels()
        self.assertEqual(((0, '', 'C'), ), indels)

        repr_result = dedent("""\
                             --ACTTGCC
                             --|||||||
                             CCACTTGCC
                             """)
        alignment = DNAPairwiseAlignment('ACTTGCC', 'CCACTTGCC',
                                         ((0, 0), (0, 2), (7, 9)), 0, 0)
        self.assertEqual(f"{alignment}", repr_result)
        indels = alignment.indels()
        self.assertEqual(((0, '', 'CC'), ), indels)

    def test_indel_both_target_query(self):
        repr_result = dedent("""\
                             CACTT-CC
                             --|||-|-
                             --CTTGC-
                             """)
        alignment = DNAPairwiseAlignment('CACTTCC', 'CTTGC',
                                         ((0, 0), (2, 0), (5, 3), (5, 4), (6, 5), (7, 5)), 0, 0)
        self.assertEqual(f"{alignment}", repr_result)
        indels = alignment.indels()
        self.assertEqual(((0, 'CA', ''), (5, 'T', 'TG'), (6, 'CC', 'C-')), indels)

        repr_result = dedent("""\
                             CACTT-CC
                             ---||-|-
                             ---TTGC-
                             """)
        alignment = DNAPairwiseAlignment('CACTTCC', 'TTGC',
                                         ((0, 0), (3, 0), (5, 2), (5, 3), (6, 4), (7, 4)), 0, 0)
        self.assertEqual(f"{alignment}", repr_result)
        indels = alignment.indels()
        self.assertEqual(((0, 'CAC', ''), (5, 'T', 'TG'), (6, 'CC', 'C-')), indels)

    def test_indel_at_end(self):
        repr_result = dedent("""\
                             CACTTGCC-
                             ||||||||-
                             CACTTGCCG
                             """)
        alignment = DNAPairwiseAlignment('CACTTGCC', 'CACTTGCCG',
                                         ((0, 0), (8, 8), (8, 9)), 0, 0)
        self.assertEqual(f"{alignment}", repr_result)
        indels = alignment.indels()
        self.assertEqual(((8, 'C-', 'CG'), ), indels)

        repr_result = dedent("""\
                             CACTTGCC--
                             ||||||||--
                             CACTTGCCGG
                             """)
        alignment = DNAPairwiseAlignment('CACTTGCC', 'CACTTGCCGG',
                                         ((0, 0), (8, 8), (8, 10)), 0, 0)
        self.assertEqual(f"{alignment}", repr_result)
        indels = alignment.indels()
        self.assertEqual(((8, 'C--', 'CGG'), ), indels)

        repr_result = dedent("""\
                             CACTTGCCG
                             ||||||||-
                             CACTTGCC-
                             """)
        alignment = DNAPairwiseAlignment('CACTTGCCG', 'CACTTGCC',
                                         ((0, 0), (8, 8), (9, 8)), 0, 0)
        self.assertEqual(f"{alignment}", repr_result)
        indels = alignment.indels()
        self.assertEqual(((8, 'CG', 'C-'), ), indels)

    def test_multiple_indels_target(self):
        repr_result = dedent("""\
                             --CTT-CC
                             --|||-||
                             CACTTGCC
                             """)
        alignment = DNAPairwiseAlignment('CTTCC', 'CACTTGCC',
                                         ((0, 0), (0, 2), (3, 5), (3, 6), (5, 8)), 0, 0)
        self.assertEqual(f"{alignment}", repr_result)
        indels = alignment.indels()
        self.assertEqual(((0, '', 'CA'), (3, 'T', 'TG')), indels)

    def test_multiple_indels_query(self):
        repr_result = dedent("""\
                             CACTTGCC
                             --|||-||
                             --CTT-CC
                             """)
        alignment = DNAPairwiseAlignment('CACTTGCC', 'CTTCC',
                                         ((0, 0), (2, 0), (5, 3), (6, 3), (8, 5)), 0, 0)
        self.assertEqual(f"{alignment}", repr_result)
        indels = alignment.indels()
        self.assertEqual(((0, 'CA', ''), (5, 'TG', 'T')), indels)

    def test_get_coordinates_multiple_indels_in_query(self):
        # CACTTGCC
        # --|||-||
        # --CTT-CC
        alignment = DNAPairwiseAlignment('CACTTGCC', 'CTTCC',
                                         ((0, 0), (2, 0), (5, 3), (6, 3), (8, 5)), 0, 0)
        for coordinate in range(0, 7):
            result = alignment.get_alignment_coordinate(coordinate, boundary_type="start")
            self.assertEqual(result, coordinate)

    def test_get_coordinates_multiple_indels_target(self):
        # --CTT-CC
        # --|||-||
        # CACTTGCC
        alignment = DNAPairwiseAlignment('CTTCC', 'CACTTGCC',
                                         ((0, 0), (0, 2), (3, 5), (3, 6), (5, 8)), 0, 0)
        coordinate_expected_start = {0: 0, 1: 3, 2: 4, 3: 5, 4: 7}
        for coordinate, expected in coordinate_expected_start.items():
            result = alignment.get_alignment_coordinate(coordinate, boundary_type="start")
            self.assertEqual(result, expected)

        coordinate_expected_end = {0: 2, 1: 3, 2: 5, 3: 6, 4: 7}
        for coordinate, expected in coordinate_expected_end.items():
            result = alignment.get_alignment_coordinate(coordinate, boundary_type="end")
            self.assertEqual(result, expected)

    def test_coordinates_indels_at_end(self):
        # CACTTGCC-
        # ||||||||-
        # CACTTGCCG
        alignment = DNAPairwiseAlignment('CACTTGCC', 'CACTTGCCG',
                                         ((0, 0), (8, 8), (8, 9)), 0, 0)
        result = alignment.get_alignment_coordinate(7, 'start')
        self.assertEqual(result, 7)
        # CACTTGCC--
        # ||||||||--
        # CACTTGCCGG
        alignment = DNAPairwiseAlignment('CACTTGCC', 'CACTTGCCGG',
                                         ((0, 0), (8, 8), (8, 10)), 0, 0)
        result = alignment.get_alignment_coordinate(7, 'start')
        self.assertEqual(result, 7)

    def test_get_coordinates_indels_at_start(self):
        # -ACTTGCC
        # -|||||||
        # CACTTGCC
        alignment = DNAPairwiseAlignment('ACTTGCC', 'CACTTGCC',
                                         ((0, 0), (0, 1), (7, 8)), 0, 0)
        result = alignment.get_alignment_coordinate(0, 'start')
        self.assertEqual(result, 0)

    def test_get_coordinated_multiple_indels_in_target(self):
        # CACTTGCC
        # ||||||||
        # CA---GCC
        alignment = DNAPairwiseAlignment('CACTTGCC', 'CAGCC',
                                         ((0, 0), (2, 2), (5, 2), (8, 10)), 0, 0)
        coordinate_expected_start = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7}
        for coordinate, expected in coordinate_expected_start.items():
            result = alignment.get_alignment_coordinate(coordinate, boundary_type="start")
            self.assertEqual(result, expected)

    def test_get_coordinate_out_of_range(self):
        alignment = DNAPairwiseAlignment('ACTTGCC', 'CACTTGCC',
                                         ((0, 0), (0, 1), (7, 8)), 0, 0)
        with self.assertRaises(ValueError):
            alignment.get_alignment_coordinate(-1, 'start')
        with self.assertRaises(ValueError):
            alignment.get_alignment_coordinate(8, 'start')

    def test_boundry_type_wrong_value(self):
        alignment = DNAPairwiseAlignment('ACTTGCC', 'CACTTGCC',
                                         ((0, 0), (0, 1), (7, 8)), 0, 0)
        with self.assertRaises(ValueError):
            alignment.get_alignment_coordinate(-1, 'foo')


class TestPairWiseAlignmentModification(TestCase):
    def setUp(self) -> None:
        table_data = [('locus1', 'CACATGCC', 'tar1', 'ref', 0),
                      ('locus1', 'CACTTGCC', 'tar2', '0', 0),
                      ('locus1', 'CACGCC', 'tar3', '-1', 0)]
        self.frequency_table_index = pd.MultiIndex.from_tuples(table_data,
                                                               names=[LOCUS_COLUMN_NAME,
                                                                      HAPLOTYPE_COLUMN_NAME,
                                                                      TARGET_COLUMN_NAME,
                                                                      REFERENCE_COLUMN_NAME,
                                                                      START_COLUMN_NAME
                                                                      ])

        self.frequency_table = pd.DataFrame([(50, 0, 20),
                                             (40, 0, 20),
                                             (10, 100, 60)],
                                            columns=['bam1', 'bam2', 'bam3'],
                                            index=self.frequency_table_index)

    def test_pairwise_alignment(self):
        modification = PairwiseAlignmentAnnotation(1, -100, -100, -10)
        result = modification.modify(self.frequency_table, logging.getLogger)
        expected_alignment1 = DNAPairwiseAlignment('CACATGCC', 'CACTTGCC',
                                                   ((0, 0), (8, 8)), -93, 0)
        expected_alignment2 = DNAPairwiseAlignment('CACATGCC', 'CACGCC',
                                                   ((0, 0), (3, 3), (5, 3), (8, 6)), -104, 0)
        index_data = [('locus1', 'CACATGCC', 'tar1',
                       'ref', 0, pd.NA, pd.NA, pd.NA),
                      ('locus1', 'CACTTGCC', 'tar2',
                       '0', 0, ((3, 'A', 'T'),), (), expected_alignment1),
                      ('locus1', 'CACGCC', 'tar3',
                       '-1', 0, (), ((3, 'CAT', 'C'),), expected_alignment2)]
        expected_index = pd.MultiIndex.from_tuples(index_data,
                                                   names=[LOCUS_COLUMN_NAME,
                                                          HAPLOTYPE_COLUMN_NAME,
                                                          TARGET_COLUMN_NAME,
                                                          REFERENCE_COLUMN_NAME,
                                                          START_COLUMN_NAME,
                                                          SNP_COLUMNNAME,
                                                          INDEL_COLUMNNAME,
                                                          ALIGNMENT_COLUMNNAME])
        expected = self.frequency_table.set_index(expected_index, inplace=False)
        pd.testing.assert_frame_equal(result.dataframe,
                                      expected)

    def test_operates_on(self):
        result = PairwiseAlignmentAnnotation.operates_on()
        self.assertEqual(result, ModificationType.LOCI)


class TestProteinPrediction(TestCase):
    def setUp(self) -> None:
        self.reference_index_entry = ('1', 'locus1', 'CCCATGGTACAGTTAGTAAAAGTAA',
                                      'mock_haplotype_ref', 'tar1', 'ref', pd.NA, 0,
                                      pd.NA, pd.NA, 0)
        self.expected_cut_site = 6
        self.start_in_reference = 0
        self.index_column_names = (CHROMOSOME_COLUMN_NAME,
                                   LOCUS_COLUMN_NAME,
                                   HAPLOTYPE_COLUMN_NAME,
                                   HAPLOTYPE_NAME,
                                   TARGET_COLUMN_NAME,
                                   REFERENCE_COLUMN_NAME,
                                   ALIGNMENT_COLUMNNAME,
                                   START_COLUMN_NAME,
                                   SNP_COLUMNNAME,
                                   INDEL_COLUMNNAME,
                                   EXPECTED_CUT_SITE_COLUM_NAME)
        self.new_column_names = ['atgCheck',
                                 'splicingSiteCheck',
                                 'stopCodonCheck',
                                 'protein_sequence',
                                 'pairwiseProteinIdentity (%)']
        self.frequency_table = pd.DataFrame([(50, 100, 13.5),
                                             (10, 0, 13.5)],
                                            columns=['bam1', 'bam2', 'bam3'])
        annotation_content = dedent("""\
                                    1	unittest	gene	1	25	.	+	.
                                    1	unittest	CDS	4	6	.	+	0	Name=foo
                                    1	unittest	CDS	13	15	.	+	0	Name=bar
                                    1	unittest	CDS	23	25	.	+	0	Name=lorem
                                    """)
        one_cds_annotation_content = dedent("""\
                                            1	unittest	gene	1	25	.	+	.
                                            1	unittest	CDS	4	25	.	+	0	Name=foo
                                            """)
        self.annotation = tempfile.NamedTemporaryFile('w')
        self.annotation.write(annotation_content)
        self.annotation.seek(0)
        self.one_cds_annotation = tempfile.NamedTemporaryFile('w')
        self.one_cds_annotation.write(one_cds_annotation_content)
        self.one_cds_annotation.seek(0)
        reference_content = dedent("""\
                                   >1
                                   CCCATGGTACAGTTAGTAAAAGTAA
                                   """)
        self.reference = StringIO(reference_content)

    def build_df_from_alignment(self, alignment):
        reference_diff = len(alignment.target) - len(alignment.query)
        index_entry = ('1', 'locus1', alignment.target, 'mock_haplotype_mut', 'tar1',
                       reference_diff, alignment, alignment.reference_start, alignment.snps(),
                       alignment.indels(), self.expected_cut_site)
        index = pd.MultiIndex.from_tuples([self.reference_index_entry,
                                           index_entry], names=self.index_column_names)
        return self.frequency_table.set_index(index, inplace=False)

    def add_new_columns_to_multiindex(self, new_columns, df):
        new_columns_df = pd.DataFrame(new_columns,
                                      columns=self.new_column_names,
                                      index=df.index)
        expected = pd.concat([df, new_columns_df], axis=1)
        return expected.set_index(self.new_column_names, append=True)

    def tearDown(self) -> None:
        self.annotation.close()
        self.one_cds_annotation.close()

    def test_snp_in_start_codon(self):
        # 0001110000001110000000111
        # CCCATGGTACAGTTAGTAAAAGTAA
        # ||||.||||||||||||||||||||
        # CCCAGGGTACAGTTAGTAAAAGTAA
        #       |     cut site
        gRNA_options = [(
                            {'with_gRNAs': False, 'tp_range_lower': 0, 'tp_range_upper': 0},
                            (True, False, False, 'RL*', 0.0)
                         ),
                        (
                            {'with_gRNAs': True, 'tp_range_lower': 1, 'tp_range_upper': 1},
                            (False, False, False, 'ML*', 100.0)
                         )]
        for (gRNA_kwarg, result_entries) in gRNA_options:
            alignment = DNAPairwiseAlignment('CCCATGGTACAGTTAGTAAAAGTAA',
                                             'CCCAGGGTACAGTTAGTAAAAGTAA',
                                             ((0, 0), (25, 25)), 18.0, 0)
            df = self.build_df_from_alignment(alignment)
            expected = self.add_new_columns_to_multiindex([('', '', '', 'ML*', np.nan),
                                                           result_entries],
                                                          df)
            op = ProteinPrediction(self.annotation.name, self.reference, **gRNA_kwarg)
            result = op.modify(df, logging.getLogger)
            pd.testing.assert_frame_equal(result.dataframe, expected)

    def test_indel_in_exon(self):
        # 0001110000001110000000111
        # CCCATGGTACAGTTAGTAAAAGTAA
        # |||||||||-|||||||||||||||
        # CCCATGGTA-AGTTAGTAAAAGTAA
        #       |     cut site
        gRNA_options = [(
                            {'with_gRNAs': False, 'tp_range_lower': 0, 'tp_range_upper': 0},
                            (False, False, False, 'ML*', 100.0)
                         ),
                        (
                            {'with_gRNAs': True, 'tp_range_lower': 7, 'tp_range_upper': 7},
                            (False, False, False, 'ML*', 100.0)
                         )]
        alignment = DNAPairwiseAlignment('CCCATGGTACAGTTAGTAAAAGTAA',
                                         'CCCATGGTAAGTTAGTAAAAGTAA',
                                         ((0, 0), (9, 9), (10, 9), (25, 24)),
                                         -83.0, 0)
        df = self.build_df_from_alignment(alignment)
        for (gRNA_kwarg, result_entries) in gRNA_options:
            expected = self.add_new_columns_to_multiindex([('', '', '', 'ML*', np.nan),
                                                           result_entries],
                                                          df)
            op = ProteinPrediction(self.annotation.name, self.reference, **gRNA_kwarg)
            result = op.modify(df, logging.getLogger)
            pd.testing.assert_frame_equal(result.dataframe, expected)

    def test_indel_in_intron(self):
        # 0001110000001110000000111
        # CCCATGGTACAGTTAGTAAAAGTAA
        # |||||||||||||-|||||||||||
        # CCCATGGTACAGT-AGTAAAAGTAA
        #       |     cut site
        gRNA_options = [(
                            {'with_gRNAs': False, 'tp_range_lower': 0, 'tp_range_upper': 0},
                            (False, False, False, 'MYX*', 33.3)
                         ),
                        (
                            {'with_gRNAs': True, 'tp_range_lower': 1, 'tp_range_upper': 1},
                            (False, False, False, 'ML*', 100.0)
                         )]
        alignment = DNAPairwiseAlignment('CCCATGGTACAGTTAGTAAAAGTAA',
                                         'CCCATGGTACAGTAGTAAAAGTAA',
                                         ((0, 0), (13, 13), (14, 13), (25, 24)), -83.0, 0)
        df = self.build_df_from_alignment(alignment)
        for (gRNA_kwarg, result_entries) in gRNA_options:
            expected = self.add_new_columns_to_multiindex([('', '', '', 'ML*', np.nan),
                                                           result_entries],
                                                          df)
            op = ProteinPrediction(self.annotation.name, self.reference, **gRNA_kwarg)
            result = op.modify(df, logging.getLogger)
            pd.testing.assert_frame_equal(result.dataframe, expected)

    def test_snp_in_exon(self):
        # 0001110000001110000000111
        # CCCATGGTACAGTTAGTAAAAGTAA
        # ||||||||.||||||||||||||||
        # CCCATGGTGCAGTTAGTAAAAGTAA
        #       |     cut site

        gRNA_options = [(
                            {'with_gRNAs': False, 'tp_range_lower': 0, 'tp_range_upper': 0},
                            (False, False, False, 'ML*', 100.0)
                         ),
                        (
                            {'with_gRNAs': True, 'tp_range_lower': 1, 'tp_range_upper': 1},
                            (False, False, False, 'ML*', 100.0)
                         )]
        alignment = DNAPairwiseAlignment('CCCATGGTACAGTTAGTAAAAGTAA',
                                         'CCCATGGTGCAGTTAGTAAAAGTAA',
                                         ((0, 0), (25, 25)), 18.0, 0)
        df = self.build_df_from_alignment(alignment)
        for (gRNA_kwarg, result_entries) in gRNA_options:
            expected = self.add_new_columns_to_multiindex([('', '', '', 'ML*', np.nan),
                                                           result_entries],
                                                          df)
            op = ProteinPrediction(self.annotation.name, self.reference, **gRNA_kwarg)
            result = op.modify(df, logging.getLogger)
            pd.testing.assert_frame_equal(result.dataframe, expected)

    def test_snp_in_acceptor_site(self):
        # 0001110000001110000000111
        # CCCATGGTACAGTTAGTAAAAGTAA
        # ||||||||||.||||||||||||||
        # CCCATGGTACGGTTAGTAAAAGTAA
        #       |     cut site

        gRNA_options = [(
                            {'with_gRNAs': False, 'tp_range_lower': 0, 'tp_range_upper': 0},
                            (False, True, False, 'M*', 50.0)
                         ),
                        (
                            {'with_gRNAs': True, 'tp_range_lower': 1, 'tp_range_upper': 1},
                            (False, False, False, 'ML*', 100.0)
                         )]
        alignment = DNAPairwiseAlignment('CCCATGGTACAGTTAGTAAAAGTAA',
                                         'CCCATGGTACGGTTAGTAAAAGTAA',
                                         ((0, 0), (25, 25)), 18.0, 0)
        df = self.build_df_from_alignment(alignment)
        for (gRNA_kwarg, result_entries) in gRNA_options:
            expected = self.add_new_columns_to_multiindex([('', '', '', 'ML*', np.nan),
                                                           result_entries],
                                                          df)
            op = ProteinPrediction(self.annotation.name, self.reference, **gRNA_kwarg)
            result = op.modify(df, logging.getLogger)
            pd.testing.assert_frame_equal(result.dataframe, expected)

    def test_in_donor_site(self):
        # 0001110000001110000000111
        # CCCATGGTACAGTTAGTAAAAGTAA
        # |||||||.|||||||||||||||||
        # CCCATGGCACAGTTAGTAAAAGTAA
        #             |    cut site
        # Needed because the snp overlaps exactly
        # and the range would not have any effect otherwise
        self.expected_cut_site = 12
        gRNA_options = [(
                            {'with_gRNAs': False, 'tp_range_lower': 0, 'tp_range_upper': 0},
                            (False, True, False, 'M*', 50.0)
                         ),
                        (
                            {'with_gRNAs': True, 'tp_range_lower': 1, 'tp_range_upper': 1},
                            (False, False, False, 'ML*', 100.0)
                         )]
        for (gRNA_kwarg, result_entries) in gRNA_options:
            alignment = DNAPairwiseAlignment('CCCATGGTACAGTTAGTAAAAGTAA',
                                             'CCCATGGCACAGTTAGTAAAAGTAA',
                                             ((0, 0), (25, 25)), 18.0, 0)
            df = self.build_df_from_alignment(alignment)
            expected = self.add_new_columns_to_multiindex([('', '', '', 'ML*', np.nan),
                                                           result_entries],
                                                          df)
            op = ProteinPrediction(self.annotation.name, self.reference, **gRNA_kwarg)
            result = op.modify(df, logging.getLogger)
            pd.testing.assert_frame_equal(result.dataframe, expected)

    def test_indel_at_target_start(self):
        #  0001110000001110000000111
        # -CCCATGGTACAGTTAGTAAAAGTAA
        # -|||||||||||||||||||||||||
        # CCCCATGGTACAGTTAGTAAAAGTAA
        #       |     cut site

        gRNA_options = [(
                            {'with_gRNAs': False, 'tp_range_lower': 0, 'tp_range_upper': 0},
                            (False, False, False, 'ML*', 100.0)
                         ),
                        (
                            {'with_gRNAs': True, 'tp_range_lower': 1, 'tp_range_upper': 1},
                            (False, False, False, 'ML*', 100.0)
                         )]
        alignment = DNAPairwiseAlignment('CCCATGGTACAGTTAGTAAAAGTAA',
                                         'CCCCATGGTACAGTTAGTAAAAGTAA',
                                         ((0, 0), (0, 1), (25, 26)), -184.0, 0)
        df = self.build_df_from_alignment(alignment)
        for (gRNA_kwarg, result_entries) in gRNA_options:
            expected = self.add_new_columns_to_multiindex([('', '', '', 'ML*', np.nan),
                                                           result_entries],
                                                          df)
            op = ProteinPrediction(self.annotation.name, self.reference, **gRNA_kwarg)
            result = op.modify(df, logging.getLogger)
            pd.testing.assert_frame_equal(result.dataframe, expected)

    def test_indel_in_cds_at_range_start(self):
        # 0001110000001110000000111
        # CCCATGGTACAG-TAGTAAAAGTAA
        # |||||||||||||||||||||||||
        # CCCATGGTACAGTTAGTAAAAGTAA
        #       |     cut site
        alignment = DNAPairwiseAlignment('CCCATGGTACAGTAGTAAAAGTAA',
                                         'CCCATGGTACAGTTAGTAAAAGTAA',
                                         ((0, 0), (12, 12), (12, 13), (24, 25)), -184.0, 0)
        gRNA_options = [(
                            {'with_gRNAs': False, 'tp_range_lower': 0, 'tp_range_upper': 0},
                            (False, True, True, 'MLX*', 66.7)
                         ),
                        (
                            {'with_gRNAs': True, 'tp_range_lower': 1, 'tp_range_upper': 1},
                            (False, False, False, 'ML*', 100.0)
                         )]

        df = self.build_df_from_alignment(alignment)
        for (gRNA_kwarg, result_entries) in gRNA_options:
            expected = self.add_new_columns_to_multiindex([('', '', '', 'ML*', np.nan),
                                                           result_entries],
                                                          df)
            op = ProteinPrediction(self.annotation.name, self.reference, **gRNA_kwarg)
            result = op.modify(df, logging.getLogger)
            pd.testing.assert_frame_equal(result.dataframe, expected)

    def test_indel_in_cds_at_range_end(self):
        # 0001110000001110000000111
        # CCCATGGTACAGTT-GTAAAAGTAA
        # |||||||||||||||||||||||||
        # CCCATGGTACAGTTAGTAAAAGTAA
        #       |     cut site
        alignment = DNAPairwiseAlignment('CCCATGGTACAGTTGTAAAAGTAA',
                                         'CCCATGGTACAGTTAGTAAAAGTAA',
                                         ((0, 0), (14, 14), (14, 15), (24, 25)), -184.0, 0)
        gRNA_options = [(
                            {'with_gRNAs': False, 'tp_range_lower': 0, 'tp_range_upper': 0},
                            (False, True, True, 'MLX*', 66.7)
                         ),
                        (
                            {'with_gRNAs': True, 'tp_range_lower': 1, 'tp_range_upper': 1},
                            (False, False, False, 'ML*', 100.0)
                         )]

        df = self.build_df_from_alignment(alignment)
        for (gRNA_kwarg, result_entries) in gRNA_options:
            expected = self.add_new_columns_to_multiindex([('', '', '', 'ML*', np.nan),
                                                           result_entries],
                                                          df)
            op = ProteinPrediction(self.annotation.name, self.reference, **gRNA_kwarg)
            result = op.modify(df, logging.getLogger)
            pd.testing.assert_frame_equal(result.dataframe, expected)

    def test_indel_in_cds_at_range_end_cut_site_boundary_start(self):
        # 000111000000-111000000111
        # CCCATGGTACAG-TAGTAAAAGTAA
        # |||||||||||||||||||||||||
        # CCCATGGTACAGTTAGTAAAAGTAA
        #                   |     cut site
        self.expected_cut_site = 18
        alignment = DNAPairwiseAlignment('CCCATGGTACAGTAGTAAAAGTAA',
                                         'CCCATGGTACAGTTAGTAAAAGTAA',
                                         ((0, 0), (12, 12), (12, 13), (24, 25)), -184.0, 0)

        df = self.build_df_from_alignment(alignment)
        expected = self.add_new_columns_to_multiindex([('', '', '', 'ML*', np.nan),
                                                       (False, True, False, 'MLX*', 66.7)],
                                                      df)
        op = ProteinPrediction(self.annotation.name, self.reference,
                               with_gRNAs=True, tp_range_lower=6, tp_range_upper=1)
        result = op.modify(df, logging.getLogger)
        pd.testing.assert_frame_equal(result.dataframe, expected)

    def test_indel_in_cds_at_range_end_cut_site_boundary_end(self):
        # 000111000000-111000000111
        # CCCATGGTACAG-TAGTAAAAGTAA
        # |||||||||||||||||||||||||
        # CCCATGGTACAGTTAGTAAAAGTAA
        #       |     cut site
        self.expected_cut_site = 6
        alignment = DNAPairwiseAlignment('CCCATGGTACAGTAGTAAAAGTAA',
                                         'CCCATGGTACAGTTAGTAAAAGTAA',
                                         ((0, 0), (12, 12), (12, 13), (24, 25)), -184.0, 0)

        df = self.build_df_from_alignment(alignment)
        expected = self.add_new_columns_to_multiindex([('', '', '', 'ML*', np.nan),
                                                       (False, True, False, 'M*', 50.0)],
                                                      df)
        op = ProteinPrediction(self.annotation.name, self.reference,
                               with_gRNAs=True, tp_range_lower=1, tp_range_upper=5)
        result = op.modify(df, logging.getLogger)
        pd.testing.assert_frame_equal(result.dataframe, expected)

    def test_indel_at_target_end(self):
        # 0001110000001110000000111
        # CCCATGGTACAGTTAGTAAAAGTAA-
        # |||||||||||||||||||||||||-
        # CCCATGGTACAGTTAGTAAAAGTAAA
        #       |     cut site

        gRNA_options = [(
                            {'with_gRNAs': False, 'tp_range_lower': 0, 'tp_range_upper': 0},
                            (False, False, True, 'ML*', 100.0)
                         ),
                        (
                            {'with_gRNAs': True, 'tp_range_lower': 1, 'tp_range_upper': 1},
                            (False, False, False, 'ML*', 100.0)
                         )]
        alignment = DNAPairwiseAlignment('CCCATGGTACAGTTAGTAAAAGTAA',
                                         'CCCATGGTACAGTTAGTAAAAGTAAA',
                                         ((0, 0), (25, 25), (25, 26)), -184.0, 0)
        df = self.build_df_from_alignment(alignment)
        for (gRNA_kwarg, result_entries) in gRNA_options:
            expected = self.add_new_columns_to_multiindex([('', '', '', 'ML*', np.nan),
                                                           result_entries],
                                                          df)
            op = ProteinPrediction(self.annotation.name, self.reference, **gRNA_kwarg)
            result = op.modify(df, logging.getLogger)
            pd.testing.assert_frame_equal(result.dataframe, expected)

    def test_indel_in_reference_start(self):
        # 0001110000001110000000111
        # CCCATGGTACAGTTAGTAAAAGTAA
        # -||||||||||||||||||||||||
        # -CCATGGTACAGTTAGTAAAAGTAA
        #       |     cut site

        gRNA_options = [(
                            {'with_gRNAs': False, 'tp_range_lower': 0, 'tp_range_upper': 0},
                            (False, False, False, 'ML*', 100.0)
                         ),
                        (
                            {'with_gRNAs': True, 'tp_range_lower': 6, 'tp_range_upper': 1},
                            (False, False, False, 'ML*', 100.0)
                         )]
        alignment = DNAPairwiseAlignment('CCCATGGTACAGTTAGTAAAAGTAA',
                                         'CCATGGTACAGTTAGTAAAAGTAA',
                                         ((0, 0), (1, 0), (26, 25)), -184.0, 0)
        df = self.build_df_from_alignment(alignment)
        for (gRNA_kwarg, result_entries) in gRNA_options:
            expected = self.add_new_columns_to_multiindex([('', '', '', 'ML*', np.nan),
                                                           result_entries],
                                                          df)
            op = ProteinPrediction(self.annotation.name, self.reference, **gRNA_kwarg)
            result = op.modify(df, logging.getLogger)
            pd.testing.assert_frame_equal(result.dataframe, expected)

    def test_indel_in_reference_middle(self):
        # 0001110000001110000000111
        # CCCATGGT-ACAGTTAGTAAAAGTAA
        # ||||||||-|||||||||||||||||
        # CCCATGGTAACAGTTAGTAAAAGTAA
        #       |     cut site

        gRNA_options = [(
                            {'with_gRNAs': False, 'tp_range_lower': 0, 'tp_range_upper': 0},
                            (False, False, False, 'ML*', 100.0)
                         ),
                        (
                            {'with_gRNAs': True, 'tp_range_lower': 1, 'tp_range_upper': 1},
                            (False, False, False, 'ML*', 100.0)
                         )]
        alignment = DNAPairwiseAlignment('CCCATGGTACAGTTAGTAAAAGTAA',
                                         'CCCATGGTAACAGTTAGTAAAAGTAA',
                                         ((0, 0), (8, 8), (8, 9), (25, 26)), -184.0, 0)
        df = self.build_df_from_alignment(alignment)
        for (gRNA_kwarg, result_entries) in gRNA_options:
            expected = self.add_new_columns_to_multiindex([('', '', '', 'ML*', np.nan),
                                                           result_entries],
                                                          df)
            op = ProteinPrediction(self.annotation.name, self.reference, **gRNA_kwarg)
            result = op.modify(df, logging.getLogger)
            pd.testing.assert_frame_equal(result.dataframe, expected)

    def test_both_insertion_and_deletion_in_ref(self):
        # 0001110000001110000000111
        # CCCATGGTA-CAGTTAGTAAAAGTAA
        # |||||||||-||||||||-|||||||
        # CCCATGGTAACAGTTAGT-AAAGTAA
        #       |     cut site

        gRNA_options = [(
                            {'with_gRNAs': False, 'tp_range_lower': 0, 'tp_range_upper': 0},
                            (False, False, True, 'MLX*', 66.7)
                         ),
                        (
                            {'with_gRNAs': True, 'tp_range_lower': 7, 'tp_range_upper': 7},
                            (False, False, False, 'ML*', 100.0)
                         )]
        alignment = DNAPairwiseAlignment('CCCATGGTACAGTTAGTAAAAGTAA',
                                         'CCCATGGTAACAGTTAGTAAAGTAA',
                                         ((0, 0), (9, 9), (9, 10), (17, 18), (18, 18), (25, 25)),
                                         -184.0, 0)
        df = self.build_df_from_alignment(alignment)
        for (gRNA_kwarg, result_entries) in gRNA_options:
            expected = self.add_new_columns_to_multiindex([('', '', '', 'ML*', np.nan),
                                                           result_entries],
                                                          df)
            op = ProteinPrediction(self.annotation.name, self.reference, **gRNA_kwarg)
            result = op.modify(df, logging.getLogger)
            pd.testing.assert_frame_equal(result.dataframe, expected)

    def test_snp_last_acceptor_site(self):
        # 0001110000001110000000111
        # CCCATGGTACAGTTAGTAAAAGTAA
        # ||||||||||||||||||||.||||
        # CCCATGGTACAGTTAGTAAATGTAA
        #       |     cut site

        gRNA_options = [(
                            {'with_gRNAs': False, 'tp_range_lower': 0, 'tp_range_upper': 0},
                            (False, True, False, 'ML*', 100.0)
                         ),
                        (
                            {'with_gRNAs': True, 'tp_range_lower': 1, 'tp_range_upper': 1},
                            (False, False, False, 'ML*', 100.0)
                         )]
        alignment = DNAPairwiseAlignment('CCCATGGTACAGTTAGTAAAAGTAA',
                                         'CCCATGGTACAGTTAGTAAATGTAA', ((0, 0), (25, 25)), -184.0, 0)
        df = self.build_df_from_alignment(alignment)
        for (gRNA_kwarg, result_entries) in gRNA_options:
            expected = self.add_new_columns_to_multiindex([('', '', '', 'ML*', np.nan),
                                                          result_entries],
                                                          df)
            op = ProteinPrediction(self.annotation.name, self.reference, **gRNA_kwarg)
            result = op.modify(df, logging.getLogger)
            pd.testing.assert_frame_equal(result.dataframe, expected)

    def test_no_reference_raises(self):
        reference_content = dedent("""\
                                   >foo
                                   AGCT
                                   """)
        reference = StringIO(reference_content)
        alignment = DNAPairwiseAlignment('CCCATGGTACAGTTAGTAAAAGTAA',
                                         'CCCAGGGTACAGTTAGTAAAAGTAA',
                                         ((0, 0), (25, 25)), 18.0, 0)
        df = self.build_df_from_alignment(alignment)
        op = ProteinPrediction(self.annotation.name, reference, 7, 7, with_gRNAs=True)
        with self.assertRaisesRegex(ValueError, (r"Could not find genomic sequence with "
                                                 r"ID 1 in input \.fasta file\.")):
            op.modify(df, logging.getLogger)

    def test_gene_not_in_annotation_raises(self):
        annotation = None
        message = r"Gene 1 not found in annotation gff\."
        try:
            annotation_content = dedent("""\
                                        not_present	unittest	gene	1	25	.	+	.
                                        not_present	unittest	CDS	4	25	.	+	0	Name=foo
                                        """)
            annotation = tempfile.NamedTemporaryFile('w')
            annotation.write(annotation_content)
            annotation.seek(0)
            alignment = DNAPairwiseAlignment('CCCATGGTACAGTTAGTAAAAGTAA',
                                             'CCCAGGGTACAGTTAGTAAAAGTAA',
                                             ((0, 0), (25, 25)), 18.0, 0)
            df = self.build_df_from_alignment(alignment)
            op = ProteinPrediction(annotation.name, self.reference, 7, 7, with_gRNAs=True)
            with self.assertRaisesRegex(ValueError, message):
                op.modify(df, logging.getLogger)
        finally:
            if annotation:
                annotation.close()

    def test_incorrect_length_raises(self):
        reference_content = dedent("""\
                                   >1
                                   C
                                   """)
        reference = StringIO(reference_content)
        alignment = DNAPairwiseAlignment('CCCATGGTACAGTTAGTAAAAGTAA',
                                         'CCCAGGGTACAGTTAGTAAAAGTAA',
                                         ((0, 0), (25, 25)), 18.0, 0)
        op = ProteinPrediction(self.annotation.name, reference, 7, 7, with_gRNAs=True)
        df = self.build_df_from_alignment(alignment)
        message = (r"The length of gene 1 specified in the gene annotation "
                   r"is smaller than the length of the reference\.")
        with self.assertRaisesRegex(AssertionError, message):
            op.modify(df, logging.getLogger)

    def test_length_reference_gene_larger_warns(self):
        # This is a warning an not an error because the user might want to analyze UTRs
        reference_content = dedent("""\
                                   >1
                                   AGCTCCCATGGTACAGTTAGTAAAAGTAACCCC
                                   """)
        reference = StringIO(reference_content)
        alignment = DNAPairwiseAlignment('CCCATGGTACAGTTAGTAAAAGTAA',
                                         'CCCAGGGTACAGTTAGTAAAAGTAA',
                                         ((0, 0), (25, 25)), 18.0, 0)
        op = ProteinPrediction(self.annotation.name, reference, 7, 7, with_gRNAs=True)
        df = self.build_df_from_alignment(alignment)
        logger = logging.getLogger()
        with self.assertLogs(logger) as logger_cm:
            res = op.modify(df, logging.getLogger)
        self.assertIn(("WARNING:root:Sequence length for gene 1 does not match "
                       "between reference fasta and annotation gff"),
                      logger_cm.output)
        df = self.build_df_from_alignment(alignment)
        expected = self.add_new_columns_to_multiindex([('', '', '', 'STK*', np.nan),
                                                       (True, True, False, 'R*', 0.0)],
                                                      df)
        pd.testing.assert_frame_equal(res.dataframe, expected)

    def test_one_cds_interval(self):
        gRNA_options = [(
                            {'with_gRNAs': False, 'tp_range_lower': 0, 'tp_range_upper': 0},
                            (False, False, False, 'MVQLVKVX*', 100.0)
                         ),
                        (
                            {'with_gRNAs': True, 'tp_range_lower': 1, 'tp_range_upper': 1},
                            (False, False, False, 'MVQLVKVX*', 100.0)
                         )]
        alignment = DNAPairwiseAlignment('CCCATGGTACAGTTAGTAAAAGTAA',
                                         'CCCATGGTGCAGTTAGTAAAAGTAA',
                                         ((0, 0), (25, 25)), 18.0, 0)
        df = self.build_df_from_alignment(alignment)
        for (gRNA_kwarg, result_entries) in gRNA_options:
            expected = self.add_new_columns_to_multiindex([('', '', '', 'MVQLVKVX*', np.nan),
                                                           result_entries],
                                                          df)
            op = ProteinPrediction(self.one_cds_annotation.name, self.reference, **gRNA_kwarg)
            result = op.modify(df, logging.getLogger)
            pd.testing.assert_frame_equal(result.dataframe, expected)

    def test_reference_start_codon_not_methionine_warning(self):
        reference_content = dedent("""\
                                   >1
                                   CCCTTGGTACAGTTAGTAAAAGTAA
                                   """)
        reference = StringIO(reference_content)
        alignment = DNAPairwiseAlignment('CCCTTGGTACAGTTAGTAAAAGTAA',
                                         'CCCTTGGTGCAGTTAGTAAAAGTAA',
                                         ((0, 0), (25, 25)), 18.0, 0)
        df = self.build_df_from_alignment(alignment)
        expected = self.add_new_columns_to_multiindex([('', '', '', 'LL*', np.nan),
                                                       (False, False, False, 'LL*', 100.0)],
                                                      df)
        op = ProteinPrediction(self.annotation.name, reference,
                               with_gRNAs=False, tp_range_lower=0, tp_range_upper=0)
        result = op.modify(df, logging.getLogger)
        pd.testing.assert_frame_equal(result.dataframe, expected)

    def test_reference_stop_codon_not_standard_warning(self):
        reference_content = dedent("""\
                                   >1
                                   CCCATGGTACAGTTAGTAAAAGTAC
                                   """)
        reference = StringIO(reference_content)
        alignment = DNAPairwiseAlignment('CCCATGGTACAGTTAGTAAAAGTAC',
                                         'CCCATGGTGCAGTTAGTAAAAGTAC',
                                         ((0, 0), (25, 25)), 18.0, 0)
        df = self.build_df_from_alignment(alignment)
        expected = self.add_new_columns_to_multiindex([('', '', '', 'MLY*', np.nan),
                                                       (False, False, False, 'MLY*', 100.0)],
                                                      df)
        op = ProteinPrediction(self.annotation.name, reference,
                               with_gRNAs=False, tp_range_lower=0, tp_range_upper=0)
        result = op.modify(df, logging.getLogger)
        pd.testing.assert_frame_equal(result.dataframe, expected)

    def test_reference_donor_site_not_correct_warning(self):
        reference_content = dedent("""\
                                   >1
                                   CCCATGCTACAGTTAGTAAAAGTAA
                                   """)
        reference = StringIO(reference_content)
        alignment = DNAPairwiseAlignment('CCCATGCTACAGTTAGTAAAAGTAA',
                                         'CCCATGCTGCAGTTAGTAAAAGTAA',
                                         ((0, 0), (25, 25)), 18.0, 0)
        df = self.build_df_from_alignment(alignment)
        expected = self.add_new_columns_to_multiindex([('', '', '', 'ML*', np.nan),
                                                       (False, False, False, 'ML*', 100.0)],
                                                      df)
        op = ProteinPrediction(self.annotation.name, reference,
                               with_gRNAs=False, tp_range_lower=0, tp_range_upper=0)
        result = op.modify(df, logging.getLogger)
        pd.testing.assert_frame_equal(result.dataframe, expected)

    def test_reference_acceptor_site_not_correct_warning(self):
        reference_content = dedent("""\
                                   >1
                                   CCCATGGTACGGTTAGTAAAAGTAA
                                   """)
        reference = StringIO(reference_content)
        alignment = DNAPairwiseAlignment('CCCATGGTACGGTTAGTAAAAGTAA',
                                         'CCCATGGTGCGGTTAGTAAAAGTAA',
                                         ((0, 0), (25, 25)), 18.0, 0)
        df = self.build_df_from_alignment(alignment)
        expected = self.add_new_columns_to_multiindex([('', '', '', 'ML*', np.nan),
                                                       (False, False, False, 'ML*', 100.0)],
                                                      df)
        op = ProteinPrediction(self.annotation.name, reference,
                               with_gRNAs=False, tp_range_lower=0, tp_range_upper=0)
        result = op.modify(df, logging.getLogger)
        pd.testing.assert_frame_equal(result.dataframe, expected)
