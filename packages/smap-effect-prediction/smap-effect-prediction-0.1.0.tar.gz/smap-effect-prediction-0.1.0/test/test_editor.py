from smap_effect_prediction.editor import MultiProcessEditor
import numpy as np
import pandas as pd
from unittest import TestCase
from unittest.mock import patch
from smap_effect_prediction.models import HaplotypeTable
from smap_effect_prediction.modifications.modification import ModificationType, TableModification
import multiprocessing


class DummyLocusModication(TableModification):
    def operates_on(self):
        return ModificationType.LOCI

    def modify(self, df, logging_configurer):
        return HaplotypeTable(df)


class DummyFrameModication(TableModification):
    def operates_on(self):
        return ModificationType.DATAFRAME

    def modify(self, df, logging_configurer):
        return HaplotypeTable(df)


class TestMultiProcessEditors(TestCase):
    def setUp(self) -> None:
        row_index = pd.MultiIndex.from_tuples([("locus1", "ACGT", "target1"),
                                               ("locus1", "ACGG", "target1"),
                                               ("locus2", "TGCA", "target2"),
                                               ("locus2", "CGCA", "target2")],
                                              names=["Locus", "Haplotypes", "target"])
        table = pd.DataFrame(data={"sample1": [100.0, np.nan, 100.0, 10.0],
                                   "sample2": [80.0, 20.0, 100.0, 100.0]},
                             index=row_index)
        self.haplotype_table = HaplotypeTable(table)
        self.editor = MultiProcessEditor(1)

    @patch('smap_effect_prediction.editor.cpu_count', return_value=2)
    def test_max_number_of_processes_raises(self, mocked_cpu_count):
        queue = multiprocessing.Queue()
        with self.assertRaises(ValueError):
            MultiProcessEditor(queue, 2)

    @patch('smap_effect_prediction.editor.cpu_count', return_value=1)
    def test_max_number_of_processes_does_not_raise_with_1(self, mocked_cpu_count):
        queue = multiprocessing.Queue()
        MultiProcessEditor(queue, 1)

    def test_edit_loci(self):
        dummy_modification = DummyLocusModication()
        self.editor.queue_modification([dummy_modification])
        new_haplotype_table = self.editor.edit(self.haplotype_table)
        pd.testing.assert_frame_equal(new_haplotype_table.dataframe, self.haplotype_table.dataframe)

    def test_edit_frame(self):
        dummy_modification = DummyFrameModication()
        self.editor.queue_modification([dummy_modification])
        new_haplotype_table = self.editor.edit(self.haplotype_table)
        pd.testing.assert_frame_equal(new_haplotype_table.dataframe, self.haplotype_table.dataframe)

    def test_edit_without_queued_modification(self):
        msg = r"No modifications queued\."
        with self.assertRaisesRegex(RuntimeError, expected_regex=msg):
            self.editor.edit(self.haplotype_table)

    def test_enqueue_wrong_object_type(self):
        msg = r"Can only queue TableModification objects\."
        with self.assertRaisesRegex(ValueError, expected_regex=msg):
            self.editor.queue_modification(['foo'])
