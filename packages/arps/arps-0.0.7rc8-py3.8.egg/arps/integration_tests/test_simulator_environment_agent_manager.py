import asyncio
import contextlib
import pathlib
from collections import Counter

import pytest  # type: ignore
import pytest_asyncio

from arps.core.agent_id_manager import AgentID
from arps.core.mobile_entity import Coordinates
from arps.core.payload_factory import MetaOp, PayloadType
from arps.core.remove_logger_files import remove_logger_files
from arps.test_resources.dummies.resources import (
    ReceivedMessagesResource,
    ResourceA,
    ResourceB,
    ResourceC,
)
from arps.test_resources.sim_agent_manager_helper import (
    build_sim_agent_manager,
    setup_sim_agent_manager_environment,
)

# pylint:disable=redefined-outer-name


@contextlib.contextmanager
def setup_sim_environment(configuration_file: str):
    conf_path = pathlib.Path('arps') / 'test_resources' / 'conf' / configuration_file
    with setup_sim_agent_manager_environment(conf_path) as agent_manager_env:
        yield agent_manager_env


def test_resources_table_loaded():
    with setup_sim_environment('dummy_simulator_environment.conf') as manager_environment:
        _, manager_environment = manager_environment

        resources_available = manager_environment.resources_table.resources_from_environment(environment_id=0)
        assert isinstance(resources_available['ResourceA'], ResourceA)
        assert isinstance(resources_available['ResourceB'], ResourceB)
        assert isinstance(resources_available['ResourceC'], ResourceC)
        assert isinstance(resources_available['ReceivedMessagesResource'], ReceivedMessagesResource)

        resources_available = manager_environment.resources_table.resources_from_environment(environment_id=1)

        assert isinstance(resources_available['ResourceA'], ResourceA)
        assert isinstance(resources_available['ResourceB'], ResourceB)
        assert isinstance(resources_available['ReceivedMessagesResource'], ReceivedMessagesResource)


async def clock_started(clock):
    while not clock.started:
        await asyncio.sleep(clock.seconds_between_ticks)


@contextlib.asynccontextmanager
async def create_agent_managers(configuration_file):
    with setup_sim_environment(configuration_file) as manager_environment:
        clock, _ = manager_environment
        agent_managers = await build_sim_agent_manager(manager_environment)

        clock_task = asyncio.ensure_future(clock.run())

        await clock_started(clock)

        yield agent_managers

        for agent_manager in agent_managers:
            for agent in agent_manager.running_agents.values():
                remove_logger_files(agent.logger)
                remove_logger_files(agent.metrics_logger.logger)

        clock_task.cancel()

        await clock_task


@pytest_asyncio.fixture()
async def agent_managers():
    """This returns a manager that handles regular agents (non-mobile agents)"""
    async with create_agent_managers('dummy_simulator_environment.conf') as ams:
        yield ams


@pytest.mark.asyncio
async def test_policy_repository(agent_managers):
    result = await agent_managers[0].policy_repository()

    assert sorted(result) == sorted(
        [
            'DummyPolicy',
            'DummyPeriodicPolicy',
            'DummyPolicyWithBehavior',
            'DefaultDummyPolicyForSimulator',
            'DummyPolicyForSimulator',
            'SenderPolicy',
            'ReceiverPolicy',
            'ResourceAMonitorPolicy',
            'ResourceBMonitorPolicy',
            'ResourceCMonitorPolicy',
            'ReceivedMessagesResourceMonitorPolicy',
            'DummyResourceMonitorPolicy',
        ]
    )

    result = await agent_managers[1].policy_repository()

    assert result == [
        'DummyPolicy',
        'DummyPeriodicPolicy',
        'SenderPolicy',
        'ReceiverPolicy',
        'ResourceAMonitorPolicy',
        'ResourceBMonitorPolicy',
        'ReceivedMessagesResourceMonitorPolicy',
    ]


@pytest.mark.asyncio
async def test_spawn_default_agent(agent_managers):
    agent_manager = agent_managers[0]
    assert agent_manager.list_agents() == {'agents': []}

    spawn_agent_result = await agent_manager.spawn_agent(policies={'DummyPolicy': None})
    assert spawn_agent_result == 'Agent 0.1 created'

    assert agent_manager.list_agents() == {'agents': ['0.1']}


