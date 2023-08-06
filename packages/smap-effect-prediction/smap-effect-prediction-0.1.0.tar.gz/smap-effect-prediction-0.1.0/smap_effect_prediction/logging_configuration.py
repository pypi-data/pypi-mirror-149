import sys
import logging
from logging.handlers import QueueHandler
import colorlog
from multiprocessing import Queue, Manager
from queue import Empty
import threading

logger = logging.getLogger()


def configure_main_logger(level: int):
    handler = logging.StreamHandler(sys.stdout)
    formatter = colorlog.ColoredFormatter(
                '%(log_color)s%(asctime)s %(levelname)s: %(message)s',
                log_colors={
                    'DEBUG':    'reset',
                    'INFO':     'reset',
                    'WARNING':  'yellow',
                    'ERROR':    'red',
                    'CRITICAL': 'red',
                })
    handler.setFormatter(formatter)
    logging.basicConfig(level=level,
                        handlers=[handler])
    logger = logging.getLogger()
    logger.debug('Configured main thread logging.')
    return logger


class QueueLogger(threading.Thread):
    def __init__(self):
        manager = Manager()
        self._logging_queue = manager.Queue(-1)
        self.stop_event = threading.Event()
        super().__init__(name='QueueLogger')
        logger.debug('Initiated %r.', self)

    def __repr__(self) -> str:
        return 'QueueLogger()'

    def run(self):
        logger.debug('Logging thread started.')
        while True:
            try:
                record = self._logging_queue.get(block=True, timeout=0.05)
            except Empty:
                continue
            if record is None:
                self._logging_queue.task_done()
                break
            logger.handle(record)
            self._logging_queue.task_done()
        logger.debug('Exiting logging thread.')

    @property
    def logging_queue(self):
        return self._logging_queue

    def stop(self):
        self._logging_queue.put(None)
        self._logging_queue.join()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args, **kwargs):
        self.stop()


def configure_subprocess_logger(queue: Queue):
    qh = QueueHandler(queue)
    logger = logging.getLogger()
    for handler in logger.handlers:
        logger.removeHandler(handler)
    logger.addHandler(qh)
    return logger
