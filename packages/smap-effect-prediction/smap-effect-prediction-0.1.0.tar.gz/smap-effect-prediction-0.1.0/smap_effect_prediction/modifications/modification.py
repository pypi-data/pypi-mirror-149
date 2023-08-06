from abc import ABC, abstractmethod
import logging
import pandas as pd
from enum import Enum, unique, auto
from smap_effect_prediction.models import HaplotypeTable
from ..utils import _FileTypePickable
from typing import IO, Callable
import numpy as np


@unique
class ModificationType(Enum):
    LOCI = auto()
    DATAFRAME = auto()
    SAMPLES = auto()

    def __repr__(self):
        return f'{self.name.lower()}'


class TableModification(ABC, _FileTypePickable):
    """An abstract class for modifications that can be performed on (parts of)
       :class:`smap_effect_prediction.models.Table`.
    """
    @classmethod
    @abstractmethod
    def operates_on(cls) -> ModificationType:
        """Expresses the :class:`ModificationType`, which is directly linked to the
           expected input for the modification, i.e. required by modify().
           All modifications that have the same :class:`ModificationType`, expect the same input
           for modify().

           :return: The type of modification that the class performs.
        """

    @abstractmethod
    def modify(self,
               df: pd.DataFrame,
               logging_configurer: Callable[[], logging.Logger]) -> pd.DataFrame:
        """Perform the modification of a :class:`smap_effect_prediction.models.Table` part.
           Even though the parts will always be passed as a :class:`pd.pd.DataFrame`, the contents
           of this :class:`pd.pd.DataFrame` must be adjusted according to the type of modification
           this class will perform.

        :param df: (Part of) a :class:`smap_effect_prediction.models.Table` which will be modified.
        """


class LocusModification(TableModification, ABC):
    """An abstract class for modifications that can be performed on a single loci from a
       :class:`smap_effect_prediction.models.Table`.
    """
    @classmethod
    def operates_on(cls) -> ModificationType:
        return ModificationType.LOCI


class WriteOperation(TableModification):
    def __init__(self, open_file: IO[str]) -> None:
        self._write_to = open_file
        super().__init__()

    @classmethod
    def operates_on(cls) -> ModificationType:
        return ModificationType.DATAFRAME

    def modify(self,
               df: pd.DataFrame,
               logging_configurer: Callable[[], logging.Logger]) -> HaplotypeTable:
        logger = logging_configurer()
        try:
            logger.info('Writing to %s', self._write_to.name)
        except AttributeError:
            logger.info('Writing to %r', self._write_to)
        to_write_index = df.index.to_frame(index=False)
        for column, dtype in zip(to_write_index.columns, to_write_index.dtypes):
            if dtype == np.dtype('O'):
                to_write_index[column] = to_write_index[column].apply(str)
        to_write_index = pd.MultiIndex.from_frame(to_write_index)
        df.set_index(to_write_index, inplace=False).to_csv(self._write_to, sep='\t', na_rep="NA")
        return HaplotypeTable(df)
