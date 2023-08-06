from .modification import LocusModification
from ..models import AggregatedTable, LOCUS_COLUMN_NAME
from .annotate import INDEL_COLUMNNAME, SNP_COLUMNNAME, HAPLOTYPE_NAME, CHROMOSOME_COLUMN_NAME
from typing import Callable
import pandas as pd
import numpy as np
import logging


logger = logging.getLogger()


class LocusAggregation(LocusModification):
    def __init__(self, aggregation_column: str) -> None:
        self._aggregation_column = aggregation_column
        super().__init__()
        logger.debug('Initiated %r', self)

    def __repr__(self) -> str:
        return f'LocusAggregation(aggregation_column={self._aggregation_column})'

    @staticmethod
    def join_tuples(tuple_list):
        result = ",".join([repr(tup) for tuples in tuple_list.dropna().to_list()
                          for tup in tuples]) if not tuple_list.isna().all() else ""
        return result if result else pd.NA

    @staticmethod
    def join_haplotype_names(names):
        return names.str.cat(sep=',')

    @staticmethod
    def sum_col(col):
        return col.sum()

    @staticmethod
    def get_nan_rows(zero_row):
        return [zero_row.index[x] for x in (np.where(zero_row.isna())[0])]

    def fill_nan_values(self, aggregated, zero_row):
        nan_values = self.get_nan_rows(zero_row)
        aggregated[nan_values] = pd.NA
        return aggregated

    def modify(self, locus: pd.DataFrame, logging_configurer: Callable[[], logging.Logger]):
        logger = logging_configurer()
        locus_name = locus.index.get_level_values(LOCUS_COLUMN_NAME)[0]
        chromosome_name = locus.index.get_level_values(CHROMOSOME_COLUMN_NAME)[0]
        # Find all columns that have no data, set value to nan and set all others to zero
        zero_row = locus.isna().all().astype(int).replace(1, pd.NA)
        logger.debug('Aggregating locus %s.', locus_name)
        try:
            locus = locus.xs(True, level=self._aggregation_column).copy()
        except KeyError:
            result_index = pd.MultiIndex.from_tuples([(chromosome_name, locus_name, tuple(),
                                                       tuple(), pd.NA)],
                                                     names=[CHROMOSOME_COLUMN_NAME,
                                                            LOCUS_COLUMN_NAME,
                                                            SNP_COLUMNNAME,
                                                            INDEL_COLUMNNAME,
                                                            HAPLOTYPE_NAME])
            result = pd.DataFrame([zero_row.tolist()],
                                  columns=locus.columns,
                                  index=result_index)
            return AggregatedTable(result)
        else:
            functional_mapping = {self.sum_col: locus.columns,
                                  self.join_tuples: [SNP_COLUMNNAME, INDEL_COLUMNNAME],
                                  self.join_haplotype_names: [HAPLOTYPE_NAME]
                                  }
            agg_functions = {col: func for func, cols in functional_mapping.items() for col in cols}

            for col in [SNP_COLUMNNAME, INDEL_COLUMNNAME, HAPLOTYPE_NAME]:
                locus[col] = locus.index.get_level_values(col)

            aggregated = locus.agg(agg_functions)
            # Fill in nan in all columns that had no data
            aggregated = self.fill_nan_values(aggregated, zero_row)
            aggregated[LOCUS_COLUMN_NAME] = locus_name
            aggregated[CHROMOSOME_COLUMN_NAME] = chromosome_name
            aggregated = aggregated.to_frame().T
            aggregated.set_index([CHROMOSOME_COLUMN_NAME,
                                  LOCUS_COLUMN_NAME,
                                  SNP_COLUMNNAME,
                                  INDEL_COLUMNNAME,
                                  HAPLOTYPE_NAME],
                                 inplace=True, append=False)
            aggregated = aggregated.infer_objects()
            return AggregatedTable(aggregated)
