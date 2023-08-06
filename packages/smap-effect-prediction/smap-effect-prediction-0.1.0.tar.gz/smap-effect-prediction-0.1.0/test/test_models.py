from typing import Generator
from unittest import TestCase
import pandas as pd
from io import StringIO, BytesIO
from textwrap import dedent
from smap_effect_prediction.models import HaplotypeTable, Gff
from numpy import nan
from tempfile import TemporaryDirectory
from pickle import Pickler, Unpickler
from pathlib import Path


class TestHaplotypeTable(TestCase):
    def setUp(self) -> None:
        row_index = pd.MultiIndex.from_tuples([("1", "locus1", "ACGT", "target1"),
                                               ("1", "locus1", "ACGG", "target1"),
                                               ("1", "locus2", "TGCA", "target2"),
                                               ("1", "locus2", "CGCA", "target2")],
                                              names=["Reference", "Locus", "Haplotypes", "target"])
        self.table = pd.DataFrame(data={"sample1": [100.0, nan, 100.0, 10.0],
                                        "sample2": [80.0, 20.0, 100.0, 100.0]},
                                  index=row_index)
        self.haplotype_table = HaplotypeTable(self.table)

    def test_read_smap_output(self):
        test_data = dedent("""\
                           Reference	Locus	Haplotypes	target	sample1	sample2
                           1	locus1	ACGT	target1	100.0	80.0
                           1	locus1	ACGG	target1	NaN	20.0
                           1	locus2	TGCA	target2	100.0	100.0
                           1	locus2	CGCA	target2	10.0	100.0
                           """)
        test_buffer = StringIO(test_data)
        haplotype_table = HaplotypeTable.read_smap_output(test_buffer)
        self.assertIsInstance(haplotype_table, HaplotypeTable)
        pd.testing.assert_frame_equal(haplotype_table.dataframe, self.table)

    def test_iter_loci(self):
        loci = self.haplotype_table.iter_loci()
        self.assertIsInstance(loci, Generator)
        loci_list = list(loci)
        self.assertEqual(len(loci_list), 2)
        locus1, locus2 = loci_list
        self.assertIsInstance(locus1, pd.DataFrame)
        self.assertIsInstance(locus2, pd.DataFrame)
        locus1_index = pd.MultiIndex.from_tuples([("1", "locus1", "ACGT", "target1"),
                                                  ("1", "locus1", "ACGG", "target1")],
                                                 names=["Reference", "Locus",
                                                        "Haplotypes", "target"])
        locus1_result = pd.DataFrame(data={"sample1": [100.0, nan],
                                           "sample2": [80.0, 20.0]},
                                     index=locus1_index)
        pd.testing.assert_frame_equal(locus1_result, locus1)
        locus2_index = pd.MultiIndex.from_tuples([("1", "locus2", "TGCA", "target2"),
                                                  ("1", "locus2", "CGCA", "target2")],
                                                 names=["Reference", "Locus",
                                                        "Haplotypes", "target"])
        locus2_result = pd.DataFrame(data={"sample1": [100.0, 10.0],
                                           "sample2": [100.0, 100.0]},
                                     index=locus2_index)
        pd.testing.assert_frame_equal(locus2_result, locus2)


class TestGff(TestCase):
    def setUp(self) -> None:
        self.gRNAs = dedent("""\
                                locus1	SMAP	Guide	1138	1161	.	+	.	\
                                NAME=locus1_1	POOL=pool108_3	SEQ=dolor
                                locus1	SMAP	Guide	3251	3274	.	+	.	\
                                NAME=locus1_2	POOL=pool108_3	SEQ=sit
                                locus1	SMAP	Guide	4371	4394	.	+	.	\
                                NAME=locus1_3	POOL=pool108_3	SEQ=amet
                                """)
        self.gff = Gff.read_file(StringIO(self.gRNAs))

    def test_get_attribute(self):
        result = self.gff.get_enties_by_attribute_value('NAME', 'locus1_1')
        expected_result = ('locus1', 'SMAP', 'Guide',
                           '1138', '1161', '.', '+', '.',
                           'NAME=locus1_1;', 'POOL=pool108_3', 'SEQ=dolor')
        self.assertTupleEqual(tuple(result[0]), expected_result)

    def test_no_such_attribute_raises(self):
        message = r"The Gff file does not contain an attribute foo for each entry\."
        with self.assertRaisesRegex(ValueError, message):
            self.gff.get_enties_by_attribute_value('foo', 'bar')

    def test_pickling(self):
        content = "locus1	SMAP	Guide	1138	1161	.	+	.	NAME=locus1_1	POOL=pool108_3	SEQ=dolor"
        with TemporaryDirectory() as temp_dir:
            temp_file = Path(temp_dir) / "dummy_file.txt"
            temp_file.touch()
            with temp_file.open('w') as open_for_writing:
                open_for_writing.write(content)
                open_for_writing.close()
            with temp_file.open('r') as open_for_reading:
                destination_file = BytesIO()
                dummy_object = Gff.read_file(open_for_reading)
                pickler = Pickler(destination_file)
                pickler.dump(dummy_object)
                destination_file.seek(0, 0)
                unpickler = Unpickler(destination_file)
                result_file = unpickler.load()
                result_content = str(result_file._gff)
                self.assertEqual(result_content.strip(), content)
