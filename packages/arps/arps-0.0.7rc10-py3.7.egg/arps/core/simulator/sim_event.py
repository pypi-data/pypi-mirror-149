import logging
from typing import Optional, Generator, Any

from arps.core.resources_table import Resources, ResourcesTable
from arps.core.simulator.estimators_table import EstimatorsTable


class SimEvent:
    '''
    Class that represents simulations event
    '''

    __slots__ = (
        '_arrival_time',
        '_start_time',
        'identifier',
        'resources_table',
        'estimators_table',
        'environment_id',
        'info',
        '_remaining_time',
        '_finished_time',
        'logger'
    )

    def __init__(self, *, identifier: int,
                 arrival_time: int,
                 remaining_time: Optional[int] = None,
                 resources_table: Optional[ResourcesTable] = None,
                 estimators_table: Optional[EstimatorsTable] = None,
                 event_specific_info: Optional[Any] = None) -> None:
        '''Initializes event. Remaining time is optional since it can be
        calculated using estimators.

        If estimator is used, the remaining_time argument will be
        overwritten.

        Args:
        - identifier: event id
        - arrival_time: event arrival time on the system
        - remaining_time: how many cycles til finishes executions
        - resources_table: table containing all resources from all
          environments
        - estimators_table: table containing estimators
        - event_specific_info: information about the event to be
        accessed from outside

        '''
        assert isinstance(arrival_time, int)
        self._arrival_time = arrival_time
        self._start_time: Optional[int] = None
        self.identifier = identifier
        self.resources_table = resources_table
        self.estimators_table = estimators_table
        self.environment_id: Optional[int] = None
        self.info = event_specific_info or ''
        self._remaining_time: Optional[int] = remaining_time
        self._finished_time: Optional[int] = None
        self.logger = logging.getLogger(self.__class__.__name__)

    @property
    def arrival_time(self) -> int:
        '''
        Returns event arrival time
        '''
        return self._arrival_time

    @property
    def start_time(self) -> Optional[int]:
        '''
        Returns event start time
        '''
        return self._start_time

    @property
    def finished_time(self) -> Optional[int]:
        '''
        Returns event finished time
        '''
        return self._finished_time

    def schedule(self, environment, epoch: int) -> None:
        self.environment_id = environment
        self._start_time = epoch

    @property
    def scheduled(self) -> bool:
        return self.environment_id is not None

    def process(self) -> Generator:
        '''Executes each step of the event.

        During development, it will check if the result type of
        main_task is boolean. This is necessary otherwise the task can
        be stuck in a infinity loop. For example, if the user forgets
        to return something, None is return by default.

        '''
        while self.environment_id is None:
            yield

        remaining_time = self._remaining_time
        assert remaining_time is not None and remaining_time > 0, remaining_time
        self.logger.debug('Processing event %s', self.identifier)
        while remaining_time:
            epoch = yield
            task_executed = self.main_task(epoch)
            assert isinstance(task_executed, bool), 'main task should return a boolean'
            if task_executed:
                remaining_time -= 1
        else:
            self._finished_time = epoch
            self.pos(epoch)

    def allocate_resource(self, resources: Resources, epoch: int) -> bool:
        '''This method tests if the event allocate resources

        Args

        - resources: resources present in a single environment
        - epoch: when it tried to allocate resources

        Returns:

        True if it allocates, False otherwise
        '''
        return True

    def main_task(self, epoch: int) -> bool:
        '''This method is executed every simulation's step

        Args:

        - epoch: the current epoch when the main_task is executed

        Returns:

        True if the task execute (so it can decrease the amount of
        time allocate to execute the task), False otherwise.

        '''
        return True

    def pos(self, epoch: int) -> None:
        '''This method is executed after the task is finished

        Args:
        - epoch: the current epoch when the main_task is executed

        '''

    def reset(self):
        '''
        Reset the event but does not undo the possible modifications done by the task
        '''
        self._finished_time = None
        self.environment_id = None

    def __repr__(self):
        return f'{self.__class__.__name__}(identifier={self.identifier}, arrival_time={self.arrival_time}, remaining_time={self._remaining_time}, start_time={self.start_time}, finished_time={self.finished_time})'

    def __str__(self):
        return f'{self.__class__.__name__}(identifier={self.identifier}, arrival={self.arrival_time}, duration={self._remaining_time}, started={self.start_time}, finished={self.finished_time})'
