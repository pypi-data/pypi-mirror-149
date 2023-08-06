import asyncio
import math
import os
import pathlib
import re

import pytest  # type: ignore
import pytest_asyncio

from arps.apps.configuration_file_loader import SimulatorManagerEnvironment
from arps.apps.simulator_handler import SimulatorHandler
from arps.core.clock import simulator_clock_factory
from arps.core.resources_table import ResourcesTable
from arps.core.simulator.estimators_table import EstimatorsTable
from arps.core.simulator.event_queue_loader import FileEventQueueLoader
from arps.core.simulator.sim_event_scheduler import SimEventScheduler
from arps.test_resources.dummies.dummy_estimators import (
    dummy_main_estimator,
    dummy_pos_estimator,
)
from arps.test_resources.dummies.dummy_event_factory import DummyEventFactory
from arps.test_resources.dummies.resources import ResourceA


@pytest_asyncio.fixture
async def simulator_handler():
    environment = 0
    resource = ResourceA(environment_identifier=environment, initial_state=0)
    resources_table = ResourcesTable(environment_types={environment: 0})
    resources_table.add_resource(resource)

    results_path = os.path.join('logs')
    log_formatter = {'module': 'test_resources.dummies.dummy_resource', 'class': 'DummyResource'}

    estimators_table = EstimatorsTable()
    estimators_table.add_estimator(0, 'main_estimate', dummy_main_estimator)
    estimators_table.add_estimator(0, 'pos_estimate', dummy_pos_estimator)

    events_path = pathlib.Path('arps') / 'test_resources' / 'dummies' / 'dummy_jobs.txt.10000'
    generator = DummyEventFactory(resources_table, estimators_table)
    event_queue_loader = FileEventQueueLoader(events_path, generator)

    sim_event_scheduler = SimEventScheduler(resources_table.environments)
    sim_env = SimulatorManagerEnvironment(
        True, resources_table, None, event_queue_loader, sim_event_scheduler, results_path, log_formatter, None
    )

    clock = simulator_clock_factory()
    simulator_handler = SimulatorHandler(clock, sim_env)

    yield simulator_handler

    if simulator_handler.clock_run_task:
        await simulator_handler.clock_run_task


@pytest.mark.asyncio
async def test_run(simulator_handler: SimulatorHandler):
    simulator_handler.run()

    assert 'running' == simulator_handler.status()

    await asyncio.sleep(0)  # to have some result

    await simulator_handler.stop()

    assert 'stopped' == simulator_handler.status()

    result_content, filename = simulator_handler.result()
    assert len(result_content)
    assert re.match(r'\d{8}-\d{6}_\d+_sim_results.zip', filename), f'Unexpected file name format {filename}'


@pytest.mark.asyncio
async def test_stats(simulator_handler: SimulatorHandler):
    with pytest.raises(RuntimeError) as err:
        simulator_handler.set_debug(True)
        simulator_handler.stats()

    assert str(err.value) == 'No simulation has been executed so far'

    simulator_handler.set_debug(False)
    simulator_handler.run()

    await asyncio.sleep(2)

    await simulator_handler.stop()

    stats = simulator_handler.stats()
    assert 'tracemalloc' not in stats
    elapsed_time, unit = stats['elapsed_time'].split()
    assert unit == 'seconds'
    assert math.isclose(float(elapsed_time), 2.00, abs_tol=0.1), f'{elapsed_time} instead of 2.00'

    simulator_handler.set_debug(True)
    simulator_handler.run()

    await asyncio.sleep(1)

    await simulator_handler.stop()

    stats = simulator_handler.stats()
    assert len(stats['tracemalloc']) == 10
    elapsed_time, unit = stats['elapsed_time'].split()
    assert unit == 'seconds'
    assert math.isclose(float(elapsed_time), 1.00, abs_tol=0.1), f'{elapsed_time} instead of 1.00'


@pytest.mark.asyncio
async def test_invoke_result_before_run(simulator_handler):
    with pytest.raises(RuntimeError) as excinfo:
        simulator_handler.result()

    assert str(excinfo.value) == 'Simulation log not found'


@pytest.mark.asyncio
async def test_invoke_result_before_stopping_the_sim(simulator_handler):
    simulator_handler.run()

    with pytest.raises(RuntimeError) as excinfo:
        simulator_handler.result()

    assert str(excinfo.value) == 'Simulation is still running; request stop before requesting result'

    # calling stop without letting the loop run causes exception. This
    # behaviour is not expected in the real world, hence I'm putting a
    # sleep here.
    await asyncio.sleep(0)

    await simulator_handler.stop()


@pytest.mark.asyncio
async def test_stop_with_no_sim_running(simulator_handler):
    assert 'stopped' == simulator_handler.status()

    await simulator_handler.stop()

    assert 'stopped' == simulator_handler.status()


@pytest.mark.asyncio
async def test_try_run_twice(simulator_handler):
    simulator_handler.run()
    assert simulator_handler.status() == 'running'

    simulator_handler.run()
    assert simulator_handler.status() == 'running'

    await asyncio.sleep(0)  # to have some result

    await simulator_handler.stop()

    assert simulator_handler.status() == 'stopped'


@pytest.mark.asyncio
async def test_save_simulation_configuration(simulator_handler):

    agent_managers = {
        0: [
            ('spawn_agent', [('policies', ['DummyPolicy'])]),
            ('spawn_agent', [('policies', ['DummyPeriodicPolicy']), ('period', '10')]),
        ],
        1: [('spawn_agent', [('policies', ['DummyPolicy'])])],
    }

    result = simulator_handler.save(agent_managers)

    assert result == {
        0: [
            {'command': 'spawn_agent', 'params': {'policies': ['DummyPolicy']}},
            {'command': 'spawn_agent', 'params': {'policies': ['DummyPeriodicPolicy'], 'period': '10'}},
        ],
        1: [{'command': 'spawn_agent', 'params': {'policies': ['DummyPolicy']}}],
    }


if __name__ == '__main__':
    pytest.main([__file__])
