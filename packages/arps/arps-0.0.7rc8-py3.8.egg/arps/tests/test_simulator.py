import asyncio

import pytest  # type: ignore
import pytest_asyncio

from arps.core.clock import simulator_clock_factory
from arps.core.resources_table import ResourcesTable
from arps.core.simulator.estimators_table import EstimatorsTable
from arps.core.simulator.resource import Resource
from arps.core.simulator.sim_event_scheduler import SimEventScheduler
from arps.core.simulator.simulator import Simulator
from arps.test_resources.dummies.dummy_resource import DummyCategory
from arps.test_resources.dummies.simple_event import STATUS, RState, SimpleEvent


@pytest_asyncio.fixture
async def simulator_components():
    changes_spy = list()

    resource_zero = Resource(
        environment_identifier=0, category=DummyCategory.Value, initial_state=RState(None, STATUS.free)
    )

    resource_one = Resource(
        environment_identifier=1, category=DummyCategory.Value, initial_state=RState(None, STATUS.free)
    )

    resource_zero.add_listener(changes_spy.append)
    resource_one.add_listener(changes_spy.append)

    resources_table = ResourcesTable(environment_types={0: 0, 1: 1})

    resources_table.add_resource(resource_zero)
    resources_table.add_resource(resource_one)

    estimators_table = EstimatorsTable()
    # task duration in environment 0 is faster than in environment 1
    estimators_table.add_estimator(0, 'duration', lambda: 2)
    estimators_table.add_estimator(1, 'duration', lambda: 4)

    def make_sim_event(arrival, task_id, env_type):
        return SimpleEvent(
            task_id,
            arrival_time=arrival,
            resources_table=resources_table,
            estimators_table=estimators_table,
            env_type=env_type,
        )

    # 2 tasks arrive at the same time
    arrival_times = [1, 1, 2, 2, 3, 3, 4, 4]
    # first is allocated in the first env, second in the second env
    environment_types = [0, 1, 0, 1, 0, 1, 0, 1]

    event_queue = [
        make_sim_event(arrival_time, task_id, env_type)
        for task_id, (arrival_time, env_type) in enumerate(zip(arrival_times, environment_types))
    ]

    clock = simulator_clock_factory()
    clock.start()

    sim_event_scheduler = SimEventScheduler(resources_table.environments)
    simulator = Simulator(event_queue, sim_event_scheduler)
    clock.add_listener(simulator.step)

    yield simulator, clock, changes_spy, event_queue

    clock.remove_listener(simulator.step)


async def clock_update(clock):
    await clock.update()

    await clock.wait_for_notified_tasks()


@pytest.mark.asyncio
async def test_single_step(simulator_components):
    simulator, clock, changes_spy, event_queue = simulator_components

    assert all(not event.scheduled for event in event_queue)
    assert all(event.finished_time is None for event in event_queue)

    WAITING = (False, False)
    SCHEDULED = (True, False)
    FINISHED = (True, True)

    # each entry is the current state of each event
    states_in_each_epoch = [
        [SCHEDULED, SCHEDULED, WAITING, WAITING, WAITING, WAITING, WAITING, WAITING],
        [FINISHED, SCHEDULED, WAITING, WAITING, WAITING, WAITING, WAITING, WAITING],
        [FINISHED, SCHEDULED, SCHEDULED, WAITING, WAITING, WAITING, WAITING, WAITING],
        [FINISHED, FINISHED, FINISHED, WAITING, WAITING, WAITING, WAITING, WAITING],
        [FINISHED, FINISHED, FINISHED, SCHEDULED, SCHEDULED, WAITING, WAITING, WAITING],
        [FINISHED, FINISHED, FINISHED, SCHEDULED, FINISHED, WAITING, WAITING, WAITING],
        [FINISHED, FINISHED, FINISHED, SCHEDULED, FINISHED, WAITING, SCHEDULED, WAITING],
        [FINISHED, FINISHED, FINISHED, FINISHED, FINISHED, WAITING, FINISHED, WAITING],
        [FINISHED, FINISHED, FINISHED, FINISHED, FINISHED, SCHEDULED, FINISHED, WAITING],
        [FINISHED, FINISHED, FINISHED, FINISHED, FINISHED, SCHEDULED, FINISHED, WAITING],
        [FINISHED, FINISHED, FINISHED, FINISHED, FINISHED, SCHEDULED, FINISHED, WAITING],
        [FINISHED, FINISHED, FINISHED, FINISHED, FINISHED, FINISHED, FINISHED, WAITING],
        [FINISHED, FINISHED, FINISHED, FINISHED, FINISHED, FINISHED, FINISHED, SCHEDULED],
        [FINISHED, FINISHED, FINISHED, FINISHED, FINISHED, FINISHED, FINISHED, SCHEDULED],
        [FINISHED, FINISHED, FINISHED, FINISHED, FINISHED, FINISHED, FINISHED, SCHEDULED],
        [FINISHED, FINISHED, FINISHED, FINISHED, FINISHED, FINISHED, FINISHED, FINISHED],
    ]

    while not all(event.finished_time is not None for event in event_queue):
        await clock_update(clock)
        assert all(
            state == (event.scheduled, event.finished_time is not None)
            for state, event in zip(states_in_each_epoch[clock.epoch_time.epoch - 1], event_queue)
        )

    assert all(event.scheduled for event in event_queue)
    assert all(event.finished_time is not None for event in event_queue)


