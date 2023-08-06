from collections import namedtuple
from enum import Enum
from typing import Optional

from arps.core.resources_table import ResourcesTable, Resources
from arps.core.simulator.resource import TrackedValue, EvtType
from arps.core.simulator.sim_event import SimEvent
from arps.core.simulator.estimators_table import EstimatorsTable

RState = namedtuple('RState', ['owner', 'status'])
STATUS = Enum('STATUS', 'acquired, free')


class SimpleEvent(SimEvent):

    def __init__(self, identifier, *, arrival_time,
                 resources_table: ResourcesTable,
                 estimators_table: EstimatorsTable, env_type: int,
                 remaining_time: Optional[int] = None) -> None:
        self._env_type = env_type
        super().__init__(identifier=identifier,
                         arrival_time=arrival_time,
                         remaining_time=remaining_time,
                         resources_table=resources_table,
                         estimators_table=estimators_table)

    def allocate_resource(self, resources: Resources, epoch: int) -> bool:
        if resources.environment_type != self._env_type:
            return False

        resource_instance = resources['Resource']
        if resource_instance.value != RState(None, STATUS.free):
            return False

        acquired = RState(self.identifier, STATUS.acquired)
        resource_instance.value = TrackedValue(acquired, epoch, self.identifier, EvtType.des_pre)
        if self._remaining_time is None:
            self._remaining_time = self.estimators_table[resources.environment_id].duration()

        return True

    def pos(self, epoch: int):
        assert self.scheduled
        assert self.resources_table is not None

        resources = self.resources_table.resources_from_environment(environment_id=self.environment_id)
        resource_instance = resources['Resource']
        if resource_instance.value.owner == self.identifier:
            resource_instance.value = TrackedValue(RState(None, STATUS.free), epoch, self.identifier, EvtType.des_pos)
