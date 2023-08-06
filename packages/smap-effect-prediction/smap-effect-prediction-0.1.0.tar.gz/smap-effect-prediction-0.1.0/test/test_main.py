import logging
from unittest import TestCase
from smap_effect_prediction.__main__ import log_args, parse_args, set_default_frequency_thresholds
from argparse import Namespace
from pathlib import Path
from textwrap import dedent
import sys
from math import inf


class TestMain(TestCase):
    def test_logging_command_line_arguments(self):
        logger = logging.getLogger()
        test_input = Namespace(borders=Path('foo/bar/borders.gff'),
                               cas_offset=-3,
                               cpu=32,
                               cut_site_range=9,
                               cut_site_range_lower=9,
                               debug=False,
                               discrete_calls='dominant',
                               effect_threshold=80.0,
                               frequency_bounds=['diploid'],
                               frequency_table=Path('foo/bar/haplotype_frequencies.tsv'),
                               gap_extension=-10,
                               gap_open_penalty=-100,
                               genome=Path('foo/bar/reference.fasta'),
                               gRNAs=Path('foo/bar/gRNAs.gff'),
                               local_gff_file='foo/bar/108_documents.gff',
                               logging_level=20,
                               match_score=1,
                               mismatch_penalty=-100)
        with self.assertLogs(logger) as logger_cm:
            log_args(test_input, logger)
        expected_result = dedent("""
        Running SMAP effect predictor using the following options:

        Input & output:
            Frequency table: foo/bar/haplotype_frequencies.tsv
            Genome: foo/bar/reference.fasta
            Borders gff: foo/bar/borders.gff
            Annotation gff: foo/bar/108_documents.gff
            gRNAs gff: foo/bar/gRNAs.gff
            Cas offset: -3

        Alignment parameters:
            Match score: 1
            Mismatch penalty: -100
            Gap open penalty: -100
            Gap extension penalty: -10

        Discrete calls options:
            Discrete call mode: dominant
            Frequency bounds: ['diploid']

        Filtering options:
            Cut site range upper bound: 9
            Cut site range lower bound: 9

        Protein effect prediction:
            Protein effect threshold: 80.0

        System resources:
            Number of processes: 32
        """)
        self.assertEqual(logger_cm.output, [f'INFO:root:{expected_result}'])

    def test_argument_parsing(self):
        arguments = ["/foo/bar/haplotype_frequencies.tsv",
                     "/foo/bar/reference.fasta",
                     "/foo/bar/borders.gff",
                     "--gene_annotation", "/foo/bar/108_documents.gff",
                     "--gRNAs", "/foo/bar/gRNAs.gff",
                     "--cas_protein", "CAS9",
                     "--effect_threshold", "80",
                     "--cut_site_range_upper_bound", "9",
                     "--cut_site_range_lower_bound", "9",
                     "-c", "32",
                     "-e", "dominant",
                     "-i", "diploid"]
        expected = Namespace(borders=Path('/foo/bar/borders.gff'),
                             cas_offset=17,
                             cpu=32,
                             cut_site_range=9,
                             cut_site_range_lower=9,
                             debug=False,
                             disable_protein_prediction=False,
                             discrete_calls='dominant',
                             effect_threshold=80.0,
                             frequency_bounds=['diploid'],
                             frequency_table=Path('/foo/bar/haplotype_frequencies.tsv'),
                             gap_extension=-10,
                             gap_open_penalty=-100,
                             genome=Path('/foo/bar/reference.fasta'),
                             gRNAs=Path('/foo/bar/gRNAs.gff'),
                             local_gff_file='/foo/bar/108_documents.gff',
                             logging_level=20,
                             match_score=1,
                             mismatch_penalty=-100,
                             no_gRNA_relative_naming=True)
        parsed_arguments = parse_args(arguments)
        self.assertEqual(parsed_arguments, expected)

    def test_cas_offset_requires_guides(self):
        arguments = ["/foo/bar/haplotype_frequencies.tsv",
                     "/foo/bar/reference.fasta",
                     "/foo/bar/borders.gff",
                     "--gene_annotation", "/foo/bar/108_documents.gff",
                     "--cas_offset", "-3"]
        err_message = r"A gRNAs \.gff needs to be specified " + \
                      r"together with '--cas_offset' or '--cas_protein'\."
        with self.assertRaisesRegex(ValueError, err_message):
            parse_args(arguments)

    def test_enable_debug_logging(self):
        if hasattr(sys, 'tracebacklimit'):
            curr_tracebacklimit = sys.tracebacklimit
            delattr(sys, 'tracebacklimit')
        else:
            curr_tracebacklimit = None
        try:
            arguments = ["/foo/bar/haplotype_frequencies.tsv",
                         "/foo/bar/reference.fasta",
                         "/foo/bar/borders.gff",
                         "--gene_annotation", "/foo/bar/108_documents.gff",
                         "--debug"]
            parsed_args = parse_args(arguments)
            self.assertEqual(parsed_args.logging_level, logging.DEBUG)
            self.assertFalse(hasattr(sys, 'tracebacklimit'))
            arguments = ["/foo/bar/haplotype_frequencies.tsv",
                         "/foo/bar/reference.fasta",
                         "/foo/bar/borders.gff",
                         "--gene_annotation", "/foo/bar/108_documents.gff"]
            parsed_args = parse_args(arguments)
            self.assertEqual(parsed_args.logging_level, logging.INFO)
            self.assertEqual(sys.tracebacklimit, 0)
            delattr(sys, 'tracebacklimit')
        finally:
            if curr_tracebacklimit:
                sys.tracebacklimit = curr_tracebacklimit

    def test_not_annotation_or_disable_protein_raises(self):
        arguments = ["/foo/bar/haplotype_frequencies.tsv",
                     "/foo/bar/reference.fasta",
                     "/foo/bar/borders.gff"]
        message = r"Please provide an annotation \.gff or use --disable_protein_prediction\."
        with self.assertRaisesRegex(ValueError, expected_regex=message):
            parse_args(arguments)

    def test_both_guides_and_disable_protein_raises(self):
        arguments = ["/foo/bar/haplotype_frequencies.tsv",
                     "/foo/bar/reference.fasta",
                     "/foo/bar/borders.gff",
                     "--gene_annotation", "/foo/bar/annotation.gff",
                     "--disable_protein_prediction"]
        message = r"--gene_annotation and --disable_protein_prediction are mutually exclusive\."
        with self.assertRaisesRegex(ValueError, expected_regex=message):
            parse_args(arguments)

    def test_only_annotation(self):
        arguments = ["/foo/bar/haplotype_frequencies.tsv",
                     "/foo/bar/reference.fasta",
                     "/foo/bar/borders.gff",
                     "--gene_annotation", "/foo/bar/annotation.gff"]
        result = parse_args(arguments)
        expected = Namespace(borders=Path('/foo/bar/borders.gff'),
                             cas_offset=None,
                             cas_protein=None,
                             cpu=1,
                             cut_site_range=inf,
                             cut_site_range_lower=-inf,
                             debug=False,
                             disable_protein_prediction=False,
                             discrete_calls=None,
                             effect_threshold=None,
                             frequency_bounds=None,
                             frequency_table=Path('/foo/bar/haplotype_frequencies.tsv'),
                             gap_extension=-10,
                             gap_open_penalty=-100,
                             genome=Path('/foo/bar/reference.fasta'),
                             gRNAs=None,
                             local_gff_file='/foo/bar/annotation.gff',
                             logging_level=20,
                             match_score=1,
                             mismatch_penalty=-100,
                             no_gRNA_relative_naming=True)
        self.assertEqual(result, expected)

    def test_disable_protein_without_guides_raises(self):
        arguments = ["/foo/bar/haplotype_frequencies.tsv",
                     "/foo/bar/reference.fasta",
                     "/foo/bar/borders.gff",
                     "--disable_protein_prediction"]
        message = r"--disable_protein_prediction requires --gRNAs\."
        with self.assertRaisesRegex(ValueError, expected_regex=message):
            parse_args(arguments)

    def test_default_frequency_thresholds(self):
        input_args = Namespace(discrete_calls='dominant',
                               frequency_bounds=['diploid'])
        result = set_default_frequency_thresholds(input_args)
        self.assertListEqual(result.frequency_bounds, [10.0])

        input_args = Namespace(discrete_calls='dosage',
                               frequency_bounds=['diploid'])
        result = set_default_frequency_thresholds(input_args)
        self.assertListEqual(result.frequency_bounds, [10.0, 10.0, 90.0, 90.0])

        input_args = Namespace(discrete_calls='dominant',
                               frequency_bounds=['tetraploid'])
        result = set_default_frequency_thresholds(input_args)
        self.assertListEqual(result.frequency_bounds, [10.0])

        input_args = Namespace(discrete_calls='dosage',
                               frequency_bounds=['tetraploid'])
        result = set_default_frequency_thresholds(input_args)
        self.assertListEqual(result.frequency_bounds,
                             [12.5, 12.5, 37.5, 37.5, 62.5, 62.5, 87.5, 87.5])

        input_args = Namespace(discrete_calls=None,
                               frequency_bounds=['tetraploid'])
        # No discrete calls requested, leave as is.
        result = set_default_frequency_thresholds(input_args)
        self.assertListEqual(result.frequency_bounds, ['tetraploid'])

        input_args = Namespace(discrete_calls='dominant',
                               frequency_bounds=[])
        message = r'If discrete calling is enabled, please define ' + \
                  r'the interval bounds using the frequency_bounds ' + \
                  r'parameter \(see --help for more information\)\."'
        with self.assertRaisesRegex(ValueError, message):
            set_default_frequency_thresholds(input_args)

    def test_wrong_default_frequency_thresholds_raises(self):
        input_args = Namespace(discrete_calls='dominant',
                               frequency_bounds=[10.0, 10.0, 90.0])
        message = r"If setting the thresholds manually in dominant mode, " + \
                  r"the thresholds must adhere to the following condition: 1 threshold"
        with self.assertRaisesRegex(ValueError, message):
            set_default_frequency_thresholds(input_args)

        input_args = Namespace(discrete_calls='dosage',
                               frequency_bounds=[10.0])
        message = r"If setting the thresholds manually in dosage mode, " + \
                  r"the thresholds must adhere to the following condition: " + \
                  r"Odd number of thresholds \(at least 4\)"
        with self.assertRaisesRegex(ValueError, message):
            set_default_frequency_thresholds(input_args)
