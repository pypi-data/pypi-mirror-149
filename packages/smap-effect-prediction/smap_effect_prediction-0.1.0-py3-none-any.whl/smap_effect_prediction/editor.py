from abc import ABC, abstractmethod
from typing import Iterable
import logging
from smap_effect_prediction.logging_configuration \
    import configure_subprocess_logger
from .modifications.modification import TableModification, ModificationType, LocusModification
from .models import Table
from operator import ge, gt
from multiprocessing import Pool, cpu_count, Queue
from functools import partial

logger = logging.getLogger()


class Editor(ABC):
    """An abstract class to edit :class:`.models.Table` objects.
       Provide means to queue modifications and finally apply the modifications.
    """
    def __init__(self) -> None:
        self._modifications = []

    @abstractmethod
    def edit(self, table: Table) -> Table:
        """Edit a :class:`.models.Table` by applying queued modifications in order.

        :param table: :class:`.models.Table` to be modified.
        :return: an edited :class:`.models.Table`.
        """

    def queue_modification(self, modification: Iterable[TableModification]) -> None:
        """Add a modification(s) to the list of modifications to be executed.

        :param modification: an iterable of :class:`.modifications.modification.TableModification`
        objects to be queued.
        """
        if not all([isinstance(mod, TableModification) for mod in modification]):
            raise ValueError("Can only queue TableModification objects.")
        self._modifications.extend(modification)
        logger.debug('Queued %s operations.', len(self._modifications))


class MultiProcessEditor(Editor):
    """Edit :class:`.models.Table` objects by applying modifications.
       Modifications can be queued, before they are applied to the Table in FIFO order.
       Faster processing is achieved by deviding the work over multiple processes is possible.

    :param number_of_processes: Maximum number of allowed processes to be used.
    :raises ValueError: The chosen number of maximum processes is larger or equal to the number of
        processing cores in the system.

    :example:
        >>> editor = MultiProcessEditor(2)
        >>> alignment_mod = PairwiseAlignment()
        >>> editor.queue_modification(alignment_mod)
        >>> edited_table = editor.edit(haplotype_table)
    """
    def __init__(self, logging_queue: Queue, number_of_processes: int = 1) -> None:
        # if the number of processes is 1 using >= will always raise
        # so use > in that case
        process_comparison = ge if number_of_processes != 1 else gt
        if process_comparison(number_of_processes, cpu_count()):
            raise ValueError("Please leave one CPU core available for the system.")
        self._number_of_processes = number_of_processes
        logger.info('Using %s proces%s.', self._number_of_processes,
                    'es' if self._number_of_processes > 1 else '')
        self._logging_queue = logging_queue
        super().__init__()
        logger.debug('%r initiated.', self)

    def __repr__(self):
        return f'MultiProcessEditor(number_of_processes={self._number_of_processes})'

    def edit(self, table: Table) -> Table:
        """Apply queued modifications to a :class:`.models.Table` by splitting the work over
           multiple processes if possible.

        :param table: :class:`.models.Table` to be modified.
        :return: an edited :class:`.models.Table`.
        """
        logger.debug('Started processing.')
        if not self._modifications:
            raise RuntimeError("No modifications queued.")
        with Pool(self._number_of_processes) as p:
            dispatch_dict = {ModificationType.LOCI: self._edit_loci,
                             ModificationType.DATAFRAME: self._edit_dataframe,
                             ModificationType.SAMPLES: self._edit_samples}
            for modification in self._modifications:
                logger.info('Applying %s', type(modification).__name__)
                mod_type = modification.operates_on()
                logger.debug('Modification needs to be applied to %r.', mod_type)
                table = dispatch_dict[mod_type](p, modification, table)
        self._modifications = []
        return table

    def _edit_loci(self, p: Pool, modification: LocusModification, table: Table) -> Table:
        """Apply a class:`.modifications.modification.LocusModification` to a :class:`.models.Table`.
           Use a class:`multiprocessing.Pool` to split the work for the loci over several processes.

        :param p: A class:`multiprocessing.Pool`
        :param modification: the class:`.modifications.modification.LocusModification` to be applied
            to the :class:`.models.Table`.
        :param table: Table object that will be modified.
        :return: The modified Table.
        """
        logger.debug('Distributing work for each locus over different processes.')
        logging_configurer = partial(configure_subprocess_logger, self._logging_queue)
        modificiation_with_queue = partial(modification.modify,
                                           logging_configurer=logging_configurer)
        modified_loci = p.map(modificiation_with_queue, table.iter_loci())
        logger.debug('All loci processed, concatenating results.')
        return table.concat(modified_loci)

    def _edit_dataframe(self, p: Pool, modification: TableModification, table: Table) -> Table:
        logger.debug('Appying modification to dataframe as a whole.')
        return modification.modify(table.dataframe, logging_configurer=logging.getLogger)

    def _edit_samples(self, table: Table) -> Table:
        raise NotImplementedError
