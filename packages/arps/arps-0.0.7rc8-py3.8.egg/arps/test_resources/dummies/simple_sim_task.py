from collections import namedtuple
from enum import Enum

from arps.core.resources_table import ResourcesTable, Resources
from arps.core.simulator.resource import TrackedValue, EvtType
from arps.core.simulator.sim_task import SimTask

RState = namedtuple('RState', ['owner', 'status'])
STATUS = Enum('STATUS', 'acquired, free')


class SimpleTask(SimTask):

    def __init__(self, identifier, *, resources_table: ResourcesTable, env_type: int) -> None:
        self._env_type = env_type
        super().__init__(identifier, resources_table=resources_table)

    def allocate_resource(self, resources: Resources,
                          epoch: int) -> bool:
        if resources.environment_type != self._env_type:
            return False

        resource_instance = resources['Resource']
        if resource_instance.value != RState(None, STATUS.free):
            return False

        acquired = RState(self.identifier, STATUS.acquired)
        resource_instance.value = TrackedValue(acquired, epoch, self.identifier, EvtType.des_pre)
        return True

    def pos(self, epoch: int):
        resources = self.resources_table.resources_from_environment(environment_id=self.environment)
        resource_instance = resources['Resource']
        if resource_instance.value.owner == self.identifier:
            resource_instance.value = TrackedValue(RState(None, STATUS.free), epoch, self.identifier, EvtType.des_pos)
