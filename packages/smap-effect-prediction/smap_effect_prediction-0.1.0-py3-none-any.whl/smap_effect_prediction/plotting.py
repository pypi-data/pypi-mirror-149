import logging
from typing import Callable
import plotly.express as px
from abc import ABC
from .modifications.modification import ModificationType, TableModification
from .models import HaplotypeTable
from .modifications.annotate import EXPECTED_CUT_SITE_COLUM_NAME, SNP_COLUMNNAME, INDEL_COLUMNNAME
import pandas as pd


class PlottingOperation(TableModification, ABC):
    """An abstract class for all plotting operations.
    """
    @classmethod
    def operates_on(cls) -> ModificationType:
        return ModificationType.DATAFRAME


class VariationRangePlot(PlottingOperation):
    """
    Create a histogram for the number of variations were found for each nucleotide position.
    Positions are relative to the cut site. Only the start of indel positions are considered,
    not 1 count for each nucleotide position affected.
    """
    def modify(self,
               locus: pd.DataFrame,
               logging_configurer: Callable[[], logging.Logger]) -> HaplotypeTable:
        logger = logging_configurer()
        # Extract the relevant columns and make sure that each variation is 1 row.
        index_columns_needed = [SNP_COLUMNNAME, INDEL_COLUMNNAME, EXPECTED_CUT_SITE_COLUM_NAME]
        data = locus.index.to_frame(index=False)[index_columns_needed]
        data.dropna(subset=[SNP_COLUMNNAME, INDEL_COLUMNNAME], how='all', inplace=True)
        data = data.explode(SNP_COLUMNNAME).explode(INDEL_COLUMNNAME)
        # Get the SNP and INDEL positions and make the relative to the cut site.
        data[SNP_COLUMNNAME] = data[SNP_COLUMNNAME].str[0]
        data[INDEL_COLUMNNAME] = data[INDEL_COLUMNNAME].str[0]
        data[SNP_COLUMNNAME] = data[SNP_COLUMNNAME] - data[EXPECTED_CUT_SITE_COLUM_NAME]
        data[INDEL_COLUMNNAME] = data[INDEL_COLUMNNAME] - data[EXPECTED_CUT_SITE_COLUM_NAME]
        data.drop(EXPECTED_CUT_SITE_COLUM_NAME, axis=1, inplace=True)
        # Create the histogram, making sure each position (1bp) is 1 bin.
        max_value = data.max(skipna=True, numeric_only=True).max()
        min_value = data.min(skipna=True, numeric_only=True).min()
        number_of_bins = -min_value + max_value
        fig = px.histogram(data, marginal="rug", nbins=int(number_of_bins))
        logger.info('Writing HTML file to "variable_sites_histogram.html".')
        fig.write_html('variable_sites_histogram.html')
        return HaplotypeTable(locus)
