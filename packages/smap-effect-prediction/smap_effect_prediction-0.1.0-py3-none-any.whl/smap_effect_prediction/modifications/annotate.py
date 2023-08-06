import logging
import sys
from pandas.core.series import Series
from .modification import LocusModification
from abc import ABC
from ..models import (TARGET_COLUMN_NAME,
                      Gff,
                      HaplotypeTable,
                      LOCUS_COLUMN_NAME,
                      HAPLOTYPE_COLUMN_NAME,
                      CHROMOSOME_COLUMN_NAME)
from typing import Iterable, TextIO, Tuple, Callable, Union, Dict, List
from pybedtools.cbedtools import Interval

from functools import partial
from Bio import Align, SeqIO
from Bio.Seq import Seq
import pandas as pd
import numpy as np
import re
import gffpandas.gffpandas as gffpd
from collections import defaultdict
import operator
from math import inf

if sys.version_info < (3, 8):
    from typing_extensions import Literal  # pragma: no cover
else:
    from typing import Literal

REFERENCE_COLUMN_VALUE = 'ref'
REFERENCE_COLUMN_NAME = 'edit'
START_COLUMN_NAME = 'start'
END_COLUMN_NAME = 'end'
INDEL_COLUMNNAME = 'INDEL'
SNP_COLUMNNAME = 'SNP'
ALIGNMENT_COLUMNNAME = 'Alignment'

# Expected target site filtering
# NUCLEASE = 'CAS9'
GUIDE_FILTER_COLUMNAME = 'FILTER_gRNA'
HAPLOTYPE_NAME = 'Haplotype_Name'
EXPECTED_CUT_SITE_COLUM_NAME = 'Expected cut site'

# Protein effect prediction
EFFECT_COLUMN_NAME = 'Effect'

logger = logging.getLogger()


class DNAPairwiseAlignment(Align.PairwiseAlignment):
    """Represent the alignment of a haplotype sequence to a reference haplotype.
    """

    def __init__(self, target, query, path, score, reference_start):
        # Store the position of the reference haplotype in the reference sequence.
        self._reference_start = reference_start
        self._coordinate_map = self._generate_coordinate_map(path)
        super().__init__(target, query, path, score)

    @staticmethod
    def _generate_coordinate_map(path) -> Dict[int, List[int]]:
        """Create a dictionary that maps the nucleotide positions of the target sequence
           to the query positions, while aggregating query positions that could map to the
           same target position together because of indels.
        """
        result = {}
        previous_vector = None
        first = True
        for vector in path:
            if not previous_vector:
                previous_vector = vector
                continue
            x, y = vector
            prev_x, prev_y = previous_vector
            diffx = prev_x - x
            diffy = prev_y - y
            if diffx == diffy:
                shift = max(y - x, 0)
                start = prev_x + 1 if not first else prev_x
                for i in range(0, abs(diffx)):
                    result[start + i] = [start + i + shift]
            elif diffx:
                for i in range(prev_x, x + 1):
                    result[i] = [i]
            else:
                result[x] = list(range(prev_y, y + 1))
            previous_vector = vector
            first = False
        return result

    @classmethod
    def from_alignment(cls, alignment, reference_start):
        """Create a DNAPairwiseAlignment from a Bio.Align.PairwiseAlignment object.
        """
        return cls(alignment.target, alignment.query,
                   alignment.path, alignment.score, reference_start)

    @property
    def reference_start(self):
        return self._reference_start

    def snps(self):
        """
        Calculate the positions of the SNPs and the nucleotide changes.
        The positions are calculated in reference to in the reference sequence.
        """
        result = []
        first = True
        # Follow the path through the alignment matrix
        # Each segment of the path represents an alignment piece
        for end1, end2 in self.path:
            if first:
                start1 = end1
                start2 = end2
                first = False
                continue
            # Extract an alignment piece and check for snps.
            # We need to do this in pieces because of indels.
            if not end1 == start1 and not end2 == start2:
                s1 = self.target[start1:end1]
                s2 = self.query[start2:end2]
                for i, (base1, base2) in enumerate(zip(s1, s2)):
                    if base1 != base2:
                        result.append((start1 + i + self._reference_start, base1, base2))
            start1 = end1
            start2 = end2
        return tuple(result)

    def indels(self):
        """
        Calculate the positions of INDELS and the nucleotide changes.
        The positions are calculated in reference to in the reference sequence.
        """
        # Aligned returns the start and end indices of subsequences in
        # the target and query sequence that were aligned to each other
        aligned_chunks = self.aligned
        target_chunks, query_chunks = aligned_chunks
        result = []
        prev_target_end = 0
        prev_query_end = 0
        positive = partial(max, 0)

        # Loop over the aligned chunks
        for target_chunk, query_chunk in zip(target_chunks, query_chunks):
            target_start, target_end = target_chunk
            query_start, query_end = query_chunk

            # When the end of the previous aligned chunks differ from the start
            # of the current chunk, there is a gap.
            target_diff = prev_target_end - target_start
            if target_diff:  # Gap in query
                result.append((prev_target_end + self._reference_start,
                               self.target[positive(prev_target_end - 1):target_start],
                               self.target[positive(prev_target_end - 1):
                                           target_start + target_diff]))

            query_diff = prev_query_end - query_start
            if query_diff:  # Gap in target
                result.append((prev_target_end + self._reference_start,
                               self.query[positive(prev_query_end - 1):query_start + query_diff],
                               self.query[positive(prev_query_end - 1):query_start]))
            prev_target_end = target_end
            prev_query_end = query_end
        extruding_target = target_chunk[-1] - self.path[-1][0]
        extruding_query = query_chunk[-1] - self.path[-1][1]
        if extruding_target:
            result.append((target_chunk[-1],
                           self.target[extruding_target - 1:],
                           f"{self.query[-1]}{'-' * abs(extruding_target)}"))
        elif extruding_query:
            result.append((target_chunk[-1],
                           f"{self.target[-1]}{'-' * abs(extruding_query)}",
                           self.query[extruding_query - 1:]))
        return tuple(result)

    def __hash__(self):
        return hash((self.target, self.query, self.path, self.score, self._reference_start))

    def __eq__(self, other):
        if not isinstance(other, DNAPairwiseAlignment):
            return False
        return (self.target, self.query, self.path, self.score, self._reference_start) == \
               (other.target, other.query, other.path, other.score, other._reference_start)

    def __ne__(self, other):
        # We need to overwrite this
        return not self == other

    def get_alignment_coordinate(self,
                                 reference_coordinate: int,
                                 boundary_type: Union[Literal["start"], Literal["end"]]):
        """Translate a coordinate from the ungapped reference sequence
           to the position in the alignment, extanding the position forward or backwards
           depending on indels occuring directly at the requested coordinate.
        """
        if reference_coordinate >= len(self.target) or reference_coordinate < 0:
            raise ValueError("Reference index out of range.")

        if boundary_type == "start":
            return self._coordinate_map[reference_coordinate][0]
        else:
            try:
                next_coordinate = self._coordinate_map[reference_coordinate + 1]
            except KeyError:
                return self._coordinate_map[reference_coordinate][-1]
            else:
                if len(next_coordinate) > 1:
                    return next_coordinate[0]
                else:
                    return self._coordinate_map[reference_coordinate][-1]


