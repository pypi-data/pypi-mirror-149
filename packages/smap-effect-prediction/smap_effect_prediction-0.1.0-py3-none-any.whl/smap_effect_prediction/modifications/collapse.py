from .modification import LocusModification
from ..models import HaplotypeTable
import pandas as pd
from typing import Callable
import logging
from .annotate import GUIDE_FILTER_COLUMNAME

HAPLOTYPE_NAME = 'Haplotype_Name'


class Collapse(LocusModification):
    """
    Collapses the TRUE edited haplotypes in to one interpretable table. Collapsing haplotypes
    that have the same TP edit.

       :param lower_cut_site_range: left border of range around the cut site that
        is considered to contain TP variations
       :param upper_cut_site_range: right border of range around the cut site that
        is considered to contain TP variations """

    def __init__(self, lower_cut_site_range: int, upper_cut_site_range: int) -> None:
        self.tp_range_lower = lower_cut_site_range
        self.tp_range_upper = upper_cut_site_range

    def __repr__(self) -> str:
        return (f'Collapse(tp_range_lower{self.tp_range_lower},'
                f'tp_range_upper={self.tp_range_upper})')

    def modify(self,
               df: pd.DataFrame,
               logging_configurer: Callable[[], logging.Logger]) -> pd.DataFrame:

        collapsed_df = self.collapse(df)

        return HaplotypeTable(collapsed_df)

    def collapse(self, df):
        index = df.index.names
        # set desired columns
        desired_columns = ['Reference', 'Locus', 'target', 'Expected cut site',
                           'FILTER_gRNA', 'atgCheck', 'splicingSiteCheck',
                           'protein_sequence', 'pairwiseProteinIdentity (%)', 'Effect']
        desired_columns = [x for x in desired_columns if x in index]
        non_desired_columns = list(set(index) - set(desired_columns))

        # Only perform collapse if gRNA filtering has been selected
        if GUIDE_FILTER_COLUMNAME not in index:
            df = df.reset_index()
            df['Haplotype'] = df['Locus'] + '_' + df[HAPLOTYPE_NAME].fillna('ref')
            return df.drop(non_desired_columns, axis=1).set_index(['Haplotype']
                                                                  + desired_columns)
        else:

            # set target ID
            target = df.index.get_level_values('Locus').tolist()[0]

            # Only retain filtered out haplotypes
            index = df.index.names
            df = df.reset_index()
            filtered_df = df.loc[df[GUIDE_FILTER_COLUMNAME].fillna(False)]

            if not filtered_df.empty:
                # Set variables
                filtered_df = filtered_df.set_index(index)
                # Get Haplotype names
                names = pd.Series(filtered_df.index.get_level_values(HAPLOTYPE_NAME)).str.split(
                    ',')

                tp_alterations = []

                # Loop over edits per haplotype
                for name in names:
                    alterations = []
                    for edit in name:
                        elms = edit.split(':')
                        bases = elms[-1].split('-')
                        alterations.append([int(elms[0]), bases[0], bases[1]])

                    # Extract the TP edits
                    t = self.check_if_tp(self, alterations, self.tp_range_lower,
                                         self.tp_range_upper)
                    tp_alteration = [name[i] for i, val in enumerate(t) if val]
                    tp_alterations.append(','.join(tp_alteration))

                # Combine Target ID and TP edit(s) name into a final TP haplotype ID
                filtered_df['Haplotype'] = ['{}_{}'.format(target, tp) for tp in tp_alterations]

                # Collapse on TP haplotype name and keep desired columns
                collapsed_df = filtered_df.reset_index().groupby(
                    ['Haplotype'] + desired_columns).sum(min_count=1)

                collapsed_df = collapsed_df.drop(
                    [x for x in collapsed_df.columns if x in non_desired_columns], axis=1)
            else:
                collapsed_df = pd.DataFrame(columns=index).set_index(index)

            # Filter out reference haplotypes
            df['FILTER_gRNA'] = df['FILTER_gRNA'].fillna(False)
            filtered_false_df = df[~df[GUIDE_FILTER_COLUMNAME]].copy()
            collapsed_df_false = filtered_false_df.set_index(index).sum(min_count=1)
            ref_mask = filtered_false_df[HAPLOTYPE_NAME] == "ref"
            values_df = filtered_false_df[ref_mask][desired_columns]
            values = values_df.values[0].tolist()
            ref_name = '{}_ref'.format(target)

            multi_index = pd.MultiIndex.from_tuples([tuple([ref_name] + values)],
                                                    names=['Haplotype'] + desired_columns)

            collapsed_df_false = pd.DataFrame(collapsed_df_false.to_dict(), index=multi_index)

            return pd.concat([collapsed_df_false, collapsed_df]).sort_values('Locus')

    @staticmethod
    def add_indel_length(y):
        return max([len(y[1]), len(y[2])]) - 1

    @staticmethod
    def lower_range(self, y, tp_range):
        return max([((y[0]) > -tp_range), ((y[0] + self.add_indel_length(y)) > tp_range)])

    @staticmethod
    def upper_range(self, y, tp_range):
        return max([((y[0]) < tp_range), ((y[0] - self.add_indel_length(y)) < tp_range)])

    @staticmethod
    def check_if_tp(self, alterations, tp_range_lower, tp_range_upper):
        """Check if edit is within TP range"""
        checks = [
            self.lower_range(self, y, tp_range_lower) if int(y[0]) < 0 else
            self.upper_range(self, y, tp_range_upper)
            for
            y in
            alterations]

        return checks
