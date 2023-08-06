import logging
from unittest import TestCase
from smap_effect_prediction.modifications.modification import ModificationType, WriteOperation
import pandas as pd
from numpy import nan
from io import StringIO
from textwrap import dedent


class TestHaplotypeTable(TestCase):
    def setUp(self) -> None:
        index_data = [("locus1", "ACGT", "target1", ((3, 'C', 'T'),), pd.NA),
                      ("locus1", "ACGG", "target1", pd.NA, ((3, 'CT', 'A'),)),
                      ("locus2", "TGCA", "target2", tuple(), tuple()),
                      ("locus2", "CGCA", "target2", pd.NA, pd.NA)]
        row_index = pd.MultiIndex.from_tuples(index_data,
                                              names=["Locus",
                                                     "Haplotypes",
                                                     "target",
                                                     "SNP",
                                                     "INDEL"])
        self.table = pd.DataFrame(data={"sample1": [100.0, nan, 100.0, 10.0],
                                        "sample2": [80.0, 20.0, 100.0, 100.0]},
                                  index=row_index)

    def test_write_table(self):
        expected_result = dedent("""\
                                 Locus	Haplotypes	target	SNP	INDEL	sample1	sample2
                                 locus1	ACGT	target1	((3, 'C', 'T'),)	nan	100.0	80.0
                                 locus1	ACGG	target1	nan	((3, 'CT', 'A'),)	NA	20.0
                                 locus2	TGCA	target2	()	()	100.0	100.0
                                 locus2	CGCA	target2	nan	nan	10.0	100.0
                                 """)
        target_file = StringIO()
        writer = WriteOperation(target_file)
        writer.modify(self.table, logging.getLogger)
        result = target_file.getvalue()
        self.assertMultiLineEqual(result, expected_result)

    def test_can_write_objects(self):
        class DummyObj():
            def __init__(self, bar) -> None:
                self.bar = bar

            def __hash__(self):
                return hash(self.bar)

            def __eq__(self, other: object) -> bool:
                if not isinstance(other, DummyObj):
                    return False
                return self.bar == other.bar

        expected_result = r"Foo\tlorem\na\t100.0\n<test_writing.TestHaplotypeTable." + \
                          r"test_can_write_objects.<locals>.DummyObj object at 0x.{12}>\tNA\n"
        index_data = [("a",),
                      (DummyObj(1),)]
        row_index = pd.MultiIndex.from_tuples(index_data,
                                              names=["Foo"])
        table = pd.DataFrame(data={"lorem": [100.0, nan]},
                             index=row_index)
        target_file = StringIO()
        writer = WriteOperation(target_file)
        writer.modify(table, logging.getLogger)
        result = target_file.getvalue()
        self.assertRegex(result, expected_result)

    def test_operates_on(self):
        result = WriteOperation.operates_on()
        self.assertEqual(result, ModificationType.DATAFRAME)