class Annotation(LocusModification, ABC):
    """
    General Annotation class
    """

    def add_index_column(self, column: pd.Series, locus: pd.DataFrame, column_name: str):
        '''
        Function to add a column to the MultiIndex
        :param column: pandas series to add
        :param locus: locus specific dataframe
        :param name: Name of the level
        :return: the locus dataframe with the column added to the multiIndex
        '''
        locus[column_name] = column.tolist()
        locus.set_index(column_name, append=True, inplace=True)
        return locus


class EffectAnnotation(Annotation):
    def __init__(self, effect_column: str, protein_effect_threshold: float) -> None:
        self._effect_column = effect_column
        self._protein_effect_threshold = protein_effect_threshold
        super().__init__()
        logger.debug('Initiated %s', self)

    def __repr__(self) -> str:
        return (f'EffectAnnotation(effect_column={self._effect_column},'
                f'protein_effect_threshold={self._protein_effect_threshold})')

    def modify(self,
               locus: pd.DataFrame,
               logging_configurer: Callable[[], logging.Logger]) -> HaplotypeTable:
        self._logger = logging_configurer()
        locus_name = locus.index.get_level_values(LOCUS_COLUMN_NAME)[0]
        self._logger.debug('Started effect annotation for locus %s', locus_name)
        if self._effect_column in locus.index.names:
            protein_identity = locus.index.get_level_values(self._effect_column).astype('float')
            mask = protein_identity <= self._protein_effect_threshold
        elif GUIDE_FILTER_COLUMNAME in locus.index.names:
            mask = locus.index.get_level_values(GUIDE_FILTER_COLUMNAME)
        locus = self.add_index_column(mask, locus, EFFECT_COLUMN_NAME)
        return HaplotypeTable(locus)


class PairwiseAlignmentAnnotation(Annotation):
    '''
    Class that inherits from Annotation and adds the pairwise alignment columns to the MultiIndex.
    '''

    def __init__(self,
                 match_score: int,
                 mismatch_penalty: int,
                 open_penalty: int,
                 extend_penalty: int):
        self._match_score = match_score
        self._mismatch_penalty = mismatch_penalty
        self._open_penalty = open_penalty
        self._extend_penalty = extend_penalty
        logger.debug('Initiated %r.', self)

    def __repr__(self) -> str:
        return (f'PairwiseAlignment(match_score={self._match_score},' +
                f'mismatch_penalty={self._mismatch_penalty},' +
                f'open_penalty={self._open_penalty},' +
                f'extend_penalty={self._extend_penalty})')

    def modify(self, locus: pd.DataFrame, logging_configurer: Callable[[], logging.Logger]):
        '''
        Adds pairwiseAligmnent index columns to  a locus specifc dataframe
        :param locus:  locus specifc pandas dataframe
        :return:  adds the INDEL, SNP and Alignment column to the MultiIndex.
        '''
        self._logger = logging_configurer()
        locus_name = locus.index.get_level_values(LOCUS_COLUMN_NAME)[0]
        self._logger.debug('Performing pairwise alignment for locus %s', locus_name)
        reference = locus.xs(REFERENCE_COLUMN_VALUE,
                             level=REFERENCE_COLUMN_NAME,
                             drop_level=False)
        locus = locus.groupby(level=HAPLOTYPE_COLUMN_NAME,
                              group_keys=False,
                              sort=False).apply(self.get_snps_indels, reference)
        return HaplotypeTable(locus)

    def get_snps_indels(self, haplotypes: pd.Series, reference: pd.DataFrame):
        '''
        Function to perform pairwise alignmnents, and extract SNPs and INDELS from them.
        :param locus: locus specific pandas dataframe
        :return: reordered locus specific pandas dataframe, dataframe with INDELS and SNPs in
                 columns, Series with alignments of all haplotypes agains specific locus
        '''
        haplotypes = haplotypes.copy()
        new_index_df = haplotypes.index.to_frame()
        if reference.index == haplotypes.index:
            new_index_df[SNP_COLUMNNAME] = np.nan
            new_index_df[INDEL_COLUMNNAME] = np.nan
            new_index_df[ALIGNMENT_COLUMNNAME] = np.nan
            new_index = pd.MultiIndex.from_frame(new_index_df)
            haplotypes.index = new_index
            return haplotypes

        reference_seq = list(reference.index.get_level_values(HAPLOTYPE_COLUMN_NAME))[0]
        start = list(reference.index.get_level_values(START_COLUMN_NAME))[0]
        aligner = Align.PairwiseAligner(match_score=self._match_score,
                                        extend_gap_score=self._extend_penalty,
                                        mismatch_score=self._mismatch_penalty,
                                        open_gap_score=self._open_penalty,
                                        mode='global')
        variant_haplotypes = list(haplotypes.index.get_level_values(HAPLOTYPE_COLUMN_NAME))
        snps = []
        indels = []
        best_alignments = []
        for variant_haplotype in variant_haplotypes:
            alignments = aligner.align(Seq(reference_seq),
                                       Seq(variant_haplotype))
            # take best alignment
            alignment = DNAPairwiseAlignment.from_alignment(alignments[0], start)
            best_alignments.append(alignment)
            # extract SNPs and INDELS from alignement
            snps.append(alignment.snps())
            indels.append(alignment.indels())

        new_index_df[SNP_COLUMNNAME] = snps
        new_index_df[INDEL_COLUMNNAME] = indels
        new_index_df[ALIGNMENT_COLUMNNAME] = best_alignments
        new_index = pd.MultiIndex.from_frame(new_index_df)
        haplotypes.index = new_index
        return haplotypes