@pytest.mark.asyncio
async def test_step_by_step(simulator_components):
    simulator, clock, changes_spy, event_queue = simulator_components
    acquired = STATUS.acquired
    free = STATUS.free

    # Each index is the current state over an epoch
    expected = [
        ('0', '0', str(RState(None, free))),
        ('1', '0', str(RState(None, free))),
        ('0', '1', str(RState(0, acquired))),
        ('1', '1', str(RState(1, acquired))),
        ('0', '2', str(RState(None, free))),
        ('0', '3', str(RState(2, acquired))),
        ('1', '4', str(RState(None, free))),
        ('0', '4', str(RState(None, free))),
        ('1', '5', str(RState(3, acquired))),
        ('0', '5', str(RState(4, acquired))),
        ('0', '6', str(RState(None, free))),
        ('0', '7', str(RState(6, acquired))),
        ('1', '8', str(RState(None, free))),
        ('0', '8', str(RState(None, free))),
        ('1', '9', str(RState(5, acquired))),
        ('1', '12', str(RState(None, free))),
        ('1', '13', str(RState(7, acquired))),
        ('1', '16', str(RState(None, free))),
    ]

    await clock.update()

    number_of_events_each_step = [2, 4, 5, 6, 8, 10, 11, 12, 14, 15, 15, 15, 16, 17, 17, 17]
    for number_of_events in number_of_events_each_step:
        simpler_data = [(r_event.env, r_event.epoch, r_event.value) for r_event in changes_spy]
        assert expected[:number_of_events] == simpler_data, number_of_events
        await clock.update()

    assert all(event.finished_time is not None for event in event_queue)


@pytest.mark.asyncio
async def test_run(simulator_components):
    simulator, clock, changes_spy, event_queue = simulator_components
    free = STATUS.free
    acquired = STATUS.acquired

    assert 2 == len(changes_spy)
    assert 0 == clock.epoch_time.epoch

    clock_task = asyncio.create_task(clock.run())

    while not all(event.finished_time is not None for event in event_queue):
        await asyncio.sleep(0)

    clock_task.cancel()

    await clock_task

    await asyncio.sleep(0)
    #            env|epoch|resource state
    expected = [
        ('0', '0', str(RState(None, free))),
        ('1', '0', str(RState(None, free))),
        ('0', '1', str(RState(0, acquired))),
        ('1', '1', str(RState(1, acquired))),
        ('0', '2', str(RState(None, free))),
        ('0', '3', str(RState(2, acquired))),
        ('1', '4', str(RState(None, free))),
        ('0', '4', str(RState(None, free))),
        ('1', '5', str(RState(3, acquired))),
        ('0', '5', str(RState(4, acquired))),
        ('0', '6', str(RState(None, free))),
        ('0', '7', str(RState(6, acquired))),
        ('1', '8', str(RState(None, free))),
        ('0', '8', str(RState(None, free))),
        ('1', '9', str(RState(5, acquired))),
        ('1', '12', str(RState(None, free))),
        ('1', '13', str(RState(7, acquired))),
        ('1', '16', str(RState(None, free))),
    ]

    simpler_data = [(resource_event.env, resource_event.epoch, resource_event.value) for resource_event in changes_spy]
    assert expected == simpler_data
    assert 16 == clock.epoch_time.epoch


if __name__ == '__main__':
    pytest.main([__file__])