@pytest.mark.asyncio
async def test_spawn_multiple_default_agents(agent_managers):
    agent_manager = agent_managers[0]
    assert agent_manager.list_agents() == {'agents': []}

    spawn_agent_result = await agent_manager.spawn_agent(policies={'DummyPolicy': None})
    assert spawn_agent_result == 'Agent 0.1 created'

    spawn_agent_result = await agent_manager.spawn_agent(policies={'DummyPolicy': None})
    assert spawn_agent_result == 'Agent 0.2 created'

    assert agent_manager.list_agents() == {'agents': ['0.1', '0.2']}


@pytest.mark.asyncio
async def test_tracked_actions(agent_managers):
    agent_manager = agent_managers[0]
    asyncio.get_event_loop().set_debug(True)

    await agent_manager.spawn_agent(policies={'DummyPolicy': None})
    await agent_manager.spawn_agent(policies={'DummyPeriodicPolicy': 10})

    expected_tracked_actions = [
        ('spawn_agent', [('policies', {'DummyPolicy': 'None'})]),
        ('spawn_agent', [('policies', {'DummyPeriodicPolicy': '10'})]),
    ]
    assert agent_manager.actions_tracker == expected_tracked_actions

    agent_one = AgentID(0, 1)
    agent_two = AgentID(0, 2)
    await agent_manager.update_agents_relationship(
        from_agent=agent_one, to_agent=str(agent_two), operation=MetaOp.add.name
    )

    expected_tracked_actions.append(
        (
            'update_agents_relationship',
            [('from_agent', str(agent_one)), ('to_agent', str(agent_two)), ('operation', 'add')],
        )
    )

    assert agent_manager.actions_tracker == expected_tracked_actions

    await agent_manager.terminate_agent(agent_id=agent_two)

    expected_tracked_actions.append(('terminate_agent', [('agent_id', str(agent_two))]))

    assert agent_manager.actions_tracker == expected_tracked_actions


@pytest.mark.asyncio
async def test_agent_info_status(agent_managers):
    agent_manager = agent_managers[0]
    result = await agent_manager.spawn_agent(policies={'DummyPolicy': None})

    assert result == 'Agent 0.1 created'

    response = await agent_manager.agents_status(request_type=PayloadType.info, provider=AgentID(0, 1))

    assert response.type == PayloadType.info
    assert response.sender_id == '0.1'
    assert response.receiver_id == '0.0'
    assert Counter(response.content.sensors) == Counter(['ResourceA', 'ResourceB', 'DummyResource'])
    assert Counter(response.content.actuators) == Counter(['ResourceB', 'ResourceC', 'ReceivedMessagesResource'])


@pytest.mark.asyncio
async def test_sensors_status(agent_managers):
    agent_manager = agent_managers[0]
    result = await agent_manager.spawn_agent(policies={'DummyPolicy': None})
    assert result == 'Agent 0.1 created'

    response = await agent_manager.agents_status(request_type=PayloadType.sensors, provider=AgentID(0, 1))

    assert response.type == PayloadType.sensors
    assert response.sender_id == '0.1'
    assert response.receiver_id == '0.0'
    assert response.content.touchpoint == {'ResourceA': 40, 'ResourceB': 'ON', 'DummyResource': 'FakeResource'}


@pytest.mark.asyncio
async def test_agent_actuator_status(agent_managers):
    agent_manager = agent_managers[0]
    result = await agent_manager.spawn_agent(policies={'DummyPolicy': None})
    assert result == 'Agent 0.1 created'

    response = await agent_manager.agents_status(request_type=PayloadType.actuators, provider=AgentID(0, 1))

    assert response.type == PayloadType.actuators
    assert response.sender_id == '0.1'
    assert response.receiver_id == '0.0'
    assert response.content.touchpoint == {'ResourceB': 'ON', 'ResourceC': 40, 'ReceivedMessagesResource': 0}


@pytest.mark.asyncio
async def test_agent_sensors_actuators_status(agent_managers):
    agent_manager = agent_managers[0]
    result = await agent_manager.spawn_agent(policies={'DummyPolicy': None})
    assert result == 'Agent 0.1 created'

    response = await agent_manager.agents_status(request_type=PayloadType.actuators, provider=AgentID(0, 1))

    assert response.type == PayloadType.actuators
    assert response.sender_id == '0.1'
    assert response.receiver_id == '0.0'
    assert response.content.touchpoint == {'ResourceB': 'ON', 'ResourceC': 40, 'ReceivedMessagesResource': 0}

    response = await agent_manager.agents_status(request_type=PayloadType.sensors, provider=AgentID(0, 1))

    assert response.type == PayloadType.sensors
    assert response.sender_id == '0.1'
    assert response.receiver_id == '0.0'
    assert response.content.touchpoint == {'ResourceA': 40, 'ResourceB': 'ON', 'DummyResource': 'FakeResource'}