class HaplotypePosition(Annotation):
    """
    Add information about the haplotype positions (start and stop) in the reference genome
    to a Table. Additionally, add a column which compares each haplotype sequenece to the reference
    and indicate if they have an exact match. If they do not, indicate the length difference between
    the sequeneces.

    :param border_gff: class:`Gff` object containing the positions of the borders that define
        a window in the reference.All Gff intervals must have an 'NAME' attribute,
        which should match for 'border pairs' that define 1 window.
    :param genome: location of a .fasta file containing the reference sequences.
    """

    def __init__(self, border_gff: Gff, genome: TextIO) -> None:
        self._genome = genome
        self._borders = border_gff
        super().__init__()
        logger.debug('Initiated %r', self)

    def __repr__(self) -> str:
        return 'HaplotypePosition(border_gff=%r, genome=%r)' % (self._borders, self._genome)

    def modify(self,
               locus: pd.DataFrame,
               logging_configurer: Callable[[], logging.Logger]) -> HaplotypeTable:
        self._logger = logging_configurer()
        locus_name = locus.index.get_level_values(LOCUS_COLUMN_NAME)[0]
        self._logger.debug('Adding haplotype positions for locus %s', locus_name)

        # From the border gff file, get the two borders flanking the locus
        border_locations = self._borders.get_enties_by_attribute_value("NAME", locus_name)
        if not border_locations:
            raise ValueError(f"No borders were found for locus {locus_name}.")
        if not len(border_locations) == 2:
            raise ValueError(f"Found {len(border_locations)} borders "
                             f"for locus {locus_name}, expected 2.")

        # Get the chromosome for the locus, check if they match for both borders
        chromosomes = set(border.chrom for border in border_locations)
        if not len(chromosomes) == 1:
            raise ValueError(f"The borders for {locus_name} do not share the same chromosome")
        chromosome = chromosomes.pop()

        # Check which border comes first.
        border1, border2 = self._order_borders(border_locations)
        reference_start = border1.end
        reference_end = border2.start

        # Get the reference haplotype sequences from the reference genome
        # (= in between the borders).
        reference_sequence = self._get_reference_haplotype_sequence(chromosome,
                                                                    reference_start,
                                                                    reference_end)

        # Add information to table
        self._add_edit_column(reference_sequence, locus)
        locus = self._add_reference_haplotype_if_missing(reference_sequence, locus)
        self._add_position_columns(reference_start, reference_end, locus)

        return HaplotypeTable(locus)

    def _add_edit_column(self, reference_sequence: str, locus: pd.DataFrame) -> None:
        """
        Add the 'edit' column to the locus table. the edit column is based on the comparison
        between the haplotype and the reference sequence. If they haplotype is the reference
        sequence, it is indicated by 'ref' in the column. Otherwise, the column value is the
        difference in length between the haplotype and the reference sequence.
        """

        def same_as_reference(haplotype):
            """Function to check if a haplotype sequence is the reference requence, if not,
               return the difference in length between the reference and the haplotype
            """
            return REFERENCE_COLUMN_VALUE \
                if haplotype == reference_sequence \
                else len(reference_sequence) - len(haplotype)

        haplotypes = locus.index.get_level_values(HAPLOTYPE_COLUMN_NAME)
        column_values = map(same_as_reference, haplotypes)
        column_series = Series(list(column_values))
        self.add_index_column(column_series, locus, REFERENCE_COLUMN_NAME)

    def _add_reference_haplotype_if_missing(self, reference_sequence, locus) -> pd.DataFrame:
        if 'ref' not in locus.index.get_level_values(REFERENCE_COLUMN_NAME):
            locus_name = locus.index.get_level_values(LOCUS_COLUMN_NAME)[0]
            reference_name = locus.index.get_level_values(CHROMOSOME_COLUMN_NAME)[0]
            target = locus.index.get_level_values(TARGET_COLUMN_NAME)[0]
            to_add_index = pd.MultiIndex.from_arrays([[reference_name],
                                                      [locus_name],
                                                      [reference_sequence],
                                                      [target],
                                                      ['ref']],
                                                     names=locus.index.names)
            to_add = pd.DataFrame([[np.nan] * len(locus.columns)],
                                  columns=locus.columns,
                                  index=to_add_index)
            locus = pd.concat([to_add, locus])
            return locus
        return locus

    def _add_position_columns(self, reference_start, reference_end, locus) -> None:
        """
        Add the position columns to the locus table. Adds two columns: one for
        the start position of the haplotype on the reference genome and one for
        the end position.
        """
        haplotypes = locus.index.get_level_values(HAPLOTYPE_COLUMN_NAME)
        start_positions = [reference_start] * len(haplotypes)
        end_positions = [reference_end] * len(haplotypes)
        self.add_index_column(Series(start_positions), locus, START_COLUMN_NAME)
        self.add_index_column(Series(end_positions), locus, END_COLUMN_NAME)

    def _get_reference_haplotype_sequence(self, chromosome: str, start: int, stop: int):
        """
        Retrieves the correct chromosome/scaffold from a fastq file containing the
        reference sequences, and returns only the part of that scaffold between the
        start and stop position. Here, this function is used to retreive the part of the
        reference genome between the borders.
        """
        for record in SeqIO.parse(self._genome, "fasta"):
            if record.id == chromosome:
                self._genome.seek(0)
                return str(record.seq[start:stop])
        raise ValueError("Could not find genomic sequence "
                         f"with ID {chromosome} in input .fasta file.")

    @staticmethod
    def _order_borders(border_locations: Iterable[Interval]) -> Tuple[Interval, Interval]:
        """Calculate which borders comes first. Assumes to only choose between two borders,
        which were defined in the same orientation (+).
        """
        border1, border2 = border_locations
        # Use assert here, because pybedtools already checks the correct gff format.
        # So this situation should never occur
        assert (border1.start < border1.stop) and (border2.start < border2.stop)
        first_border = border1 if border1.start < border2.start else border2
        second_border = border1 if first_border is border2 else border2
        return first_border, second_border


