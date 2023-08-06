import contextlib
import asyncio
from functools import partial
from collections import Counter

import pytest # type: ignore

from arps.core.environment import Environment
from arps.core.agent_id_manager import AgentID
from arps.core.clock import EpochTime
from arps.core.policies_executor import PoliciesExecutor
from arps.core.payload_factory import create_periodic_action
from arps.core.simulator.fake_communication_layer import FakeCommunicationLayer
from arps.core.agent_factory import AgentFactory
from arps.core.agent_id_manager import AgentIDManager
from arps.core.metrics_logger import MetricsLoggers
from arps.core.remove_logger_files import remove_logger_files
from arps.core.touchpoint import Sensor, Actuator

from arps.core.clock import simulator_clock_factory

from arps.test_resources.dummies.dummy_policy import (DummyPolicy,
                                                      DummyPeriodicPolicy)
from arps.test_resources.dummies.resources import ResourceA, ResourceB


class dummy_host:
    identifier = AgentID(0, 0)

    def update_touchpoints(self, *args):
        pass


def test_add_policy():
    policies_executor = PoliciesExecutor(policies=[],
                                         epoch_time=EpochTime(),
                                         clock_callback=(lambda _: None, lambda _: None))
    policies_executor.host = dummy_host()

    assert not policies_executor._policies

    policies_executor.add_policy(DummyPolicy())

    assert policies_executor._policies


def test_remove_policy():
    policies_executor = PoliciesExecutor(policies=[DummyPolicy()],
                                         epoch_time=EpochTime(),
                                         clock_callback=(lambda _: None, lambda _: None))
    policies_executor.remove_policy('DummyPolicy')

    assert not policies_executor._policies


# PeriodicPolicies tests

@pytest.fixture
def env_setup():
    resource_a = ResourceA(environment_identifier=0)
    resource_b = ResourceB(environment_identifier=0)
    environment = Environment(sensors=[Sensor(resource_a), Sensor(resource_b)],
                              actuators=[Actuator(resource_b)])
    communication_layer = FakeCommunicationLayer()
    asyncio.run(communication_layer.start())
    agent_factory = AgentFactory(
        environment=environment,
        communication_layer=communication_layer,
        metrics_loggers=MetricsLoggers())
    clock = simulator_clock_factory()
    agent_id = AgentIDManager(root_id=0).next_available_id()

    clock.start()

    yield partial(create_agent, clock, agent_factory, agent_id)

    clock.reset()


@contextlib.asynccontextmanager
async def create_agent(clock, agent_factory, agent_id, policies, n_steps=1):
    policies_executor = PoliciesExecutor(policies=policies,
                                         epoch_time=clock.epoch_time,
                                         clock_callback=clock.observer_interface)

    agent = agent_factory.create_agent(identifier=agent_id,
                                       policies_executor=policies_executor)

    clock.add_listener_low_priority(agent.run)
    for _ in range(n_steps):
        await clock.update()
    await clock.wait_for_notified_tasks()

    yield policies_executor.policy_action_results

    remove_logger_files(agent.logger)
    remove_logger_files(agent.metrics_logger.logger)


@pytest.mark.asyncio
async def test_generate_single_event(env_setup):
    policy = DummyPeriodicPolicy()
    policy.period = 1
    async with env_setup([policy]) as results:
        periodic_action = create_periodic_action(id(policy))
        assert results[0] == periodic_action


@pytest.mark.asyncio
async def test_generate_longer_period_event(env_setup):
    policy = DummyPeriodicPolicy()
    policy.period = 10
    async with env_setup([policy], n_steps=10) as results:
        periodic_action = create_periodic_action(id(policy))
        assert list(results) == [periodic_action]


@pytest.mark.asyncio
async def test_generate_more_results_than_it_can_stored(env_setup):
    policy = DummyPeriodicPolicy()
    policy.period = 1

    async with env_setup([policy], n_steps=200) as results:
        assert len(results) == 50


@pytest.mark.asyncio
async def test_different_periods(env_setup):
    policy1 = DummyPeriodicPolicy()
    policy1.period = 1

    policy2 = DummyPeriodicPolicy()
    policy2.period = 5
    async with env_setup([policy1, policy2], n_steps=10) as results:
        periodic_action1 = create_periodic_action(id(policy1))
        periodic_action2 = create_periodic_action(id(policy2))

        # Since period of policy1 is 1 and the clock ticks 10 times it is expected 10 events
        # Since period of policy2 is 5 and the clock ticks 10 times it is expected 2 events
        assert Counter(results) == {periodic_action1: 10, periodic_action2: 2}


if __name__ == '__main__':
    pytest.main([__file__])