@pytest.mark.asyncio
async def test_multiple_agent_info_status(agent_managers):
    agent_manager = agent_managers[0]
    result = await agent_manager.spawn_agent(policies={'DummyPolicy': None})
    assert result == 'Agent 0.1 created'
    result = await agent_manager.spawn_agent(policies={'DummyPolicy': None})
    assert result == 'Agent 0.2 created'

    response = await agent_manager.agents_status(request_type=PayloadType.info, provider=AgentID(0, 1))

    assert response.type == PayloadType.info
    assert response.sender_id == '0.1'
    assert response.receiver_id == '0.0'
    assert Counter(response.content.sensors) == Counter(['ResourceA', 'ResourceB', 'DummyResource'])
    assert Counter(response.content.actuators) == Counter(['ResourceB', 'ResourceC', 'ReceivedMessagesResource'])

    response = await agent_manager.agents_status(request_type=PayloadType.info, provider=AgentID(0, 2))

    assert response.type == PayloadType.info
    assert response.sender_id == '0.2'
    assert response.receiver_id == '0.0'
    assert Counter(response.content.sensors) == Counter(['ResourceA', 'ResourceB', 'DummyResource'])
    assert Counter(response.content.actuators) == Counter(['ResourceB', 'ResourceC', 'ReceivedMessagesResource'])


@pytest.mark.asyncio
async def test_multiple_agent_sensor_status(agent_managers):
    agent_manager = agent_managers[0]
    result = await agent_manager.spawn_agent(policies={'DummyPolicy': None})
    assert result == 'Agent 0.1 created'
    result = await agent_manager.spawn_agent(policies={'DummyPolicy': None})
    assert result == 'Agent 0.2 created'

    response = await agent_manager.agents_status(request_type=PayloadType.sensors, provider=AgentID(0, 1))

    assert response.type == PayloadType.sensors
    assert response.sender_id == '0.1'
    assert response.receiver_id == '0.0'
    assert response.content.touchpoint == {'ResourceA': 40, 'ResourceB': 'ON', 'DummyResource': 'FakeResource'}

    response = await agent_manager.agents_status(request_type=PayloadType.sensors, provider=AgentID(0, 2))

    assert response.type == PayloadType.sensors
    assert response.sender_id == '0.2'
    assert response.receiver_id == '0.0'
    assert response.content.touchpoint == {'ResourceA': 40, 'ResourceB': 'ON', 'DummyResource': 'FakeResource'}


@pytest.mark.asyncio
async def test_multiple_agent_actuator_status(agent_managers):
    agent_manager = agent_managers[0]
    result = await agent_manager.spawn_agent(policies={'DummyPolicy': None})
    assert result == 'Agent 0.1 created'
    result = await agent_manager.spawn_agent(policies={'DummyPolicy': None})
    assert result == 'Agent 0.2 created'

    response = await agent_manager.agents_status(request_type=PayloadType.actuators, provider=AgentID(0, 1))

    assert response.type == PayloadType.actuators
    assert response.sender_id == '0.1'
    assert response.receiver_id == '0.0'
    assert response.content.touchpoint == {'ResourceB': 'ON', 'ResourceC': 40, 'ReceivedMessagesResource': 0}

    response = await agent_manager.agents_status(request_type=PayloadType.actuators, provider=AgentID(0, 2))

    assert response.type == PayloadType.actuators
    assert response.sender_id == '0.2'
    assert response.receiver_id == '0.0'
    assert response.content.touchpoint == {'ResourceB': 'ON', 'ResourceC': 40, 'ReceivedMessagesResource': 0}


