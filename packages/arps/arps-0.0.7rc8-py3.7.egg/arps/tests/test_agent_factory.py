import asyncio

import pytest # type: ignore

from arps.core.agent_factory import (AgentFactory,
                                     AgentCreationError,
                                     build_agent)
from arps.core.agent_id_manager import AgentIDManager
from arps.core.environment import Environment
from arps.core.clock import simulator_clock_factory, EpochTime
from arps.core.metrics_logger import MetricsLoggers
from arps.core.policy import ReflexPolicy
from arps.core.policies_executor import PoliciesExecutor
from arps.core.policies.monitor import build_monitor_policy_class, MonitorType
from arps.core.touchpoint import Sensor, Actuator

from arps.core.simulator.fake_communication_layer import FakeCommunicationLayer

from arps.test_resources.dummies.resources import ResourceA, ResourceB
from arps.test_resources.dummies.dummy_policy import DummyPolicy
from arps.core.remove_logger_files import remove_logger_files


@pytest.fixture
def setup_environment():
    comm_layer = FakeCommunicationLayer()
    asyncio.run(comm_layer.start())

    def abstract_factory(environment=None):
        environment = environment or Environment(sensors=[], actuators=[])
        return AgentFactory(environment=environment,
                            metrics_loggers=MetricsLoggers(),
                            communication_layer=comm_layer)

    yield AgentIDManager(0).next_available_id(), abstract_factory


def test_agent_creation(setup_environment):
    agent_id, abstract_factory = setup_environment
    policies_executor = PoliciesExecutor(policies=[],
                                         epoch_time=EpochTime(),
                                         clock_callback=(lambda _: None, lambda _: None))
    agent_factory = abstract_factory()
    agent = agent_factory.create_agent(identifier=agent_id, policies_executor=policies_executor)
    assert str(agent.identifier) == '0.1'
    assert agent.policies_executor
    assert policies_executor is agent.policies_executor

    assert not agent.sensors()
    assert not agent.actuators()

    remove_logger_files(agent.metrics_logger.logger)


def test_agent_creation_based_on_policy(setup_environment):
    agent_id, abstract_factory = setup_environment

    class SomePolicy(ReflexPolicy):
        def __init__(self):
            super().__init__()

    policies_executor = PoliciesExecutor(policies=[SomePolicy()],
                                         epoch_time=EpochTime(),
                                         clock_callback=(lambda _: None, lambda _: None))

    resource_a = ResourceA(environment_identifier=0)
    sensor = Sensor(resource_a)
    actuator = Actuator(resource_a)
    environment = Environment(sensors=[sensor], actuators=[actuator])
    environment.register_policy(SomePolicy.__name__, SomePolicy)

    agent_factory = abstract_factory(environment)
    agent = agent_factory.create_agent(identifier=agent_id, policies_executor=policies_executor)
    assert str(agent.identifier) == '0.1'
    assert agent.policies_executor
    assert policies_executor is agent.policies_executor

    sensors = agent.sensors()
    assert sensors == ['ResourceA']

    actuators = agent.actuators()
    assert actuators == ['ResourceA']

    remove_logger_files(agent.metrics_logger.logger)
    environment.unregister_policy(SomePolicy.__name__)


def test_build_agent_success(setup_environment):
    agent_id, abstract_factory = setup_environment

    resource_a = ResourceA(environment_identifier=0)
    resource_b = ResourceB(environment_identifier=0)
    sensors = [Sensor(resource_a), Sensor(resource_b)]
    actuators = [Actuator(resource_b)]
    environment = Environment(sensors=sensors, actuators=actuators)
    environment.register_policy(DummyPolicy.__name__, DummyPolicy)

    agent_factory = abstract_factory(environment)

    policies = {DummyPolicy.__name__: None}
    agent = build_agent(agent_factory, agent_id, policies, simulator_clock_factory())
    assert agent is not None

    remove_logger_files(agent.metrics_logger.logger)
    environment.unregister_policy(DummyPolicy.__name__)


def test_build_agent_error(setup_environment):
    agent_id, abstract_factory = setup_environment

    SomeMonitorPolicy = build_monitor_policy_class('SomeMonitorPolicy',
                                                   touchpoint_category='ResourceA',
                                                   monitor_type=MonitorType.Sensor)

    policies = {SomeMonitorPolicy.__name__: None}  # periodic policy with no period

    agent_factory = abstract_factory()

    with pytest.raises(AgentCreationError):
        build_agent(agent_factory, agent_id, policies, simulator_clock_factory())


if __name__ == '__main__':
    pytest.main([__file__])