class AddGuideFilter(Annotation):
    """
    Add information about the gRNA design to the table and generate the haplotype
    name and gRNA Filter based on that information

    :param gRNAs_gff: class:`Gff` object containing the positions of the gRNAs that define
        that were used for the base editor.
    : param gRNA_relative_naming if set to True the relative naming will take the gRNA
        strandedness into account, if set to False relative naming will be done to the reference.
    """

    def __init__(self, gRNAs_gff: Gff, nuclease_offset: int, cut_site_range_lower: int,
                 cut_site_range_upper: int, gRNA_relative_naming) -> None:
        self._gRNAs: Gff = gRNAs_gff
        self.nuclease_offset = nuclease_offset
        self.tp_range_lower = cut_site_range_lower
        self.tp_range_upper = cut_site_range_upper
        self.gRNA_relative_naming = gRNA_relative_naming
        super().__init__()

    def modify(self,
               locus: pd.DataFrame,
               logging_configurer: Callable[[], logging.Logger]) -> HaplotypeTable:
        logger = logging_configurer()
        logger.debug('Performing filtering based in cut-site range.')
        # Get expected cutt site
        self.get_expected_cut_site(locus)

        # Compare observed and expected sites
        all_alterations = self.compare_observed_expected_site(locus)

        # reformat
        all_alterations_reformat = (all_alterations.pivot(index='index',
                                                          columns='type',
                                                          values=GUIDE_FILTER_COLUMNAME))

        # Add filter values for INDELS and SNPs separately
        for type_ in [INDEL_COLUMNNAME, SNP_COLUMNNAME]:
            locus = self.add_index_column(all_alterations_reformat[type_],
                                          locus,
                                          GUIDE_FILTER_COLUMNAME + '_' + type_)

        # Add filter values for INDELS and SNPs combined
        combined = (all_alterations_reformat.max(axis=1).astype('boolean'))
        self.add_index_column(combined, locus, GUIDE_FILTER_COLUMNAME)

        # Add haplotype Names
        haplotype_names = self.create_haplotype_names(all_alterations)
        locus = self.add_index_column(haplotype_names, locus, HAPLOTYPE_NAME)

        # Add Expected cut site
        locus = self.add_index_column(pd.Series([self.expected_cut_site] * locus.shape[0]), locus,
                                      EXPECTED_CUT_SITE_COLUM_NAME)

        return HaplotypeTable(locus)

    def get_expected_cut_site(self, locus):
        '''
        Get the expected cut-site for the design, uses the NUCLEASE and NUCLEASE_CONFIG
        to extract that information if the nuclease_offset is negative, extract it from
        the end of the gRNA, if it is positive add it to the start location of the gRNA.

        :param locus: pd.DataFrame
        :return: set the self.expected_cut_site variable
        '''
        # get gRNA location
        locus_name = locus.index.get_level_values(LOCUS_COLUMN_NAME)[0]
        gRNA_location = self._gRNAs.get_enties_by_attribute_value("NAME", locus_name)

        if len(gRNA_location) != 1:
            raise ValueError(f'You have provided {len(gRNA_location)} gRNAs for {locus_name}. '
                             f'Please provide exactly one gRNA per locus')

        gRNA_location = gRNA_location[0]
        if gRNA_location.strand not in ['+', '-']:
            raise ValueError(f'gRNA for {locus_name} did not have a strand defined. '
                             f'Please define the strandedness of your gRNA')

        self.strand = 1
        if gRNA_location.strand == '+':
            gRNA_start = gRNA_location.start
            nuclease_offset = self.nuclease_offset

        elif gRNA_location.strand == '-':
            gRNA_start = gRNA_location.end
            nuclease_offset = -self.nuclease_offset
            if self.gRNA_relative_naming:
                self.strand = -1
            tp_range_lower = self.tp_range_lower
            tp_range_upper = self.tp_range_upper
            self.tp_range_lower = tp_range_upper
            self.tp_range_upper = tp_range_lower

        # calculate expected cut site.
        self.expected_cut_site = gRNA_start + nuclease_offset

    def compare_observed_expected_site(self, locus):
        '''
        Compares observed and expected cut site
        :param locus: pd.DataFrame
        :return: pd.DataFrame: all alterations dataframe
             index FILTER_gRNA   type               0
              0          NaN    SNP             NaN
              1          NaN    SNP             NaN
              2          NaN    SNP             NaN
              3        False    SNP    (-12, A, T)
              0          NaN  INDEL            None
              1        False  INDEL    (-14, A, AA)
              2        False  INDEL  (-14, AGAG, A)
              3        False  INDEL   (-16, TGA, T)

        '''

        def check_if_in_tp_range(self, alteration):
            # return TRUE if one of the SNPs is within the TP_RANGE or if INDEL
            # start position or indel postion + indel position + indel length is in TP_RANGE
            def add_indel_length(y):
                return max([len(y[1]), len(y[2])]) - 1

            def calculate_range(y, tp_range, how):
                mode = {'lower': [operator.gt, operator.neg], 'upper': [operator.lt, operator.pos]}
                comp_op, sign_op = mode[how]
                return max([comp_op(y[0], sign_op(tp_range)),
                            comp_op(
                                y[0] + sign_op(add_indel_length(y)),
                                tp_range)]
                           )

            checks = [max([
                calculate_range(y, self.tp_range_lower, 'lower') if int(y[0]) < 0
                else calculate_range(y, self.tp_range_upper, 'upper')
                for y in x
            ])
                      if x
                      else np.nan
                      for x in alteration]
            return checks

        all_alterations = []
        for type_ in [SNP_COLUMNNAME, INDEL_COLUMNNAME]:
            # Parse SNP and INDEL data
            # calculate observed edit sites, for each SNP/INDEL detected
            # Correct if gRNA is on the reverse strand
            alteration = [[(self.strand * (y[0] - self.expected_cut_site + 2), y[1], y[2])
                           for y in x]
                          if not pd.isna(x)
                          else []
                          for x in locus.index.get_level_values(type_)]
            alteration_df = pd.DataFrame(alteration)
            # check if edit is in TP range
            alteration_df[GUIDE_FILTER_COLUMNAME] = check_if_in_tp_range(self, alteration)
            alteration_df['type'] = type_
            all_alterations.append(alteration_df)

        all_alterations = pd.concat(all_alterations).reset_index()
        return all_alterations

    def create_haplotype_names(self, all_alterations):
        '''
        Create a name for each haplotype based on the difference
        between expected and observed cut site.

        Reference: "ref"
        SNPS: <distance between obs and expected>:S:<REF>-<ALT>
        DELETIONS: <distance between obs and expected>:<length of deletion>D:<REF>-<ALT>
        INSERTIONS: <distance between obs and expected>:<length of insetion>I:<REF>-<ALT>


        :param all_alterations: pd.DataFrame: all alterations dataframe
        :return: pd.Series with names for each haplotype in locus dataframe
        '''

        def create_indel_tuple(x):
            '''
            Extends the indel tuple with additional information
            :param x: tuple with (POS, REF, ALT)
            :return:
            '''
            pos, ref, alt = x
            first = len(ref)
            sec = len(alt)
            if first > sec:
                return (pos, first - sec, 'D', ref, alt)
            else:
                return (pos, sec - first, 'I', ref, alt)

        def create_names(x):
            '''
            Row function that does the actual creation of the names
            :param x: pandas.core.groupby.GroupBy
            :return:
            '''
            # reference row
            col = GUIDE_FILTER_COLUMNAME if GUIDE_FILTER_COLUMNAME in x.columns else 0
            if x[col].isna().all():
                return 'ref'
            # non reference row
            # reformat
            numeric_cols = [col for col in x.columns if str(col).isnumeric()]
            reformatted = (x[numeric_cols + ['type']].set_index('type'))
            # loop over INDELS and SNPS (INDELS first)
            indel_name, snp_name = '', ''
            for type_ in [INDEL_COLUMNNAME, SNP_COLUMNNAME]:
                reformatted_line = reformatted.loc[type_]
                if type_ == INDEL_COLUMNNAME:
                    indel_name = ','.join(
                        ['%i:%i%s:%s-%s' % create_indel_tuple(x) for x in
                         reformatted_line if not pd.isna(x)])

                else:
                    snp_name = ','.join(['%i:S:%s-%s' % x
                                         for x in reformatted_line if not pd.isna(x)])

            return ','.join([x for x in [indel_name, snp_name] if x])

        return all_alterations.groupby('index').apply(create_names)