@pytest.mark.asyncio
async def test_changing_relationship_from_one_agent_to_another(agent_managers):
    agent_manager = agent_managers[0]
    result = await agent_manager.spawn_agent(policies={'DummyPolicy': None})
    assert result == 'Agent 0.1 created'
    result = await agent_manager.spawn_agent(policies={'DummyPolicy': None})
    assert result == 'Agent 0.2 created'

    agent_one = AgentID(0, 1)
    agent_two = AgentID(0, 2)
    result = await agent_manager.agents_status(request_type=PayloadType.info, provider=agent_one)
    assert not result.content.related_agents

    result = await agent_manager.agents_status(request_type=PayloadType.info, provider=agent_two)
    assert not result.content.related_agents

    result = await agent_manager.update_agents_relationship(
        from_agent=agent_one, to_agent=str(agent_two), operation=MetaOp.add.name
    )
    assert 'Operation include_as_related of 0.2 performed in 0.1' == result.content.status

    result = await agent_manager.update_agents_relationship(
        from_agent=agent_two, to_agent=str(agent_one), operation=MetaOp.add.name
    )
    assert 'Operation include_as_related of 0.1 performed in 0.2' == result.content.status

    result = await agent_manager.agents_status(request_type=PayloadType.info, provider=agent_one)
    assert ['0.2'] == result.content.related_agents

    result = await agent_manager.agents_status(request_type=PayloadType.info, provider=agent_two)
    assert ['0.1'] == result.content.related_agents

    result = await agent_manager.update_agents_relationship(
        from_agent=agent_two, to_agent=str(agent_one), operation=MetaOp.remove.name
    )
    assert 'Operation remove_as_related of 0.1 performed in 0.2' == result.content.status

    result = await agent_manager.agents_status(request_type=PayloadType.info, provider=agent_one)
    assert ['0.2'] == result.content.related_agents

    result = await agent_manager.agents_status(request_type=PayloadType.info, provider=agent_two)
    assert not result.content.related_agents


@pytest.mark.asyncio
async def test_communication_between_agent_in_different_environments(agent_managers):
    spawn_agent_result = await agent_managers[0].spawn_agent(policies={'SenderPolicy': 3})
    assert spawn_agent_result == 'Agent 0.1 created'

    spawn_agent_result = await agent_managers[1].spawn_agent(policies={'ReceiverPolicy': None})
    assert spawn_agent_result == 'Agent 1.1 created'

    agent_in_zero = AgentID(0, 1)
    agent_in_one = AgentID(1, 1)
    actuators = await agent_managers[1].agents_status(request_type=PayloadType.actuators, provider=agent_in_one)

    assert actuators.content.touchpoint['ReceivedMessagesResource'] == 0

    result = await agent_managers[0].update_agents_relationship(
        from_agent=agent_in_zero, to_agent=str(agent_in_one), operation=MetaOp.add.name
    )
    assert 'Operation include_as_related of 1.1 performed in 0.1' == result.content.status

    assert agent_managers[0].clock is agent_managers[1].clock

    # Give time to execute three times (since period is 3; 10 is used
    # because epoch starts on 1)
    while agent_managers[0].clock.epoch_time.epoch < 10:
        await asyncio.sleep(0)

    assert agent_managers[0].clock.epoch_time.epoch == 10

    actuators = await agent_managers[1].agents_status(request_type=PayloadType.actuators, provider=agent_in_one)

    # it can be both since the execution of the agents is non-deterministic
    assert actuators.content.touchpoint['ReceivedMessagesResource'] in [2, 3]


# ************ mobile agents ************


@pytest_asyncio.fixture()
async def mobile_agent_managers():
    """This returns a manager that handles mobile agents"""
    async with create_agent_managers('dummy_simulator_environment_mobile_infinite_events.conf') as ams:
        yield ams


@pytest.mark.asyncio
async def test_mobile_agent_boundaries(mobile_agent_managers):
    agent_manager = mobile_agent_managers[0]
    mobile_agent_id = AgentID(0, 1)
    spawn_agent_result = await agent_manager.spawn_agent(policies={'MoveWithinBoundariesPolicy': 1})
    assert spawn_agent_result == 'Agent 0.1 created'

    result = await agent_manager.agents_status(request_type=PayloadType.info, provider=mobile_agent_id)
    assert result.content.coordinates == Coordinates(0, -5, 3)

    while agent_manager.clock.epoch_time.epoch < 10:
        await asyncio.sleep(0)

    result = await agent_manager.agents_status(request_type=PayloadType.info, provider=mobile_agent_id)
    assert result.content.coordinates == Coordinates(8, -5, 3)


if __name__ == '__main__':
    pytest.main([__file__])
