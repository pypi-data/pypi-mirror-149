from abc import ABC, abstractmethod
import logging
import pandas as pd
from pathlib import Path
from typing import Iterable, List, TextIO, Union
from operator import itemgetter
from pybedtools import BedTool
from pybedtools.cbedtools import Interval, MalformedBedLineError
from .utils import _FileTypePickable

CHROMOSOME_COLUMN_NAME: str = "Reference"
LOCUS_COLUMN_NAME: str = "Locus"
HAPLOTYPE_COLUMN_NAME: str = "Haplotypes"
TARGET_COLUMN_NAME: str = "target"

logger = logging.getLogger()


class Table(ABC):
    def __init__(self, dataframe: pd.DataFrame):
        self._table = dataframe

    @classmethod
    def concat(cls, tables: Iterable['Table']) -> 'Table':
        """Construct a new Table by concatenating the rows of one or more Tables.

        :param tables: A number of tables to concatenate.
        :return: one new Table containing all rows from the input
        """
        return cls(pd.concat([table._table for table in tables]))

    @abstractmethod
    def iter_loci(self) -> Iterable[pd.DataFrame]:
        """Splits the table into different dataframes per locus.
        """

    @property
    def dataframe(self) -> pd.DataFrame:
        return self._table.copy(deep=True)


class FrequencyTable(Table, ABC):
    def iter_loci(self) -> Iterable[pd.DataFrame]:
        get_second = itemgetter(1)
        yield from map(get_second, iter(self.groupby(level=LOCUS_COLUMN_NAME)))

    def groupby(self, *args, **kwargs) -> pd.core.groupby.GroupBy:
        return self._table.groupby(*args, **kwargs)


class HaplotypeTable(FrequencyTable):
    """
    A class to represent haplotype frequencies in a table.
    Rows in the table represent the frequencies for one haplotype at a given locus.
    Columns can represent either biological samples for which the frequencies are given,
    or extra annotations that provide metadata about the haplotypes.

    :param haplotypes_df: A :class:`pd.DataFrame` object representing the haplotype
        frequencies table. The dataframe rows should be indexed by a three-level
        ("Locus", "Haplotypes" and "target") :class:`pd.MultiIndex` object.
    :example:
        >>> row_index = pd.MultiIndex.from_tuples([("locus1", "ACGT", "target1"),
        ...                                        ("locus1", "ACGG", "target1"),
        ...                                        ("locus2", "TGCA", "target2"),
        ...                                        ("locus2", "CGCA", "target2")],
        ...                                        names=["Locus", "Haplotypes", "target"])
        >>> df = pd.DataFrame(data={"sample1": [100.0, nan, 100.0, 10.0],
        ...                         "sample2": [80.0, 20.0, 100.0, 100.0]},
        ...                         index=row_index)
        >>> HaplotypeTable(df)
        Name                      sample1 sample2
        Sample_column                True    True
        Locus  Haplotypes target
        locus1 ACGT       target1   100.0    80.0
               ACGG       target1     NaN    20.0
        locus2 TGCA       target2   100.0   100.0
               CGCA       target2    10.0   100.0

    """

    def __init__(self, haplotypes_df: pd.DataFrame):
        super().__init__(haplotypes_df)
        logger.debug('Initiated %r', self)

    def __repr__(self):
        return f'HaplotypeTable(haplotypes_df=<pandas.DataFrame object at {hex(id(self._table))}>)'

    @classmethod
    def read_smap_output(cls, filepath_or_buffer: Union[str, Path, TextIO], delimiter: str = "\t"):
        """
        Read an .tsv file originating from SMAP-haplotype-window and create a HaplotypeTable.

        :param filepath_or_buffer: A path representing the location of the .tsv file,
            or a buffer that is ready for reading.
        :param delimiter: The delimiter that has been used to format the file, defaults to "\\t".
        """
        logger.info('Reading from %s', filepath_or_buffer)
        table = pd.read_csv(filepath_or_buffer,
                            delimiter=delimiter,
                            index_col=[CHROMOSOME_COLUMN_NAME,
                                       LOCUS_COLUMN_NAME,
                                       HAPLOTYPE_COLUMN_NAME,
                                       TARGET_COLUMN_NAME],
                            dtype={col: str for col in [CHROMOSOME_COLUMN_NAME,
                                                        LOCUS_COLUMN_NAME,
                                                        HAPLOTYPE_COLUMN_NAME,
                                                        TARGET_COLUMN_NAME]})
        logger.debug('Table shape: %s.', table.shape)
        return cls(table)


class AggregatedTable(FrequencyTable):
    pass


class Gff(_FileTypePickable):
    def __init__(self, gff: BedTool) -> None:
        assert isinstance(gff, BedTool)
        self._gff = gff

    def __repr__(self) -> str:
        try:
            return f'Gff(gff=BedTool({self._gff.fn.name}))'
        except AttributeError:
            return f'Gff(gff=<pybedtools.BedTool object at {hex(id(self._gff))}>)'

    @classmethod
    def read_file(cls, open_gff: TextIO):
        try:
            logger.info('Reading %s', open_gff.name)
        except AttributeError:
            logger.info('Reading %r', open_gff)
        gff = BedTool(open_gff)
        return cls(gff)

    def get_enties_by_attribute_value(self, attr: str, value: str) -> List[Interval]:
        result = []
        try:
            for interval in self._gff:
                try:
                    if interval.attrs[attr].split(' ')[0] == value:
                        result.append(interval)
                except KeyError:
                    raise ValueError("The Gff file does not contain an attribute "
                                     f"{attr} for each entry.")
        except MalformedBedLineError:
            try:
                name = self._gff.fn.name
                raise ValueError(f"Gff file {name} has an incorrect format.")
            except AttributeError:
                raise ValueError("Malformatted .gff")
        return result

    def __getstate__(self):
        state = self.__dict__.copy()
        state['_gff'] = state['_gff'].fn.name
        return state

    def __setstate__(self, state):
        state['_gff'] = BedTool(state['_gff'])
        self.__dict__.update(state)
