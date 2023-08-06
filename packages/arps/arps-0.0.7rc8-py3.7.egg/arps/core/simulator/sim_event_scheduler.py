from typing import Set, List, Generator

from arps.core.simulator.sim_event import SimEvent
from arps.core.resources_table import Resources


class NoEnvironmentAvailable(Exception):
    '''Error used when no resource is available so it is pointless to try
    to allocate a resource to the event

    '''


class SimEventScheduler:
    def __init__(self, environments: Set[Resources]) -> None:
        '''Initializes the scheduler

        Args:

        - environments: a dict with each environment and its
        resources. It should be retrieved from the ResourcesTable
        class

        '''
        self._environments = environments

    def schedule(self, sim_events: List[SimEvent], epoch: int) -> Generator[SimEvent, None, None]:
        '''This method is responsible for the assignment of an environment to
        the SimEvent's task based on the strategy

        Args:
        - sim_events: list of SimEvent instances
        - epoch: current epoch

        Return:
        - generator of scheduled events that has just been scheduled
        '''

        try:
            for sim_event in sim_events:
                if sim_event.scheduled:
                    continue

                for resources in self._load_available_environments():
                    if sim_event.allocate_resource(resources, epoch):
                        sim_event.schedule(resources.environment_id, epoch)
                        yield sim_event
                        break
        except NoEnvironmentAvailable:
            return

    def _load_available_environments(self) -> Set[Resources]:
        environments = set(resources for resources in self._environments if all(resource.available() for resource in resources))
        if not environments:
            raise NoEnvironmentAvailable
        return environments
