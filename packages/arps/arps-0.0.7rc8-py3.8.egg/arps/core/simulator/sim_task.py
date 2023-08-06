from typing import Optional

from arps.core.simulator.estimators_table import EstimatorsTable
from arps.core.resources_table import ResourcesTable, Resources


class SimTask:
    '''
    Class that represents a task to be executed during the simulation
    '''

    def __init__(self, identifier, *, resources_table: ResourcesTable = None,
                 estimators_table: EstimatorsTable = None) -> None:
        '''
        Args
        - identifier : unique identifier
        - resources_table: a table containing available resources to be modified.
        - estimators_table: a table containing available estimators to modify resources.
        '''
        self.identifier = identifier
        self._environment: Optional[int] = None
        self.resources_table = resources_table
        self.estimators_table = estimators_table

    @property
    def environment(self) -> Optional[int]:
        return self._environment

    @environment.setter
    def environment(self, environment: int) -> None:
        if self._environment is None or environment is None:
            self._environment = environment

    def allocate_resource(self, resources: Resources, epoch: int) -> bool:
        '''This method tests if the task allocate resources

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
