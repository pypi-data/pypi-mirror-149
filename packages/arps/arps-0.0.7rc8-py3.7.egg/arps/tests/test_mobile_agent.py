import pytest

from arps.core.agent_factory import AgentFactory
from arps.core.agent_id_manager import AgentIDManager
from arps.core.clock import simulator_clock_factory
from arps.core.environment import Environment
from arps.core.metrics_logger import MetricsLoggers
from arps.core.mobile_entity import Boundaries, Coordinates
from arps.core.policies_executor import PoliciesExecutor
from arps.core.simulator.fake_communication_layer import FakeCommunicationLayer
from arps.core.touchpoint import Actuator, Sensor
from arps.test_resources.mobile.policies import (
    CaptureAndMoveResourcePolicy,
    MoveWithinBoundariesPolicy,
)
from arps.test_resources.mobile.resources import MobileResources


@pytest.fixture
async def env_setup():
    mobile_resources = MobileResources(environment_identifier=0)
    sensors = [Sensor(mobile_resources)]
    actuators = [Actuator(mobile_resources)]

    comm_layer = FakeCommunicationLayer()
    await comm_layer.start()
    environment = Environment(
        sensors=sensors,
        actuators=actuators,
        boundaries=Boundaries(lower=Coordinates(0, 0, 0), upper=Coordinates(10, 10, 10)),
    )
    agent_factory = AgentFactory(
        environment=environment,
        metrics_loggers=MetricsLoggers(),
        communication_layer=comm_layer,
    )

    clock = simulator_clock_factory()
    clock.start()

    agent_id_manager = AgentIDManager(0)

    yield clock, agent_factory, agent_id_manager, mobile_resources

    clock.reset()

    await comm_layer.close()


@pytest.mark.asyncio
async def test_simple_mobile_agent_within_a_boundary(env_setup):
    """This test just make the agent move around. No further action is performed"""
    clock, agent_factory, agent_id_manager, _ = env_setup

    move_policy = MoveWithinBoundariesPolicy()
    move_policy.period = 1

    policies_executor = PoliciesExecutor(
        policies=[move_policy],
        epoch_time=clock.epoch_time,
        clock_callback=clock.observer_interface,
    )

    mobile_agent_id = agent_id_manager.next_available_id()
    agent_id_manager.commit()
    mobile_agent = agent_factory.create_agent(identifier=mobile_agent_id, policies_executor=policies_executor)

    clock.add_listener(mobile_agent.run)

    assert mobile_agent.coordinates == Coordinates(0, 0, 0)

    for i in range(5):
        await clock.update()
        await clock.wait_for_notified_tasks()

    # XXX: this is not totally deterministic. Investigate why
    assert mobile_agent.coordinates == Coordinates(4, 0, 0) or mobile_agent.coordinates == Coordinates(5, 0, 0)


@pytest.mark.asyncio
async def test_single_mobile_agent_multiple_resources(env_setup):
    """This test makes the agent move towards a mobile resource. The agent
    captures it, and move it to a target coordinate

    """
    clock, agent_factory, agent_id_manager, mobile_resources = env_setup

    move_policy = CaptureAndMoveResourcePolicy()
    move_policy.period = 1

    policies_executor = PoliciesExecutor(
        policies=[move_policy],
        epoch_time=clock.epoch_time,
        clock_callback=clock.observer_interface,
    )

    mobile_agent_id = agent_id_manager.next_available_id()
    agent_id_manager.commit()
    mobile_agent = agent_factory.create_agent(identifier=mobile_agent_id, policies_executor=policies_executor)

    clock.add_listener(mobile_agent.run)

    assert mobile_agent.coordinates == Coordinates(0, 0, 0)

    while any(mobile_resource["active"] for mobile_resource in mobile_resources.value.values()):
        await clock.update()
        await clock.wait_for_notified_tasks()

    assert mobile_agent.coordinates == Coordinates(9, 1, 3)

    assert all(str(mobile_resource["owner"]) == '0.1' for mobile_resource in mobile_resources.value.values())


@pytest.mark.asyncio
async def test_multiple_mobile_agent_multiple_resources(env_setup):
    """This test makes the agent move towards a mobile resource. The agent
    captures it, and move it to a target coordinate

    """
    clock, agent_factory, agent_id_manager, mobile_resources = env_setup

    mobile_agents = []
    for _ in range(2):
        move_policy = CaptureAndMoveResourcePolicy()
        move_policy.period = 1

        policies_executor = PoliciesExecutor(
            policies=[move_policy],
            epoch_time=clock.epoch_time,
            clock_callback=clock.observer_interface,
        )

        agent_id = agent_id_manager.next_available_id()
        agent_id_manager.commit()
        mobile_agent = agent_factory.create_agent(identifier=agent_id, policies_executor=policies_executor)
        clock.add_listener(mobile_agent.run)
        mobile_agents.append(mobile_agent)

    assert all(mobile_agent.coordinates == Coordinates(0, 0, 0) for mobile_agent in mobile_agents)

    while any(mobile_resource["active"] for mobile_resource in mobile_resources.value.values()):
        await clock.update()
        await clock.wait_for_notified_tasks()

    # It is non deterministic, but one is always going to get one resource, and the other the remaining resource
    if mobile_agents[1].coordinates == Coordinates(8, 7, 1):
        assert str(mobile_resources.value[1]['owner']) == '0.1'
        assert str(mobile_resources.value[0]['owner']) == '0.2'
        assert mobile_agents[0].coordinates == Coordinates(9, 1, 3)

    if mobile_agents[0].coordinates == Coordinates(8, 7, 1):
        assert str(mobile_resources.value[0]['owner']) == '0.1'
        assert str(mobile_resources.value[1]['owner']) == '0.2'
        assert mobile_agents[1].coordinates == Coordinates(9, 1, 3)