class AddHaploTypeName(AddGuideFilter):
    """
    Create the Haplotypes column when no gRNAs are present

    """

    def __init__(self) -> None:
        next

    def modify(self,
               locus: pd.DataFrame,
               logging_configurer: Callable[[], logging.Logger]) -> HaplotypeTable:
        logger = logging_configurer()
        logger.debug('Create name for each haplotype')

        # Reformat locus columns
        all_alterations = self.reformat(locus)
        # Create haplotype names
        haplotype_names = self.create_haplotype_names(all_alterations)
        locus = self.add_index_column(haplotype_names, locus, HAPLOTYPE_NAME)

        return HaplotypeTable(locus)

    def reformat(self, locus):
        """Function that reformats SNP and INDEL column names"""
        all_alterations = []
        for type_ in [SNP_COLUMNNAME, INDEL_COLUMNNAME]:
            # Parse SNP and INDEL data
            # calculate observed edit sites, for each SNP/INDEL detected
            # Correct if gRNA is on the reverse strand
            alteration = [[((y[0]), y[1], y[2]) for y in x]
                          if not pd.isna(x)
                          else []
                          for x in locus.index.get_level_values(type_)]
            alteration_df = pd.DataFrame(alteration)
            # check if edit is in TP range
            alteration_df['type'] = type_
            all_alterations.append(alteration_df)
        all_alterations = pd.concat(all_alterations).reset_index()
        return all_alterations


