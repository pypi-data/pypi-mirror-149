import logging
from contextlib import suppress
from random import randrange
from typing import Union

from arps.core.resources_table import Resources, ResourcesTable
from arps.core.simulator.estimators_table import (EstimatorsTable,
                                                  EstimatorsTableError)
from arps.core.simulator.event_factory import EventFactory
from arps.core.simulator.resource import EvtType, TrackedValue
from arps.core.simulator.sim_event import SimEvent
from arps.test_resources.dummies.dummy_estimators import (dummy_main_estimator,
                                                          dummy_pos_estimator)

estimators_table = EstimatorsTable()
estimators_table.add_estimator(0, 'main_estimate', dummy_main_estimator)
estimators_table.add_estimator(0, 'pos_estimate', dummy_pos_estimator)


class DummySimEvent(SimEvent):
    __slots__ = ('modifier', 'original')

    def __init__(
        self,
        *,
        identifier: int,
        arrival_time: int,
        remaining_time: int,
        resources_table: ResourcesTable,
        estimators_table: EstimatorsTable,
        modifier: int,
    ) -> None:
        self.modifier = modifier
        self.original = modifier
        super().__init__(
            arrival_time=arrival_time,
            remaining_time=remaining_time,
            identifier=identifier,
            resources_table=resources_table,
            estimators_table=estimators_table,
            event_specific_info=f'initial state: {self.modifier}',
        )
        self.logger = logging.getLogger(self.__class__.__name__)

    def allocate_resource(self, resources: Resources, epoch: int) -> bool:
        resource = resources['ResourceA']
        environment_id = resources.environment_id
        try:
            result = estimators_table[environment_id].main_estimate(
                resource.value, self.modifier
            )
            resource.value = TrackedValue(
                result, epoch, self.identifier, EvtType.des_pre
            )
            return True
        except (EstimatorsTableError, ValueError):
            # self.logger.warning('Error while allocating resource: %s', err)
            return False

    def pos(self, epoch):
        resources = self.resources_table.resources_from_environment(
            environment_id=self.environment_id
        )
        resource = resources['ResourceA']
        with suppress(ValueError):
            resource.value = TrackedValue(
                estimators_table[self.environment_id].pos_estimate(
                    resource.value, self.modifier
                ),
                epoch,
                self.identifier,
                EvtType.des_pos,
            )


class DummyEventFactory(EventFactory):
    def __call__(
        self,
        identifier: Union[str, int],
        arrival_time: Union[str, int],
        remaining_time: Union[str, int],
        modifier: Union[str, int],
    ) -> SimEvent:
        '''Parse an entry from a file.

        Args:

        - line: a line containing 4 items, an identifier, arrival
        time, remaining_time, and op_value (the value that will change
        the resource)

        '''
        assert self.resources_table
        assert self.estimators_table

        return DummySimEvent(
            identifier=int(identifier),
            arrival_time=int(arrival_time),
            remaining_time=int(remaining_time),
            resources_table=self.resources_table,
            estimators_table=self.estimators_table,
            modifier=int(modifier),
        )


class DummyEventParamsGenerator:
    def __init__(self) -> None:
        self.arrival_time = 1
        self.task_id = 0

    def __call__(self):
        self.arrival_time += randrange(0, 4)
        self.task_id += 1
        remaining_time = randrange(1, 3)
        modifier = randrange(1, 30)
        return self.task_id, self.arrival_time, remaining_time, modifier
