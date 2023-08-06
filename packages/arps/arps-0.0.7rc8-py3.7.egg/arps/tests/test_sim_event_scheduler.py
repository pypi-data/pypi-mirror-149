import asyncio
from contextlib import suppress

import pytest  # type: ignore

from arps.core.clock import simulator_clock_factory
from arps.core.resources_table import ResourcesTable
from arps.core.simulator.estimators_table import EstimatorsTable
from arps.core.simulator.resource import Resource
from arps.core.simulator.sim_event_scheduler import SimEventScheduler
from arps.core.simulator.simulator import Simulator
from arps.test_resources.dummies.dummy_resource import DummyCategory
from arps.test_resources.dummies.simple_event import STATUS, RState, SimpleEvent


def arrival_started_finished_tuple(event_queue, task_id):
    task_id = task_id - 1
    return (event_queue[task_id].arrival_time, event_queue[task_id].start_time, event_queue[task_id].finished_time)


async def run_clock(clock, event_queue):
    clock.start()

    clock_task = asyncio.create_task(clock.run())

    while not all(event.finished_time is not None for event in event_queue):
        await asyncio.sleep(0)

    clock_task.cancel()

    await clock_task


class SimpleEventFactory:
    def __init__(self, resources_table, estimators_table):
        self.resources_table = resources_table
        self.estimators_table = estimators_table
        self.identifier = 1

    def __call__(self, arrival, remaining, env_type=0):
        event = SimpleEvent(
            identifier=self.identifier,
            arrival_time=arrival,
            remaining_time=remaining,
            resources_table=self.resources_table,
            estimators_table=self.estimators_table,
            env_type=env_type,
        )
        self.identifier += 1
        return event


class Resource_(Resource):
    def available(self):
        return self.value == RState(None, STATUS.free)


@pytest.mark.asyncio
async def test_schedule():
    resource = Resource_(
        environment_identifier=0, category=DummyCategory.Value, initial_state=RState(None, STATUS.free)
    )
    resource.__class__.__name__ = 'Resource'  # to work with SimpleEvent

    resources_table = ResourcesTable(environment_types={0: 0})

    resources_table.add_resource(resource)

    estimators_table = EstimatorsTable()
    estimators_table.add_estimator(0, 'duration', lambda: None)

    make_sim_event = SimpleEventFactory(resources_table, estimators_table)
    event_queue = [make_sim_event(arrival=1, remaining=3), make_sim_event(arrival=1, remaining=1)]

    sim_event_scheduler = SimEventScheduler(resources_table.environments)

    assert all(not event.scheduled for event in event_queue)
    events_scheduled = list(sim_event_scheduler.schedule(event_queue, 1))
    assert event_queue[0] in events_scheduled
    assert event_queue[1] not in events_scheduled
    assert event_queue[0].scheduled
    assert not event_queue[1].scheduled

    process_task = event_queue[0].process()
    process_task.send(None)
    for epoch, resource_available in zip(range(1, 4), (False, False, True)):
        with suppress(StopIteration):
            process_task.send(epoch)
            assert resource.available() == resource_available
    else:
        assert resource.available() == resource_available

    events_scheduled = list(sim_event_scheduler.schedule(event_queue, 3))
    # since it is already scheduled
    assert event_queue[0] not in events_scheduled
    assert event_queue[1] in events_scheduled
    assert all(event.scheduled for event in event_queue)


@pytest.mark.asyncio
async def test_default_scheduler_single_environment():
    resource = Resource(environment_identifier=0, category=DummyCategory.Value, initial_state=RState(None, STATUS.free))

    resources_table = ResourcesTable(environment_types={0: 0})

    resources_table.add_resource(resource)

    estimators_table = EstimatorsTable()
    estimators_table.add_estimator(0, 'duration', lambda: None)

    make_sim_event = SimpleEventFactory(resources_table, estimators_table)

    event_queue = [
        make_sim_event(arrival=1, remaining=4),
        make_sim_event(arrival=3, remaining=3),
        make_sim_event(arrival=4, remaining=1),
        make_sim_event(arrival=4, remaining=2),
        make_sim_event(arrival=4, remaining=3),
    ]

    sim_event_scheduler = SimEventScheduler(resources_table.environments)

    clock = simulator_clock_factory()

    simulator = Simulator(event_queue, sim_event_scheduler)
    clock.add_listener(simulator.step)

    await run_clock(clock, event_queue)

    assert (1, 1, 4) == arrival_started_finished_tuple(event_queue, 1)
    assert (3, 5, 7) == arrival_started_finished_tuple(event_queue, 2)
    assert (4, 8, 8) == arrival_started_finished_tuple(event_queue, 3)
    assert (4, 9, 10) == arrival_started_finished_tuple(event_queue, 4)
    assert (4, 11, 13) == arrival_started_finished_tuple(event_queue, 5)


