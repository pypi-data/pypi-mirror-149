from unittest import TestCase
from smap_effect_prediction.utils import _FileTypePickable
from typing import IO
from io import BytesIO
from pickle import Pickler, Unpickler
from tempfile import TemporaryDirectory
from pathlib import Path


class DummyFile(_FileTypePickable):
    def __init__(self, file_handler: IO[str]) -> None:
        self._file = file_handler
        super().__init__()


class TestFileTypePickable(TestCase):
    def test_pickling_files(self):
        with TemporaryDirectory() as temp_dir:
            temp_file = Path(temp_dir) / "dummy_file.txt"
            temp_file.touch()
            with temp_file.open('w') as open_for_writing:
                open_for_writing.write('foo bar.')
                open_for_writing.close()
            with temp_file.open('r') as open_for_reading:
                destination_file = BytesIO()
                dummy_object = DummyFile(open_for_reading)
                pickler = Pickler(destination_file)
                pickler.dump(dummy_object)
                destination_file.seek(0, 0)
                unpickler = Unpickler(destination_file)
                result_file = unpickler.load()
                result_content = result_file._file.read()
                self.assertEqual(result_content, 'foo bar.')
                result_file._file.close()

    def test_picke_for_writing_fails(self):
        with TemporaryDirectory() as temp_dir, self.assertRaises(RuntimeError):
            temp_file = Path(temp_dir) / "dummy_file.txt"
            temp_file.touch()
            file_handler = temp_file.open('w')
            destination_file = BytesIO()
            dummy_object = DummyFile(file_handler)
            pickler = Pickler(destination_file)
            pickler.dump(dummy_object)
            file_handler.close()