class ProteinPrediction(Annotation):
    """
    Add information about the effect of the true positive mutations (ie within the TP_RANGE)
    on the protein. If mutations occur out of the TP_RANGE, output 100% of identity as these
    mutations should not be considered.

    :param local_gff: class:'Gff' object containing the positions of the CDS.
                      All CDS interval must be in the + orientation.
    :param genome: location of a .fasta file containing the reference sequences.
    """

    def __init__(self,
                 local_gff: str,
                 genome: TextIO,
                 tp_range_lower: int,
                 tp_range_upper: int,
                 with_gRNAs=False) -> None:
        self._genome = genome
        self._local_gff = local_gff
        self._tp_range_lower = tp_range_lower
        self._tp_range_upper = tp_range_upper
        self._with_gRNAs = with_gRNAs
        super().__init__()
        logger.debug('Initiated %s.', self)

    def __repr__(self) -> str:
        return (f'ProteinPrediction(local_gff={self._local_gff!r},' +
                f'genome={self._genome!r},' +
                f'tp_range_lower={self._tp_range_lower},' +
                f'tp_range_upper={self._tp_range_upper})')

    def modify(self,
               locus: pd.DataFrame,
               logging_configurer: Callable[[], logging.Logger]) -> HaplotypeTable:
        self._logger = logging_configurer()
        locus_name = locus.index.get_level_values(LOCUS_COLUMN_NAME)[0]
        self._logger.debug('Adding effect on protein for %s.', locus_name)
        gene_id = locus.index.get_level_values(CHROMOSOME_COLUMN_NAME)[0]
        # read the local gff file
        annotation = gffpd.read_gff3(self._local_gff)
        annotation_df = annotation.df
        annotation_df[['seq_id', 'source']] = annotation_df[['seq_id', 'source']].astype(str)
        # run the protein prediction
        locus = self._predict_protein(gene_id, locus, annotation_df)
        return HaplotypeTable(locus)

    def _predict_protein(self,
                         gene_id: str,
                         locus: pd.DataFrame,
                         annot_df: pd.DataFrame) -> pd.DataFrame:
        """
        Backbone function that integrates all the other functions required to estimate the
        mutated protein sequences, the presence of mutations at strategic sites (ATG, donor/acceptor
        splicing sites). It takes advantage of the column included via other class (GuideFilter,
        PairwiseAlignment, ...). It relies on a annotation file that should contain at least gene
        and CDS information. All features should be oriented in the + direction.
        """
        protein_id_res, splicing_res, atg_res, prot_seq_res, stop_codon_res = [], [], [], [], []
        # Get additional columns
        aln_list = list(locus.index.get_level_values(ALIGNMENT_COLUMNNAME))
        cut_site_list = [None] * len(aln_list)
        if self._with_gRNAs:
            cut_site_list = list(locus.index.get_level_values(EXPECTED_CUT_SITE_COLUM_NAME))
        amplicon_start_list = list(locus.index.get_level_values(START_COLUMN_NAME))
        loc_name_list = list(locus.index.get_level_values(LOCUS_COLUMN_NAME))
        hap_name_list = list(locus.index.get_level_values(HAPLOTYPE_NAME))
        # amplicon_stop_list = list(locus.index.get_level_values(END_COLUMN_NAME))
        edit_list = list(locus.index.get_level_values(REFERENCE_COLUMN_NAME))
        columns = zip(aln_list, cut_site_list, amplicon_start_list,
                      edit_list, loc_name_list, hap_name_list)
        # Initiate locus-level list of warnings
        loc_warning = []

        # 1. Get the genomic seq
        gene_seq = self._get_gene_seq(gene_id)

        # 2. Check that the gene length are equal between gff and fasta
        if not self._test_gene_length(gene_id, annot_df, len(gene_seq)):
            logger.warning('Sequence length for gene %s does not match between ' +
                           'reference fasta and annotation gff', (gene_id))

        # Loop through the rows
        for (aln, cut_site, amplicon_start, edit_item, loc_name, hap_name) in columns:
            # 3. Get the CDS code
            global_ref_cds_code, extended_global_ref_cds_code = \
                self._get_global_cds_code(gene_id, len(gene_seq), annot_df)

            # Get the wild-type protein
            wt_prot_seq = self.get_protein_sequence(gene_seq, global_ref_cds_code)

            # Focus on haplotype different than REF
            if edit_item == REFERENCE_COLUMN_VALUE:
                protein_id_res.append(np.nan)
                splicing_res.append('')
                atg_res.append('')
                stop_codon_res.append('')
                prot_seq_res.append(wt_prot_seq)
                continue

            # 4. Extract the aligned and non-aligned local sequences
            aln_ref_seq, aln_mut_seq = str(aln).split('\n')[0], str(aln).split('\n')[2]
            ref_seq = aln_ref_seq.replace('-', '')

            # 5. Extract the zone around the guide cut size (TP_RANGE) --> local coordinates
            # If this is Crispr edited data, extract the zone around the cut site
            # considered true positives
            if cut_site:
                if self._tp_range_lower == -inf:
                    logger.warning("A guide gff file has been provided to the command line "
                                   "but the lower bound of the region of interest is set to "
                                   "-infinite (default). Please consider providing a negative "
                                   "integer to the command line using the -r flag.")
                    raise ValueError("Please provide a negative integer instead of default "
                                     "-inf using the -r flag")
                if self._tp_range_upper == inf:
                    logger.warning("A guide gff file has been provided to the command line "
                                   "but the upper bound of the region of interest is set to "
                                   "+infinite (default). Please consider providing a positive "
                                   "integer to the command line using the -s flag.")
                    raise ValueError("Please provide a positive integer instead of default inf "
                                     "using the -s flag")
                local_cut_site = cut_site - amplicon_start
                extraction_range = (max(local_cut_site - self._tp_range_lower, 0),
                                    min(local_cut_site + self._tp_range_upper,
                                        len(ref_seq) - 1))
            else:
                extraction_range = (0, len(ref_seq) - 1)
            local_start, local_end = extraction_range
            # 6. Find the local area to extract in the aln
            aln_extraction_area = (aln.get_alignment_coordinate(extraction_range[0], 'start'),
                                   aln.get_alignment_coordinate(extraction_range[1], 'end'))
            # 7. Extract the local aln and associated sequences
            local_aln = [seq[aln_extraction_area[0]:aln_extraction_area[1] + 1]
                         for seq in [aln_ref_seq, aln_mut_seq]]
            _, local_mut_aln = local_aln
            local_mut_seq = local_mut_aln.replace('-', '')
            # 8. Extract the local reference cds code
            ref_cds_start, ref_cds_stop = local_start, local_end + 1
            local_ref_cds_code_range = slice(amplicon_start + ref_cds_start,
                                             amplicon_start + ref_cds_stop)
            local_ref_cds_code = extended_global_ref_cds_code[local_ref_cds_code_range]
            # 9. Mutate the local CDS code
            local_mut_cds_code = self.modify_local_cds_code(local_ref_cds_code,
                                                            local_aln[0],
                                                            local_aln[1])
            # 10. Replace local mutations in the genomic context
            mut_gene_seq = "".join((gene_seq[:amplicon_start + ref_cds_start],
                                    local_mut_seq,
                                    gene_seq[amplicon_start + ref_cds_stop:]))
            mut_cds_code = "".join(
                (extended_global_ref_cds_code[:amplicon_start + ref_cds_start],
                    local_mut_cds_code,
                    extended_global_ref_cds_code[amplicon_start + ref_cds_stop:]))
            # 11. Check if strategic sites are impacted
            ref_win = (amplicon_start + ref_cds_start, amplicon_start + ref_cds_stop)
            atg_test, splicing_test, stop_codon_test, break_site, hap_warning = \
                self.check_strategic_sites(loc_name,
                                           hap_name,
                                           gene_seq,
                                           global_ref_cds_code,
                                           ref_win,
                                           mut_gene_seq,
                                           mut_cds_code)
            # 11b. Append haplotype-level annotation warnings to the locus-level annotation warning
            loc_warning.extend(hap_warning)
            # 12. Get the WT and mutated protein sequences, considering mutation
            # in splicing site (break_site)
            wt_prot_seq = self.get_protein_sequence(gene_seq, extended_global_ref_cds_code)
            if not np.isnan(break_site):
                mut_prot_seq = self.get_protein_sequence(mut_gene_seq[0:break_site],
                                                         mut_cds_code[0:break_site])
            else:
                mut_prot_seq = self.get_protein_sequence(mut_gene_seq, mut_cds_code)
            # 13. Get the percentage of identity between the two proteins
            id_perc = self.get_prot_aln_indices(wt_prot_seq, mut_prot_seq)
            id_perc_str = round(id_perc, 1)
            # 14. Overwrite the id result if the initial ATG codon is modified
            if atg_test:
                id_perc_str = 0
            # Add elements on initial codon and splicing codon to the list of results
            prot_seq_res.append(mut_prot_seq)
            protein_id_res.append(id_perc_str)
            splicing_res.append(splicing_test)
            atg_res.append(atg_test)
            stop_codon_res.append(stop_codon_test)

        if loc_warning:
            for w in set(loc_warning):
                logger.warning("Strange annotation in gene {}: {}".format(gene_id, w))

        # Add results to the locus data frame
        self.add_index_column(Series(atg_res), locus, 'atgCheck')
        self.add_index_column(Series(splicing_res), locus, 'splicingSiteCheck')
        self.add_index_column(Series(stop_codon_res), locus, 'stopCodonCheck')
        self.add_index_column(Series(prot_seq_res), locus, 'protein_sequence')
        self.add_index_column(Series(protein_id_res).astype(float),
                              locus,
                              'pairwiseProteinIdentity (%)')
        return locus

    def get_prot_aln_indices(self, wt_prot: str, mut_prot: str):
        """
        Function to compute the percentage of identity of the pairwise alignment
        of the wild type and mutated proteins. It counts the numbers of identical amino
        acides that are aligned. Then it divides this number by the length of the alignment.
        It returns the percentage of identity as a float.
        """
        blosum64 = Align.substitution_matrices.load("BLOSUM62")
        aligner = Align.PairwiseAligner(mode='global',
                                        substitution_matrix=blosum64,
                                        open_gap_score=-5,
                                        extend_gap_score=-0.5
                                        )
        alignments = aligner.align(wt_prot.replace('*', ''),
                                   mut_prot.replace('*', ''))
        alignment = alignments[0]
        aln_id = (str(alignment).split('\n')[1].count('|') / len(
            str(alignment).split('\n')[0])) * 100
        return aln_id

    def check_strategic_sites(self,
                              loc_name: str,
                              hap_name: str,
                              global_ref_seq: str,
                              global_ref_cds_code: str,
                              ref_win: tuple,
                              global_mut_seq: str,
                              global_mut_cds_code: str):
        """
        Function to check if the START codon (ATG), the donor and acceptor sites
        are altered by mutations. If it is the case, it raises a warning to True. Two kind
        of warnings are raised, whether the START codon is impacted (atg_warning) or splicing
        are modified (splicing_warning). These two informations are indicated in the final output
        table and could serve to predict the impact of the mutation.
        """

        def extract_sites(s, c):
            """
            Function to extract information about strategic sites, such as the type
            (ATG, acceptor/donor splicing sites, stop codon), the sequence,
            the position in the whole nucleotide sequence. It uses the genomic (s) and cds code (c)
            sequences as inputs. It returns a nested dictionary that stores all the information
            about strategic sites.
            """
            cds_intervals = sorted([(m.start(0), m.end(0)) for m in re.finditer(r'[1]+', c)])
            strategic_sites_dict = defaultdict(dict)
            if len(cds_intervals) > 1:
                for i, cds in enumerate(cds_intervals):
                    descr = f"strategic_site_{((i + 1) * 2) - 1}"
                    next_descr = f"strategic_site_{(i + 1) * 2}"
                    if i == 0:  # First codon
                        strategic_sites_dict[descr]["type"] = "start_codon"
                        strategic_sites_dict[descr]["loc"] = list(range(cds[0], cds[0] + 3))
                        strategic_sites_dict[descr]["seq"] = s[cds[0]:cds[0] + 3]
                        strategic_sites_dict[next_descr]["type"] = "donor_site"
                        strategic_sites_dict[next_descr]["loc"] = list(
                            range(cds[-1] + 1, cds[-1] + 3))
                        strategic_sites_dict[next_descr]["seq"] = s[cds[-1]:cds[-1] + 2]
                    elif i == len(cds_intervals) - 1:  # Last codon
                        strategic_sites_dict[descr]["type"] = "acceptor_site"
                        strategic_sites_dict[descr]["loc"] = list(range(cds[0] - 2, cds[0]))
                        strategic_sites_dict[descr]["seq"] = s[cds[0] - 2:cds[0]]
                        strategic_sites_dict[next_descr]["type"] = "stop_codon"
                        strategic_sites_dict[next_descr]["loc"] = list(
                            range(cds[-1] - 2, cds[-1] + 1))
                        strategic_sites_dict[next_descr]["seq"] = s[cds[-1] - 3:cds[-1]]
                    else:  # Any intermediate cds chunk
                        strategic_sites_dict[next_descr]["type"] = "acceptor_site"
                        strategic_sites_dict[next_descr]["loc"] = list(range(cds[0] - 2, cds[0]))
                        strategic_sites_dict[next_descr]["seq"] = s[cds[0] - 2:cds[0]]
                        strategic_sites_dict[descr]["type"] = "donor_site"
                        strategic_sites_dict[descr]["loc"] = list(range(cds[-1] + 1, cds[-1] + 3))
                        strategic_sites_dict[descr]["seq"] = s[cds[-1]:cds[-1] + 2]
            elif len(cds_intervals) == 1:  # Only 1 CDS in annotation
                site1 = "strategic_site_1"
                site2 = "strategic_site_2"
                strategic_sites_dict[site1]["type"] = "start_codon"
                strategic_sites_dict[site1]["loc"] = list(range(cds_intervals[0][0],
                                                                cds_intervals[0][0] + 3))
                strategic_sites_dict[site1]["seq"] = s[cds_intervals[0][0]:cds_intervals[0][0] + 3]
                strategic_sites_dict[site2]["type"] = "stop_codon"
                strategic_sites_dict[site2]["loc"] = list(range(cds_intervals[0][-1] - 2,
                                                                cds_intervals[0][-1] + 1))
                strategic_sites_dict[site2]["seq"] = s[cds_intervals[0][-1] - 3:
                                                       cds_intervals[0][-1]]
            return strategic_sites_dict

        def check_strategic_sites_annotations(ss_dict: dict):
            """
            Function to check that the START codon is ATG, that the stop codon
            is TAA, TAG or TGA, that acceptor site is AG and donor site is GT.
            Any deviation from these rules prints a warning to sdout.
            """
            warning_list = []
            for ss, attributes in ss_dict.items():
                if attributes['type'] == "start_codon":
                    if attributes['seq'] != "ATG":
                        warning_list.append("Warning: The start codon differs from ATG "
                                            "(Methionine) in the reference annotation.")
                elif attributes['type'] == "stop_codon":
                    if attributes['seq'] not in ["TAA", "TAG", "TGA"]:
                        warning_list.append("Warning: The stop codon differs from "
                                            "TAA/TAG/TGA in the reference annotation.")
                elif attributes['type'] == "donor_site":
                    if attributes['seq'] != "GT":
                        warning_list.append("Warning: The donor splicing site located at position "
                                            f"{attributes['loc'][0]}-{attributes['loc'][-1]} "
                                            "differs from GT.")
                elif attributes['type'] == "acceptor_site":
                    if attributes['seq'] != "AG":
                        warning_list.append("Warning: The acceptor splicing site located at "
                                            f"position {attributes['loc'][0]}-"
                                            f"{attributes['loc'][-1]} differs from AG.")
            return(set(warning_list))

        def test_local_mutation(tag_name, ref_dict, mut_dict):
            """
            Function that takes a strategic site tag ID and tests if the sequences
            of the strategic site are the same between the reference and the mutant
            dictionaries of strategic sites.
            """
            """
            print("\nREF DICT\n")
            print(json.dumps(ref_dict, indent=2))
            print("\nMUT DICT\n")
            print(json.dumps(mut_dict, indent=2))
            """
            return ref_dict[tag_name]["seq"] != mut_dict[tag_name]["seq"]

        def test_tuple_overlap(x, y):
            """
            Function to test for overlap between two tuples
            """
            return max(x[0], y[0]) <= min(x[-1], y[-1])

        atg_warning, stop_codon_warning, splicing_warning, break_site = False, False, False, np.nan

        ref_ss_dict = extract_sites(global_ref_seq, global_ref_cds_code)
        mut_ss_dict = extract_sites(global_mut_seq, global_mut_cds_code)

        warning_list = check_strategic_sites_annotations(ref_ss_dict)

        for ss in ref_ss_dict:
            if test_tuple_overlap(ref_win, ref_ss_dict[ss]["loc"]) and \
                    test_local_mutation(ss, ref_ss_dict, mut_ss_dict):
                logger.info(f"Locus {loc_name}, haplotype {hap_name}: mutations "
                            "detected in a strategic site "
                            f"({ref_ss_dict[ss]['type']}) located at positions "
                            f"{ref_ss_dict[ss]['loc'][0]}-{ref_ss_dict[ss]['loc'][-1]}")
                if ref_ss_dict[ss]["type"] == "start_codon":
                    atg_warning = True
                elif ref_ss_dict[ss]["type"] == "donor_site":
                    splicing_warning = True
                    break_site = mut_ss_dict[ss]["loc"][0] - 1
                elif ref_ss_dict[ss]["type"] == "acceptor_site":
                    splicing_warning = True
                    break_site = mut_ss_dict[ss]["loc"][-1] - 1
                elif ref_ss_dict[ss]["type"] == "stop_codon":
                    stop_codon_warning = True
        return atg_warning, splicing_warning, stop_codon_warning, break_site, warning_list

    def get_protein_sequence(self, gene_seq: str, global_ref_cds_code: str):
        """
        Function that translate a genomic DNA sequence into a protein based on
        the binary annotation code. It gather the genomic areas corresponding to '1's
        (ie coding regions) and then translate using Bio.Seq. It returns the protein seq
        as a string.
        """

        def scale_cds(cds):
            """
            Function to scale a CDS sequence to a multiple of 3 otherwise a
            warning is raised by Bio.Seq
            """
            if len(cds) % 3 != 0:
                scaled_cds = cds + 'N' * (3 - (len(cds) % 3))
            else:
                scaled_cds = cds
            return scaled_cds

        cds = ''
        for i, pos in enumerate(gene_seq):
            if global_ref_cds_code[i] == '1':
                cds += pos
        protein_seq = str(Seq(scale_cds(cds)).translate(to_stop=True)) + '*'
        return protein_seq

    def modify_local_cds_code(self,
                              ref_cds_code: str,
                              ref_allele_aln: str,
                              mut_allele_aln: str):
        """
        Function that modify a reference binary CDS code into a mutated one. Deletions and SNPs
        are easy to treat but insertions are more difficult because the surronding genomic context
        has to be considered. If the insertions occurs in a non-coding region, the insertion is
        assumed non-coding as well. Same reasoning for coding regions. If the insertions happens
        right at the junction between coding and non-coding regions, it is assumed that the
        insertion is coding because the splicing site should not be modified.
        """

        def fill_gaps_in_cds_code(gappy_cds_code: str):
            """
            Function that takes a gappy CDS binary code a fill the gaps by either '0' or '1'
            depending on the surrounding context. Gappy extremities are filled with the
            closest annotation.
            """
            # First check for gappy extremities with no context and fill them
            if gappy_cds_code[0] == '-':
                first_gap_window = re.findall(r"-+", gappy_cds_code)[0]
                gappy_cds_code = \
                    gappy_cds_code[len(first_gap_window)] * len(first_gap_window) + \
                    gappy_cds_code.lstrip('-')

            if gappy_cds_code[-1] == '-':
                last_gap_window = re.findall(r"-+", gappy_cds_code)[-1]
                gappy_cds_code = \
                    gappy_cds_code.rstrip('-') + \
                    gappy_cds_code[-len(last_gap_window) - 1] * len(last_gap_window)

            gaps = re.findall(r"-+", gappy_cds_code)
            new_cds_code = gappy_cds_code
            for gap in gaps:
                fill_dict = {('0', '0'): (len(gap) * '0', 1),
                             ('1', '1'): (len(gap) * '1', 1)}
                left_pos_index = new_cds_code.find(gap) - 1
                right_pos_index = new_cds_code.find(gap) + len(gap)
                flanking_bases = new_cds_code[left_pos_index], new_cds_code[right_pos_index]
                orig, repl = fill_dict.get(flanking_bases, (len(gap) * '1', 1))
                new_cds_code = new_cds_code.replace(gap, orig, repl)
            return new_cds_code

        def insert_in_cds_code(insertions: list, cds_code: str):
            """
            Function that inserts gaps in a CDS binary code based on a list
            of insertions to include. The list contains the index of the gap
            opening and the length of the gap window. Then it calls another function
            to fill the gaps depending on the surrounding context.
            """
            inserted_cds_code = cds_code
            for index, length in insertions:
                cds_with_gaps = (
                    inserted_cds_code[:index], "-" * length, inserted_cds_code[index:])
                inserted_cds_code = "".join(cds_with_gaps)
            filled_cds_code = fill_gaps_in_cds_code(inserted_cds_code)
            return filled_cds_code

        def delete_in_cds_code(mut_allele_aln: str, cds_code: str):
            """
            Function that delete items in the CDS binary code based on a gappy mutated
            sequence whose length is the same as the CDS binary code. It returns a shorter
            CDS code with deletions and no gaps.
            """
            return "".join([del_cds for pos, del_cds in
                            zip(mut_allele_aln, cds_code) if pos != '-'])

        # Record the INDELs
        list_insertions, list_deletions = [], []
        # Record insertions in the aln (focus on the reference allele aln)
        for match in re.finditer(r"-+", ref_allele_aln):
            list_insertions.append((match.start(), len(match.group())))
        # Record deletions in the aln (focus on the mutated allele aln)
        for match in re.finditer(r"-+", mut_allele_aln):
            list_deletions.append((match.start(), len(match.group())))
        # Identify different scenarios
        mutated_cds_code = ''
        if list_insertions and list_deletions:
            inserted_cds_code = insert_in_cds_code(list_insertions, ref_cds_code)
            deleted_cds_code = delete_in_cds_code(mut_allele_aln, inserted_cds_code)
            mutated_cds_code = deleted_cds_code
        elif list_insertions and not list_deletions:
            inserted_cds_code = insert_in_cds_code(list_insertions, ref_cds_code)
            mutated_cds_code = inserted_cds_code
        elif list_deletions and not list_insertions:
            deleted_cds_code = delete_in_cds_code(mut_allele_aln, ref_cds_code)
            mutated_cds_code = deleted_cds_code
        else:
            mutated_cds_code = ref_cds_code
        return mutated_cds_code

    def _get_global_cds_code(self, gene_id, gene_len, annot_df: pd.DataFrame):
        """
        Function that uses a gff file with CDS annotations to build a binary CDS code with
        0 meaning non-coding and 1 meaning coding areas. The last CDS chunk is extended
        with 1 beyond the stop codon. This is to allow the translation to continue if any earlier
        shift changes the reading frame.
        """
        # WARNING: Assuming that CDS are always of type 'CDS', in + orientation
        cds_annotation = annot_df[(annot_df.seq_id == gene_id) & (annot_df.type == 'CDS')]
        cds_ranges = [(i, j) for i, j in zip(cds_annotation.start, cds_annotation.end)]
        # Get the CDS code. Note that annotations are 1-based (GFF) while python is 0-based
        cds_code = []
        for i in range(1, gene_len + 1):
            test = False
            for cds_range in cds_ranges:
                start, stop = cds_range[0], cds_range[1]
                if start <= i <= stop:
                    test = True
                    break

            cds_code.append('1' if test else '0')

        # Extend the last cds code to 'open' the frameshift in the end
        cds_code = "".join(cds_code)
        extended_cds_code = cds_code.rstrip('0') + '1' * (
                len(cds_code) - len(cds_code.rstrip('0')))
        return cds_code, extended_cds_code

    def _test_gene_length(self, gene_id: str, annot_df: pd.DataFrame, gene_len_seq: int):
        """
        Function that does a sanity check to make sure that the gene in the fasta sequence and
        the 'gene' as mentionned in the annotation file are of same length.
        """
        # Get the length of the gene in the annotation file.
        # WARNING: many hypothesis here regarding the structure of the GFF
        # For instance the gene should always start at position 1 and should
        # always be of type 'gene'
        genes = (annot_df.seq_id == gene_id) & (annot_df.type == "gene")
        if not genes.any():
            raise ValueError(f'Gene {gene_id} not found in annotation gff.')
        gene_len_annot = annot_df.loc[genes, 'end'].iloc[0]
        assert gene_len_annot <= gene_len_seq, (f"The length of gene {gene_id} specified in the "
                                                "gene annotation is smaller than the length of "
                                                "the reference.")
        return gene_len_annot == gene_len_seq

    def _get_gene_seq(self, gene_id: str):
        """
        Function that fetches the genomic sequence in the fasta reference file provided by the user
        """
        for rec in SeqIO.parse(self._genome, "fasta"):
            if rec.id == gene_id:
                self._genome.seek(0)
                return str(rec.seq)
        raise ValueError(f"Could not find genomic sequence with ID {gene_id} in input .fasta file.")