@pytest.mark.asyncio
async def test_homogeneous_environment():
    resource_one = Resource(
        environment_identifier=0, category=DummyCategory.Value, initial_state=RState(None, STATUS.free)
    )
    resource_two = Resource(
        environment_identifier=1, category=DummyCategory.Value, initial_state=RState(None, STATUS.free)
    )

    resources_table = ResourcesTable(environment_types={0: 0, 1: 0})

    resources_table.add_resource(resource_one)
    resources_table.add_resource(resource_two)

    estimators_table = EstimatorsTable()
    estimators_table.add_estimator(0, 'duration', lambda: None)
    estimators_table.add_estimator(1, 'duration', lambda: None)

    make_sim_event = SimpleEventFactory(resources_table, estimators_table)

    event_queue = [
        make_sim_event(arrival=1, remaining=4),
        make_sim_event(arrival=3, remaining=3),
        make_sim_event(arrival=4, remaining=1),
        make_sim_event(arrival=4, remaining=2),
        make_sim_event(arrival=4, remaining=3),
    ]

    sim_event_scheduler = SimEventScheduler(resources_table.environments)

    clock = simulator_clock_factory()

    simulator = Simulator(event_queue, sim_event_scheduler)
    clock.add_listener(simulator.step)

    await run_clock(clock, event_queue)

    assert (1, 1, 4) == arrival_started_finished_tuple(event_queue, 1)
    assert (3, 3, 5) == arrival_started_finished_tuple(event_queue, 2)
    assert (4, 5, 5) == arrival_started_finished_tuple(event_queue, 3)
    assert (4, 6, 7) == arrival_started_finished_tuple(event_queue, 4)
    assert (4, 6, 8) == arrival_started_finished_tuple(event_queue, 5)


@pytest.mark.asyncio
async def test_heterogeneous_environment():
    resource_one = Resource(
        environment_identifier=0, category=DummyCategory.Value, initial_state=RState(None, STATUS.free)
    )
    resource_two = Resource(
        environment_identifier=1, category=DummyCategory.Value, initial_state=RState(None, STATUS.free)
    )

    resources_table = ResourcesTable(environment_types={0: 0, 1: 1})

    resources_table.add_resource(resource_one)
    resources_table.add_resource(resource_two)

    estimators_table = EstimatorsTable()
    estimators_table.add_estimator(0, 'duration', lambda: None)
    estimators_table.add_estimator(1, 'duration', lambda: None)

    make_sim_event = SimpleEventFactory(resources_table, estimators_table)
    event_queue = [
        make_sim_event(arrival=1, remaining=3, env_type=0),
        make_sim_event(arrival=5, remaining=4, env_type=1),
        make_sim_event(arrival=6, remaining=2, env_type=0),
        make_sim_event(arrival=7, remaining=2, env_type=1),
    ]

    sim_event_scheduler = SimEventScheduler(resources_table.environments)

    clock = simulator_clock_factory()

    simulator = Simulator(event_queue, sim_event_scheduler)
    clock.add_listener(simulator.step)

    await run_clock(clock, event_queue)

    assert (1, 1, 3) == arrival_started_finished_tuple(event_queue, 1)
    assert (5, 5, 8) == arrival_started_finished_tuple(event_queue, 2)
    assert (6, 6, 7) == arrival_started_finished_tuple(event_queue, 3)
    assert (7, 9, 10) == arrival_started_finished_tuple(event_queue, 4)
