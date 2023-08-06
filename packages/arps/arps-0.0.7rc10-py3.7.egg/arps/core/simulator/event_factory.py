import abc
from typing import Any, Optional

from arps.core.resources_table import ResourcesTable
from arps.core.simulator.estimators_table import EstimatorsTable
from arps.core.simulator.sim_event import SimEvent


class EventFactory(metaclass=abc.ABCMeta):

    def __init__(self,
                 resources_table: Optional[ResourcesTable] = None,
                 estimators_table: Optional[EstimatorsTable] = None) -> None:
        self.resources_table = resources_table
        self.estimators_table = estimators_table

    @abc.abstractmethod
    def __call__(self, identifier: int, arrival_time: Any,
                 remaining_time: Optional[Any]) -> SimEvent:
        '''This method should create a new event with a new task
        '''
