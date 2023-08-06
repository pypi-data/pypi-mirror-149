import sys
from unittest import TestCase, mock
import logging
from smap_effect_prediction.logging_configuration import (configure_main_logger,
                                                          QueueLogger,
                                                          QueueHandler,
                                                          configure_subprocess_logger)
import colorlog
import multiprocessing
import time
from queue import Queue

logger = logging.getLogger()


class TestLoggingConfiguration(TestCase):
    @mock.patch('smap_effect_prediction.logging_configuration.logging.basicConfig')
    def test_configure_main_logger(self, mocked_basicconfig):
        returned_logger = configure_main_logger(logging.DEBUG)
        mocked_basicconfig.assert_called_once()
        self.assertEqual(returned_logger, logging.getLogger())
        _, call_args = mocked_basicconfig.call_args_list[0]
        # Cannot use assert_called_once_with because __eq__ is not implemented for StreamHandler
        self.assertEqual(len(call_args), 2)
        self.assertEqual(call_args['level'], logging.DEBUG)
        self.assertEqual(len(call_args['handlers']), 1)
        handler = call_args['handlers'][0]
        self.assertIsInstance(handler, logging.StreamHandler)
        self.assertEqual(handler.stream, sys.stdout)
        self.assertIsInstance(handler.formatter, colorlog.ColoredFormatter)
        self.assertDictEqual(handler.formatter.log_colors,
                             {'DEBUG': 'reset',
                              'INFO': 'reset',
                              'WARNING': 'yellow',
                              'ERROR': 'red',
                              'CRITICAL': 'red'})

    @mock.patch('smap_effect_prediction.logging_configuration.logging.Logger.addHandler')
    def test_configure_subprocess_logger(self, mocked_addhandler):
        queue = Queue()
        stored_handler = logger.handlers
        logger.handlers = [logging.StreamHandler(sys.stdout)]
        try:
            returned_logger = configure_subprocess_logger(queue)
            self.assertEqual(returned_logger, logger)
            mocked_addhandler.assert_called_once()
            call_args, _ = mocked_addhandler.call_args_list[0]
            self.assertEqual(len(call_args), 1)
            handler = call_args[0]
            self.assertIsInstance(handler, QueueHandler)
            self.assertEqual(handler.queue, queue)
            self.assertEqual(logger.handlers, [])
        finally:
            logger.handlers = stored_handler


class TestQueueLogger(TestCase):
    def test_queue_logging(self):
        def subprocess(logging_queue):
            qh = QueueHandler(logging_queue)
            logger = logging.getLogger()
            for handler in logger.handlers:
                logger.removeHandler(handler)
            logger.addHandler(qh)
            time.sleep(0.1)
            logger.info('Test')
        stream_handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(stream_handler)
        try:
            with self.assertLogs(logger) as logger_cm:
                with QueueLogger() as queue_logger:
                    logging_queue = queue_logger.logging_queue
                    process = multiprocessing.Process(target=subprocess, args=(logging_queue,))
                    process.start()
                    process.join()
            self.assertListEqual(logger_cm.output, ['INFO:root:Test'])
        finally:
            logger.removeHandler(stream_handler)
